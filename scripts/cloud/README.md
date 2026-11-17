# PX1 cloud CAD (no local PC required)

This is a **real build pipeline**, not a new CAD concept. The current assembly at
`current/CAD/PX1_Current_Master.py` uses **CadQuery**, not the FreeCAD Python API.
It imports three genuine vendor STEP models, builds the current full master,
exports a STEP assembly, and runs the existing collision/clearance validation.

## Codex Cloud

1. From a browser on Android or desktop, open Codex Cloud, connect GitHub
   `lelelelelelele543-star/PX1-teleinspection-robot`, and **create/publish**
   an environment for this repository (the ChatGPT GitHub app connection is
   not by itself a published Codex environment).
2. Choose the repository as a source; on an Ubuntu/Debian environment set the
   setup command to `bash scripts/cloud/setup_codex.sh`. This installs CadQuery
   and FreeCAD (the installation must complete successfully).
3. Start the task from the published environment; direct Codex to
   `AGENTS.md`, `current/REV_A_FAST_TRACK.md`, and
   `scripts/cloud/build_current.sh`.
4. Run `bash scripts/cloud/build_current.sh` and inspect
   `_cloud_build/cloud_build_summary.json`, `px1_side_envelope.svg`,
   `PX1_Current_Validation.json`, and `CAD/PX1_Current_Master.step`.
   Review actual violations; do not call an export a pressure or manufacture PASS.
5. Make changes in a **separate branch/PR** and commit the generated
   visualizations that really correspond to the modified CAD. Do not overwrite
   main automatically or publish proprietary Proteus reference assets.

## GitHub Actions

The PR workflow `.github/workflows/px1-cloud-cad.yml` also builds the
current full assembly on a GitHub-hosted runner. It uploads the STEP,
actual-solid bbox SVG, QA JSON and logs as a run artifact. It does **not**
install FreeCAD (that part runs in the optional Codex cloud environment).
GitHub Actions availability depends on repository settings. Build time,
runner quotas and available Codex credits are account-dependent.

## Next engineering milestone

Integrate 6 wheels, 2 motors, the two full 5-gear side trains, body and
bearing/seal stacks into a collision-reviewed **single** build. Track the
interference list as an explicit repair queue. After resolving physical
blocking interfaces, progress to camera + manual lift, six-core/40m tether,
and control/console. Do not spawn another isolated shaft study unless it
directly resolves a blocker in this assembled model.

### Caveats

This pipeline does not convert the STEP into native `FCStd` automatically,
does not certify tooth geometry or water/pressure tightness, and does not
launch Codex by itself. A user must publish/authorize a Codex environment.
