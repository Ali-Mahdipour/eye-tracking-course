# Setup guide — NBML Eye-Tracking Workshop (2026)

Primary analysis stack for this edition: **Python** (+ **Excel** for quick metric tables). R materials in the repo are legacy reference only.

## 1. Clone the course repository

```bash
git clone https://github.com/Ali-Mahdipour/eye-tracking-course.git
cd eye-tracking-course
```

Or use [GitHub Desktop](https://desktop.github.com/) (see `downloads.md`).

## 2. Python environment

### Option A — pip + venv (recommended for most laptops)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m ipykernel install --user --name eye-tracking-workshop
```

### Option B — conda

```bash
conda env create -f environment.yml
conda activate eye-tracking-workshop
```

## 3. Open notebooks

```bash
jupyter notebook workshop/notebooks
# or: jupyter lab workshop/notebooks
```

Map to Ali’s teaching blocks:

| Notebook | Session |
|----------|---------|
| `01_python_crash_course.ipynb` | Fri analysis intro |
| `02_import_eye_tracking_csvs.ipynb` | Thu / Fri |
| `03_fixation_saccade_metrics.ipynb` | Fri |
| `04_aoi_analysis.ipynb` | Fri |
| `05_pupillometry.ipynb` | Next Thu (advanced) |
| `06_visualization.ipynb` | Next Fri |
| `07_optional_stats.ipynb` | Next Thu |

## 4. Excel starters

Open `workshop/excel/metrics-starter.xlsx` and `workshop/excel/aoi-tables-starter.xlsx`. Sheets include formulas for dwell time, fixation count, and simple AOI summaries. Use with `Data/demo/tobii_like_aoi_metrics.csv` (File → Import / Get Data).

## 5. Pupil Labs software (Day 1 hardware lab)

Install **Pupil Capture** and **Pupil Player** from the [Pupil Labs Core docs](https://docs.pupil-labs.com/core/). NBML staff will help with headset setup and recordings on site.

## 6. Tobii Pro Lab (intro / comparison)

Trial / demo links remain in `downloads.md`. Day 2 includes a screen-based AOI walkthrough (software demo).

## 7. Demo data

Synthetic CSVs live in `Data/demo/`. Regenerate with:

```bash
python workshop/scripts/synthesize_demo_data.py
```

Larger Tobii-style TSVs from past courses are under `Data/decision making/` and `Data/Glass/`.

## Troubleshooting

- **Notebook kernel missing:** select the `eye-tracking-workshop` kernel in Jupyter.
- **Import path errors:** run notebooks with the repo root as the working directory, or adjust `DATA = Path("../../Data/demo")`.
- **Plotly not showing:** use JupyterLab / classic Notebook; VS Code also works with the Python + Jupyter extensions.

## Analysis training sessions

```bash
jupyter notebook workshop/sessions
```

Start with `S01_python_and_data_landscape.ipynb`. Full map: `workshop/ANALYSIS_TRAINING.md`.
