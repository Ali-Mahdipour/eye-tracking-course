<#
.SYNOPSIS
  Pulls the instructor Food Decision Making notebook into your local
  Workshop course folder and opens it in Explorer.

.DESCRIPTION
  Target (default):
    C:\Users\snapp\Documents\Github\Workshop\2026-Sep-NBML-eye-tracking\eye-tracking-course\

  Fetches branch: cursor/analysis-training-sessions-feaa
  Notebook ends up at:
    workshop\private_food_decision_analysis\Food_Decision_Making_Full_Analysis.ipynb

  If git is unavailable or the course folder is missing, falls back to
  expanding the companion zip next to this script (if present).
#>
[CmdletBinding()]
param(
    [string]$WorkshopRoot = "C:\Users\snapp\Documents\Github\Workshop\2026-Sep-NBML-eye-tracking",
    [string]$CourseFolderName = "eye-tracking-course",
    [string]$RepoUrl = "https://github.com/Ali-Mahdipour/eye-tracking-course.git",
    [string]$Branch = "cursor/analysis-training-sessions-feaa",
    [string]$ZipFallback = ""
)

$ErrorActionPreference = "Stop"
function Step($m) { Write-Host "`n==> $m" -ForegroundColor Cyan }
function Ok($m)   { Write-Host "    $m" -ForegroundColor Green }
function Warn($m) { Write-Host "    $m" -ForegroundColor Yellow }

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CourseDir = Join-Path $WorkshopRoot $CourseFolderName
$NotebookRel = "workshop\private_food_decision_analysis"
$NotebookDir = Join-Path $CourseDir $NotebookRel
$NotebookFile = Join-Path $NotebookDir "Food_Decision_Making_Full_Analysis.ipynb"

if (-not $ZipFallback) {
    $ZipFallback = Join-Path $ScriptDir "Food_Decision_Making_Instructor_LOCAL.zip"
}

Step "Ensure workshop root exists: $WorkshopRoot"
New-Item -ItemType Directory -Path $WorkshopRoot -Force | Out-Null

$placed = $false

if (Get-Command git -ErrorAction SilentlyContinue) {
    Step "Sync course repo via git ($Branch)"
    if (Test-Path -LiteralPath (Join-Path $CourseDir ".git")) {
        Push-Location $CourseDir
        try {
            git fetch origin
            git checkout $Branch
            if ($LASTEXITCODE -ne 0) {
                git checkout -B $Branch "origin/$Branch"
            }
            git pull --ff-only origin $Branch
            if ($LASTEXITCODE -ne 0) { throw "git pull failed" }
            Ok "Updated existing clone on $Branch"
            $placed = $true
        } finally { Pop-Location }
    } else {
        if (Test-Path -LiteralPath $CourseDir) {
            Warn "Course folder exists without .git — will try zip fallback / overlay copy"
        } else {
            git clone --branch $Branch $RepoUrl $CourseDir
            if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
            Ok "Cloned $Branch"
            $placed = $true
        }
    }
} else {
    Warn "git not on PATH — using zip fallback if available"
}

if (-not (Test-Path -LiteralPath $NotebookFile)) {
    if (Test-Path -LiteralPath $ZipFallback) {
        Step "Expand zip into course folder: $ZipFallback"
        New-Item -ItemType Directory -Path $CourseDir -Force | Out-Null
        Expand-Archive -LiteralPath $ZipFallback -DestinationPath $CourseDir -Force
        Ok "Expanded zip"
        $placed = $true
    } else {
        # Try overlay from Agent Store / script-neighbor copy
        $overlayCandidates = @(
            (Join-Path $ScriptDir "instructor-food-decision-analysis"),
            (Join-Path $ScriptDir "2026-Sep-NBML-eye-tracking\instructor-food-decision-analysis"),
            (Join-Path $env:LOCALAPPDATA "Cursor\AgentStores\cursor_agent_stores\bc-aeb92694-f667-47b5-8f08-8598fc81feaa\files\Workshop\2026-Sep-NBML-eye-tracking\instructor-food-decision-analysis")
        )
        foreach ($src in $overlayCandidates) {
            if (Test-Path -LiteralPath (Join-Path $src "Food_Decision_Making_Full_Analysis.ipynb")) {
                Step "Copy overlay from: $src"
                New-Item -ItemType Directory -Path $NotebookDir -Force | Out-Null
                Copy-Item -Path (Join-Path $src "*") -Destination $NotebookDir -Recurse -Force
                Ok "Copied instructor notebook package"
                $placed = $true
                break
            }
        }
    }
}

if (-not (Test-Path -LiteralPath $NotebookFile)) {
    throw @"
Notebook still not found at:
  $NotebookFile

Fix options:
  1) Run this script again after git is available, OR
  2) Place Food_Decision_Making_Instructor_LOCAL.zip next to this script, OR
  3) In Cursor: download the artifact zip and extract into:
     $CourseDir
"@
}

Ok "Notebook ready:"
Write-Host "  $NotebookFile" -ForegroundColor Green

# Helpful: copy Desktop TSV reminder
$DataTsv = Join-Path $CourseDir "Data\food_decision_making\Food Decision Making Data Export.tsv"
$DesktopTsv = "C:\Users\snapp\Desktop\Food Decision Making Data Export.tsv"
if (-not (Test-Path -LiteralPath $DataTsv) -and (Test-Path -LiteralPath $DesktopTsv)) {
    Step "Copy canonical Desktop TSV into Data\food_decision_making\"
    New-Item -ItemType Directory -Path (Split-Path $DataTsv) -Force | Out-Null
    Copy-Item -LiteralPath $DesktopTsv -Destination $DataTsv -Force
    Ok "Copied Desktop TSV into course Data folder"
} elseif (Test-Path -LiteralPath $DataTsv) {
    Ok "Data Export TSV already present"
} else {
    Warn "Data Export TSV missing — copy Desktop file into Data\food_decision_making\ before running the notebook"
}

Step "Open Explorer"
try { explorer.exe /select,$NotebookFile } catch { explorer.exe $NotebookDir }

Write-Host "`nDone. Open the .ipynb in Cursor / Jupyter from:" -ForegroundColor Green
Write-Host "  $NotebookDir"
