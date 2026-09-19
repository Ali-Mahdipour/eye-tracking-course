"""Academic-style summary tables and simple inferential helpers for training."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def mean_sd_table(
    df: pd.DataFrame,
    value_col: str,
    by: str | list[str],
    *,
    digits: int = 2,
) -> pd.DataFrame:
    """Mean (SD) and N by group — classic paper-style descriptive table."""
    if isinstance(by, str):
        by = [by]
    g = df.groupby(by, dropna=False)[value_col]
    out = g.agg(N="count", Mean="mean", SD="std").reset_index()
    out["Mean_SD"] = out.apply(
        lambda r: f"{r['Mean']:.{digits}f} ({r['SD']:.{digits}f})" if pd.notna(r["SD"]) else f"{r['Mean']:.{digits}f}",
        axis=1,
    )
    return out


def cohens_d(a: pd.Series | np.ndarray, b: pd.Series | np.ndarray) -> float:
    """Cohen's d for two independent samples (pooled SD)."""
    x = np.asarray(a, dtype=float)
    y = np.asarray(b, dtype=float)
    x = x[np.isfinite(x)]
    y = y[np.isfinite(y)]
    nx, ny = len(x), len(y)
    if nx < 2 or ny < 2:
        return float("nan")
    sx, sy = x.std(ddof=1), y.std(ddof=1)
    pooled = np.sqrt(((nx - 1) * sx**2 + (ny - 1) * sy**2) / (nx + ny - 2))
    if pooled == 0:
        return float("nan")
    return float((x.mean() - y.mean()) / pooled)


def apa_ttest(
    a: pd.Series | np.ndarray,
    b: pd.Series | np.ndarray,
    *,
    alternative: str = "two-sided",
    label_a: str = "A",
    label_b: str = "B",
) -> dict:
    """
    Independent-samples t-test with APA-like string for slides / reports.

    Example: t(28) = 2.14, p = .041, d = 0.78
    """
    x = np.asarray(a, dtype=float)
    y = np.asarray(b, dtype=float)
    x = x[np.isfinite(x)]
    y = y[np.isfinite(y)]
    res = stats.ttest_ind(x, y, equal_var=False, alternative=alternative)
    d = cohens_d(x, y)
    df_approx = len(x) + len(y) - 2
    p = float(res.pvalue)
    p_txt = "< .001" if p < 0.001 else f"= {p:.3f}".replace("0.", ".")
    apa = f"t({df_approx}) = {res.statistic:.2f}, p {p_txt}, d = {d:.2f}"
    return {
        "label_a": label_a,
        "label_b": label_b,
        "n_a": len(x),
        "n_b": len(y),
        "mean_a": float(np.mean(x)) if len(x) else np.nan,
        "mean_b": float(np.mean(y)) if len(y) else np.nan,
        "t": float(res.statistic),
        "p": p,
        "df": df_approx,
        "cohens_d": d,
        "apa": apa,
    }
