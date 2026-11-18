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

## Integrated verification (2026-11-18)

The active master uses the RF JGA25 brushed motor **fit candidate** described in
`current/08_PROCUREMENT/RF_MOTOR_CANDIDATES_20261117.md`, not a qualified traction
selection. FAULHABER is excluded by the user. The prior 146-part count is historical;
the expected wheel/gear/motor counts remain enforced.

After `build_current.sh`, run:

```sh
python scripts/cloud/check_integrated.py _cloud_build --roundtrip
python scripts/cloud/render_model.py _cloud_build
```

The first command fails on rigid/wheel collisions, invalid geometry, boolean
errors, source-hash mismatch, sampled Z50 interference or STEP roundtrip changes.
It retains seal/thread/bevel contact HOLDs and separately reports DN150 and
service-path limitations. It does not qualify manufacturing or actual traction.
The second command renders the actual saved triangle mesh with a depth buffer,
using numpy/Pillow and `cc`, without FreeCAD, a display, or generative images.
`images/render_manifest.json` records source, mesh and image hashes and hidden
components for the drivetrain view. The bounding-box SVG remains only an outline.

Validated release evidence is indexed in `current/09_RELEASE/integrated_20261117/`.
Historical PDFs, part drawings and old illustrations are not current release evidence.


## Nominal pipe and service-window revision (2026-11-18)

The active wheel outer shoulder is an engineered profile, not an OEM tyre
reconstruction. The nominal contact-derived pose and the enlarged pressure-cover
opening are documented in `current/09_RELEASE/pipe_service_20261118/`.

```sh
python scripts/cloud/check_pipe_pose.py --active --mesh _cloud_build/images/assembly_mesh.json.gz --out _cloud_build/pipe_verification.json
python scripts/cloud/check_integrated.py _cloud_build --roundtrip --require-pipe-service
python scripts/cloud/render_model.py _cloud_build
```

The added gate requires analytical tyre containment, conservative nonwheel solid
bounds, continuous candidate-motor exit,32 diagnostic motor poses and four service
tool approaches. The pipe view renders actual CAD inside the nominal circle.
Passing this gate does not prove real tyre compliance, pipe passage, pressure
integrity or the preceding dismantling sequence. The active motor remains a fit
candidate with insufficient demonstrated full-load torque.
