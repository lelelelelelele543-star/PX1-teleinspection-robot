# PX-1 Rev.DL — DN150 wheel-profile correction

Status: geometric correction to the six-wheel CRP150-style master. Supersedes the Rev.DA assumption that the Ø90 wheel can be represented as a full-width cylinder.

## Why this correction is required
The old CAD sanity rule only checked `overall crawler width < 150 mm`. That is not sufficient inside a circular DN150 pipe.

With the current packaging:
- DN150 internal radius = 75 mm;
- wheel axis height in crawler coordinates = Z=45 mm;
- body half-width = 46 mm;
- side-cover outer plane = |Y|≈51 mm;
- wheel outer face = |Y|≈67 mm.

A sharp-edged Ø90 x 16 mm rectangular/cylindrical tire section collides with the circular pipe wall at the outer shoulder. The wheel therefore needs a CRP150-style system solution: a narrow full-diameter traction crown and a strongly tapered/crowned outboard shoulder. PX-1 uses its own geometry, not MiniCam proprietary wheel geometry.

## Important coordinate correction
The wheel axle is **not** located on the DN150 pipe centerline in operation.

The crawler settles onto the lower pipe quadrants until both left/right traction crowns touch the wall. Therefore the pipe-axis Z coordinate must be solved from wheel contact rather than arbitrarily set to Z=45 mm.

For a wheel surface point at transverse Y and local wheel radius r, lower contact requires:

`Z_pipe = Z_wheel - r + sqrt(R_pipe^2 - Y^2)`

## PX-1 prototype wheel envelope
Positive-Y side, mirrored left/right:
- cover outer plane: Y=51 mm;
- wheel outer face: Y=67 mm;
- full Ø90 traction crown: Y=51…54 mm, radius 45 mm;
- tapered outer shoulder: radius 45 mm at Y=54 reducing to about 21 mm at Y=67;
- hub/retaining hardware remains inside this external profile.

For the critical crown edge Y=54, r=45:

`Z_pipe = 45 - 45 + sqrt(75²-54²) ≈ 52.05 mm`

So the working DN150 cross-section for the current wheel candidate uses pipe-axis **Z≈52.05 mm** in crawler coordinates.

The contact occurs symmetrically on the lower left/right pipe quadrants. The wheels are supposed to touch the pipe here; there is no artificial 3–5 mm gap at the traction crown.

## Body and cover clearance after settling
Using Z_pipe≈52.05 mm:
- body envelope 92 mm wide, Z=14…90 mm retains roughly 10+ mm radial clearance at its worst rectangular corner;
- side cover outer plane |Y|=51 mm, Z=4…86 mm retains about 5 mm nominal radial clearance at its worst lower corner before screw-head/local-boss refinement.

This is the useful clearance margin that must be protected. Wheel contact itself is not counted as a clearance failure.

## Tread width
A 3 mm full-Ø90 crown is only the first packaging baseline.

Preferred follow-up:
- shallow annular relief on the outer face of the side cover at each wheel station;
- widen the high-radius traction crown to approximately 5–7 mm if the relief can be made without weakening the bearing boss or O-ring land;
- keep the outer shoulder aggressively tapered to remain inside the DN150 cross-section.

## Wheel construction philosophy
Prototype wheel remains modular:
- metallic hub keyed to Ø10 shaft;
- replaceable traction element/ring;
- torque is transmitted mechanically through the keyed hub, not glue;
- base tread optimized for wet PVC/clay/concrete and sewer slime;
- optional high-grip/carbide wheel can later share the same hub interface.

Exact tread material remains HOLD until physical traction testing.

## Wheel retention
The uploaded Proteus crawler wheel-lock drawing shows a simple axial retaining disk/bolt plus O-ring. PX-1 keeps that service philosophy with its own dimensions:
- keyed Ø10 shaft carries torque;
- M6 stainless axial retaining screw candidate;
- Schnorr/spring washer;
- retaining disk/washer;
- small O-ring under the retaining disk where useful for dirt exclusion.

The axial screw is not the torque-transmission element.

## Release gates
1. build the revolved/tapered wheel profile in CAD;
2. solve pipe-axis position from wheel contact automatically;
3. include cover screw heads, bearing bosses and wheel-retainer disk in DN150 section;
4. rerun camera TILT sweep using the corrected pipe-axis Z;
5. test one physical wheel/crawler mock-up in a real 150 mm tube;
6. check wet traction, turning current, wheel shoulder rubbing and tire compression;
7. freeze wheel profile only after those tests.
