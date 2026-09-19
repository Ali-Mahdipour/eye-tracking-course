"""
I-VT (Velocity-Threshold Identification) eye-movement classifier.

Teaching implementation of Salvucci & Goldberg (2000)-style I-VT:
classify each sample as fixation or saccade by point-to-point velocity.

Notes for class
---------------
- Thresholds depend on units. Here we support screen pixels / second
  (common for Tobii pixel gaze) or degrees / second if you convert first.
- This is intentionally readable, not a production DSP pipeline.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def ivt_classify(
    time_s: Iterable[float],
    x: Iterable[float],
    y: Iterable[float],
    *,
    velocity_threshold: float = 5000.0,
    min_fixation_duration_s: float = 0.06,
) -> pd.DataFrame:
    """
    Classify gaze samples with I-VT.

    Parameters
    ----------
    time_s, x, y
        Sample timestamps (seconds) and gaze coordinates (same units for x/y).
    velocity_threshold
        Samples with instantaneous speed >= threshold are labeled saccade.
        For Tobii **pixel** gaze on ~1366×768 stimuli, classroom starting
        values are often **1000–5000 px/s** (inspect your Δt units first).
        For degrees/second after proper conversion, try ~30–100.
    min_fixation_duration_s
        Fixation runs shorter than this are relabeled as unclassified.

    Returns
    -------
    DataFrame with columns: time_s, x, y, velocity, label
      label ∈ {fixation, saccade, unclassified}
    """
    t = np.asarray(list(time_s), dtype=float)
    xx = np.asarray(list(x), dtype=float)
    yy = np.asarray(list(y), dtype=float)
    if not (len(t) == len(xx) == len(yy)):
        raise ValueError("time_s, x, y must have the same length")
    if len(t) < 2:
        raise ValueError("Need at least 2 samples")

    dt = np.diff(t, prepend=t[0])
    dt[0] = np.nan
    # avoid divide-by-zero on duplicate timestamps
    dt_safe = np.where((~np.isfinite(dt)) | (dt <= 0), np.nan, dt)
    dx = np.diff(xx, prepend=xx[0])
    dy = np.diff(yy, prepend=yy[0])
    dx[0] = np.nan
    dy[0] = np.nan
    dist = np.sqrt(dx**2 + dy**2)
    velocity = dist / dt_safe

    label = np.full(len(t), "unclassified", dtype=object)
    valid = np.isfinite(velocity)
    label[valid & (velocity < velocity_threshold)] = "fixation"
    label[valid & (velocity >= velocity_threshold)] = "saccade"

    # Enforce minimum fixation duration on contiguous runs
    i = 0
    n = len(label)
    while i < n:
        if label[i] != "fixation":
            i += 1
            continue
        j = i + 1
        while j < n and label[j] == "fixation":
            j += 1
        dur = t[j - 1] - t[i]
        if not np.isfinite(dur) or dur < min_fixation_duration_s:
            label[i:j] = "unclassified"
        i = j

    return pd.DataFrame(
        {
            "time_s": t,
            "x": xx,
            "y": yy,
            "velocity": velocity,
            "label": label,
        }
    )


def summarize_ivt_events(classified: pd.DataFrame) -> pd.DataFrame:
    """Collapse sample labels into fixation/saccade event table."""
    df = classified.copy()
    if df.empty:
        return pd.DataFrame(
            columns=["event_id", "label", "start_s", "end_s", "duration_s", "centroid_x", "centroid_y"]
        )

    # run-length encode labels
    change = df["label"].ne(df["label"].shift(fill_value=df["label"].iloc[0]))
    run_id = change.cumsum()
    rows = []
    for rid, g in df.groupby(run_id, sort=True):
        lab = g["label"].iloc[0]
        if lab == "unclassified":
            continue
        rows.append(
            {
                "event_id": int(rid),
                "label": lab,
                "start_s": float(g["time_s"].iloc[0]),
                "end_s": float(g["time_s"].iloc[-1]),
                "duration_s": float(g["time_s"].iloc[-1] - g["time_s"].iloc[0]),
                "centroid_x": float(g["x"].mean()),
                "centroid_y": float(g["y"].mean()),
                "peak_velocity": float(np.nanmax(g["velocity"].to_numpy())),
                "n_samples": int(len(g)),
            }
        )
    return pd.DataFrame(rows)
