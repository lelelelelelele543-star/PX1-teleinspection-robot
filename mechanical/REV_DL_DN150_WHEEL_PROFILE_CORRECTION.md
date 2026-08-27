# PX-1 Rev.DL — DN150 wheel-profile correction

Status: geometric correction to the six-wheel CRP150-style master. Supersedes the Rev.DA assumption that the Ø90 wheel can be represented as a full-width cylinder.

## Why this correction is required
The current master has:
- DN150 internal radius: 75 mm;
- wheel axis approximately on the pipe axis: Z = 45 mm;
- body half-width = 46 mm;
- 5 mm side cover;
- outer wheel face around |Y| = 67 mm.

A sharp-edged Ø90 x 16 mm cylindrical wheel does **not** fit the DN150 circular cross-section at that outer Y position, even though the overall crawler width is less than 150 mm.

Therefore the old `overall width < DN150` test is invalid as a full clearance test.

The proven CRP150-class machine uses Ø90 wheel options in 150 mm pipe, so PX-1 must use the same system-level idea: a narrow full-diameter traction crown and a strongly tapered/crowned wheel shoulder, not a rectangular tire section.

## Clearance rule
For a required nominal radial clearance C inside a pipe of radius R, the wheel radial envelope allowed at transverse coordinate Y is:

`r_max(Y) = sqrt((R-C)^2 - Y^2)`

For DN150 and a design target around 4.5–5 mm nominal clearance, the wheel profile must rapidly reduce in radius as it moves outboard.

## PX-1 prototype wheel envelope
Current preferred own geometry, not copied from MiniCam:

Positive-Y side, mirrored on the opposite side:
- side-cover outer plane nominal: Y = +51 mm;
- wheel outer face: Y = +67 mm;
- full Ø90 traction crown: approximately Y = +51…+54 mm;
- outer shoulder: linear/convex taper from radius 45 mm at Y=54 to radius about 21 mm at Y=67;
- hub/retainer remains inside this tapered external envelope.

At the critical points:
- Y=54, r=45 -> radial envelope ≈70.29 mm -> ≈4.71 mm clearance to an ideal DN150 wall;
- Y=67, r=21 -> radial envelope ≈70.21 mm -> ≈4.79 mm clearance.

The straight taper between those points stays inside that envelope.

This is deliberately more conservative than the old 3 mm target because real tires compress, pipes are imperfect, bolts protrude and manufacturing tolerances accumulate.

## Tread width
A 3 mm full-Ø90 crown is only a packaging baseline, not the final tread design.

Preferred improvement after the side-cover solid is complete:
- machine a shallow annular relief on the outside of the side cover at each wheel station;
- allow the high-radius tread crown to overlap the cover axially without touching it;
- widen the useful traction crown to approximately 5–7 mm while keeping the outboard shoulder tapered.

The cover relief must not intersect the O-ring land or reduce the bearing/seal boss stiffness.

## Wheel construction philosophy
Prototype wheel should be modular:
- metallic hub, keyed to Ø10 shaft;
- replaceable traction element/ring;
- no bonded tire as the only means of torque transfer;
- tread profile selected for wet PVC/clay/concrete and sewer slime;
- later optional high-grip/carbide wheel can share the same hub interface.

Exact tread material remains HOLD until traction tests.

## Wheel retention correction
The uploaded CRP crawler wheel-lock drawing uses a simple axial wheel disk/bolt with an O-ring. PX-1 adopts the same service philosophy, not the proprietary geometry.

PX-1 baseline is now:
- keyed Ø10 shaft carries torque;
- M6 A4/A2 high-strength stainless axial retaining screw candidate;
- spring/Schnorr washer;
- sealing O-ring under the retaining disk/washer where the wheel-hub cavity needs exclusion sealing.

The M6 bolt retains the wheel axially; it does not transmit drive torque.

## Release gates
1. build real revolved wheel profile in CAD;
2. include side-cover screw heads and bearing bosses in DN150 section;
3. sweep complete six-wheel crawler through DN150, not only camera head;
4. print/machine one wheel prototype and test in a real 150 mm pipe;
5. check wet traction, turn-in-place current and sidewall rubbing;
6. freeze tread width/material only after those tests.
