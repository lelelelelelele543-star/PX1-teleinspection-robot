# Multi-agent PX1 — first run on Windows

Already existing files and the original single-agent runner are preserved.
A branch is prepared; it does not run by itself or automatically modify main.

Open PowerShell in the project folder and execute:

    git fetch origin
    git switch --track origin/feature/px1-multiagent-autonomy
    py -3 tools/px1_team_autorun.py --dry-run
    py -3 tools/px1_team_autorun.py --cycles 3 --timeout 2400

If branch already exists locally, use git switch feature/px1-multiagent-autonomy.
The first command is only for a clone with no local unfinished changes:
review git status before switching branches. Existing uncommitted work should
be saved safely first.

The team has 11 specialist roles but intentionally only 3 concurrent
specialists plus chief engineer. The running Codex version/account must expose
native subagent spawn/message tools; a prompt alone cannot provision them.
Check the recorded actual team count after first cycle.

Results: autonomy/PX1_TEAM_PROGRESS.md
Logs: .px1-agent/runs/
Original runner: tools/px1_autorun.py (unchanged)
Team runner: tools/px1_team_autorun.py

The runner reuses the original single-agent loop's bounded cycles, sandbox,
logs and error-stop behavior. It stops at cycle budget/errors, when laptop is
off, when model limits are reached, or when a human decision is essential.
For longer sessions, explicitly rerun with --cycles 8 after reviewing progress.

No purchases, physical machining, power-on or release are automated. FreeCAD
and internet tools must actually work in the local environment. CAD validation
must not be confused with tested watertightness or electrical safety.
