# GA24 integration — 2026-11-19

Engineering prototype, NOT manufacturing release. Main unchanged.

Continues f0ed199. Two GA24Y-370-2485 / 138:1 provisional family envelopes replace JGA25 study motors. Face X189.5 avoids input-shaft interference. Conservative OD24.4/body67.6/shaft4x17.5 dimensions are ESTIMATED, not verified for the AliExpress units. See ../../08_PROCUREMENT/GA24Y_370_SELECTION_20261119.md.

Service opening now X118..278 (160x53), lid177x68x7. Seal centreline166x58, centreX198, width1.9/depth1.2; material, pressure and strength remain HOLD. Front lid screw stations move to X113. Provisional motor holder uses 4 clearance2.7 holes per motor on PCD19 and pilot6.6; fasteners, thread depth, body attachment and strength remain HOLD. No physical assembly/traction/thermal/sealing tests performed.

See integrated_checks.json for actual local validation, PX1_Current_Validation.json for all pairs and explicit remaining seal/thread/bevel HOLD contacts. Continuous motor envelope extraction includes the documented preceding removals, not proof of the entire service process. Nominal pipe fit is not a real DN150 pass.

Actual model renders: images/px1_isometric.png, images/px1_drivetrain.png, images/px1_side.png, images/px1_pipe.png. Hidden parts in drivetrain view recorded in render_manifest.json. Source and STEP: ../../CAD/PX1_Current_Master.py and ../../CAD/PX1_Current_Master.step. Older release directories are immutable historical evidence, not checks for this revision. Historical PDFs were not regenerated.

Reproduce with build_current.sh, check_pipe_pose.py --active, check_integrated.py --roundtrip --require-pipe-service and render_model.py as in prior release, using _ga24_build output.

Local outcome: 19/19 requested CAD checks pass; zero rigid/unknown collisions, zero Boolean errors. 20 seal/thread/bevel contact HOLD pairs remain. STEP reimport passes validity, solid count, volume and bounds.
