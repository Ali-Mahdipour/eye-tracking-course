#!/usr/bin/env python3
"""Build four 1.5-hour analysis-training session notebooks."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "sessions"


def nb(cells: list[dict]) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
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
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    path.write_text(json.dumps(nb(cells), indent=1), encoding="utf-8")
    print("wrote", path)


def session1() -> None:
    write(
        "S01_python_and_data_landscape.ipynb",
        [
            md(
                """# Session 1 — Python preliminaries & the eye-tracking data landscape  
**Duration:** 1.5 hours · NBML analysis training

### Learning goals
1. Survive in a Jupyter notebook (run cells, read errors, restart kernel).
2. Load Tobii and Pupil Labs tables with **pandas**.
3. Know which famous Python libraries we will use this week — and what each is for.
4. Map **files → analysis questions** for the workshop datasets.

> Audience assumption: little or no Python. We go slowly and compare every step to Excel.
"""
            ),
            md(
                """## 0. Classroom setup (10 min)

1. Open a terminal in the course repo root.
2. Activate your environment (see `workshop/SETUP.md`).
3. Launch Jupyter:

```bash
jupyter notebook workshop/sessions
```

4. Open this file (`S01_...`).

**Rule of the room:** if a cell fails, read the **last line** of the error first.
"""
            ),
            md("## 1. Variables, lists, and a tiny loop (15 min)"),
            code(
                """participant = "Recording3"
aois = ["food-pic", "buy", "not-buy"]
print("Hello,", participant)
for i, name in enumerate(aois, start=1):
    print(i, name)"""
            ),
            md(
                """## 2. Libraries we will actually use (15 min)

| Library | Why eye-tracking people care |
|---------|------------------------------|
| **numpy** | Fast numeric arrays (gaze samples, velocity) |
| **pandas** | Tables — like Excel sheets with scripts |
| **matplotlib** / **seaborn** | Publication-style figures |
| **scipy** | Stats utilities, filters, t-tests |
| **statsmodels** | Regression / ANOVA with academic output |
| **pingouin** | Friendly stats API (t-tests, corr, reliability) |
| **Pillow (PIL)** | Load stimulus images for overlays |
| **openpyxl** | Read Tobii `.xlsx` exports |

Also know the names (we may only demo briefly): **neurokit2** (GSR/EDA), **PyGaze** / analysis tools, vendor SDKs (Tobii, Pupil).  
We prioritize **open tables + transparent code** over black-box GUIs.
"""
            ),
            code(
                """import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("Python", sys.version.split()[0])
print("numpy", np.__version__, "| pandas", pd.__version__)"""
            ),
            md("## 3. Point notebooks at the repo (5 min)"),
            code(
                """# This notebook lives in workshop/sessions/
# Add workshop/ to the path so `import analysis` works.
import sys
from pathlib import Path

SESSION_DIR = Path.cwd()
WORKSHOP_DIR = SESSION_DIR.parent if SESSION_DIR.name == "sessions" else SESSION_DIR / "workshop"
REPO = WORKSHOP_DIR.parent if WORKSHOP_DIR.name == "workshop" else SESSION_DIR.parents[1]

sys.path.insert(0, str(WORKSHOP_DIR))
from analysis.paths import data_path, stimuli_path, REPO_ROOT

print("REPO_ROOT =", REPO_ROOT)
print("Food data exists?", data_path("food_decision_making").exists())
print("Stimuli exist?", stimuli_path("Decision Making").exists())
list(data_path("food_decision_making").glob("*"))"""
            ),
            md(
                """## 4. Load workshop datasets (25 min)

### 4a. Tobii food metrics (event table — friendly first view)
"""
            ),
            code(
                """metrics = pd.read_csv(
    data_path("food_decision_making", "Food_Decision_Making_Metrics.tsv"),
    sep="\\t",
)
metrics.head()"""
            ),
            code(
                """print(metrics.shape)
print(metrics.columns.tolist())
metrics["AOI"].value_counts(dropna=False).head(15)"""
            ),
            md("### 4b. Teaching sample (one recording, sample-level gaze + mouse)"),
            code(
                """sample = pd.read_csv(data_path("food_decision_making", "Food_Decision_Making_Teaching_Sample.csv"))
print(sample.shape)
sample[["Recording timestamp", "Sensor", "Presented Stimulus name", "Gaze point X", "Gaze point Y", "Eye movement type"]].head(10)"""
            ),
            code(
                """sample["Sensor"].value_counts(dropna=False)
# How many gaze samples have coordinates?
gaze = sample.query("Sensor == 'Eye Tracker'").copy()
gaze["Gaze point X"].notna().mean()"""
            ),
            md("### 4c. Pupil Labs fixations & blinks"),
            code(
                """pupil_fix = pd.read_csv(data_path("pupil_labs_recording", "fixations.csv"))
pupil_blinks = pd.read_csv(data_path("pupil_labs_recording", "blinks.csv"))
print("fixations", pupil_fix.shape, "blinks", pupil_blinks.shape)
pupil_fix[["start_timestamp", "duration", "norm_pos_x", "norm_pos_y", "confidence"]].head()"""
            ),
            md("### 4d. Tobii GSR metrics (wide table)"),
            code(
                """gsr = pd.read_csv(data_path("tobii_gsr_demo", "Tobii_Pro_Lab_GSR_Demo_Project_Metrics.tsv"), sep="\\t")
print(gsr.shape)
keep = [c for c in gsr.columns if c in {
    "Recording","Participant","TOI","Media","Average_GSR","Number_of_SCR",
    "Last_key_press","Number_of_whole_fixations","Average_whole-fixation_pupil_diameter"
} or c.startswith("Number_of_mouse_clicks.") or c.startswith("Time_to_first_fixation.")]
gsr[keep].head()"""
            ),
            md(
                """## 5. Excel-brain → pandas-brain (15 min)

| Excel | pandas |
|-------|--------|
| Filter rows | `df.query("AOI == 'cake-pic'")` |
| Pivot / average | `df.groupby("AOI")["Duration"].mean()` |
| Sort | `df.sort_values("Duration", ascending=False)` |
| Save | `df.to_csv("out.csv", index=False)` |
"""
            ),
            code(
                """# Duration in the metrics file is often milliseconds — check a few values
m = metrics.dropna(subset=["Duration", "AOI"]).copy()
summary = (
    m.groupby("AOI", as_index=False)["Duration"]
    .agg(n="count", mean_ms="mean", median_ms="median")
    .sort_values("mean_ms", ascending=False)
)
summary.head(12)"""
            ),
            code(
                """ax = summary.head(8).plot(x="AOI", y="mean_ms", kind="bar", legend=False, color="#2a6f6f")
ax.set_ylabel("Mean fixation duration (ms)")
ax.set_title("Session 1 — first real metric plot")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()"""
            ),
            md(
                """## 6. Mini practice (10 min)

1. From `metrics`, keep only rows where `Event_type` looks like fixations (inspect unique values).
2. Compute mean `Average_pupil_size` by `AOI`.
3. Name one analysis question you could ask with **mouse clicks + gaze** in the GSR table.

## Exit ticket
Write one sentence: *Which file will you open first in Session 2 for I-VT, and why?*
"""
            ),
        ],
    )


def session2() -> None:
    write(
        "S02_ivt_aoi_heatmaps.ipynb",
        [
            md(
                """# Session 2 — I-VT filter, AOI/TOI metrics, heatmaps & gaze plots  
**Duration:** 1.5 hours

### Learning goals
1. Implement **I-VT** (velocity-threshold identification) on real Tobii samples.
2. Compare I-VT events with Tobii’s `Eye movement type` labels.
3. Assign **AOIs**, compute dwell / TTFF-style metrics, think in **TOIs**.
4. Draw **fixation-count** and **duration** heatmaps and a **Tobii-like gaze plot** on `Stimuli/Decision Making`.
"""
            ),
            code(
                """import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SESSION_DIR = Path.cwd()
WORKSHOP_DIR = SESSION_DIR.parent if SESSION_DIR.name == "sessions" else SESSION_DIR / "workshop"
sys.path.insert(0, str(WORKSHOP_DIR))

from analysis.paths import data_path, stimuli_path
from analysis.ivt import ivt_classify, summarize_ivt_events
from analysis.aoi import load_default_food_aois, hit_test_rectangles, aoi_metrics_from_fixations
from analysis.viz import fixation_heatmap, gaze_plot_tobii_like"""
            ),
            md(
                """## 1. What I-VT is doing (concept, 10 min)

For each sample, estimate speed ≈ distance / Δt.

- If speed **< threshold** → provisional **fixation**
- If speed **≥ threshold** → **saccade**
- Drop fixation runs shorter than a minimum duration

Threshold units matter: we use **pixels/second** on 1366×768 stimuli.
"""
            ),
            md("## 2. Prepare gaze samples (15 min)"),
            code(
                """raw = pd.read_csv(data_path("food_decision_making", "Food_Decision_Making_Teaching_Sample.csv"))
gaze = raw.query("Sensor == 'Eye Tracker'").copy()
gaze = gaze.dropna(subset=["Gaze point X", "Gaze point Y", "Recording timestamp"])
# Tobii recording timestamps are microseconds in this export
# In THIS export, Recording timestamp is milliseconds (≈17 ms steps ≈ 60 Hz).
# Always print median Δt before choosing an I-VT threshold.
gaze["time_s"] = gaze["Recording timestamp"].astype(float) / 1e3
gaze = gaze.sort_values("time_s")
print("median Δt (s) =", gaze["time_s"].diff().median())
# Focus on one food image TOI/stimulus for a clean demo
stim = "cake"
g = gaze[gaze["Presented Stimulus name"] == stim].copy()
print("samples on", stim, ":", len(g))
g[["time_s", "Gaze point X", "Gaze point Y", "Eye movement type"]].head()"""
            ),
            md("## 3. Run I-VT (20 min)"),
            code(
                """classified = ivt_classify(
    g["time_s"], g["Gaze point X"], g["Gaze point Y"],
    velocity_threshold=5000,  # px/s starting point for this screen; try 1000–8000
    min_fixation_duration_s=0.06,
)
classified["label"].value_counts()"""
            ),
            code(
                """events = summarize_ivt_events(classified)
fix = events.query("label == 'fixation'").copy()
sac = events.query("label == 'saccade'").copy()
print(fix.head())
print({"n_fix": len(fix), "n_sac": len(sac), "mean_fix_s": fix["duration_s"].mean()})"""
            ),
            code(
                """# Compare with Tobii vendor labels on the same samples
cmp = g[["Eye movement type"]].copy()
cmp["ivt"] = classified["label"].to_numpy()
pd.crosstab(cmp["Eye movement type"], cmp["ivt"])"""
            ),
            md(
                """## 4. AOIs & TOIs (20 min)

- **AOI** = region on the stimulus (food picture, buy, not-buy).
- **TOI** = time window of interest (here: while `cake` is on screen).

Teaching AOIs are approximate rectangles — refine them live if needed.
"""
            ),
            code(
                """aois = load_default_food_aois(stim)
aois"""
            ),
            code(
                """fix["aoi"] = hit_test_rectangles(fix["centroid_x"], fix["centroid_y"], aois)
fix["start_s"] = fix["start_s"] - fix["start_s"].min()  # TOI-relative optional
aoi_table = aoi_metrics_from_fixations(fix, toi=stim)
aoi_table"""
            ),
            md("## 5. Heatmaps & Tobii-like gaze plot (25 min)"),
            code(
                """stim_img = stimuli_path("Decision Making", f"{stim}.png")
assert stim_img.exists(), stim_img

# For heatmap helpers, use columns x/y/duration_s
plot_df = fix.rename(columns={"centroid_x": "x", "centroid_y": "y"})

fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
fixation_heatmap(plot_df, stim_img, ax=axes[0], title="Fixation COUNT heatmap")
fixation_heatmap(plot_df, stim_img, weight_col="duration_s", ax=axes[1], title="Fixation DURATION heatmap")
plt.tight_layout()
plt.show()"""
            ),
            code(
                """fig, ax = plt.subplots(figsize=(8.5, 4.8))
gaze_plot_tobii_like(plot_df, stim_img, ax=ax, title=f"Gaze plot — {stim}")
plt.show()"""
            ),
            md(
                """## 6. Practice / discussion (10 min)

1. Change `velocity_threshold` to 1000 and 8000. What happens to fixation count?
2. Re-run for `stim = "pizza"`.
3. Debate: when would you prefer **vendor classification** vs **your I-VT**?

### Exit ticket
Paste your AOI metrics table for one stimulus and one sentence interpreting dwell on `buy` vs `food-pic`.
"""
            ),
        ],
    )


def session3() -> None:
    write(
        "S03_behavior_gsr_pupil.ipynb",
        [
            md(
                """# Session 3 — Behavior (clicks / keys / RT), GSR, and pupil  
**Duration:** 1.5 hours

### Learning goals
1. Align **gaze** with **mouse** and stimulus events.
2. Compute simple response-time style metrics (stimulus → click).
3. Read Tobii **GSR** / SCR columns and discuss confounds.
4. Analyze **pupil** + **blinks** (Tobii food sample + Pupil Labs export).
"""
            ),
            code(
                """import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SESSION_DIR = Path.cwd()
WORKSHOP_DIR = SESSION_DIR.parent if SESSION_DIR.name == "sessions" else SESSION_DIR / "workshop"
sys.path.insert(0, str(WORKSHOP_DIR))
from analysis.paths import data_path"""
            ),
            md("## 1. Multimodal timeline on the food task (20 min)"),
            code(
                """raw = pd.read_csv(data_path("food_decision_making", "Food_Decision_Making_Teaching_Sample.csv"))
raw["time_s"] = raw["Recording timestamp"].astype(float) / 1e3  # ms → s in this export

events = raw.dropna(subset=["Event"]).copy()
events[["time_s", "Event", "Event value", "Presented Stimulus name"]].head(20)"""
            ),
            code(
                """# Stimulus intervals from ImageStimulusStart / End
starts = events.query("Event == 'ImageStimulusStart'")[["time_s", "Event value"]].rename(
    columns={"time_s": "start_s", "Event value": "stimulus"}
)
ends = events.query("Event == 'ImageStimulusEnd'")[["time_s", "Event value"]].rename(
    columns={"time_s": "end_s", "Event value": "stimulus"}
)
# Pair by order within stimulus name (teaching approach)
intervals = []
for stim, sgrp in starts.groupby("stimulus"):
    e = ends[ends["stimulus"] == stim].sort_values("end_s")
    s = sgrp.sort_values("start_s")
    for (_, row_s), (_, row_e) in zip(s.iterrows(), e.iterrows()):
        intervals.append({"stimulus": stim, "start_s": row_s["start_s"], "end_s": row_e["end_s"]})
intervals = pd.DataFrame(intervals)
intervals"""
            ),
            code(
                """mouse = raw.query("Sensor == 'Mouse'").dropna(subset=["Mouse position X", "Mouse position Y"]).copy()
clicks = events.query("Event == 'MouseEvent'").copy()
clicks.head()"""
            ),
            md(
                """## 2. Response times: stimulus onset → first click (20 min)

Not every export has a dedicated RT column — we **construct** RT from the timeline.
"""
            ),
            code(
                """# First mouse event after each food stimulus start (skip instruction/fixation/thanks)
foods = ["cake", "pizza", "ice-cream", "cereal", "date"]
rt_rows = []
for _, iv in intervals.query("stimulus in @foods").iterrows():
    c = clicks[(clicks["time_s"] >= iv["start_s"]) & (clicks["time_s"] <= iv["end_s"])]
    if len(c) == 0:
        continue
    first = c.sort_values("time_s").iloc[0]
    rt_rows.append({
        "stimulus": iv["stimulus"],
        "rt_s": float(first["time_s"] - iv["start_s"]),
        "click_value": first.get("Event value"),
    })
rt = pd.DataFrame(rt_rows)
rt"""
            ),
            code(
                """if len(rt):
    ax = rt.plot(x="stimulus", y="rt_s", kind="bar", legend=False, color="#8c2d4a")
    ax.set_ylabel("RT (s) — onset to first click")
    ax.set_title("Constructed response times")
    plt.tight_layout()
    plt.show()
else:
    print("No click-aligned RTs in this teaching sample — discuss why.")"""
            ),
            md(
                """## 3. GSR metrics table (20 min)

We use Tobii’s **aggregated** GSR metrics (classroom-friendly). Raw EDA pipelines (neurokit2) can be a bonus demo.
"""
            ),
            code(
                """gsr = pd.read_csv(data_path("tobii_gsr_demo", "Tobii_Pro_Lab_GSR_Demo_Project_Metrics.tsv"), sep="\\t")
cols = [
    "Recording", "Participant", "TOI", "Media", "Average_GSR", "Number_of_SCR",
    "Amplitude_of_event_related_SCR", "Average_whole-fixation_pupil_diameter",
    "Last_key_press",
]
cols = [c for c in cols if c in gsr.columns]
g = gsr[cols].copy()
# Coerce numeric fields that may contain strings
for c in ["Average_GSR", "Number_of_SCR", "Amplitude_of_event_related_SCR", "Average_whole-fixation_pupil_diameter"]:
    if c in g.columns:
        g[c] = pd.to_numeric(g[c], errors="coerce")
g.head()"""
            ),
            code(
                """# Participant-level GSR summary
part = g.groupby("Participant", as_index=False).agg(
    mean_gsr=("Average_GSR", "mean"),
    mean_scr=("Number_of_SCR", "mean"),
    mean_pupil=("Average_whole-fixation_pupil_diameter", "mean"),
)
part.head()"""
            ),
            code(
                """fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(part["mean_gsr"], part["mean_scr"], alpha=0.8)
ax.set_xlabel("Mean Average_GSR")
ax.set_ylabel("Mean Number_of_SCR")
ax.set_title("GSR level vs SCR count (participants)")
plt.tight_layout()
plt.show()"""
            ),
            md("## 4. Pupil diameter on the food sample (15 min)"),
            code(
                """gaze = raw.query("Sensor == 'Eye Tracker'").copy()
gaze["time_s"] = gaze["Recording timestamp"].astype(float) / 1e3
pup = gaze.dropna(subset=["Pupil diameter left"]).copy()
pup["pupil"] = pup[["Pupil diameter left", "Pupil diameter right"]].mean(axis=1, skipna=True)
# Simple baseline: first 0.5 s of each stimulus (if available)
rows = []
for stim, gstim in pup.groupby("Presented Stimulus name"):
    gstim = gstim.sort_values("time_s")
    t0 = gstim["time_s"].iloc[0]
    base = gstim.loc[gstim["time_s"] <= t0 + 0.5, "pupil"].mean()
    gstim = gstim.copy()
    gstim["pupil_baseline_corrected"] = gstim["pupil"] - base
    rows.append(gstim)
pup_c = pd.concat(rows, ignore_index=True)
pup_c.groupby("Presented Stimulus name")["pupil_baseline_corrected"].mean().sort_values()"""
            ),
            code(
                """# Blink awareness from Pupil Labs export
blinks = pd.read_csv(data_path("pupil_labs_recording", "blinks.csv"))
blinks["duration"].describe()"""
            ),
            md(
                """## 5. Combining gaze + behavior (15 min)

Classic teaching metric already present in GSR metrics:  
`Time_from_first_fixation_to_mouse_click.*`

We also build a transparent version on the food sample when AOI hit columns exist.
"""
            ),
            code(
                """aoi_cols = [c for c in raw.columns if c.startswith("AOI hit")]
print("AOI hit columns:", len(aoi_cols))
aoi_cols[:8]"""
            ),
            md(
                """## Practice
1. Plot pupil (baseline-corrected) over time for `cake`.
2. List three confounds for GSR in a lab with talking + movement.
3. Explain why RT from mouse events can disagree with Tobii “time to first click” metrics.

### Exit ticket
One multimodal question you could publish as a figure caption.
"""
            ),
        ],
    )


def session4() -> None:
    write(
        "S04_stats_models_and_libraries.ipynb",
        [
            md(
                """# Session 4 — Statistical models, academic outputs & library map  
**Duration:** 1.5 hours

### Learning goals
1. Build paper-style **Mean (SD)** tables.
2. Run a transparent **t-test** with Cohen’s *d* and an APA-like sentence.
3. Fit a simple **regression / group model** with statsmodels or pingouin.
4. Leave with a **library roadmap** for continued learning.
"""
            ),
            code(
                """import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SESSION_DIR = Path.cwd()
WORKSHOP_DIR = SESSION_DIR.parent if SESSION_DIR.name == "sessions" else SESSION_DIR / "workshop"
sys.path.insert(0, str(WORKSHOP_DIR))

from analysis.paths import data_path
from analysis.stats_report import mean_sd_table, apa_ttest

# Optional richer APIs
import pingouin as pg
import statsmodels.formula.api as smf"""
            ),
            md("## 1. Prepare an analysis-ready metrics table (15 min)"),
            code(
                """gsr = pd.read_csv(data_path("tobii_gsr_demo", "Tobii_Pro_Lab_GSR_Demo_Project_Metrics.tsv"), sep="\\t")
# Example: dwell-like metric on Snake AOI if present
col = "Total_duration_of_whole_fixations.Snake"
if col not in gsr.columns:
    # fallback: first matching duration column
    cand = [c for c in gsr.columns if c.startswith("Total_duration_of_whole_fixations.")]
    col = cand[0]
    print("Using", col)

df = gsr[["Recording", "Participant", "TOI", "Media", col, "Average_GSR", "Average_whole-fixation_pupil_diameter"]].copy()
df = df.rename(columns={col: "dwell_snake"})
for c in ["dwell_snake", "Average_GSR", "Average_whole-fixation_pupil_diameter"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna(subset=["dwell_snake"])
df.head()"""
            ),
            md("## 2. Descriptive table — Mean (SD) (15 min)"),
            code(
                """desc = mean_sd_table(df, "dwell_snake", by="TOI")
desc"""
            ),
            md("## 3. Inferential test for training (20 min)"),
            code(
                """# Split TOIs into two groups if possible; otherwise demonstrate on median split of GSR
toi_counts = df["TOI"].value_counts()
print(toi_counts.head())
if toi_counts.shape[0] >= 2:
    a_name, b_name = toi_counts.index[:2]
    a = df.loc[df["TOI"] == a_name, "dwell_snake"]
    b = df.loc[df["TOI"] == b_name, "dwell_snake"]
else:
    a_name, b_name = "low_GSR", "high_GSR"
    med = df["Average_GSR"].median()
    a = df.loc[df["Average_GSR"] <= med, "dwell_snake"]
    b = df.loc[df["Average_GSR"] > med, "dwell_snake"]

result = apa_ttest(a, b, label_a=str(a_name), label_b=str(b_name))
result"""
            ),
            code(
                """print(result["apa"])
# pingouin version (nice for teaching)
pg.ttest(a, b, correction=True)"""
            ),
            md("## 4. Regression model with statsmodels (20 min)"),
            code(
                """model_df = df.dropna(subset=["Average_GSR", "Average_whole-fixation_pupil_diameter"]).copy()
model_df = model_df.rename(columns={"Average_whole-fixation_pupil_diameter": "pupil"})
# Predict dwell from GSR + pupil (illustrative — discuss causality!)
fit = smf.ols("dwell_snake ~ Average_GSR + pupil", data=model_df).fit()
print(fit.summary())"""
            ),
            md(
                """### How to read this in an academic workshop
- **Coefficient**: expected change in dwell for +1 unit predictor (holding others constant).
- **Std. Err. / t / P>|t|**: uncertainty and null-hypothesis test.
- **R²**: variance explained — not proof of theory.
- Always report **N**, design (TOI/AOI definitions), and preprocessing (I-VT thresholds, blink handling).
"""
            ),
            md(
                """## 5. Library roadmap (15 min)

### Core (this workshop)
`numpy`, `pandas`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `pingouin`, `Pillow`, `openpyxl`

### Eye-tracking ecosystem (know the names)
| Tool | Typical use |
|------|-------------|
| Vendor exports (Tobii Pro Lab, Pupil Player) | What we used today |
| **PyGaze** / analysis add-ons | Experiment + basic analysis |
| **eyelinkio** / SR Research tools | EyeLink EDF access |
| **neurokit2** | GSR/EDA, ECG feature pipelines |
| **MNE-Python** | Mostly EEG/MEG, but great for epochs mindset |
| Custom I-VT / I-DT | Transparent methods sections |

### Reproducibility habits
- Keep a `requirements.txt`
- Save analysis-ready CSVs
- Never overwrite raw exports
- Document AOI polygons and I-VT thresholds in the paper/supplement
"""
            ),
            code(
                """# Capstone sketch: participant-level table for "publication demo"
cap = (
    df.groupby("Participant", as_index=False)
    .agg(
        n_rows=("dwell_snake", "size"),
        dwell_snake_mean=("dwell_snake", "mean"),
        gsr_mean=("Average_GSR", "mean"),
        pupil_mean=("Average_whole-fixation_pupil_diameter", "mean"),
    )
)
cap.head()"""
            ),
            md(
                """## Capstone (remaining time)

In pairs, produce **one figure + one APA-like sentence** using either:
- Food decision AOI dwell, or
- GSR demo dwell / GSR / pupil

### Exit ticket
Submit: figure filename idea + the statistical sentence + which library produced it.
"""
            ),
        ],
    )


def main() -> None:
    session1()
    session2()
    session3()
    session4()


if __name__ == "__main__":
    main()
