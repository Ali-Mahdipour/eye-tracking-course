# Demo / sample datasets (workshop)

Small clean CSVs for hands-on Python and Excel exercises in the NBML 2026 workshop edition.

## Provenance

| File | What it is | Source |
|------|------------|--------|
| `pupil_gaze_demo.csv` | Normalized gaze + confidence + pupil diameter (Pupil-like columns) | **Synthetic** teaching data (`workshop/scripts/synthesize_demo_data.py`) |
| `pupil_events_demo.csv` | Fixation / saccade event table | **Synthetic** |
| `tobii_like_aoi_metrics.csv` | AOI metrics table shaped like Tobii Pro Lab exports | **Synthetic** (column names inspired by Tobii metrics TSVs already in this repo) |
| `pupillometry_demo.csv` | Pupil diameter time series with a mid-trial load bump | **Synthetic** |

## Also in this repository (real course exports)

| Path | Notes |
|------|--------|
| `Data/decision making/*.tsv` | Tobii-style metrics from a food decision-making study (existing course materials) |
| `Data/Glass/*.tsv` | Glass / board AOI metrics (existing) |
| `Stimuli/` | Example images and video stimuli used in past demos |

## Public datasets (download yourself)

See the repo root file [`eye-tracking-datasets.md`](../../eye-tracking-datasets.md) for linked open datasets. Prefer small subsets for class; document any download path you use in your own notes.

## Regenerate synthetic files

```bash
python workshop/scripts/synthesize_demo_data.py
```

**Ethics note:** Synthetic demos are for learning pipelines only. Do not treat them as scientific results. Real lab recordings stay on NBML systems unless shared under an approved protocol.
