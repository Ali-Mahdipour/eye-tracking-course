"""AOI hit-testing and simple TOI/AOI metrics for teaching."""

from __future__ import annotations

from typing import Mapping

import numpy as np
import pandas as pd

# Default rectangles for 1366×768 Decision Making stimuli (approximate teaching AOIs).
# Coordinates are pixel boxes: (x_min, y_min, x_max, y_max) with origin top-left.
# Refine live in class using the stimulus image axes if needed.
DEFAULT_FOOD_AOIS: dict[str, dict[str, tuple[float, float, float, float]]] = {
    # Shared layout across cake/pizza/ice-cream/cereal/date screenshots
    "_shared": {
        "food-pic": (430, 140, 930, 520),
        "buy": (180, 560, 520, 700),
        "not-buy": (840, 560, 1180, 700),
    }
}


def load_default_food_aois(stimulus: str | None = None) -> dict[str, tuple[float, float, float, float]]:
    """Return AOI rectangles for a food stimulus name (or shared defaults)."""
    shared = DEFAULT_FOOD_AOIS["_shared"]
    if stimulus is None:
        return dict(shared)
    key = stimulus.strip().lower()
    return dict(DEFAULT_FOOD_AOIS.get(key, shared))


def hit_test_rectangles(
    x: pd.Series | np.ndarray,
    y: pd.Series | np.ndarray,
    aois: Mapping[str, tuple[float, float, float, float]],
) -> pd.Series:
    """
    Return AOI name for each (x, y), or NA if outside all rectangles.
    First matching AOI wins (dict insertion order).
    """
    xs = np.asarray(x, dtype=float)
    ys = np.asarray(y, dtype=float)
    out = np.array([pd.NA] * len(xs), dtype=object)
    remaining = np.isfinite(xs) & np.isfinite(ys)
    for name, (x0, y0, x1, y1) in aois.items():
        inside = remaining & (xs >= x0) & (xs <= x1) & (ys >= y0) & (ys <= y1)
        out[inside] = name
        remaining &= ~inside
    return pd.Series(out, index=getattr(x, "index", None), name="aoi")


def aoi_metrics_from_fixations(
    fixations: pd.DataFrame,
    *,
    aoi_col: str = "aoi",
    duration_col: str = "duration_s",
    time_col: str | None = "start_s",
    toi: str | None = None,
) -> pd.DataFrame:
    """
    Classic teaching metrics per AOI (and optional TOI label).

    Expects a fixation-event table with AOI labels already assigned.
    """
    df = fixations.copy()
    if toi is not None:
        df["toi"] = toi
    if aoi_col not in df.columns:
        raise KeyError(f"Missing AOI column: {aoi_col}")
    if duration_col not in df.columns:
        raise KeyError(f"Missing duration column: {duration_col}")

    df = df.dropna(subset=[aoi_col])
    rows = []
    group_cols = ["toi", aoi_col] if "toi" in df.columns else [aoi_col]
    for keys, g in df.groupby(group_cols, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        record = dict(zip(group_cols, keys))
        durs = g[duration_col].astype(float)
        record.update(
            {
                "n_fixations": int(len(g)),
                "dwell_s": float(durs.sum()),
                "mean_fixation_s": float(durs.mean()) if len(g) else np.nan,
                "ttff_s": float(g[time_col].min()) if time_col and time_col in g else np.nan,
            }
        )
        rows.append(record)
    return pd.DataFrame(rows)
