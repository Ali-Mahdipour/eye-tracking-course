"""Heatmaps and Tobii-like gaze / scanpath plots over stimulus images."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image


def _load_image(path: Path | str) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGBA"))


def fixation_heatmap(
    fixations: pd.DataFrame,
    stimulus_path: Path | str,
    *,
    x_col: str = "x",
    y_col: str = "y",
    weight_col: str | None = None,
    bins: int = 64,
    alpha: float = 0.45,
    ax: plt.Axes | None = None,
    title: str | None = None,
) -> plt.Axes:
    """
    Fixation-count heatmap (default) or duration-weighted heatmap.

    Set weight_col='duration_s' for duration-based heatmaps.
    """
    img = _load_image(stimulus_path)
    h, w = img.shape[0], img.shape[1]
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5.2))

    ax.imshow(img)
    xs = fixations[x_col].astype(float).to_numpy()
    ys = fixations[y_col].astype(float).to_numpy()
    mask = np.isfinite(xs) & np.isfinite(ys)
    xs, ys = xs[mask], ys[mask]
    if weight_col is None:
        weights = None
        kind = "count"
    else:
        weights = fixations.loc[mask, weight_col].astype(float).to_numpy()
        kind = "duration"

    if len(xs) == 0:
        ax.set_title(title or f"Heatmap ({kind}) — no fixations")
        ax.axis("off")
        return ax

    heatmap, xedges, yedges = np.histogram2d(
        xs,
        ys,
        bins=bins,
        range=[[0, w], [0, h]],
        weights=weights,
    )
    # histogram2d uses x along columns; imshow needs careful orientation
    heat = heatmap.T
    # mild smoothing via convolution-like expansion (teaching-friendly)
    from scipy.ndimage import gaussian_filter

    heat = gaussian_filter(heat.astype(float), sigma=1.6)

    cmap = LinearSegmentedColormap.from_list(
        "et_heat",
        ["#00000000", "#2c7bb6", "#fdae61", "#d7191c"],
    )
    ax.imshow(
        heat,
        extent=[0, w, h, 0],
        cmap=cmap,
        alpha=alpha,
        interpolation="bilinear",
    )
    ax.set_title(title or f"Fixation {kind} heatmap")
    ax.axis("off")
    return ax


def gaze_plot_tobii_like(
    fixations: pd.DataFrame,
    stimulus_path: Path | str,
    *,
    x_col: str = "x",
    y_col: str = "y",
    duration_col: str = "duration_s",
    order_col: str | None = None,
    ax: plt.Axes | None = None,
    title: str | None = None,
    max_radius: float = 40.0,
) -> plt.Axes:
    """
    Tobii-style gaze plot: circles sized by fixation duration, numbered in order,
    connected by scanpath lines.
    """
    img = _load_image(stimulus_path)
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 5.2))
    ax.imshow(img)

    df = fixations.copy()
    if order_col and order_col in df.columns:
        df = df.sort_values(order_col)
    else:
        # stable order as provided
        df = df.reset_index(drop=True)

    xs = df[x_col].astype(float).to_numpy()
    ys = df[y_col].astype(float).to_numpy()
    durs = df[duration_col].astype(float).to_numpy() if duration_col in df.columns else np.ones(len(df))
    mask = np.isfinite(xs) & np.isfinite(ys)
    xs, ys, durs = xs[mask], ys[mask], durs[mask]
    if len(xs) == 0:
        ax.set_title(title or "Gaze plot — no fixations")
        ax.axis("off")
        return ax

    # connect scanpath
    ax.plot(xs, ys, color="#222222", linewidth=1.0, alpha=0.7, zorder=2)
    scale = max_radius / max(float(np.nanmax(durs)), 1e-6)
    for i, (x, y, d) in enumerate(zip(xs, ys, durs), start=1):
        r = max(6.0, float(d) * scale)
        circ = plt.Circle((x, y), r, facecolor="#e41a1c88", edgecolor="#7f0000", linewidth=1.2, zorder=3)
        ax.add_patch(circ)
        ax.text(x, y, str(i), ha="center", va="center", fontsize=7, color="white", zorder=4)

    ax.set_title(title or "Tobii-like gaze plot (order + duration)")
    ax.axis("off")
    return ax
