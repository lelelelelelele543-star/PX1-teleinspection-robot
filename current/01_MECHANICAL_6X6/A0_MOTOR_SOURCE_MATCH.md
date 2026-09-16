# A0 motor-source match — ASS-002-386

Status: SOURCE TOPOLOGY FROZEN / FINAL MOTOR-GEARHEAD PACKAGE NOT YET RELEASED.

## What the MiniCam source actually proves
ASS-002-386 / DRW-002-386 lists:
- 2 × `MOT-001-760` MOTOR and GEAR;
- 2 × `GEA-002-531` bevel gear small Z16;
- 2 × `FSS-002-083` axle bevel gear;
- 2 × `BEA-002-701` bearing 61801-2RS (12×21×5);
- one common `FAL-002-082` motor holder.

The source therefore proves the two-motor topology, separate supported Z16 shafts and the common holder. It does **not** identify the manufacturer or ratio of `MOT-001-760`.

The 1:1 drawing proportions are consistent with an approximately Ø26 gearhead / Ø22 motor class, but that is an envelope reconstruction, not an OEM identity claim.

## Candidate A — existing FAULHABER 2250 + 26/1 S 66:1 stock path
Mechanical study envelope:
- motor `2250S024BX4`: Ø22 mm, L=51.8 mm, 24 V BLDC;
- `26/1 S` three-stage 66:1: Ø26 mm, L2=44.4 mm, nominal ratio 66:1, exact ratio 66.220408;
- 26/1 S output shaft Ø5 × 12 mm;
- combined body length about 96.2 mm.

Two Ø26 gearhead envelopes on the recovered 27 mm motor-centre spacing occupy 53 mm overall and reproduce the current dry-cavity width screen closely.

**Important compatibility gate:** the current FAULHABER 2250 product-combination table does not list the legacy 26/1 S as a standard current combination. Therefore PX1 must not assume that two loose parts can simply be bolted together. Use this path only when the actual stock drive is already a mechanically compatible/assembled unit or its interface is otherwise proven.

## Candidate B — current manufacturer-supported 2250 + 26A path
FAULHABER currently lists `26A` as a supported gearhead family for 2250 BX4 motors. The 26A family is manufacturer-mounted rather than sold as a loose retrofit combination.

A three-stage 26A has:
- Ø26 mm body;
- L2=44.3 mm;
- available ratios around the required range, including nominal 64:1;
- `2250S...BX4 + 26A` total length about 96.1 mm.

This is almost the same envelope as the 26/1 S study and is therefore the cleanest currently supported FAULHABER packaging fallback. Its output/interface differs from the 26/1 S, so the Z16 adapter must be regenerated for the actual purchased/stock package.

## Electrical facts for 2250S024BX4
- nominal voltage 24 V;
- no-load speed about 6200 rpm;
- rated speed about 4870 rpm;
- rated torque 26.2 mNm;
- rated current 0.85 A;
- three motor phases;
- +5 V Hall supply and Hall A/B/C;
- digital Hall sensors.

Therefore BTS7960 and Pololu G2 brushed H-bridges cannot directly commutate this motor. If a 2250 path is used, traction requires a BLDC controller with Hall inputs or a supported FAULHABER controller.

## A0 mechanical interface rule
The A0 drivetrain fixture intentionally separates the motor package decision from the six-wheel side train:

`motor/gearhead candidate -> serviceable coupling/socket -> Ø12 supported pinion axle -> 61801 -> Z16 -> Z40 -> rear X250 long axle`.

This lets the Z50 chain and rear axle be proven before a final motor package is frozen. No production shaft or holder is released from envelope matching alone.

## Ratio planning
For the 26/1 S 66:1 study only, with Z16/Z40=2.5, 3500 motor rpm corresponds to roughly 21 wheel rpm, or about 6 m/min at a nominal 90 mm wheel diameter before slip. This remains a planning value, not an acceptance result.

## Release rule
Final motor package selection requires all of the following:
1. mechanically supported motor+gearhead combination;
2. reproducible mounting in the PX1 dry body;
3. correct BLDC/brushed driver class;
4. A0 current/temperature/forward-reverse test;
5. no change to the mandatory two-motor / Z16→Z40 / six-wheel topology.

References: MiniCam DRW-002-386; FAULHABER 2250 BX4 current datasheet; FAULHABER 26/1 S and 26A gearhead datasheets.
