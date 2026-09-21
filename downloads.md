**Here we list the software packages and files that you will need to download and install.**

---

# Python (primary analysis stack — NBML 2026 workshop)

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

---

# Tobii Pro Lab and Tobii Studio software packages
Use [this](https://drive.google.com/file/d/1mJHSgWrOfuOUtn7IRFSn7o8hcbS0jLz4/view?usp=sharing) link for downloading the trial version of the Tobii Pro Lab (will work for one month).<br/>
Also, use [this](https://drive.google.com/file/d/1uGyZdCEd503LD0BKrSI670DT3yryXuVC/view?usp=sharing) link to download the Tobii Studio software package. <br/>
**Caution:** You will need to send an access request. In the request message write your full-name in Latin (identical to your registration full-name). <br/>

# GitHub Desktop software package
For windows download and install [this](https://central.github.com/deployments/desktop/desktop/latest/win32) and for macOS [this](https://central.github.com/deployments/desktop/desktop/latest/darwin) file.

# R 4.2.3 / 4.2.2
For windows download and install [this](https://cran.r-project.org/bin/windows/base/old/4.2.3/R-4.2.3-win.exe) file.<br>
For macOS Big Sur download and install [this](https://cran.rstudio.com/bin/macosx/big-sur-arm64/base/R-4.2.2-arm64.pkg) and for High Sierra [this](https://cran.rstudio.com/bin/macosx/base/R-4.2.2.pkg) file.

# Rstudio software package 
For windows download and install [this](https://download1.rstudio.org/electron/windows/RStudio-2022.12.0-353.exe) file.<br>
You can find the link for macOS installer [here](https://posit.co/download/rstudio-desktop/). 

> **Note (2026 workshop):** New analysis sessions use **Python + Excel**. The R / RStudio installers above remain for alumni materials such as `Analysis_Decision_making.Rmd`.

# Demo projects
You can download demo projects using the [this link](https://drive.google.com/drive/folders/1Xkv60ouUshc9Wv50oEPDQ1L320UB9PmY?usp=share_link). <br>
**Caution:** You will need to send an access request. In the request message write your full-name in Latin (identical to your registration full-name).

# Cloning this repository
In order to clone (or you might say download) a repository using GitHub Desktop you will neet ot first [create a GitHub account](https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home), which is so simple. Then you can clone any repository (including this one) using the clone option under file menue of the GitHub Desktop software.  For a guide on how to clone this repository using GitHub desktop see this [link](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop).

You can also clone with git:

```bash
git clone https://github.com/Ali-Mahdipour/eye-tracking-course.git
```
