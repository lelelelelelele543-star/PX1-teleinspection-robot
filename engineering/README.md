# PX1 Engineering Team and Independent Verification

This is an executable starter harness for the existing PX1 project, not a completed product. The current working master is in current/. Historical revs are research, NOT active CAD.

## Local Windows instructions

Install Python 3, Git and the Codex CLI on the Windows PC and sign in. In a clean local clone of the repo, open PowerShell at the repository root:

1. py -3 -m unittest discover -s engineering/tests -v
2. py -3 tools/px1_gate.py
3. Open engineering/out/gates.md for the CURRENT release blockers.
4. py -3 tools/px1_team.py --dry-run
5. py -3 tools/px1_team.py --role mechanics --cycles 1
6. py -3 tools/px1_team.py --cycles 1 (one pass across all 7 roles)

Codex calls occur locally, sequentially, in bounded time windows. They are not running in the background from mobile ChatGPT. Logs and checkpoints are written under .px1-team/. No server push, purchasing or physical operations are done by this script. The runner STOPS on failures or edits outside the chosen role paths; it does not silently discard engineering work.

## Who does what

reference — CRP150 and CAM026 photo/drawing reconstruction.
mechanics — six-wheel gear train, housing, CAD solids, interferences.
camera_lift — sealed camera and hand-operated lift.
power_tether — six-wire cable, power, RS-485, video, protection.
controls — firmware watchdog, V1 protocol, operator controls.
reel_console_bom — reel and control case, checked Russian suppliers.
independent_reviewer — adversarial report ONLY, never writes CAD release.

## What the simulation really checks

It mathematically screens the nominal drive speed for a candidate 66.2204:1 gearhead / Z16:Z40 bevel / 90mm wheels, cable voltage under 40m copper load and V1 250ms command watchdog behavior. Negative tests intentionally verify that four wheels are rejected, rigid collision blocks machining, excessive RPM fails and corrupted commands do not keep traction alive.

The checker also reads the existing current CAD validation, every rigid interference, HOLD items, actual source-script SHA256 and active BOM. It writes engineering/out/gates.json and gates.md. A green CI run validates the CHECKER; it does not approve any mechanical or electrical release. The project already has unresolved rigid collisions and H01-H10 items.

Not covered by this numerical model: true CAD rebuilding, seal grooves, torque under wet load, acoustic/thermal effects, electromagnetic interference, video integrity or live electrical emergency stop. Existing current CAD build and physical A0-A5 tests remain separate mandatory gates. The 110V tether computation is a numerical what-if ONLY — do not apply such voltage to an unqualified cable, slip ring, reel or console.

Manufacturing drawings must not be signed off unless all real-component fits, sourcing, electrical safety and physical qualification tests are independently verified. The automatic tool has NO authorization to issue manufacturing release.
