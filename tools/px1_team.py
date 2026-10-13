#!/usr/bin/env python3
"""Bounded sequential Codex engineering roles, with independent fail-closed gate.

Run this on a Windows checkout. It does not execute from a mobile chat.
Never pushes code, purchases parts, flashes hardware or certifies physical tests.
"""
import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / ".px1-team"


def shell(argv, **kwargs):
    return subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kwargs)


def changes():
    p = shell(["git", "status", "--porcelain", "-uall"])
    if p.returncode:
        raise RuntimeError(p.stderr)
    return {line[3:].replace("\\", "/") for line in p.stdout.splitlines() if len(line) > 3}


def verify():
    p = shell([sys.executable, str(ROOT / "tools/px1_gate.py")])
    return p.returncode, p.stdout + p.stderr


def main():
    p = argparse.ArgumentParser(description="PX1 local engineering agents")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--cycles", type=int, default=1)
    p.add_argument("--timeout", type=int, default=2400)
    p.add_argument("--role", action="append")
    args = p.parse_args()
    if not 1 <= args.cycles <= 20 or not 60 <= args.timeout <= 7200:
        p.error("cycles must be 1..20; timeout 60..7200 seconds")
    data = json.loads((ROOT / "engineering/roles.json").read_text(encoding="utf-8"))
    known = {x["id"] for x in data["roles"]}
    if args.role and not set(args.role).issubset(known):
        p.error("Unknown role; use: " + ", ".join(sorted(known)))
    selected = [x for x in data["roles"] if not args.role or x["id"] in args.role]
    if not shutil.which("git") or shell(["git", "rev-parse", "--is-inside-work-tree"]).returncode:
        print("Full Git checkout required", file=sys.stderr)
        return 2
    check_rc, output = verify()
    print(output)
    if check_rc:
        print("Checker integrity failed; agents not started", file=sys.stderr)
        return 1
    codex = shutil.which("codex")
    if args.dry_run:
        print("Roles:", ", ".join(x["id"] for x in selected))
        print("Codex CLI:", codex or "not installed / not in PATH")
        return 0 if codex else 2
    if not codex:
        print("Install and sign in to Codex CLI on Windows", file=sys.stderr)
        return 2
    for cycle in range(1, args.cycles + 1):
        for role in selected:
            stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            directory = LOGS / stamp / role["id"]
            directory.mkdir(parents=True)
            before = changes()
            policy = (ROOT / role["prompt"]).read_text(encoding="utf-8")
            prompt = (
                "READ AGENTS.md and current/README.md. Execute REAL engineering work "
                "with source-backed files and tests, not just another plan. "
                "Do not edit the independent gate, the gate tests or CI. "
                "Unverified assumptions must be labelled UNVERIFIED. "
                "Do not push, purchase, flash, operate hardware or self-certify release. "
                "Work only in allowed paths. Record evidence and next tasks.\n"
                + "ROLE: " + role["id"] + "\n"
                + "ALLOWED: " + ", ".join(role["allowed"]) + "\n"
                + "INSTRUCTIONS:\n" + policy
            )
            (directory / "prompt.txt").write_text(prompt, encoding="utf-8")
            cmd = [codex, "exec", "--sandbox", "workspace-write",
                   "--output-last-message", str(directory / "summary.txt"), "-"]
            try:
                result = shell(cmd, input=prompt, timeout=args.timeout)
                rc, stdout, stderr = result.returncode, result.stdout, result.stderr
            except subprocess.TimeoutExpired as e:
                rc, stdout, stderr = 124, str(e.stdout or ""), str(e.stderr or "")
            (directory / "stdout.log").write_text(stdout, encoding="utf-8")
            (directory / "stderr.log").write_text(stderr, encoding="utf-8")
            touched = sorted(changes() - before)
            outside = [path for path in touched
                       if not any(path.startswith(a) for a in role["allowed"])]
            gate_rc, gates = verify()
            (directory / "gate.log").write_text(gates, encoding="utf-8")
            info = {"cycle": cycle, "role": role["id"], "codex_exit": rc,
                    "new_changed_paths": touched, "outside_scope": outside,
                    "checker_exit": gate_rc, "physical_tests": "NOT_RUN"}
            (directory / "result.json").write_text(
                json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps(info, ensure_ascii=False))
            if rc or gate_rc or outside:
                print("STOP: inspect logs. No changes automatically reverted.", file=sys.stderr)
                return 1
    print("Agent passes ended; production release NOT granted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
