**Software and files to download for the NBML eye-tracking workshop (2026 Python / Excel edition).**

# Python (primary analysis stack)

1. Install **Python 3.10+** from [python.org](https://www.python.org/downloads/) (Windows: tick “Add Python to PATH”).
2. Clone this repository, then follow [`workshop/SETUP.md`](workshop/SETUP.md):

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Alternatively create the conda env from `environment.yml`.

Optional: [VS Code](https://code.visualstudio.com/) with the Python + Jupyter extensions, or [JupyterLab](https://jupyter.org/).

# Excel

Use Microsoft Excel or [LibreOffice Calc](https://www.libreoffice.org/). Starter workbooks are in `workshop/excel/`.

# Pupil Labs (Day 1 hardware)

Install **Pupil Capture** and **Pupil Player** using the official [Pupil Labs Core documentation](https://docs.pupil-labs.com/core/). NBML provides headsets and on-site specialist support for recordings.

# Tobii Pro Lab and Tobii Studio (comparison / screen-based demo)

Use [this](https://drive.google.com/file/d/1mJHSgWrOfuOUtn7IRFSn7o8hcbS0jLz4/view?usp=sharing) link for the Tobii Pro Lab trial (≈ one month).<br/>
Also, use [this](https://drive.google.com/file/d/1uGyZdCEd503LD0BKrSI670DT3yryXuVC/view?usp=sharing) link for Tobii Studio if needed.<br/>
**Caution:** You will need to send an access request. In the request message write your full name in Latin (identical to your registration full name).

# GitHub Desktop

For Windows download and install [this](https://central.github.com/deployments/desktop/desktop/latest/win32) and for macOS [this](https://central.github.com/deployments/desktop/desktop/latest/darwin) file.

# Demo projects (legacy Tobii demos)

You can download demo projects using [this link](https://drive.google.com/drive/folders/1Xkv60ouUshc9Wv50oEPDQ1L320UB9PmY?usp=share_link).<br/>
**Caution:** Access request required; use your registration full name in Latin.

# Cloning this repository

Create a [GitHub account](https://github.com/signup), then clone with GitHub Desktop or:

```bash
git clone https://github.com/Ali-Mahdipour/eye-tracking-course.git
```

Guide: [cloning with GitHub Desktop](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop).

# Legacy R stack (optional reference only)

Earlier editions used R / RStudio. Installers below remain for alumni materials such as `Analysis_Decision_making.Rmd` — **new workshop analysis sessions use Python + Excel**.

- R 4.2.3 Windows: [installer](https://cran.r-project.org/bin/windows/base/old/4.2.3/R-4.2.3-win.exe)
- RStudio: [posit.co/download](https://posit.co/download/rstudio-desktop/)
