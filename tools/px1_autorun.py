#!/usr/bin/env python3
"""Bounded checkpoint-driven local Codex runner for PX1 reference reconstruction.

Run inside a clone of PX1. Does NOT upload, publish, install or buy anything.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASK = Path("autonomy/CRP150_REFERENCE_TASK.md")
STATE = Path("autonomy/CRP150_REFERENCE_PROGRESS.md")


def checkpoint_status(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    for line in path.read_text(encoding="utf-8").splitlines()[:25]:
        if line.startswith("STATUS: "):
            return line.removeprefix("STATUS: ").strip().upper()
    return "UNKNOWN"


def build_prompt(run_number: int) -> str:
    return f"""Continue PX1 engineering autonomously. Cycle {run_number}.
Read AGENTS.md, current/README.md, {TASK.as_posix()},
and {STATE.as_posix()} before editing.
The task file defines the objective, source hierarchy, files and acceptance gates.
Do real research/reconstruction/CAD/validation work; do not just rewrite plans.
Choose the highest-priority unfinished verifiable subtask and execute it.
If a dimension cannot be sourced, derive or estimate it with confidence label and
continue; do not ask the user to measure it. If network or a CAD tool is unavailable,
record that limitation, use already available evidence and continue other work.
Work only inside this repository and never modify current/ as an alternative robot.
Never overwrite source drawings, delete files, push, publish, place orders or invoke
unsafe unrestricted access. Do not claim a CAD PASS from script execution alone.
Before ending, update {STATE.as_posix()} with artifacts created, actual checks,
remaining differences, exact next actions, and STATUS: IN_PROGRESS or COMPLETE.
Use COMPLETE only when ALL acceptance requirements are supported by files and tests.
Do not put tasks on hold merely because a factory dimension is unknown.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Local bounded Codex work loops for PX1")
    ap.add_argument("--cycles", type=int, default=6,
                    help="Maximum Codex cycles per run (default 6)")
    ap.add_argument("--timeout", type=int, default=3600,
                    help="Seconds allowed per cycle")
    ap.add_argument("--pause", type=float, default=2.0,
                    help="Seconds between cycles")
    ap.add_argument("--dry-run", action="store_true",
                    help="Check local setup without invoking Codex")
    args = ap.parse_args()

    if args.cycles < 1 or args.cycles > 100 or args.timeout < 60 or args.pause < 0:
        ap.error("Use 1..100 cycles, timeout >= 60 sec and nonnegative pause")
    if not (ROOT / "AGENTS.md").is_file() or not (ROOT / TASK).is_file():
        print("Run from a full PX1 repository containing AGENTS.md and the task file.",
              file=sys.stderr)
        return 2
    if checkpoint_status(ROOT / STATE) == "MISSING":
        print(f"Missing checkpoint: {ROOT / STATE}", file=sys.stderr)
        return 2
    git = shutil.which("git")
    if not git:
        print("Git is required for workspace provenance.", file=sys.stderr)
        return 2
    verify_git = subprocess.run([git, "-C", str(ROOT), "rev-parse",
                                 "--is-inside-work-tree"],
                                capture_output=True, text=True)
    if verify_git.returncode != 0:
        print("The PX1 directory must be a Git working tree.", file=sys.stderr)
        return 2
    codex = shutil.which("codex")
    if not codex:
        print("Codex CLI not found. Install/sign in to Codex and retry.",
              file=sys.stderr)
        return 2
    if args.dry_run:
        print(f"OK: Git={git}; Codex={codex}; root={ROOT}; "
              f"checkpoint={checkpoint_status(ROOT / STATE)}")
        return 0

    logs = ROOT / ".px1-agent" / "runs"
    logs.mkdir(parents=True, exist_ok=True)
    consecutive_failures = 0
    for num in range(1, args.cycles + 1):
        status = checkpoint_status(ROOT / STATE)
        if status == "COMPLETE":
            print("Checkpoint marked COMPLETE. Confirm evidence before fabrication.")
            return 0
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir = logs / f"{stamp}-{num:02d}"
        run_dir.mkdir(parents=True, exist_ok=False)
        prompt = build_prompt(num)
        (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
        command = [codex, "exec", "--sandbox", "workspace-write",
                   "--ask-for-approval", "never", "--output-last-message",
                   str(run_dir / "final_message.txt"), "-"]
        print(f"[PX1] cycle={num}/{args.cycles} status={status} "
              f"log={run_dir}", flush=True)
        t0 = time.monotonic()
        try:
            p = subprocess.run(command, input=prompt, cwd=str(ROOT),
                               text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, encoding="utf-8",
                               errors="replace", timeout=args.timeout)
            exit_code = p.returncode
            stdout, stderr = p.stdout, p.stderr
        except subprocess.TimeoutExpired as exc:
            exit_code = 124
            stdout = ((exc.stdout or b"").decode("utf-8", "replace")
                      if isinstance(exc.stdout, bytes) else (exc.stdout or ""))
            stderr = ((exc.stderr or b"").decode("utf-8", "replace")
                      if isinstance(exc.stderr, bytes) else (exc.stderr or ""))
            stderr += ("\nRunner timeout: the next cycle will resume "
                       "from files, not conversation memory.\n")
        (run_dir / "stdout.log").write_text(stdout, encoding="utf-8")
        (run_dir / "stderr.log").write_text(stderr, encoding="utf-8")
        new_status = checkpoint_status(ROOT / STATE)
        summary = {"time": stamp, "cycle": num, "return_code": exit_code,
                   "seconds": round(time.monotonic() - t0, 1),
                   "checkpoint": new_status}
        (run_dir / "run.json").write_text(json.dumps(summary, indent=2),
                                           encoding="utf-8")
        print(f"[PX1] finished: exit={exit_code}, status={new_status}",
              flush=True)
        if new_status == "COMPLETE":
            print("[PX1] Agent marked COMPLETE; verify acceptance gates independently.")
            return 0
        if exit_code != 0:
            consecutive_failures += 1
            if consecutive_failures >= 2:
                print("[PX1] Stopped after 2 failed cycles; "
                      "inspect latest stderr.log.", file=sys.stderr)
                return 1
        else:
            consecutive_failures = 0
        if num < args.cycles:
            time.sleep(args.pause)
    print("[PX1] Cycle budget reached. Run the same command again "
          "to continue from checkpoint.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
