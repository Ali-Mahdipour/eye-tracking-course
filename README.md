# Eye-Tracking Course — NBML Workshop Edition (2026)

Student materials for **تسلط بر ردیابی چشم با Pupil Labs و Tobii Pro Lab** at [NBML](https://www.nbml.ir/), co-taught by **Dr. Anahita Khorrami** (cognitive neuroscience framing) and **Ali Golbazi Mahdipour** (practical eye tracking & analysis).

This edition emphasizes **hands-on practice** with **Python** (primary) and **Excel** (also taught). Legacy R notebooks/scripts in the repo remain as reference only.

## Schedule overview (Ali’s teaching focus)

| Day | Date (approx.) | Format | Focus |
|-----|----------------|--------|--------|
| **1** | Wed 2026-09-16 · 09:00–16:00 | **In person (NBML)** | Concepts + **Pupil Labs** calibration, recording, Player basics |
| **2** | Thu · Ali block **14:00–16:00** (full day online context) | Online | Preprocessing, qualitative viz context, **Tobii Pro Lab** intro/demo |
| **3** | Fri · Ali block **11:00–16:00** | Online | **Python + Excel** intro, fixation/saccade metrics, AOIs |
| **4** | Next Thu · **12:30–16:00** | Online | Advanced: pupillometry, time series, stats in Python |
| **5** | Next Fri · **12:30–16:00** | Online | Visualization / reporting + project consult framing |

Published syllabus topics still include Pupil Core/Invisible, fixation/saccade, Tobii AOIs, heatmaps/scanpaths, dwell/velocity/complexity, static/dynamic AOIs, pupillometry, gaze sequences, mixed models, interactive viz, and reproducible research (Git, notebooks).

## Quick start

1. Clone this repository.
2. Follow [`workshop/SETUP.md`](workshop/SETUP.md) to install Python deps (`requirements.txt` or `environment.yml`).
3. Day 1 lab: print [`workshop/day1/concepts-handout.md`](workshop/day1/concepts-handout.md) and [`workshop/day1/pupil-labs-lab-checklist.md`](workshop/day1/pupil-labs-lab-checklist.md).
4. Open notebooks under [`workshop/notebooks/`](workshop/notebooks/).
5. Excel starters: [`workshop/excel/`](workshop/excel/).
6. Demo data: [`Data/demo/`](Data/demo/) (see provenance README there). Broader public dataset links: [`eye-tracking-datasets.md`](eye-tracking-datasets.md).

## Repository map

```
workshop/
  day1/           # Wed in-person handout + Pupil Labs checklist
  notebooks/      # Python teaching notebooks (mapped to sessions)
  excel/          # Starter workbooks for metrics & AOI tables
  scripts/        # Demo data + notebook/excel builders
  SETUP.md
Data/
  demo/           # Small synthetic CSVs for class
  decision making/  # Existing Tobii-style metrics (past courses)
  Glass/
Stimuli/          # Example images & videos
content/          # Manuals / readings (as previously shared)
downloads.md      # Installers & external demo links
```

## Software

- **Pupil Labs** Capture + Player (Day 1 hardware; NBML specialist supports recordings)
- **Python 3.10+** + Jupyter
- **Excel** (or LibreOffice Calc) for metric tables
- **Tobii Pro Lab** trial for screen-based comparison (see `downloads.md`)

## Older session outline

The previous 6×3-hour outline (history, Tobii workflows, R case studies) is retained below for alumni of earlier editions. New workshop participants should follow the **NBML 2026** schedule and `workshop/` folder above.

<details>
<summary>Legacy session headlines</summary>

### Session 1 (3 hours)
1-1 History and taxonomy of eye tracking systems · 1-2 Visual system & attention · 1-3 Psychophysics · 1-4 Taxonomy of eye movements · 1-5 Designing ET experiments · 1-6 Stimulus design basics

### Session 2–6
Calibration & recording pipelines, Tobii Pro Lab qualitative/quantitative workflows, raw data analysis, open datasets/tools, R modeling, and case studies (decision making, GSR, occlusion, reading, visual search, wearable shopping). See git history / `Analysis_Decision_making.Rmd` for R examples.

</details>

## License

See [`LICENSE`](LICENSE). Respect NBML recording/copyright rules for workshop videos and shared recordings.
