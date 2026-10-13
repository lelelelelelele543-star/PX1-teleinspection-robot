@echo off
setlocal
cd /d "%~dp0"
echo === PX1 ENGINEERING TEAM / SAFE LOCAL RUN ===
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher not found. Install Python 3 for Windows.
  pause
  exit /b 2
)
py -3 tools\px1_team.py --dry-run
if errorlevel 1 (
  echo Preflight FAILED. Install/login to Codex CLI; see engineering\README.md.
  pause
  exit /b 2
)
echo Running one bounded pass across seven roles. Logs: .px1-team
py -3 tools\px1_team.py --cycles 1
set "RESULT=%ERRORLEVEL%"
echo Completed with exit code %RESULT%. Check engineering\out\gates.md.
echo This is NOT a manufacturing release or real-world equipment test.
pause
exit /b %RESULT%
