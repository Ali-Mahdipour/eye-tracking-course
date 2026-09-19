"""
I-VT (Velocity-Threshold Identification) — one teaching function.

Salvucci & Goldberg (2000)-style classifier: label each sample by
point-to-point speed, then collapse runs into events.

Duration rule (important):
  An event that runs from sample i through sample j-1 (exclusive end j)
  lasts from t[i] until t[j] (onset of the next different label).
  If the run reaches the last sample, we add one median sample step so
  the final sample still contributes duration. Using only t[j-1]-t[i]
  would systematically under-count by about one sample interval.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def ivt_classify(
    time_s,
    x,
    y,
    *,
    velocity_threshold: float = 5000.0,
    min_fixation_s: float = 0.06,
):
    """
    Classify gaze samples and return (samples_df, events_df).

    Parameters
    ----------
    time_s, x, y : array-like
        Timestamps in **seconds** and gaze in the same spatial units (e.g. px).
    velocity_threshold : float
        Speed cutoff in spatial_units / second. For this course's Tobii pixel
        data on 1366×768 media, start near 5000 px/s (try 2000–8000).
    min_fixation_s : float
        Fixation runs shorter than this become "unclassified".

    Returns
    -------
    samples : DataFrame
        time_s, x, y, velocity, label
    events : DataFrame
        label, start_s, end_s, duration_s, x_mean, y_mean, n_samples
    """
    t = np.asarray(time_s, dtype=float)
    xx = np.asarray(x, dtype=float)
    yy = np.asarray(y, dtype=float)
    if len(t) != len(xx) or len(t) != len(yy):
        raise ValueError("time_s, x, y must be the same length")
    if len(t) < 2:
        raise ValueError("need at least 2 samples")

    dt = np.diff(t)
    step = float(np.nanmedian(dt[dt > 0])) if np.any(dt > 0) else np.nan

    # Velocity of the transition INTO sample i (undefined for i=0)
    velocity = np.full(len(t), np.nan)
    good = dt > 0
    velocity[1:] = np.where(
        good,
        np.sqrt(np.diff(xx) ** 2 + np.diff(yy) ** 2) / np.where(good, dt, np.nan),
        np.nan,
    )

    label = np.full(len(t), "unclassified", dtype=object)
    ok = np.isfinite(velocity)
    label[ok & (velocity < velocity_threshold)] = "fixation"
    label[ok & (velocity >= velocity_threshold)] = "saccade"
    # First sample inherits the second sample's provisional class when possible
    if len(label) > 1 and label[0] == "unclassified" and label[1] in ("fixation", "saccade"):
        label[0] = label[1]

    # Drop very short fixation runs
    i = 0
    n = len(label)
    while i < n:
        if label[i] != "fixation":
            i += 1
            continue
        j = i + 1
        while j < n and label[j] == "fixation":
            j += 1
        end_t = t[j] if j < n else (t[n - 1] + step if np.isfinite(step) else t[n - 1])
        if (end_t - t[i]) < min_fixation_s:
            label[i:j] = "unclassified"
        i = j

    samples = pd.DataFrame({"time_s": t, "x": xx, "y": yy, "velocity": velocity, "label": label})

    # Collapse to events with correct end time = onset of next label (or +step)
    change = samples["label"].ne(samples["label"].shift(fill_value=samples["label"].iloc[0]))
    run = change.cumsum()
    rows = []
    for _, g in samples.groupby(run, sort=True):
        lab = g["label"].iloc[0]
        if lab == "unclassified":
            continue
        i0 = int(g.index[0])
        i1 = int(g.index[-1])  # last index in this run
        start = float(t[i0])
        if i1 + 1 < n:
            end = float(t[i1 + 1])
        else:
            end = float(t[i1] + step) if np.isfinite(step) else float(t[i1])
        rows.append(
            {
                "label": lab,
                "start_s": start,
                "end_s": end,
                "duration_s": end - start,
                "x_mean": float(g["x"].mean()),
                "y_mean": float(g["y"].mean()),
                "n_samples": int(len(g)),
            }
        )
    events = pd.DataFrame(rows)
    return samples, events
