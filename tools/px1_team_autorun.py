#!/usr/bin/env python3
"""Bounded PX1 coordinator loop using actual Codex native subagents.

This does not create fictitious workers or continue after laptop shutdown.
Requires a Codex CLI build with multi_agent support; captures JSONL evidence.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
CHECKPOINT = ROOT / "autonomy/PX1_TEAM_PROGRESS.md"
BRIEF = ROOT / "autonomy/PX1_TEAM_BRIEF.md"
RUNS = ROOT / ".px1-agent/team-runs"


def status(path: Path = CHECKPOINT) -> str:
    if not path.is_file():
        return "MISSING"
    for line in path.read_text(encoding="utf-8").splitlines()[:15]:
        if line.startswith("STATUS: "):
            return line.partition(": ")[2].strip().upper()
    return "UNKNOWN"


def command(codex: str, final_path: Path) -> list[str]:
    # CLI supports feature/config overrides; no global config or credentials changed.
    return [
        codex, "exec", "--enable", "multi_agent",
        "-c", "agents.max_threads=4",
        "-c", "agents.max_depth=1",
        "--sandbox", "workspace-write",
        "--ask-for-approval", "never",
        "--json", "--output-last-message", str(final_path), "-",
    ]


def prompt(cycle: int) -> str:
    return f"""PX1 Engineering CHIEF ENGINEER, run {cycle}.
Read AGENTS.md, current/README.md, current/REV_A_FAST_TRACK.md,
current/HOLD_REGISTER.json, autonomy/PX1_TEAM_BRIEF.md,\nautonomy/PX1_TEAM_TASKS.json,
autonomy/PX1_TEAM_PROGRESS.md, autonomy/CRP150_REFERENCE_PROGRESS.md.

Work toward complete CRP150-like crawler+camera+reel+console, 2-3 repeatable
units, standard purchasable electronic modules only, no custom PCB.
The authoritative release status is HOLD; never fake a fabrication PASS.

Use REAL native spawn_agent to delegate to no more than THREE simultaneous
specialists for mutually independent first-wave tasks T001, T002, T003\nfrom autonomy/PX1_TEAM_TASKS.json. Send and receive actual messages
about mounting dimensions, pinouts, source conflicts and dependencies. After
worker completion, verify file paths, actual tools/commands, test results and
sources; only coordinator integrates master files or changes the checkpoint.
Separate reference CAD from adapted PX1; follow frozen six-wheel drive and
six-core tether constraints. Pick actual engineering tasks, not just planning.
If native subagents are unavailable, record SUBAGENTS_UNAVAILABLE and perform
one bounded engineering task. NEVER invent agent results or supplier claims.
Never upload proprietary, privately obtained or restricted factory documents.\nDo not publish, push, buy, exfiltrate repository sources, alter files outside
workspace or override electrical and pressure safety tests.

When done, update autonomy/PX1_TEAM_PROGRESS.md with:
STATUS: IN_PROGRESS (until prototype physically validated),
TEAM_RUNTIME: actual agent status (not a guess),
concrete changed paths, commands/tests with outcomes, unresolved blockers,
affected engineering interfaces, and the next tasks.
"""


def spawn_event_count(jsonl: str) -> int:
    """Count explicit completed spawn_agent tool-call events, not role mentions."""
    observed: set[str] = set()
    for line in jsonl.splitlines():
        try:
            event = json.loads(line)
        except (TypeError, ValueError):
            continue
        if not isinstance(event, dict) or event.get("type") not in (
            "item.completed", "item.updated", "item.started"
        ):
            continue
        item = event.get("item")
        if not isinstance(item, dict):
            continue
        if item.get("type") not in ("collab_tool_call", "tool_call"):
            continue
        if item.get("tool") != "spawn_agent" and item.get("name") != "spawn_agent":
            continue
        # Count distinct tool calls; this is evidence of call attempts only.
        observed.add(str(item.get("id") or item.get("call_id") or line))
    return len(observed)


def preflight() -> tuple[str | None, list[str]]:
    problems = []
    for p in ("AGENTS.md", "current/README.md", "current/HOLD_REGISTER.json"):
        if not (ROOT / p).exists():
            problems.append("Missing " + p)
    if not BRIEF.is_file() or status() == "MISSING":
        problems.append("Missing team brief/checkpoint")
    git = shutil.which("git")
    codex = shutil.which("codex")
    if not git:
        problems.append("Git executable not found")
    elif subprocess.run([git, "-C", str(ROOT), "rev-parse", "--is-inside-work-tree"],
                        capture_output=True, text=True).returncode != 0:
        problems.append("PX1 directory is not a git checkout")
    if not codex:
        problems.append("Codex CLI executable not found; install and login first")
    return codex, problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="PX1 native multi-agent Codex runner")
    ap.add_argument("--cycles", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=2400, help="Seconds per cycle")
    ap.add_argument("--dry-run", action="store_true", help="Verify setup, do not invoke Codex")
    args = ap.parse_args(argv)
    if not (1 <= args.cycles <= 24) or not (120 <= args.timeout <= 7200):
        ap.error("Use --cycles 1..24 and --timeout 120..7200")
    codex, problems = preflight()
    print("PX1 TEAM PREFLIGHT")
    print("root:", ROOT)
    print("checkpoint:", status())
    print("Codex:", codex or "NOT FOUND")
    print("Note: checked environment, NOT agent startup or CAD readiness.")
    if problems:
        for error in problems:
            print("ERROR:", error, file=sys.stderr)
        return 2
    assert codex is not None
    if args.dry_run:
        return 0
    RUNS.mkdir(parents=True, exist_ok=True)
    failures = 0
    for cycle in range(1, args.cycles + 1):
        if status() == "COMPLETE":
            print("Checkpoint says COMPLETE; manually verify physical release evidence.")
            return 0
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        run_dir = RUNS / f"{stamp}-cycle-{cycle:02d}"
        run_dir.mkdir(parents=True, exist_ok=False)
        work = prompt(cycle)
        (run_dir / "prompt.txt").write_text(work, encoding="utf-8")
        cmd = command(codex, run_dir / "last_message.txt")
        (run_dir / "command.json").write_text(json.dumps(cmd, indent=2), encoding="utf-8")
        print(f"[PX1] Cycle {cycle}/{args.cycles} — local logs: {run_dir}", flush=True)
        began = time.monotonic()
        try:
            p = subprocess.run(cmd, input=work, cwd=ROOT, capture_output=True,
                               text=True, encoding="utf-8", errors="replace",
                               timeout=args.timeout)
            code, stdout, stderr = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            code = 124
            stdout = e.stdout or ""
            stderr = e.stderr or ""
            if isinstance(stdout, bytes):
                stdout = stdout.decode("utf-8", "replace")
            if isinstance(stderr, bytes):
                stderr = stderr.decode("utf-8", "replace")
            stderr += "\\nCycle timeout; artifacts/checkpoint may be incomplete.\\n"
        (run_dir / "events.jsonl").write_text(stdout, encoding="utf-8")
        (run_dir / "stderr.log").write_text(stderr, encoding="utf-8")
        summary = {
            "cycle": cycle, "exit_code": code,
            "elapsed_seconds": round(time.monotonic() - began, 1),
            "checkpoint": status(),
            "observed_spawn_tool_calls": spawn_event_count(stdout),
            "spawn_evidence_note": "Tool calls are not proof of finished subagents.",
        }
        (run_dir / "run.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print("[PX1]", summary, flush=True)
        failures = failures + 1 if code != 0 else 0
        if failures >= 2:
            print("Stopped after two failed cycles; inspect stderr.log.", file=sys.stderr)
            return 1
        if status() == "COMPLETE":
            print("Checkpoint says COMPLETE; verify before manufacture.")
            return 0
    print("Cycle limit reached. Check artifacts before starting next set of cycles.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
