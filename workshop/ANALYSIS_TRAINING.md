# Analysis training track — 4 × 1.5 hours

Hands-on Python labs using:

| Folder | Role |
|--------|------|
| `Data/food_decision_making/` | Tobii food task (sample-level + metrics) |
| `Data/tobii_gsr_demo/` | Tobii GSR / AOI / click metrics |
| `Data/pupil_labs_recording/` | Pupil Labs fixations & blinks |
| `Stimuli/Decision Making/` | Heatmap / gaze-plot backgrounds |

## Design choices (for instructors)

- **Mostly inline notebook code** so students see the math.
- Only one analysis helper is imported in Session 2: `analysis.ivt.ivt_classify`.
- Tables stay **small** (a few rows) and charts show **one idea each**.
- Metrics are defined before they are computed (e.g. TTFF = first AOI fixation − stimulus onset; RT = first in-window click − onset; missing RT stays `NaN`).

## Sessions

| # | Notebook | Focus |
|---|----------|--------|
| 1 | `sessions/S01_python_and_data_landscape.ipynb` | Python preliminaries, data map, first summaries |
| 2 | `sessions/S02_ivt_aoi_heatmaps.ipynb` | I-VT, AOI/TOI, heatmaps, gaze plots |
| 3 | `sessions/S03_behavior_gsr_pupil.ipynb` | Clicks/RT, GSR/SCR, pupil + blinks |
| 4 | `sessions/S04_stats_models_and_libraries.ipynb` | Mean(SD), Welch t-test + *d*, regression |

## Run

```bash
pip install -r requirements.txt
python workshop/scripts/build_analysis_sessions.py
jupyter notebook workshop/sessions
```
