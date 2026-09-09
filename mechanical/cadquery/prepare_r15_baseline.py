"""Prepare reproducible R12 camera and named R13 inputs for the R15 study.

Generated/vendor CAD is not redistributed with source. An existing cache is
left intact; R15 checks its metadata and solids. --rebuild replaces only the
generated cache, using the committed R12/R13 sources and supplied motor STEP.
"""
from pathlib import Path
import argparse
import hashlib
import json
import cadquery as cq
import PX1_R12_Camera as camera
import PX1_R12_SelectedParts as r12
import PX1_R13_WetChannels as r13

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor-step", type=Path, required=True)
    ap.add_argument("--cache", type=Path, default=ROOT / "build_r14/r13_named_cache")
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()
    motor_sha = digest(args.motor_step)
    camera_target = ROOT / "build_r12/PX1_R12_CAMERA_CANDIDATE.step"
    if not camera_target.exists() or args.rebuild:
        camera.build(camera_target.parent)
    index = args.cache / "index.json"
    if index.exists() and not args.rebuild:
        old = json.loads(index.read_text())
        for key, expected in (("r13_source_sha256", digest(r13.__file__)),
                              ("motor_step_sha256", motor_sha), ("cadquery", cq.__version__)):
            if old.get(key) != expected:
                raise ValueError(f"Cache differs in {key}; use --rebuild for a fresh derived cache")
        print("Existing R13 cache retained. R15 will import/check every solid and record all input hashes.")
        return
    parts, groups, report = r13.build(ROOT / "build_r15_baseline", args.motor_step, 5)
    args.cache.mkdir(parents=True, exist_ok=True)
    files = {n: f"{i:03}.brep" for i, n in enumerate(parts)}
    for n, p in parts.items():
        p.val().exportBrep(str(args.cache / files[n]))
    index.write_text(json.dumps({"r13_source_sha256": digest(r13.__file__),
        "r12_source_sha256": digest(r12.__file__), "camera_source_sha256": digest(camera.__file__),
        "motor_step_sha256": motor_sha, "cadquery": cq.__version__, "files": files,
        "groups": groups, "r13_report": report,
        "brep_sha256": {n: digest(args.cache / f) for n, f in files.items()}}, indent=2) + "\n")
    print("R13 reference inputs regenerated. Its historical integration result does not replace R15 validation.")


if __name__ == "__main__":
    main()
