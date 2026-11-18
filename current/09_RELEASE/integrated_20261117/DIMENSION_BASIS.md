# Integrated packaging dimension basis — 2026-11-17

All values mm. Confidence describes evidence, not manufacturing readiness.

| Interface | Value | Basis | Qualification still needed |
|---|---:|---|---|
| Wheel X stations | 50 / 150 / 250 | CONFIRMED project architecture | Real wheel profile/contact |
| Side gears | 5 × m1 Z50 each side, 50 pitch spacing | CONFIRMED topology; DERIVED pitch geometry | OEM pressure angle, backlash, tooth material |
| Motor axes | Y ±13.5, Z45 | DERIVED from existing body/source layout | Terminal/lead space and tolerances |
| RF JGA25 motor body | Ø24.4 × 40 | Seller-published family envelope, exact variant unconfirmed | Actual motor, rear lead clearance |
| RF JGA25 gearbox | Ø25 × 25 | Seller envelope, conservative versus manufacturer 23 at 77 rpm | Ratio/variant conflict; torque inadequate for full-load target |
| RF JGA25 shaft | Ø4 × 10 | Seller listing; manufacturer drawing differs | Pilot/shaft origin and usable length |
| Middle shaft inner end | abs(Y)=26.8 | ESTIMATED to clear motor envelope | Retention, stiffness, bearing pressure |
| Middle plain bush | Ø12/14 × 3, abs(Y)=26.8…29.8 | ESTIMATED, replaces 4-mm bush | Wear/contact pressure; no lifetime claim |
| Support bosses | abs(Y)=26.5…29.8, middle R8.5 / idler R7 | ESTIMATED; restored material behind seats | Wall strength, machining and pressure continuity |
| Idler pin inner end | abs(Y)=27, outer end34 | ESTIMATED to clear motors/holder | Press fit, shoulder, axial retention |
| Camera setback | 52 toward front | ESTIMATED to clear SP13/body with retained full camera | Lift moment, joints, bend passage, camera pressure interface |
| Harness service loop | R27 in XZ plane, lower Z85 | ESTIMATED, full six-core model retained | All transition bends and moving lift, no fatigue qualification |
| Gas-spring moving eye | (47,16,102) | ESTIMATED, clear of carrier deck | End-fitting specification, stroke stops, force/balance |

The central harness loop and camera bracket are integrated proposed geometry, not
recovered OEM dimensions. The shortened middle bush has a housing boss in CAD;
its safe load and retention are not proven by collision clearance. Coupling and
socket geometry remain schematic. Static clearance does not establish functional
torque transfer, support adequacy or sealing.

No custom electronics PCB is introduced. Brushed H-bridge package geometry remains
in the assembly; it is not proof of current/thermal suitability for an unselected
traction motor. Main tether stays six-core, no coax, 40-m first system target.


## Retained open geometric checks

The inherited DN150 pose uses pipe centre Z=52.0480547 and the unverified QRW90
profile. Its tyre shoulders protrude ~4.4427 mm radially. This is explicitly not
a DN150 fit pass; changing the pipe pose or tyre solely to make a report green
would not establish physical passage. Actual tyre profile and supported pose need
an integrated revision and pipe test. Motor vertical extraction also remains
blocked under the existing removal sequence; the body opening and gland must be
considered in a revised service sequence/design. No serviceability pass is claimed.
