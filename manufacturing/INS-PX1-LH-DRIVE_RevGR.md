# INS-PX1-LH-DRIVE — first LEFT side-drive inspection — Rev.GR

Status: FIRST-ARTICLE INSPECTION BASELINE; prototype only, not machining release.

## Purpose
Verify one complete left side drivetrain before any mirrored right-side production. This sheet uses the active Rev.GL geometry and assumes the WS-01 wheel-station first article has already passed.

## Active left-side kinematic chain
`Ø32 motor -> supported Z16 bevel pinion -> compact Z40 bevel -> internal-supported X200 shaft -> X200 m1 Z50 -> X150/X250 Z50 neighbors -> X100 idler -> X50 wheel Z50`

Five equal side gears are located at:
- X50 wheel output;
- X100 idler;
- X150 wheel output;
- X200 driven input;
- X250 wheel output.

Nominal pitch-center spacing is 50 mm between adjacent Z50 centers. Wheel output centers X50/X150/X250 are 100 mm apart.

## Datum scheme
**Datum A — side-cover / side-bay longitudinal reference plane.** Establishes X locations.

**Datum B — wheel/X200 shaft center height plane, nominal Z45.**

**Datum C — side-cover locating face / transverse Y datum.**

**Datum M — traction-motor mounting face/axis.** Motor-hole pattern is measured from the exact purchased motor, not from a generic Ø32 envelope.

## Purchased-part record
- motor manufacturer/model: ___
- motor serial/lot: ___
- measured motor OD: ___ mm
- measured overall length: ___ mm
- output shaft diameter/profile: ___
- output shaft protrusion: ___ mm
- mounting PCD/hole size/depth: ___
- no-load current at 24 V: ___ A
- no-load speed at 24 V: ___ rpm
- bevel pair supplier/lot: ___
- Z50 supplier/lot: ___
- bearing/seal lots: ___

## Center-location metrology
Do not accept the bench plate merely because gears can be forced into place.

| Station | Nominal X | Measured X | Measured Z | Notes |
|---|---:|---:|---:|---|
| wheel Z50 #1 | 50.000 | ___ | ___ | |
| idler Z50 | 100.000 | ___ | ___ | |
| wheel Z50 #2 | 150.000 | ___ | ___ | |
| X200 input Z50 | 200.000 | ___ | ___ | |
| wheel Z50 #3 | 250.000 | ___ | ___ | |

Record adjacent measured center distances:
- X50-X100: ___ mm
- X100-X150: ___ mm
- X150-X200: ___ mm
- X200-X250: ___ mm

The functional acceptance limit is contact/backlash quality with the **actual** measured gears. Do not freeze a universal machining tolerance until actual pitch/runout data are known.

## X200 shaft / bevel station record
Active Rev.GL support concept:
- two 61800-class bearings fully inside P0;
- Z40 between those supports;
- outer bearing center approximately Y32 mm in the current model;
- 18x30x7 shaft seal immediately outboard;
- side-input Z50 entirely inside dry side bay, approximately Y42.0..45.5;
- outer side-cover surface remains smooth at X200.

Record:
- X200 shaft radial runout at Z50 seat: ___ mm
- X200 seal-land runout: ___ mm
- X200 axial endplay before bevel preload/retention: ___ mm
- X200 final axial endplay: ___ mm
- Z40 axial position relative to supports: ___
- Z16/Z40 contact-pattern position: ___
- side Z50 axial position: ___
- measured X200-to-X150 tooth-face overlap: ___ mm
- measured X200-to-X250 tooth-face overlap: ___ mm

Target tooth-face overlap from Rev.GL is approximately 3.3 mm; investigate any materially lower value before powered testing.

## Dry hand-rotation gate
With motor disconnected electrically:
1. rotate the supported pinion/input by hand through at least 20 output-equivalent revolutions;
2. record any cyclic tight spot and angular position;
3. verify X50, X150 and X250 wheel outputs all rotate in the same direction;
4. verify X200 input rotates opposite the three wheel outputs, consistent with the four equal spur meshes;
5. inspect for axial gear walk toward side cover or membrane;
6. use marking compound/contact blue where practical on Z16/Z40 and representative Z50 meshes.

Acceptance: no hard tight spot, no tooth-tip binding, no axial contact with fixed structure, and a repeatable contact pattern not concentrated at one edge.

## Powered no-load test
Use a current-limited supply and protective cover/guard.

Record at minimum:

| Command | Supply V | Motor current | Motor/input rpm | Wheel rpm | Noise/temp notes |
|---|---:|---:|---:|---:|---|
| low forward | ___ | ___ | ___ | ___ | |
| mid forward | ___ | ___ | ___ | ___ | |
| full allowed forward | ___ | ___ | ___ | ___ | |
| low reverse | ___ | ___ | ___ | ___ | |
| full allowed reverse | ___ | ___ | ___ | ___ | |

The current command ceiling remains limited by the provisional 1.0 N·m motor-output protection rule until the exact motor torque-current relation and bevel allowable torque are measured/frozen.

## Thermal run
- 30 min unloaded;
- 30 min representative loaded;
- record temperatures every 5 min at motor case, supported pinion bearing, both X200 61800 supports, X200 seal boss, X100 idler region, and all three wheel-flange regions.

Stop for rapidly rising temperature, lubricant distress, abnormal noise or increasing current at constant load.

## Individual blocked-wheel test
For each wheel output X50, X150 and X250:
- mechanically block only that wheel using a safe fixture;
- command only a short current-limited pulse;
- record peak current and any observable gear/bearing deflection/noise;
- inspect keys and Z50 teeth afterward.

Never use an uncontrolled motor stall as the acceptance method.

## Forward/reverse endurance
Prototype gate:
- minimum 100 controlled reversals before right-side duplication;
- inspect backlash/contact pattern after the sequence;
- record any increase in current, gear dust, key fretting, shaft migration or fastener loosening.

A later qualification test will increase this count; Rev.GR is only the first-article manufacturing gate.

## PASS conditions before duplicating RIGHT side
- WS-01 architecture already passed;
- five-Z50 train has no hard tight spot through 20 revolutions;
- all three wheel outputs rotate same direction;
- bevel contact is acceptable and not edge-loaded;
- no Z50 walks into side cover/membrane;
- no-load and loaded current are repeatable in both directions;
- temperatures stabilize during the 30+30 min run;
- short blocked-wheel tests remain within controlled current limit and cause no visible damage;
- 100 reversals complete without loosening/fretting;
- all measured datums are saved back into CAD/inspection records.

Failure of any item stops duplication and returns the exact measured deviation to the CAD/fit decision process.
