#!/usr/bin/env python3
"""Build comprehensive 4×1.5h analysis-session notebooks (mostly inline code)."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "sessions"


def nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def md(source: str):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str):
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def write(name: str, cells):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    path.write_text(json.dumps(nb(cells), indent=1), encoding="utf-8")
    print("wrote", path)


BOOT = '''import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Readable plots for projection
plt.rcParams.update({
    "figure.figsize": (7, 4),
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

SESSION_DIR = Path.cwd()
WORKSHOP_DIR = SESSION_DIR.parent if SESSION_DIR.name == "sessions" else Path("workshop")
sys.path.insert(0, str(WORKSHOP_DIR))
from analysis.paths import data_path, stimuli_path
'''


def s01():
    write(
        "S01_python_and_data_landscape.ipynb",
        [
            md(
                """# Session 1 — Python preliminaries & eye-tracking data landscape
**90 minutes** · For participants new to Python

### What you will leave with
1. Confidence running notebook cells and reading simple tables.
2. A map of **which file answers which question**.
3. Names of the main Python libraries used in eye-tracking analysis.
4. Your first **summary table + bar chart** from real workshop data.

We keep tables small (a few rows) and charts simple (one idea per figure).
"""
            ),
            md("## Setup"),
            code(BOOT + "print('OK — data folder:', data_path('food_decision_making').exists())"),
            md(
                """## 1. Python in 10 minutes (no prior experience)

Think of a notebook cell like a calculator that can also hold tables.
"""
            ),
            code(
                """# Numbers and text
n_participants = 4
course = "NBML eye-tracking"
print(course, "| participants:", n_participants)

# A list (ordered collection)
foods = ["cake", "pizza", "ice-cream"]
print("first food:", foods[0])
print("how many foods:", len(foods))"""
            ),
            code(
                """# A table = DataFrame (like an Excel sheet)
demo = pd.DataFrame({
    "AOI": ["food-pic", "buy", "not-buy"],
    "dwell_ms": [1200, 450, 300],
})
demo"""
            ),
            md(
                """### Presentation output — tiny bar chart
One chart, three bars. This is the style we want all session: **clear, not dense**.
"""
            ),
            code(
                """fig, ax = plt.subplots()
ax.bar(demo["AOI"], demo["dwell_ms"], color="#2a6f6f")
ax.set_ylabel("Dwell (ms)")
ax.set_title("Toy example — dwell by AOI")
plt.tight_layout()
plt.show()"""
            ),
            md(
                """## 2. Libraries you will hear about this week

| Library | Role in this course |
|---------|---------------------|
| **pandas** | Load CSV/TSV/XLSX, filter, group, summarize |
| **numpy** | Numeric arrays (velocity, pupil series) |
| **matplotlib** | Figures for slides |
| **scipy** / **pingouin** / **statsmodels** | Tests & models (Session 4) |
| **Pillow** | Open stimulus images under heatmaps (Session 2) |

Optional names to recognize later: neurokit2 (GSR), vendor SDKs, PyGaze.
"""
            ),
            md(
                """## 3. Workshop data map

| Folder | Best for |
|--------|----------|
| `Data/food_decision_making/` | Sample-level gaze, mouse, AOI hits, pupil |
| `Data/tobii_gsr_demo/` | Aggregated GSR, SCR, AOI metrics, clicks |
| `Data/pupil_labs_recording/` | Wearable fixations & blinks |
| `Stimuli/Decision Making/` | Images for overlays |
"""
            ),
            md("## 4. Load food metrics (event table) and summarize safely"),
            code(
                """metrics = pd.read_csv(
    data_path("food_decision_making", "Food_Decision_Making_Metrics.tsv"),
    sep="\\t",
)
print("rows, cols:", metrics.shape)
metrics.head(5)"""
            ),
            md(
                """### Metric check before plotting
`Duration` in this Tobii metrics export is the **event duration**.
We only keep rows that look like fixations and have an AOI label.
"""
            ),
            code(
                """print("Event_type values:")
print(metrics["Event_type"].value_counts(dropna=False).head(8))

fix = metrics.copy()
# Keep fixation-like rows if the column uses that vocabulary
if "Event_type" in fix.columns:
    # Tobii often uses 'Fixation' — be explicit
    mask = fix["Event_type"].astype(str).str.contains("Fixation", case=False, na=False)
    if mask.any():
        fix = fix.loc[mask].copy()

fix = fix.dropna(subset=["AOI", "Duration"]).copy()
fix["Duration"] = pd.to_numeric(fix["Duration"], errors="coerce")
fix = fix.dropna(subset=["Duration"])

# Summarize: few AOIs only (top by count) so the table stays readable
top_aois = fix["AOI"].value_counts().head(6).index
summary = (
    fix[fix["AOI"].isin(top_aois)]
    .groupby("AOI", as_index=False)
    .agg(
        n_fixations=("Duration", "size"),
        mean_duration=("Duration", "mean"),
        total_dwell=("Duration", "sum"),
    )
    .sort_values("total_dwell", ascending=False)
)
# Round for slides
summary["mean_duration"] = summary["mean_duration"].round(1)
summary["total_dwell"] = summary["total_dwell"].round(1)
summary"""
            ),
            code(
                """fig, ax = plt.subplots()
ax.barh(summary["AOI"], summary["total_dwell"], color="#345995")
ax.set_xlabel("Total dwell (same units as Duration column)")
ax.set_title("Food metrics — total dwell by AOI (top 6)")
plt.tight_layout()
plt.show()"""
            ),
            md("## 5. Peek at sample-level teaching CSV (one recording)"),
            code(
                """sample = pd.read_csv(data_path("food_decision_making", "Food_Decision_Making_Teaching_Sample.csv"))
# Compact overview table for presentation
overview = pd.DataFrame({
    "n_rows": [len(sample)],
    "n_eye_rows": [(sample["Sensor"] == "Eye Tracker").sum()],
    "n_mouse_rows": [(sample["Sensor"] == "Mouse").sum()],
    "n_stimuli": [sample["Presented Stimulus name"].nunique(dropna=True)],
})
overview"""
            ),
            code(
                """stim_counts = (
    sample.loc[sample["Sensor"] == "Eye Tracker", "Presented Stimulus name"]
    .value_counts()
    .head(8)
    .rename_axis("stimulus")
    .reset_index(name="n_gaze_samples")
)
stim_counts"""
            ),
            code(
                """fig, ax = plt.subplots()
ax.bar(stim_counts["stimulus"], stim_counts["n_gaze_samples"], color="#6b4c9a")
ax.set_ylabel("Gaze samples")
ax.set_title("Teaching recording — gaze samples by stimulus")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()"""
            ),
            md("## 6. Pupil Labs vs Tobii (one small table each)"),
            code(
                """pupil_fix = pd.read_csv(data_path("pupil_labs_recording", "fixations.csv"))
pupil_blinks = pd.read_csv(data_path("pupil_labs_recording", "blinks.csv"))
compare = pd.DataFrame([
    {"source": "Pupil Labs fixations.csv", "n_events": len(pupil_fix), "duration_col": "duration", "mean_duration": round(pupil_fix["duration"].mean(), 3)},
    {"source": "Pupil Labs blinks.csv", "n_events": len(pupil_blinks), "duration_col": "duration", "mean_duration": round(pupil_blinks["duration"].mean(), 3)},
])
compare"""
            ),
            md(
                """## 7. Practice (10 min)
1. From `summary`, which AOI has the largest total dwell?
2. Why might `total_dwell` use the same units as `Duration` (not always milliseconds)?
3. Exit ticket: which file will you open first for I-VT tomorrow — metrics TSV or teaching CSV — and why?
"""
            ),
        ],
    )


def s02():
    write(
        "S02_ivt_aoi_heatmaps.ipynb",
        [
            md(
                """# Session 2 — I-VT, AOI/TOI metrics, heatmaps & gaze plots
**90 minutes**

### Goals
1. Convert timestamps correctly, then run **I-VT**.
2. Build fixation events with **rational durations**.
3. Compute **AOI dwell** and **TTFF relative to stimulus onset** (not absolute clock time).
4. Show **count** vs **duration** heatmaps and a Tobii-like gaze plot.

Only one helper function is imported: `ivt_classify`. Everything else is written inline so you can see the math.
"""
            ),
            code(
                BOOT
                + """from analysis.ivt import ivt_classify
from PIL import Image
from scipy.ndimage import gaussian_filter
"""
            ),
            md(
                """## 1. Load gaze for one stimulus (cake)

**Timestamp rule for this export:** `Recording timestamp` is in **milliseconds**.  
We divide by `1e3` to get seconds. Always check median Δt (should be ~0.008–0.020 s for ~60–120 Hz).
"""
            ),
            code(
                """raw = pd.read_csv(data_path("food_decision_making", "Food_Decision_Making_Teaching_Sample.csv"))
gaze = raw.loc[raw["Sensor"] == "Eye Tracker"].copy()
gaze = gaze.dropna(subset=["Gaze point X", "Gaze point Y", "Recording timestamp"])
gaze["time_s"] = gaze["Recording timestamp"].astype(float) / 1e3
gaze = gaze.sort_values("time_s")

stim = "cake"
g = gaze.loc[gaze["Presented Stimulus name"] == stim].copy()
toi_onset = g["time_s"].iloc[0]
toi_offset = g["time_s"].iloc[-1]

qc = pd.DataFrame({
    "stimulus": [stim],
    "n_samples": [len(g)],
    "median_dt_s": [g["time_s"].diff().median()],
    "toi_duration_s": [toi_offset - toi_onset],
})
qc"""
            ),
            md(
                """## 2. I-VT classification

Velocity at sample *i* ≈ distance(i-1 → i) / Δt.  
Fixation if velocity < threshold; then remove fixation runs shorter than 60 ms.
"""
            ),
            code(
                """samples, events = ivt_classify(
    g["time_s"].to_numpy(),
    g["Gaze point X"].to_numpy(),
    g["Gaze point Y"].to_numpy(),
    velocity_threshold=5000,  # px/s for this screen; try 2000 and 8000 later
    min_fixation_s=0.06,
)

label_counts = samples["label"].value_counts().rename_axis("label").reset_index(name="n_samples")
label_counts"""
            ),
            code(
                """fix = events.loc[events["label"] == "fixation"].copy()
sac = events.loc[events["label"] == "saccade"].copy()

# Sanity: fixation dwell cannot exceed the stimulus window by much
event_summary = pd.DataFrame([
    {"metric": "n_fixations", "value": len(fix)},
    {"metric": "n_saccades", "value": len(sac)},
    {"metric": "mean_fix_duration_s", "value": round(fix["duration_s"].mean(), 3) if len(fix) else np.nan},
    {"metric": "total_fixation_dwell_s", "value": round(fix["duration_s"].sum(), 3) if len(fix) else 0.0},
    {"metric": "dwell_fraction_of_TOI", "value": round(fix["duration_s"].sum() / (toi_offset - toi_onset), 3) if len(fix) else 0.0},
])
event_summary"""
            ),
            code(
                """fig, ax = plt.subplots()
ax.bar(["fixations", "saccades"], [len(fix), len(sac)], color=["#2a6f6f", "#b85c38"])
ax.set_ylabel("Number of events")
ax.set_title(f"I-VT events on '{stim}'")
plt.tight_layout()
plt.show()"""
            ),
            md(
                """### Compare with Tobii labels (sample level, compact)
We compare **sample labels**, not event counts (different segmentation → counts need not match).
"""
            ),
            code(
                """cmp = pd.DataFrame({
    "tobii": g["Eye movement type"].to_numpy(),
    "ivt": samples["label"].to_numpy(),
})
# Agreement only on rows where Tobii says Fixation or Saccade
both = cmp[cmp["tobii"].isin(["Fixation", "Saccade"])].copy()
both["agree"] = (
    ((both["tobii"] == "Fixation") & (both["ivt"] == "fixation"))
    | ((both["tobii"] == "Saccade") & (both["ivt"] == "saccade"))
)
agree_tbl = pd.DataFrame({
    "n_compared_samples": [len(both)],
    "pct_agree": [round(100 * both["agree"].mean(), 1)],
})
agree_tbl"""
            ),
            md(
                """## 3. AOI assignment + metrics (inline)

Teaching AOIs are approximate rectangles on 1366×768 images.  
**TTFF** = time of first fixation in that AOI **minus stimulus/TOI onset** (not absolute recording time).
"""
            ),
            code(
                """# Pixel boxes: (x_min, y_min, x_max, y_max), origin top-left
aois = {
    "food-pic": (430, 140, 930, 520),
    "buy": (180, 560, 520, 700),
    "not-buy": (840, 560, 1180, 700),
}

def which_aoi(x, y):
    for name, (x0, y0, x1, y1) in aois.items():
        if (x0 <= x <= x1) and (y0 <= y <= y1):
            return name
    return pd.NA

fix["aoi"] = [which_aoi(x, y) for x, y in zip(fix["x_mean"], fix["y_mean"])]
fix["ttff_from_onset_s"] = fix["start_s"] - toi_onset
fix[["start_s", "duration_s", "x_mean", "y_mean", "aoi", "ttff_from_onset_s"]].head(8)"""
            ),
            code(
                """# Per-AOI metrics (only AOIs that were hit)
rows = []
for aoi_name, grp in fix.dropna(subset=["aoi"]).groupby("aoi"):
    rows.append({
        "AOI": aoi_name,
        "n_fixations": len(grp),
        "dwell_s": round(grp["duration_s"].sum(), 3),
        "mean_fix_s": round(grp["duration_s"].mean(), 3),
        "TTFF_s": round(grp["ttff_from_onset_s"].min(), 3),  # earliest fixation in AOI after onset
    })
aoi_metrics = pd.DataFrame(rows).sort_values("dwell_s", ascending=False)
aoi_metrics"""
            ),
            code(
                """fig, ax = plt.subplots()
ax.bar(aoi_metrics["AOI"], aoi_metrics["dwell_s"], color="#345995")
ax.set_ylabel("Dwell (s)")
ax.set_title(f"AOI dwell during '{stim}' (I-VT fixations)")
plt.tight_layout()
plt.show()"""
            ),
            md("## 4. Heatmaps (count vs duration) — one stimulus, two panels"),
            code(
                """img = np.asarray(Image.open(stimuli_path("Decision Making", f"{stim}.png")).convert("RGBA"))
h, w = img.shape[0], img.shape[1]
xs = fix["x_mean"].to_numpy()
ys = fix["y_mean"].to_numpy()
durs = fix["duration_s"].to_numpy()

def make_heat(weights=None):
    heat, _, _ = np.histogram2d(xs, ys, bins=50, range=[[0, w], [0, h]], weights=weights)
    heat = gaussian_filter(heat.T.astype(float), sigma=1.5)
    return heat

fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
for ax, weights, title in [
    (axes[0], None, "Fixation COUNT heatmap"),
    (axes[1], durs, "Fixation DURATION heatmap"),
]:
    ax.imshow(img)
    ax.imshow(make_heat(weights), extent=[0, w, h, 0], alpha=0.45, cmap="jet", interpolation="bilinear")
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.show()"""
            ),
            md("## 5. Tobii-like gaze plot (order + duration)"),
            code(
                """fig, ax = plt.subplots(figsize=(8, 4.5))
ax.imshow(img)
fx = fix.sort_values("start_s")
ax.plot(fx["x_mean"], fx["y_mean"], color="black", linewidth=1, alpha=0.7)
# Circle radius proportional to duration (readable, not huge)
max_r = 36
scale = max_r / max(fx["duration_s"].max(), 1e-6)
for i, (_, r) in enumerate(fx.iterrows(), start=1):
    rad = max(6, r["duration_s"] * scale)
    ax.add_patch(plt.Circle((r["x_mean"], r["y_mean"]), rad, facecolor="#e41a1c88", edgecolor="#7f0000"))
    ax.text(r["x_mean"], r["y_mean"], str(i), ha="center", va="center", color="white", fontsize=7)
ax.set_title(f"Gaze plot — {stim} (numbers = fixation order)")
ax.axis("off")
plt.tight_layout()
plt.show()

# Keep the plot readable: if many fixations, show only first 12 in a table
fx[["duration_s", "aoi"]].head(12)"""
            ),
            md(
                """## Practice
1. Re-run I-VT with threshold 2000 and 8000. Watch `n_fixations` and `dwell_fraction_of_TOI`.
2. Why is TTFF from onset more interpretable than absolute `start_s`?
3. Exit ticket: paste your `aoi_metrics` table for cake.
"""
            ),
        ],
    )


def s03():
    write(
        "S03_behavior_gsr_pupil.ipynb",
        [
            md(
                """# Session 3 — Behavior (clicks / RT), GSR, and pupil
**90 minutes**

### Goals
1. Build a clean multimodal timeline (stimulus onsets, clicks).
2. Compute **response time = first click − stimulus onset** (only if the click falls inside that stimulus window).
3. Summarize Tobii **GSR / SCR** without over-claiming causality.
4. Baseline-correct **pupil** within each stimulus; respect blinks as missingness.

No custom library beyond path helpers — calculations stay visible.
"""
            ),
            code(BOOT),
            md("## 1. Events on the teaching recording"),
            code(
                """raw = pd.read_csv(data_path("food_decision_making", "Food_Decision_Making_Teaching_Sample.csv"))
raw["time_s"] = raw["Recording timestamp"].astype(float) / 1e3

events = raw.dropna(subset=["Event"]).copy()
event_counts = events["Event"].value_counts().rename_axis("Event").reset_index(name="n").head(8)
event_counts"""
            ),
            code(
                """fig, ax = plt.subplots()
ax.barh(event_counts["Event"], event_counts["n"], color="#6b4c9a")
ax.set_xlabel("Count")
ax.set_title("Event types in teaching recording")
plt.tight_layout()
plt.show()"""
            ),
            md(
                """## 2. Stimulus intervals (TOIs) from start/end markers

We pair each `ImageStimulusStart` with the next `ImageStimulusEnd` **of the same name**.
"""
            ),
            code(
                """starts = events.loc[events["Event"] == "ImageStimulusStart", ["time_s", "Event value"]].rename(
    columns={"time_s": "onset_s", "Event value": "stimulus"}
)
ends = events.loc[events["Event"] == "ImageStimulusEnd", ["time_s", "Event value"]].rename(
    columns={"time_s": "offset_s", "Event value": "stimulus"}
)

intervals = []
for stim, sgrp in starts.groupby("stimulus"):
    egrp = ends.loc[ends["stimulus"] == stim].sort_values("offset_s")
    sgrp = sgrp.sort_values("onset_s")
    for (_, srow), (_, erow) in zip(sgrp.iterrows(), egrp.iterrows()):
        if erow["offset_s"] >= srow["onset_s"]:
            intervals.append({
                "stimulus": stim,
                "onset_s": srow["onset_s"],
                "offset_s": erow["offset_s"],
                "duration_s": erow["offset_s"] - srow["onset_s"],
            })
intervals = pd.DataFrame(intervals)
# Readable: food trials only
foods = ["cake", "pizza", "ice-cream", "cereal", "date"]
food_intervals = intervals.loc[intervals["stimulus"].isin(foods)].copy()
food_intervals.round(3)"""
            ),
            md(
                """## 3. Response times (stimulus onset → first mouse event in window)

Rational rule: only clicks with `onset ≤ click_time ≤ offset` count.  
If there is no click in the window, RT is missing (not zero).
"""
            ),
            code(
                """clicks = events.loc[events["Event"] == "MouseEvent", ["time_s", "Event value"]].copy()

rt_rows = []
for _, iv in food_intervals.iterrows():
    in_win = clicks[(clicks["time_s"] >= iv["onset_s"]) & (clicks["time_s"] <= iv["offset_s"])]
    if len(in_win) == 0:
        rt_rows.append({"stimulus": iv["stimulus"], "RT_s": np.nan, "n_clicks_in_window": 0})
        continue
    first = in_win.sort_values("time_s").iloc[0]
    rt_rows.append({
        "stimulus": iv["stimulus"],
        "RT_s": first["time_s"] - iv["onset_s"],
        "n_clicks_in_window": len(in_win),
        "first_click_value": first["Event value"],
    })
rt = pd.DataFrame(rt_rows)
rt["RT_s"] = rt["RT_s"].round(3)
rt"""
            ),
            code(
                """plot_rt = rt.dropna(subset=["RT_s"])
fig, ax = plt.subplots()
if len(plot_rt):
    ax.bar(plot_rt["stimulus"], plot_rt["RT_s"], color="#8c2d4a")
    ax.set_ylabel("RT (s)")
    ax.set_title("First click after stimulus onset")
    plt.xticks(rotation=30, ha="right")
else:
    ax.text(0.5, 0.5, "No in-window clicks in this recording", ha="center")
    ax.set_axis_off()
plt.tight_layout()
plt.show()"""
            ),
            md(
                """## 4. GSR metrics (aggregated Tobii table)

These are **interval-level** metrics from Tobii, not raw EDA samples.  
Good for teaching summaries; not a full SCR detection pipeline.
"""
            ),
            code(
                """gsr = pd.read_csv(data_path("tobii_gsr_demo", "Tobii_Pro_Lab_GSR_Demo_Project_Metrics.tsv"), sep="\\t")
for c in ["Average_GSR", "Number_of_SCR", "Average_whole-fixation_pupil_diameter"]:
    if c in gsr.columns:
        gsr[c] = pd.to_numeric(gsr[c], errors="coerce")

# Participant-level means (keeps the table small)
part = (
    gsr.groupby("Participant", as_index=False)
    .agg(
        mean_GSR=("Average_GSR", "mean"),
        mean_SCR=("Number_of_SCR", "mean"),
        mean_pupil=("Average_whole-fixation_pupil_diameter", "mean"),
        n_intervals=("Average_GSR", "size"),
    )
)
part[["mean_GSR", "mean_SCR", "mean_pupil"]] = part[["mean_GSR", "mean_SCR", "mean_pupil"]].round(3)
part.head(8)"""
            ),
            code(
                """fig, ax = plt.subplots()
ax.scatter(part["mean_GSR"], part["mean_SCR"], s=60, alpha=0.8, color="#2a6f6f")
ax.set_xlabel("Mean Average_GSR")
ax.set_ylabel("Mean Number_of_SCR")
ax.set_title("Participants — GSR level vs SCR count")
plt.tight_layout()
plt.show()"""
            ),
            md(
                """### Optional: mouse-click metrics already computed by Tobii
Example column family: `Number_of_mouse_clicks.Snake` (AOI-specific).  
We show a **single** AOI summary, not the whole wide matrix.
"""
            ),
            code(
                """click_cols = [c for c in gsr.columns if c.startswith("Number_of_mouse_clicks.")]
# Prefer primary AOI columns without .1/.2 duplicates when possible
primary = [c for c in click_cols if c.count(".") == 1]
use_cols = primary[:4] if primary else click_cols[:4]
click_summary = gsr[use_cols].apply(pd.to_numeric, errors="coerce").mean().rename("mean_clicks")
click_summary = click_summary.reset_index().rename(columns={"index": "metric"})
click_summary["mean_clicks"] = click_summary["mean_clicks"].round(2)
click_summary"""
            ),
            md(
                """## 5. Pupil on the food teaching sample (baseline per stimulus)

**Baseline:** mean pupil in the first 0.5 s after stimulus onset (same stimulus rows only).  
**Corrected pupil** = pupil − baseline.  
This is a teaching baseline, not a full dilatory model.
"""
            ),
            code(
                """gaze = raw.loc[raw["Sensor"] == "Eye Tracker"].copy()
gaze["pupil"] = gaze[["Pupil diameter left", "Pupil diameter right"]].mean(axis=1, skipna=True)
gaze = gaze.dropna(subset=["pupil", "Presented Stimulus name", "time_s"])

pup_rows = []
for stim, grp in gaze.groupby("Presented Stimulus name"):
    grp = grp.sort_values("time_s")
    t0 = grp["time_s"].iloc[0]
    baseline = grp.loc[grp["time_s"] <= t0 + 0.5, "pupil"].mean()
    pup_rows.append({
        "stimulus": stim,
        "baseline_pupil_mm": baseline,
        "mean_pupil_mm": grp["pupil"].mean(),
        "mean_pupil_baseline_corrected": (grp["pupil"] - baseline).mean(),
        "n_samples": len(grp),
    })
pup_tbl = pd.DataFrame(pup_rows)
pup_tbl = pup_tbl.loc[pup_tbl["stimulus"].isin(foods + ["fixation", "instruction"])].copy()
pup_tbl = pup_tbl.round(3)
pup_tbl"""
            ),
            code(
                """plot = pup_tbl.loc[pup_tbl["stimulus"].isin(foods)]
fig, ax = plt.subplots()
ax.bar(plot["stimulus"], plot["mean_pupil_baseline_corrected"], color="#3d5a80")
ax.axhline(0, color="black", linewidth=1)
ax.set_ylabel("Baseline-corrected pupil (mm)")
ax.set_title("Pupil by food stimulus (teaching sample)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()"""
            ),
            md("## 6. Blinks (Pupil Labs) — keep the summary tiny"),
            code(
                """blinks = pd.read_csv(data_path("pupil_labs_recording", "blinks.csv"))
blink_summary = pd.DataFrame({
    "n_blinks": [len(blinks)],
    "mean_duration_s": [round(blinks["duration"].mean(), 3)],
    "median_duration_s": [round(blinks["duration"].median(), 3)],
})
blink_summary"""
            ),
            md(
                """## Practice
1. Why is RT missing (`NaN`) more honest than putting `0` when no click occurs?
2. Name two confounds for GSR in a talking classroom demo.
3. Exit ticket: one sentence linking gaze (Session 2) to click RT (this session).
"""
            ),
        ],
    )


def s04():
    write(
        "S04_stats_models_and_libraries.ipynb",
        [
            md(
                """# Session 4 — Statistical models & academic outputs
**90 minutes**

### Goals
1. Build a **small** Mean (SD) table suitable for a slide.
2. Run a transparent two-group comparison with effect size.
3. Fit one simple regression and read the summary without mystique.
4. Leave with a library roadmap (not a zoo of wrappers).

Calculations are inline. We use `scipy` / `pingouin` / `statsmodels` directly.
"""
            ),
            code(
                BOOT
                + """from scipy import stats
import pingouin as pg
import statsmodels.formula.api as smf
"""
            ),
            md(
                """## 1. Analysis-ready table from GSR metrics

We use **Average_GSR** on the two search TOIs (`search_fearful` vs `search_nonfearful`).  
That contrast is interpretable; AOI-specific dwell columns are mostly empty outside name screens.
"""
            ),
            code(
                """gsr = pd.read_csv(data_path("tobii_gsr_demo", "Tobii_Pro_Lab_GSR_Demo_Project_Metrics.tsv"), sep="\\t")
for c in ["Average_GSR", "Number_of_SCR", "Average_whole-fixation_pupil_diameter"]:
    gsr[c] = pd.to_numeric(gsr[c], errors="coerce")

df = gsr.loc[
    gsr["TOI"].isin(["search_fearful", "search_nonfearful"]),
    ["Participant", "TOI", "Media", "Average_GSR", "Number_of_SCR", "Average_whole-fixation_pupil_diameter",
     "Self-reported_animal_phobia"],
].copy()
df = df.rename(columns={"Average_whole-fixation_pupil_diameter": "pupil"})
df = df.dropna(subset=["Average_GSR"])
print("N rows:", len(df))
df.head(5)"""
            ),
            md("## 2. Descriptive table — Mean (SD) by TOI"),
            code(
                """desc = (
    df.groupby("TOI")["Average_GSR"]
    .agg(N="count", Mean="mean", SD="std")
    .reset_index()
)
desc["Mean (SD)"] = desc.apply(lambda r: f"{r['Mean']:.2f} ({r['SD']:.2f})", axis=1)
desc_slide = desc[["TOI", "N", "Mean (SD)"]]
desc_slide"""
            ),
            code(
                """fig, ax = plt.subplots()
ax.bar(desc["TOI"].astype(str), desc["Mean"], yerr=desc["SD"], capsize=4, color="#345995")
ax.set_ylabel("Average_GSR")
ax.set_title("Mean GSR by search TOI (± SD)")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()
plt.show()"""
            ),
            md(
                """## 3. Two-group comparison (Welch t-test)

Compare `search_fearful` vs `search_nonfearful` on Average_GSR.  
Report Welch’s df when scipy provides it — do not invent `n1+n2-2` for Welch.
"""
            ),
            code(
                """a = df.loc[df["TOI"] == "search_fearful", "Average_GSR"].dropna()
b = df.loc[df["TOI"] == "search_nonfearful", "Average_GSR"].dropna()

t_res = stats.ttest_ind(a, b, equal_var=False, alternative="two-sided")
nx, ny = len(a), len(b)
pooled = np.sqrt(((nx - 1) * a.std(ddof=1) ** 2 + (ny - 1) * b.std(ddof=1) ** 2) / (nx + ny - 2))
d = (a.mean() - b.mean()) / pooled if pooled > 0 else np.nan
welch_df = float(getattr(t_res, "df", np.nan))

p = float(t_res.pvalue)
p_txt = "< .001" if p < 0.001 else f"= {p:.3f}".replace("0.", ".")
apa = f"t({welch_df:.1f}) = {t_res.statistic:.2f}, p {p_txt}, d = {d:.2f}"

result = pd.DataFrame([
    {"group": "search_fearful", "N": nx, "Mean": round(a.mean(), 3), "SD": round(a.std(ddof=1), 3)},
    {"group": "search_nonfearful", "N": ny, "Mean": round(b.mean(), 3), "SD": round(b.std(ddof=1), 3)},
])
print(apa)
result"""
            ),
            code(
                """# Cross-check with pingouin
pg.ttest(a, b, correction=True)"""
            ),
            md(
                """## 4. Simple regression (illustrative)

Model: `Number_of_SCR ~ Average_GSR + pupil` on the same search rows.  
Coefficients are for reading practice — not a causal claim.
"""
            ),
            code(
                """model_df = df.dropna(subset=["Average_GSR", "pupil", "Number_of_SCR"]).copy()
fit = smf.ols("Number_of_SCR ~ Average_GSR + pupil", data=model_df).fit()
coef_tbl = fit.summary2().tables[1][["Coef.", "Std.Err.", "t", "P>|t|"]].round(3)
coef_tbl"""
            ),
            code(
                """fit_stats = pd.DataFrame([
    {"stat": "N", "value": int(fit.nobs)},
    {"stat": "R-squared", "value": round(fit.rsquared, 3)},
    {"stat": "Adj. R-squared", "value": round(fit.rsquared_adj, 3)},
])
fit_stats"""
            ),
            md(
                """### Optional second slide: phobia group on fearful search only
"""
            ),
            code(
                """fear = df.loc[df["TOI"] == "search_fearful"].dropna(subset=["Self-reported_animal_phobia", "Average_GSR"])
ph = (
    fear.groupby("Self-reported_animal_phobia")["Average_GSR"]
    .agg(N="count", Mean="mean", SD="std")
    .reset_index()
    .round(3)
)
ph"""
            ),
            md(
                """## 5. Library roadmap (discussion, 10 min)

**Core this week:** numpy, pandas, matplotlib, scipy, pingouin, statsmodels, Pillow, openpyxl  

**Recognize later:** neurokit2 (EDA/GSR pipelines), vendor SDKs, PyGaze, EyeLink toolkits  

**Reproducibility:** never overwrite raw exports; write analysis-ready CSVs; document I-VT thresholds and AOI definitions.
"""
            ),
            md(
                """## Capstone (remaining time)
In pairs, produce **one** bar chart and **one** APA-like sentence using either:
- AOI dwell from Session 2, or
- Search TOI GSR from this session

### Exit ticket
Figure idea + statistical sentence + which library computed it.
"""
            ),
        ],
    )


def main():
    s01()
    s02()
    s03()
    s04()


if __name__ == "__main__":
    main()
