@echo off
setlocal
cd /d "%~dp0"
echo PX1 TEAM - Codex multi-agent engineering
echo ---------------------------------------
where py >nul 2>&1
if errorlevel 1 (
  echo Python launcher py was not found. Install Python 3 and rerun.
  goto :fail
)
py -3 tools\px1_team_autorun.py --dry-run
if errorlevel 1 goto :fail
echo.
echo Starting up to 3 bounded Codex cycles with native agent delegation...
py -3 tools\px1_team_autorun.py --cycles 3 --timeout 2400
if errorlevel 1 goto :fail
echo.
echo Run finished. See autonomy\PX1_TEAM_PROGRESS.md and .px1-agent\team-runs.
goto :done
:fail
echo.
echo Preflight or agent run failed. Read errors and setup instructions.
:done
pause
