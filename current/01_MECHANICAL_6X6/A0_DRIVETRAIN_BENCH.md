# A0 — 6×6 DRIVETRAIN BENCH

Status: ACTIVE FAST-TRACK TEST ARTICLE. Not a production release.

Purpose: prove the mandatory Rev.A six-wheel transmission and source-like traction package before machining the final pressure body.

## Frozen drivetrain
- Three driven wheel stations per side: X50 / X150 / X250.
- Five m1 Z50 stations per side: X50 / X100 / X150 / X200 / X250.
- Rear X250 is the driven long-axle station.
- Two traction motors total, one per side.
- Input topology: motor + reduction gearhead -> separately supported Z16 pinion shaft -> Z16/Z40 bevel pair -> rear X250 axle -> five-Z50 side train.
- Wheel count and this topology may not be simplified to close A0.

## A0 motor baseline
The active mechanical baseline is now the source-envelope-matched FAULHABER package:
- 2250S024BX4, 24 V BLDC, Ø22 x 51.8 mm;
- 26/1 S, three-stage 66:1 candidate, Ø26 x 44.4 mm, output shaft Ø5 x 12 mm;
- two units on Y = ±13.5 mm centres;
- source-like separate Z16 axle supported in 61801 (12x21x5).

Reason: ASS-002-386 shows two Ø26-class three-stage gearheads and Ø22-class motors in the same proportions. Two Ø26 gearheads on 27 mm centres occupy exactly 53 mm overall, matching the reconstructed CRP150 dry-cavity width. This is a strong geometry match, not proof that MiniCam MOT-001-760 used this exact FAULHABER part number or ratio.

The former Pololu 5707 / external 20 mm coupling adaptation is no longer the active A0 mechanical path. It stays as an archived fallback until the source-match path is physically disproved.

## Speed limit
The 26/1 S datasheet limits recommended continuous input speed to 4000 rpm. Therefore Rev.A control must not command the 2250 motor above that limit while this gearhead is installed.

For 66.2204:1 and the Z16/Z40 ratio 2.5:1:
- 3500 motor rpm -> about 21.1 wheel rpm -> about 6.0 m/min with Ø90 wheels;
- 4000 motor rpm -> about 24.2 wheel rpm -> about 6.8 m/min with Ø90 wheels.

A0 normal test ceiling is 3500 rpm. 4000 rpm is a hard gearhead ceiling, not a target operating speed.

## A0 fixture supplied by CAD script
`CAD/PX1_A0_SourceMatch.py` generates:
- two printable/machinable side fixture plates;
- a printable PA20 m1 Z50 test gear (test only, not OEM tooth release);
- the source-match two-motor holder study;
- the 2250 + 26/1S envelope study;
- reference Z16/Z40 mounting envelopes;
- validation JSON.

The side-train fixture uses 6001-2RS 12x28x8 bearings only for A0.1. It preserves the 50 mm shaft-centre spacing but does not pretend to release the CRP150 production bearing/shaft/seal package.

## Test phases
### A0.1 — side train geometry
Use ten printed PA20 m1 Z50 test gears or one five-gear set reused on both sides.
1. Assemble five gears on 50 mm centres.
2. Hand-turn 20 full output revolutions in each direction.
3. Run at low speed with a temporary drive input.
4. Check tight spots, tooth tip interference and plate deflection.
5. Repeat with the mirrored side.

PASS: smooth full rotation in both directions, no tooth collision, no shaft/bearing walk.

### A0.2 — source-match motor module
1. Install both 2250 + 26/1S 66:1 units in the source-match holder.
2. Use the 5 mm output-to-12 mm supported pinion adapter only as an A0 test part.
3. Run each motor separately, then both together.
4. Confirm 61801 support remains seated and the two Ø26 gearheads do not touch.
5. Record no-load current, motor/gearhead temperature and commanded speed.

PASS: stable forward/reverse operation to 3500 motor rpm with no gearhead contact, holder distortion or pinion-shaft movement.

### A0.3 — bevel and full side chain
The actual Z16/Z40 parts must be suitable for the expected torque. Do not use a generic low-torque unhardened C45 pair for a full-load qualification merely because the tooth count fits.
1. Install actual Z16/Z40 pair.
2. Adjust mounting distance/backlash using the A0 fixture/shims before freezing machining dimensions.
3. Couple bevel output to the five-Z50 train.
4. Run forward/reverse unloaded, then with representative wheel/tether resistance.
5. Inspect tooth contact and temperature.

PASS: both complete sides run without binding, tooth damage, shaft walk or bearing displacement.

## Measurements to record
- exact motor and gearhead markings;
- controller/driver used and configuration revision;
- motor rpm command;
- 24 V bus voltage;
- current per motor at no-load and representative load;
- run duration;
- motor and gearhead temperature;
- observed backlash/noise/vibration;
- bevel contact pattern;
- any spacer/shim dimensions required.

## Manufacturing gate
A0 CAD is deliberately a test fixture. Final body, motor holder, Z16/Z40 tooth form, source shaft shoulders and sealing details remain HOLD until physical A0 closes those dimensions.
