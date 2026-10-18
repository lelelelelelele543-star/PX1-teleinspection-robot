#!/usr/bin/env python3
"""Isolated, truly concurrent Codex engineering roles plus serial chief engineer.

No purchase, no push, no autonomous execution until explicitly run on a PC.
Every worker gets a separate throwaway Git worktree and may only contribute
files inside its role-owned autonomy/team_work/ directory.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parent.parent
ROLES = {
    "reference": (
        "Research actual Mini-Cam CRP150/CAM026 source evidence and existing CAD. "
        "Identify verifiable dimensions, source conflicts, and the most useful "
        "next reference-CAD reconstruction or reproducible geometry script."
    ),
    "tether": (
        "Evaluate the six-core tether electrical/video/power feasibility with "
        "actual existing evidence. Quantify required conductor data, 40 m "
        "voltage drop and transmission constraints; identify safety tests. "
        "DO NOT energize equipment or assume 100-120V DC is safe."
    ),
    "qa": (
        "Independently audit the CURRENT mechanical and electrical release HOLD "
        "items, identify runnable non-physical checks, run available tests, "
        "and report exact output. Do not declare release PASS."
    ),
}
FILES = ("PX1_TEAM_BRIEF.md", "PX1_TEAM_PROGRESS.md", "PX1_WORK_PACKAGES.json")
MAX_FILE_BYTES = 6 * 1024 * 1024


def command(args: list[str], cwd: Path, *, input_text: str | None = None,
            timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, input=input_text, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          timeout=timeout, check=False)


def git(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return command(["git", *args], cwd)


def load_plan() -> dict[str, str]:
    p = ROOT / "autonomy" / "PX1_WORK_PACKAGES.json"
    if not p.is_file():
        return {}
    value = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or any(
        not isinstance(k, str) or not isinstance(v, str) for k, v in value.items()
    ):
        raise ValueError("Work packages must be a JSON object of role:string")
    return value


def overlay_handoffs(worker: Path) -> None:
    src = ROOT / "autonomy"
    dst = worker / "autonomy"
    dst.mkdir(parents=True, exist_ok=True)
    for filename in FILES:
        source = src / filename
        if source.exists():
            shutil.copy2(source, dst / filename)
    src_packages = src / "team_work"
    if src_packages.exists():
        shutil.copytree(src_packages, dst / "team_work", dirs_exist_ok=True)


def worker_prompt(role: str, round_number: int, task: str) -> str:
    return f"""PX1 isolated specialist: {role}. Round {round_number}.
Read AGENTS.md, current/README.md, autonomy/PX1_TEAM_BRIEF.md,
autonomy/PX1_TEAM_PROGRESS.md and current/HOLD_REGISTER.json.

Your engineering work package:
{task}

You MUST work only inside autonomy/team_work/{role}/. Do not change any
other file, use git push, purchase parts, edit shared CAD/BOM, or fabricate
sources, dimensional measurements or test outcomes. Read other agents'
previous reports in autonomy/team_work/ and the latest checkpoint.
Build something tangible: a calculation with reproducible assumptions,
validation script, CAD source confined to your work directory, or source
evidence register. Do not spend the cycle just writing a new task plan.

Write autonomy/team_work/{role}/REPORT.md with:
- actual files created and direct relevance to a 3-unit PX1 system;
- original evidence URLs, manufacturer part numbers, confidence levels;
- tests run, exact commands and PASS/FAIL/SKIPPED;
- interface-change message for chief engineer and dependent roles;
- open blockers and next executable task.
Do NOT mark the system manufacturing-ready. Never ask the user to measure
the original or physically test high-voltage hardware.
"""


def run_agent(role: str, round_number: int, task: str, codex: str,
              worker: Path, logdir: Path, timeout: int) -> dict:
    output = worker / "autonomy" / "team_work" / role
    output.mkdir(parents=True, exist_ok=True)
    prompt = worker_prompt(role, round_number, task)
    (logdir / f"{role}.prompt.txt").write_text(prompt, encoding="utf-8")
    start = time.monotonic()
    try:
        proc = command([codex, "exec", "--sandbox", "workspace-write",
                        "--ask-for-approval", "never", "--output-last-message",
                        str(output / "LAST_MESSAGE.txt"), "-"],
                       cwd=worker, input_text=prompt, timeout=timeout)
        rc, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as ex:
        rc = 124
        stdout = ex.stdout or ""
        stderr = ex.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
        stderr += "\nTimeout; agent was stopped. Only valid owned files may be merged.\n"
    (logdir / f"{role}.stdout.log").write_text(stdout, encoding="utf-8")
    (logdir / f"{role}.stderr.log").write_text(stderr, encoding="utf-8")
    return {"role": role, "return_code": rc,
            "seconds": round(time.monotonic() - start, 1),
            "report_exists": (output / "REPORT.md").is_file()}


def import_role_outputs(role: str, worker: Path) -> list[str]:
    src = worker / "autonomy" / "team_work" / role
    dest = ROOT / "autonomy" / "team_work" / role
    files = []
    if not (src / "REPORT.md").is_file():
        return files
    for p in src.rglob("*"):
        if not p.is_file() or p.is_symlink():
            continue
        relative = p.relative_to(src)
        if p.stat().st_size > MAX_FILE_BYTES:
            continue
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
        files.append(str(target.relative_to(ROOT)).replace("\\", "/"))
    return sorted(files)


def run_coordinator(round_number: int, results: list[dict], codex: str,
                    logdir: Path, timeout: int) -> dict:
    prompt = f"""PX1 chief engineer, round {round_number}.
Read AGENTS.md, autonomy/PX1_TEAM_BRIEF.md,
autonomy/PX1_TEAM_PROGRESS.md, current/README.md, current/HOLD_REGISTER.json.
Real independently executed specialist subprocess results follow:
{json.dumps(results, ensure_ascii=False, indent=2)}
Inspect ONLY the actual specialist files in autonomy/team_work/. Treat
failed worker reports as unverified. Integrate verifiable findings, fix
conflicting interface assumptions, assign next independent work packages in
autonomy/PX1_WORK_PACKAGES.json (JSON mapping role to task).
Update autonomy/PX1_TEAM_PROGRESS.md with actual status, artifacts,
tests, blockers, next tasks, and communications for next round.
Preserve six-wheel CRP150 reference versus PX1 adapted split, COTS-only
electronics and 40 m six-conductor tether. Do not replace current/ with a
different robot. Avoid touching authoritative current/ CAD/BOM until
cross-checked, and do not claim validated build/release or physical testing.
Never delete sources, push, purchase, energize equipment, or disable
engineering validation. Work only within the git repository.
"""
    (logdir / "coordinator.prompt.txt").write_text(prompt, encoding="utf-8")
    start = time.monotonic()
    try:
        proc = command([codex, "exec", "--sandbox", "workspace-write",
                        "--ask-for-approval", "never", "--output-last-message",
                        str(logdir / "coordinator.final.txt"), "-"],
                       cwd=ROOT, input_text=prompt, timeout=timeout)
        rc, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as ex:
        rc = 124
        stdout, stderr = ex.stdout or "", ex.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
        stderr += "\nCoordinator timeout; review before continuing.\n"
    (logdir / "coordinator.stdout.log").write_text(stdout, encoding="utf-8")
    (logdir / "coordinator.stderr.log").write_text(stderr, encoding="utf-8")
    return {"return_code": rc, "seconds": round(time.monotonic() - start, 1)}


def main() -> int:
    parser = argparse.ArgumentParser(description="PX1 parallel Codex engineering")
    parser.add_argument("--rounds", type=int, default=1, help="1..8 (default 1)")
    parser.add_argument("--timeout", type=int, default=1800,
                        help="seconds per parallel role and coordinator (min 60)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true",
                        help="explicitly permit existing local changes, without overwriting them")
    args = parser.parse_args()
    if not 1 <= args.rounds <= 8 or not 60 <= args.timeout <= 7200:
        parser.error("Use 1..8 rounds and 60..7200 seconds timeout")
    if not shutil.which("git"):
        print("Git not installed.", file=sys.stderr)
        return 2
    codex = shutil.which("codex")
    if not codex:
        print("Codex CLI not found or not on PATH.", file=sys.stderr)
        return 2
    top = git("rev-parse", "--show-toplevel")
    if top.returncode or Path(top.stdout.strip()).resolve() != ROOT.resolve():
        print("Run with a full checked-out Git repository.", file=sys.stderr)
        return 2
    must_exist = [ROOT / "AGENTS.md", ROOT / "autonomy/PX1_TEAM_BRIEF.md",
                  ROOT / "autonomy/PX1_TEAM_PROGRESS.md"]
    if any(not f.is_file() for f in must_exist):
        print("PX1 team files absent; switch to prepared feature branch.",
              file=sys.stderr)
        return 2
    try:
        load_plan()
    except (ValueError, json.JSONDecodeError) as ex:
        print(f"Invalid role work packages: {ex}", file=sys.stderr)
        return 2
    current = git("status", "--porcelain", "--untracked-files=normal")
    if current.returncode:
        print("Cannot inspect Git status.", file=sys.stderr)
        return 2
    if current.stdout.strip() and not args.allow_dirty and not args.dry_run:
        print("Existing working tree changes detected. Save/commit them, "
              "or explicitly choose --allow-dirty after reviewing git status.",
              file=sys.stderr)
        return 2
    if args.dry_run:
        print("DRY RUN OK: Codex CLI:", codex, "Git:", shutil.which("git"))
        print("Project:", ROOT)
        print("Role count: 3, concurrent process limit: 3")
        print("Working tree:", "dirty" if current.stdout.strip() else "clean")
        print("No Codex calls, branches, Git worktrees, or writes performed.")
        return 0

    session = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    run_base = ROOT / ".px1-agent" / "parallel" / session
    run_base.mkdir(parents=True, exist_ok=False)
    for n in range(1, args.rounds + 1):
        rounddir = run_base / f"round-{n:02d}"
        rounddir.mkdir()
        worktrees: dict[str, Path] = {}
        results: list[dict] = []
        try:
            plan = load_plan()
            for role in ROLES:
                path = run_base / "worktrees" / f"{n:02d}-{role}"
                path.parent.mkdir(exist_ok=True, parents=True)
                added = git("worktree", "add", "--detach", str(path), "HEAD")
                if added.returncode:
                    raise RuntimeError(f"Cannot prepare {role}: {added.stderr}")
                worktrees[role] = path
                overlay_handoffs(path)

            print(f"[PX1] Parallel engineering round {n}/{args.rounds}; workers=3",
                  flush=True)
            with ThreadPoolExecutor(max_workers=3) as pool:
                tasks = {pool.submit(run_agent, role, n, plan.get(role, task),
                                     codex, worktrees[role], rounddir,
                                     args.timeout): role
                         for role, task in ROLES.items()}
                for finished in as_completed(tasks):
                    results.append(finished.result())
            results.sort(key=lambda item: item["role"])
            for item in results:
                role = item["role"]
                if item["return_code"] == 0 and item["report_exists"]:
                    item["imported_files"] = import_role_outputs(
                        role, worktrees[role])
                else:
                    item["imported_files"] = []
                    print(f"[PX1] {role} failed or did not produce REPORT.md",
                          file=sys.stderr)
        except (OSError, RuntimeError, ValueError) as ex:
            (rounddir / "setup_error.txt").write_text(str(ex), encoding="utf-8")
            print(f"PX1 setup failed: {ex}", file=sys.stderr)
            return 1
        finally:
            for path in worktrees.values():
                git("worktree", "remove", "--force", str(path))

        if not all(item["return_code"] == 0 and item["imported_files"]
                   for item in results):
            (rounddir / "results.json").write_text(
                json.dumps(results, indent=2, ensure_ascii=False),
                encoding="utf-8")
            print("Some specialists failed; review logs. Coordinator skipped.",
                  file=sys.stderr)
            return 1
        integrated = run_coordinator(n, results, codex, rounddir, args.timeout)
        (rounddir / "results.json").write_text(
            json.dumps({"roles": results, "coordinator": integrated},
                       indent=2, ensure_ascii=False), encoding="utf-8")
        if integrated["return_code"]:
            print("Coordinator failed; review logs before continuing.",
                  file=sys.stderr)
            return 1
        print(f"[PX1] round {n} complete. Check team checkpoint and artifacts.",
              flush=True)
    print(f"[PX1] Logs: {run_base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
