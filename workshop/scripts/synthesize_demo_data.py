#!/usr/bin/env python3
"""Generate small, clean demo CSVs for NBML workshop notebooks.

These files mimic Pupil Labs Player exports and Tobii-like AOI metrics tables.
They are synthetic teaching data — not real participant recordings.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Data" / "demo"
RNG = np.random.default_rng(42)


def make_pupil_gaze(n: int = 600, fs: float = 120.0) -> pd.DataFrame:
    t = np.arange(n) / fs
    # Two AOI-ish clusters + a few saccades
    x = np.concatenate(
        [
            RNG.normal(0.25, 0.02, n // 3),
            np.linspace(0.25, 0.75, n // 6),
            RNG.normal(0.75, 0.02, n // 3),
            np.linspace(0.75, 0.40, n - (n // 3 + n // 6 + n // 3)),
        ]
    )
    y = np.concatenate(
        [
            RNG.normal(0.40, 0.02, n // 3),
            np.linspace(0.40, 0.55, n // 6),
            RNG.normal(0.55, 0.02, n // 3),
            np.linspace(0.55, 0.35, n - (n // 3 + n // 6 + n // 3)),
        ]
    )
    confidence = np.clip(RNG.normal(0.92, 0.05, n), 0.4, 1.0)
    pupil = 3.2 + 0.15 * np.sin(2 * np.pi * t / 8) + RNG.normal(0, 0.05, n)
    return pd.DataFrame(
        {
            "timestamp": np.round(t, 4),
            "norm_pos_x": np.round(x, 5),
            "norm_pos_y": np.round(y, 5),
            "confidence": np.round(confidence, 3),
            "diameter_3d_mm": np.round(pupil, 4),
            "participant": "demo_p01",
            "recording": "demo_rec_01",
        }
    )


def make_fixations(gaze: pd.DataFrame) -> pd.DataFrame:
    """Simple I-DT-like event table for teaching."""
    events = []
    # Hard-code a few clear fixation / saccade events for demos
    specs = [
        ("fixation", 0.00, 1.80, 0.25, 0.40),
        ("saccade", 1.80, 2.10, 0.50, 0.48),
        ("fixation", 2.10, 4.00, 0.75, 0.55),
        ("saccade", 4.00, 4.25, 0.58, 0.45),
        ("fixation", 4.25, 5.00, 0.40, 0.35),
    ]
    for i, (etype, start, end, x, y) in enumerate(specs, start=1):
        dur = end - start
        events.append(
            {
                "event_id": i,
                "type": etype,
                "start_time": start,
                "end_time": end,
                "duration_s": round(dur, 3),
                "norm_pos_x": x,
                "norm_pos_y": y,
                "dispersion": 0.015 if etype == "fixation" else np.nan,
                "amplitude_deg": np.nan if etype == "fixation" else round(12 + i, 1),
                "peak_velocity_deg_s": np.nan if etype == "fixation" else round(180 + 20 * i, 1),
                "aoi": "left_panel" if x < 0.5 else "right_panel",
                "participant": "demo_p01",
                "recording": "demo_rec_01",
            }
        )
    return pd.DataFrame(events)


def make_tobii_like_aoi() -> pd.DataFrame:
    rows = []
    participants = [f"p{i:02d}" for i in range(1, 9)]
    media = ["cake", "cereal", "date", "ice-cream"]
    aois = ["product", "ingredients", "buy_button"]
    for p in participants:
        for m in media:
            for aoi in aois:
                n_fix = int(RNG.integers(0, 12))
                total_fix = float(np.round(RNG.uniform(0, 2500) if n_fix else 0, 1))
                rows.append(
                    {
                        "Recording": f"Recording_{p}",
                        "Participant": p,
                        "Media": m,
                        "AOI": aoi,
                        "Number_of_fixations": n_fix,
                        "Total_duration_of_fixations": total_fix,
                        "Average_duration_of_fixations": round(total_fix / n_fix, 1)
                        if n_fix
                        else 0.0,
                        "Time_to_first_fixation": round(float(RNG.uniform(50, 2000)), 1)
                        if n_fix
                        else np.nan,
                        "Average_pupil_diameter": round(float(RNG.uniform(2.8, 4.2)), 3)
                        if n_fix
                        else np.nan,
                        "Number_of_Visits": int(RNG.integers(0, 5)),
                        "condition": RNG.choice(["high_cal", "low_cal"]),
                    }
                )
    return pd.DataFrame(rows)


def make_pupillometry(n: int = 400, fs: float = 60.0) -> pd.DataFrame:
    t = np.arange(n) / fs
    baseline = 3.4
    # Cognitive load bump mid-trial
    load = 0.35 * np.exp(-0.5 * ((t - 3.5) / 0.8) ** 2)
    blink = (t > 2.0) & (t < 2.12)
    diameter = baseline + load + RNG.normal(0, 0.03, n)
    diameter[blink] = np.nan
    return pd.DataFrame(
        {
            "timestamp": np.round(t, 4),
            "diameter_mm": np.round(diameter, 4),
            "task_phase": np.where(t < 1.5, "baseline", np.where(t < 5.0, "task", "recovery")),
            "participant": "demo_p01",
            "trial": 1,
        }
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gaze = make_pupil_gaze()
    fix = make_fixations(gaze)
    aoi = make_tobii_like_aoi()
    pupil = make_pupillometry()

    gaze.to_csv(OUT / "pupil_gaze_demo.csv", index=False)
    fix.to_csv(OUT / "pupil_events_demo.csv", index=False)
    aoi.to_csv(OUT / "tobii_like_aoi_metrics.csv", index=False)
    pupil.to_csv(OUT / "pupillometry_demo.csv", index=False)
    print(f"Wrote demo CSVs to {OUT}")


if __name__ == "__main__":
    main()
