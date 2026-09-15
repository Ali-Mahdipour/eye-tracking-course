#!/usr/bin/env python3
"""Build workshop Jupyter notebooks as .ipynb JSON."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "notebooks"


def nb(cells: list[dict]) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def md(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def write(name: str, cells: list[dict]) -> None:
    path = OUT / name
    path.write_text(json.dumps(nb(cells), indent=1), encoding="utf-8")
    print("wrote", path)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    write(
        "01_python_crash_course.ipynb",
        [
            md(
                """# 01 — Python crash course for eye-tracking

**Session:** Fri analysis block · NBML workshop 2026

Goals: load tables, filter rows, group metrics, make a first plot. We use pandas the way you might use Excel pivot tables — but scriptable.
"""
            ),
            code(
                """from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

DATA = Path("../../Data/demo")
DATA.exists()"""
            ),
            md("## Series & DataFrames (think: columns in a spreadsheet)"),
            code(
                """fix_durations_ms = pd.Series([180, 240, 90, 410, 300], name="fixation_duration_ms")
fix_durations_ms.describe()"""
            ),
            code(
                """df = pd.DataFrame({
    "participant": ["p01", "p01", "p02", "p02"],
    "aoi": ["logo", "price", "logo", "price"],
    "dwell_ms": [820, 310, 640, 500],
})
df"""
            ),
            md("## Filter, group, summarize"),
            code(
                """df.query("dwell_ms >= 500")"""
            ),
            code(
                """df.groupby("aoi", as_index=False)["dwell_ms"].mean()"""
            ),
            md("## Tiny plot"),
            code(
                """ax = df.groupby("aoi")["dwell_ms"].mean().plot(kind="bar", color="#2a6f6f")
ax.set_ylabel("Mean dwell (ms)")
ax.set_title("AOI dwell — toy example")
plt.tight_layout()
plt.show()"""
            ),
            md(
                """## Practice
1. Add a third AOI and two more rows.
2. Compute total dwell per participant.
3. Open `Data/demo/tobii_like_aoi_metrics.csv` and list its columns.
"""
            ),
        ],
    )

    write(
        "02_import_eye_tracking_csvs.ipynb",
        [
            md(
                """# 02 — Import Pupil-like & Tobii-like CSVs

**Session:** Thu preprocess / Fri analysis

We load: (1) synthetic Pupil-style gaze, (2) event table, (3) Tobii-like AOI metrics, (4) optional real TSV from `Data/decision making/`.
"""
            ),
            code(
                """from pathlib import Path
import pandas as pd

DEMO = Path("../../Data/demo")
TOBII_SAMPLE = Path("../../Data/decision making/sample Metrics 13-01-23.tsv")

gaze = pd.read_csv(DEMO / "pupil_gaze_demo.csv")
events = pd.read_csv(DEMO / "pupil_events_demo.csv")
aoi = pd.read_csv(DEMO / "tobii_like_aoi_metrics.csv")

gaze.head(), events.head(), aoi.head()"""
            ),
            md("## Quality peek: confidence & missingness"),
            code(
                """gaze["confidence"].describe()
# Rule of thumb for demos: drop very low confidence samples before metrics
gaze_q = gaze.query("confidence >= 0.6").copy()
len(gaze), len(gaze_q)"""
            ),
            md("## Tobii-style TSV (tab-separated)"),
            code(
                """if TOBII_SAMPLE.exists():
    tobii = pd.read_csv(TOBII_SAMPLE, sep="\\t")
    print(tobii.head())
    print(tobii.columns[:12].tolist())
else:
    print("Sample TSV not found — use demo AOI CSV instead.")"""
            ),
            md(
                """## Export tips (from Player / Tobii)
- Prefer CSV/TSV with a clear header row.
- Keep a README next to exports: software version, filter settings, participant codes.
- Never overwrite raw exports — copy then clean.
"""
            ),
        ],
    )

    write(
        "03_fixation_saccade_metrics.ipynb",
        [
            md(
                """# 03 — Fixation & saccade metrics

**Session:** Fri · dwell, counts, saccade velocity / amplitude

From an event table you can already compute many “headline” metrics without raw gaze.
"""
            ),
            code(
                """from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

events = pd.read_csv(Path("../../Data/demo/pupil_events_demo.csv"))
events"""
            ),
            code(
                """fix = events.query("type == 'fixation'").copy()
sac = events.query("type == 'saccade'").copy()

summary = {
    "n_fixations": len(fix),
    "total_dwell_s": fix["duration_s"].sum(),
    "mean_fix_s": fix["duration_s"].mean(),
    "n_saccades": len(sac),
    "mean_peak_velocity": sac["peak_velocity_deg_s"].mean(),
    "mean_amplitude_deg": sac["amplitude_deg"].mean(),
}
summary"""
            ),
            md("## Scanpath complexity (simple teaching proxies)"),
            code(
                """# Proxy 1: number of saccades
# Proxy 2: sum of saccade amplitudes (path length in degrees)
complexity = pd.Series({
    "n_saccades": len(sac),
    "path_length_deg": sac["amplitude_deg"].sum(),
    "mean_fix_duration_s": fix["duration_s"].mean(),
})
complexity"""
            ),
            code(
                """fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(fix["event_id"].astype(str), fix["duration_s"], color="#c45c26")
ax.set_xlabel("Fixation event id")
ax.set_ylabel("Duration (s)")
ax.set_title("Fixation durations — demo recording")
plt.tight_layout()
plt.show()"""
            ),
            md(
                """## Stretch
Implement a toy I-DT on `pupil_gaze_demo.csv`: window samples by time, mark low-dispersion windows as fixations, compare counts to `pupil_events_demo.csv`.
"""
            ),
        ],
    )

    write(
        "04_aoi_analysis.ipynb",
        [
            md(
                """# 04 — AOI analysis

**Session:** Fri · static AOIs, dwell, TTFF, visits

AOIs turn continuous gaze into region-level psychology (and UX questions): *Did they see the price? How long until the buy button?*
"""
            ),
            code(
                """from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

aoi = pd.read_csv(Path("../../Data/demo/tobii_like_aoi_metrics.csv"))
aoi.head()"""
            ),
            code(
                """# Dwell by AOI
dwell = aoi.groupby("AOI", as_index=False)["Total_duration_of_fixations"].mean()
dwell.sort_values("Total_duration_of_fixations", ascending=False)"""
            ),
            code(
                """plt.figure(figsize=(7, 4))
sns.boxplot(data=aoi, x="AOI", y="Total_duration_of_fixations", hue="condition")
plt.ylabel("Total fixation duration (ms)")
plt.title("AOI dwell by condition (synthetic)")
plt.tight_layout()
plt.show()"""
            ),
            code(
                """# Time to first fixation (TTFF) — lower often means earlier attention
ttff = aoi.dropna(subset=["Time_to_first_fixation"]).groupby("AOI")[
    "Time_to_first_fixation"
].median()
ttff"""
            ),
            md(
                """## Static vs dynamic AOIs
- **Static:** fixed rectangles/polygons on an image (product, button).
- **Dynamic:** AOIs that move/appear with video timeline (Tobii Pro Lab shines here).

Map gaze → AOI with polygon tests later; for Player/world video, surface tracking / manual coding may be needed.
"""
            ),
            md(
                """## Excel bridge
Import this CSV into `workshop/excel/aoi-tables-starter.xlsx` and rebuild the pivot for mean dwell by AOI.
"""
            ),
        ],
    )

    write(
        "05_pupillometry.ipynb",
        [
            md(
                """# 05 — Pupillometry basics

**Session:** Next Thu · advanced

Pupil size responds to light **and** cognitive/affective load. Always think about luminance confounds before claiming “cognitive load.”
"""
            ),
            code(
                """from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pupil = pd.read_csv(Path("../../Data/demo/pupillometry_demo.csv"))
pupil.head()"""
            ),
            code(
                """# Interpolate short blink gaps for teaching demos only
pupil["diameter_filled"] = pupil["diameter_mm"].interpolate(limit=8)

baseline = pupil.loc[pupil["task_phase"] == "baseline", "diameter_filled"].mean()
pupil["diameter_baseline_corrected"] = pupil["diameter_filled"] - baseline
baseline"""
            ),
            code(
                """fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(pupil["timestamp"], pupil["diameter_baseline_corrected"], color="#1f4e5f")
for phase, color in [("baseline", "#aaa"), ("task", "#e6c07b"), ("recovery", "#aaa")]:
    sub = pupil.query("task_phase == @phase")
    if len(sub):
        ax.axvspan(sub["timestamp"].min(), sub["timestamp"].max(), color=color, alpha=0.25)
ax.axhline(0, color="k", lw=0.8)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Δ diameter (mm)")
ax.set_title("Baseline-corrected pupil — synthetic trial")
plt.tight_layout()
plt.show()"""
            ),
            code(
                """pupil.groupby("task_phase")["diameter_baseline_corrected"].agg(["mean", "std"])"""
            ),
            md(
                """## Good practice
- Record a **pre-stimulus baseline**.
- Log lighting changes.
- Report preprocessing (blink handling, filtering) in your methods.
"""
            ),
        ],
    )

    write(
        "06_visualization.ipynb",
        [
            md(
                """# 06 — Visualization & light reporting

**Session:** Next Fri · matplotlib + plotly

Prefer clear single-message figures over dashboard soup.
"""
            ),
            code(
                """from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

gaze = pd.read_csv(Path("../../Data/demo/pupil_gaze_demo.csv"))
aoi = pd.read_csv(Path("../../Data/demo/tobii_like_aoi_metrics.csv"))"""
            ),
            code(
                """# Gaze scatter (normalized scene coordinates)
fig, ax = plt.subplots(figsize=(5, 4))
hb = ax.hexbin(gaze["norm_pos_x"], gaze["norm_pos_y"], gridsize=25, cmap="YlOrBr", mincnt=1)
ax.set_xlabel("norm_pos_x")
ax.set_ylabel("norm_pos_y")
ax.set_title("Gaze density (demo)")
ax.set_aspect("equal")
fig.colorbar(hb, ax=ax, label="count")
plt.tight_layout()
plt.show()"""
            ),
            code(
                """fig = px.box(
    aoi,
    x="AOI",
    y="Number_of_fixations",
    color="condition",
    title="Fixation counts by AOI (interactive)",
)
fig.show()"""
            ),
            md(
                """## Reporting checklist
- State sample size and exclusions.
- Define AOIs with a figure.
- Match colors across related plots.
- Export PNG/SVG for slides; keep notebooks for reproducibility (Git).
"""
            ),
        ],
    )

    write(
        "07_optional_stats.ipynb",
        [
            md(
                """# 07 — Optional stats (statsmodels / pingouin)

**Session:** Next Thu · optional

Tiny illustrative tests on synthetic AOI dwell. Real studies need power, random effects, and preregistration — this is just plumbing practice.
"""
            ),
            code(
                """from pathlib import Path
import pandas as pd
import pingouin as pg
import statsmodels.formula.api as smf

aoi = pd.read_csv(Path("../../Data/demo/tobii_like_aoi_metrics.csv"))
# Collapse to participant × AOI mean dwell
agg = (
    aoi.groupby(["Participant", "AOI", "condition"], as_index=False)[
        "Total_duration_of_fixations"
    ].mean()
    .rename(columns={"Total_duration_of_fixations": "dwell"})
)
agg.head()"""
            ),
            code(
                """# Nonparametric comparison example: product vs buy_button dwell
wide = agg.pivot_table(index="Participant", columns="AOI", values="dwell")
pg.wilcoxon(wide["product"], wide["buy_button"])"""
            ),
            code(
                """# Simple OLS (teaching only — prefer mixed models for repeated measures)
model = smf.ols("dwell ~ C(AOI) + C(condition)", data=agg).fit()
print(model.summary().tables[1])"""
            ),
            md(
                """## Mixed models (conceptual)
For repeated measures: `dwell ~ condition + (1|Participant)`.  
In R you may have used `lme4`; in Python try `statsmodels` mixedlm or `pymer4` if you have R installed. Discuss design with Dr. Khorrami for cognitive framing.
"""
            ),
        ],
    )


if __name__ == "__main__":
    main()
