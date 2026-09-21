# eye-tracking-course

This repository has been created for sharing parts of the educational content related to the Eye-Tracking course that you have taken (or probably are interested to take 😉).

---

## NBML Workshop Edition (2026) — Python / Excel

Student materials for the NBML workshop **Mastery of eye tracking with Pupil Labs and Tobii Pro Lab** at [NBML](https://www.nbml.ir/), co-taught by **Dr. Anahita Khorrami** (cognitive neuroscience framing) and **Ali Golbazi Mahdipour** (practical eye tracking & analysis).

This edition emphasizes **hands-on practice** with **Python** (primary) and **Excel** (also taught). Legacy R notebooks/scripts in the repo remain as reference only (see the original session outline below).

### Schedule overview (Ali’s teaching focus)

| Day | Date (approx.) | Format | Focus |
|-----|----------------|--------|--------|
| **1** | Wed 2026-09-16 · 09:00–16:00 | **In person (NBML)** | Concepts + **Pupil Labs** calibration, recording, Player basics |
| **2** | Thu · Ali block **14:00–16:00** (full day online context) | Online | Preprocessing, qualitative viz context, **Tobii Pro Lab** intro/demo |
| **3** | Fri · Ali block **11:00–16:00** | Online | **Python + Excel** intro, fixation/saccade metrics, AOIs |
| **4** | Next Thu · **12:30–16:00** | Online | Advanced: pupillometry, time series, stats in Python |
| **5** | Next Fri · **12:30–16:00** | Online | Visualization / reporting + project consult framing |

Published syllabus topics still include Pupil Core/Invisible, fixation/saccade, Tobii AOIs, heatmaps/scanpaths, dwell/velocity/complexity, static/dynamic AOIs, pupillometry, gaze sequences, mixed models, interactive viz, and reproducible research (Git, notebooks).

### Quick start (2026 workshop)

1. Clone this repository.
2. Follow [`workshop/SETUP.md`](workshop/SETUP.md) to install Python deps (`requirements.txt` or `environment.yml`).
3. Day 1 lab: print [`workshop/day1/concepts-handout.md`](workshop/day1/concepts-handout.md) and [`workshop/day1/pupil-labs-lab-checklist.md`](workshop/day1/pupil-labs-lab-checklist.md).
4. Open notebooks under [`workshop/notebooks/`](workshop/notebooks/).
5. Excel starters: [`workshop/excel/`](workshop/excel/).
6. Demo data: [`Data/demo/`](Data/demo/) (see provenance README there). Broader public dataset links: [`eye-tracking-datasets.md`](eye-tracking-datasets.md).
7. Installers and links: [`downloads.md`](downloads.md).

### Repository map (2026 additions)

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

### Software (2026)

- **Pupil Labs** Capture + Player (Day 1 hardware; NBML specialist supports recordings)
- **Python 3.10+** + Jupyter
- **Excel** (or LibreOffice Calc) for metric tables
- **Tobii Pro Lab** trial for screen-based comparison (see `downloads.md`)

---

## Original course headlines (kept from earlier editions)

Here are the headlines of the subjects that will be discussed during the course:

### Session 1 (3 hours):
    1-1 An introduction on the history and taxonomy of eye tracking systems
    1-2 The theoretical foundations of the visual system and visual attention
    1-3 Psychophysics of the visual system
    1-4 The taxonomy of eye movements (saccades, vergence, etc.)
    1-5 Introduction to designing experimental research making use of eye tracking
    1-6 Basics of designing stimuli with regard to psychophysics
### Session 2 (3 hours):
    2-1 The role of eye movements in basic, behavioral, and applied social and clinical research
    2-2 The Role of eye tracking in brain maping with regard to psychophysics of human visual system
    2-3 Eye tracking calibration
    2-4 recording eye movement data
    2-5 An introduction to the pipline and taxonomy of quantitative analyses of eye movements
    2-6 An introduction to the pipline and taxonomy of qualitative analyses of eye movements
### Session 3 (3 hours):
    3-1 Installing an eye tracking software (Tobii Pro Lab—trial version)
    3-2 Introducing the common configuration of the eye tracking systems
    3-3 Calibrating the eye tracker
    3-4 Recording the eye movement data
    3-5 Introducing the common eye movement filters
    3-6 Introducing the User Interface of the software
    3-7 Introducing the configuration of different types of the stimuli
    3-8 Qualitative analyses of the eye movements
### Session 4 (3 hours):
    4-1 Segmenting and exporting different types of qualitative outputs
    4-2 Interpreting the qualitative results 
    4-3 Areas of Interest (AOIs) and setting them up
    4-4 An introduction to quantitative analysis of eye movements 
    4-5 exporting quantitative preprocessing results
    4-6 Intrepretation of eye movement metrics and discussing their relation to cognition
### Session 5 (3 hours):
    5-1 Exporting the raw eye movement data
    5-2 Analyzing the raw eye movement data
    5-3 Introduction to an other eye movement analysis tool
    5-4 Introducing some of the availble eye tracking datasets
    5-5 Introducing some of the open source eye movement analysis tools
    5-6 An introduction to statistical analysis of eye movement data
    5-7 Introducing statistical analysis and modeling tools availble in R
### Session 6 (3 hours):
    6-1 case study: decision making study
    6-2 case study: Eye-Tracking and GSR
    6-3 case study: infant occlusion test
    6-4 Case study: reading task
    6-5 Case study: Visual search task
    6-6 Case study: wearable eye tracking in shopping environment

New workshop participants should follow the **NBML 2026** schedule and `workshop/` folder above; the session list remains for alumni of earlier editions and for reference.

## License

See [`LICENSE`](LICENSE). Respect NBML recording/copyright rules for workshop videos and shared recordings.

Analysis training (4×1.5h Python labs): see `workshop/ANALYSIS_TRAINING.md` and `workshop/sessions/`.
