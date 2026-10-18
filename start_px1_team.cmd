@echo off
setlocal
cd /d "%~dp0"
echo.
echo ========================================
echo    PX1 - PARALLEL ENGINEERING TEAM
echo ========================================
echo Three isolated specialists, then chief engineer.
echo No purchases, no Git push, no manufacturing release.
echo.
where py >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python 3 launcher not found.
  goto :fail
)
echo [1/2] Dry-run preflight...
py -3 tools\px1_parallel.py --dry-run
if errorlevel 1 goto :fail
echo.
echo [2/2] Starting first bounded round...
py -3 tools\px1_parallel.py --rounds 1 --timeout 1200
if errorlevel 1 goto :fail
echo.
echo First round finished. Review:
echo   autonomy\PX1_TEAM_PROGRESS.md
echo   autonomy\team_work\
echo   .px1-agent\parallel\
echo.
echo For further rounds after reviewing changes, see:
echo   autonomy\PX1_TEAM_README.md
goto :done
:fail
echo.
echo Setup or engineering round failed. Inspect the error above.
echo Safe instructions: autonomy\PX1_TEAM_README.md
:done
pause
