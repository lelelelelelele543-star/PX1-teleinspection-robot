# PX1 multi-agent — Windows launch

**Prepared in GitHub, not running.** This is an experimental orchestration layer on top of the existing repository. It does not manufacture hardware, access your laptop remotely, or continue when the laptop is switched off.

## What has been prepared
- Eleven engineering specializations, one accountable chief engineer.
- Native Codex multi-agent delegation requested with a cap of three simultaneous specialists plus coordinator.
- Inter-agent messages and centralized integration required by the brief.
- A persistent checkpoint, first-wave dependency/acceptance board, local run logs, and Windows/Linux CI checks for the Python launcher.
- No custom PCBs; COTS electronic modules and repeatable firmware/CAD/BOM target for 2–3 equivalent complete PX1 complexes.
- CRP150_REFERENCE and CAM026_REFERENCE are **not** allowed to be mixed with adapted PX1 master.
- Physical manufacturing release remains HOLD until all relevant mechanical, power, tether, pressure, camera and endurance tests pass.

## Tonight, on your Windows laptop

Save local unfinished changes before switching branches. In PowerShell **inside the existing PX1 repo**, enter:

```powershell
git status --short
git fetch origin
git switch --track origin/feature/px1-multiagent-autonomy
py -3 tools/px1_team_autorun.py --dry-run
py -3 tools/px1_team_autorun.py --cycles 3 --timeout 2400
```

If that branch already exists locally, use `git switch feature/px1-multiagent-autonomy` instead. **Do not discard or overwrite local changes.**

Alternatively, after switching branches, double-click `start_px1_team.cmd` in the project directory for preflight + three bounded cycles (Python launcher and a signed-in Codex CLI must already be installed).

If `codex` is missing or outdated, install/update its CLI using the current OpenAI instructions, sign in and check `codex --version`. Codex also needs a working Internet connection.

## What the launcher actually does
- Checks Git and Codex executables and required project files.
- Starts `codex exec --enable multi_agent`, limiting Codex to four total threads and a single delegation depth.
- Sets sandbox to `workspace-write` and does not grant unrestricted computer control.
- Sends the coordinating agent a project-specific task, preserves STDOUT JSON events, STDERR, last message, exact command and summary.
- Runs bounded cycles (default 3), each with a timeout (default 2400s), and stops after two consecutive failed cycles.
- Resumes from the checkpoint on subsequent explicit invocation.

Native child agents and messaging must be available in your local Codex version. The runner **requests** them, but only events/logs can establish whether they actually ran. `observed_spawn_tool_calls` indicates tool-call attempts, **not** a proof that three agents finished their tasks.

## Review progress

- `autonomy/PX1_TEAM_PROGRESS.md` — coordinator-owned persistent checkpoint.
- `autonomy/PX1_TEAM_BRIEF.md` — 11 roles, ownership, communication and release rules.
- `autonomy/PX1_TEAM_TASKS.json` — first actual engineering wave (reference geometry / tether feasibility / QA).
- `.px1-agent/team-runs/` — local logs; ignored by Git.
- `current/HOLD_REGISTER.json` — actual outstanding release blockers H01–H10.
- `autonomy/CRP150_REFERENCE_PROGRESS.md` — earlier single-agent reference reconstruction.
- `tools/px1_autorun.py` — previous limited single-agent tool, left untouched.

Do not mix team and old single-agent runs concurrently on the same checkout. Do not start a second team run against the same checkout while one is already running.

### Important practical limits
- Both native agents and the coordinator work in a **shared repository** in this mode. Their editing boundaries are enforced by instructions and review, not OS-level write isolation. For strict parallel editing isolation, the next iteration should use separate Codex App worktrees or a controlled Git-worktree integration queue.
- Do not run `git reset --hard` or `git clean -fd` to resolve branch conflicts. Preserve unknown files.
- Codex tokens/rate limits, permissions, FreeCAD installations, bad source data, safety blockers and power loss can stop progress.
- AI-simulated validation never replaces physical pressure, electrical safety and underwater system tests; high-voltage tether work needs qualified review.

## Delivery target

First a testable robot + camera + reel + console and 40m tether; verify it; then identical systems #2 and #3 from one revision-controlled production package. Spare parts as a separate business come later.
