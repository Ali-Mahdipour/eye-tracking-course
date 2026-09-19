# Analysis training track — 4 × 1.5 hours

Hands-on Python analysis using the workshop datasets under `Data/`:

| Folder | Contents |
|--------|----------|
| `Data/food_decision_making/` | Tobii food buy/not-buy (sample-level + metrics) |
| `Data/tobii_gsr_demo/` | Tobii GSR / AOI / click metrics |
| `Data/pupil_labs_recording/` | Pupil Labs fixations, blinks, world timestamps |
| `Stimuli/Decision Making/` | Images for heatmap / gaze-plot overlays |

Code helpers live in `workshop/analysis/` (I-VT, AOI, viz, stats tables).

## Session map

| # | Notebook | Focus |
|---|----------|--------|
| 1 | [`sessions/S01_python_and_data_landscape.ipynb`](sessions/S01_python_and_data_landscape.ipynb) | Python preliminaries, pandas, library landscape, load all datasets |
| 2 | [`sessions/S02_ivt_aoi_heatmaps.ipynb`](sessions/S02_ivt_aoi_heatmaps.ipynb) | I-VT filter, AOI/TOI metrics, count & duration heatmaps, Tobii-like gaze plots |
| 3 | [`sessions/S03_behavior_gsr_pupil.ipynb`](sessions/S03_behavior_gsr_pupil.ipynb) | Mouse/key events, constructed RTs, GSR/SCR, pupil + blinks |
| 4 | [`sessions/S04_stats_models_and_libraries.ipynb`](sessions/S04_stats_models_and_libraries.ipynb) | Mean(SD) tables, t-tests + *d*, regression, academic reporting, library roadmap |

Each session is paced for **~90 minutes** including practice and an exit ticket.

## How to run

```bash
# from repo root
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
python workshop/scripts/build_analysis_sessions.py   # rebuild notebooks if needed
jupyter notebook workshop/sessions
```

Import helpers from notebooks:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path("..").resolve()))  # workshop/
from analysis.ivt import ivt_classify
```

## Teaching notes (instructor)

- Majority of participants are **new to Python** — Session 1 is mandatory warm-up.
- Prefer the **teaching CSV** (`Food_Decision_Making_Teaching_Sample.csv`) for live I-VT; keep the full `.xlsx` for homework.
- Default food AOIs in `analysis/aoi.py` are **approximate rectangles** on 1366×768 stimuli — adjust live if needed.
- One wearable eye tracker on hardware days does not limit these analysis labs (they use recorded exports).

## Rebuild notebooks from the script

```bash
python workshop/scripts/build_analysis_sessions.py
```
