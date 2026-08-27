# PX-1 Rev.DN — side-cover structural sanity check

Status: conservative hand-check for prototype packaging. Final release still requires CAD/FEA and physical proof testing.

## Current cover basis
Per Rev.CY:
- cover nominal length: 276 mm;
- height: 82 mm;
- base thickness: 5 mm;
- material: Al 6082-T6 / 6061-T6 class;
- continuous 3 mm FKM O-ring candidate;
- perimeter M4 screws;
- machined locating pilot + two dowels;
- local bearing/seal bosses at three wheel stations.

## Pressure load
Structural qualification target remains 1.0 bar differential = 0.10 MPa.

Gross pressure force on a 276 x 82 mm rectangular projected area is approximately:
- area ≈0.0226 m²;
- force ≈2.26 kN at 1 bar;
- only ≈0.68 kN at the normal +0.30 bar operating pressure.

This force is distributed around the perimeter fasteners; it is not carried by one screw or one boss.

## Plate-deflection sanity check
Using the 82 mm short span as the controlling idealized plate dimension, 5 mm aluminum, E≈69 GPa and nu≈0.33:
- plate flexural rigidity D is about 807 N·m;
- common clamped/supported rectangular-plate coefficients put idealized central deflection at roughly **0.01–0.08 mm at 1 bar**, depending on boundary assumption.

This is below the current <=0.20 mm target and indicates that 5 mm is a sensible starting thickness.

This is NOT a release calculation because the real cover has:
- three large bearing/seal bosses;
- screw holes;
- O-ring groove;
- local wheel-clearance reliefs;
- non-rectangular contour;
- manufacturing tolerances.

## Fastener concept
Use approximately 18 M4 stainless screws around one complete side cover, exact number optimized after solid layout.

Rules:
- nominal pitch around 35–40 mm;
- extra fasteners near long unsupported edge regions if FEA requests them;
- >=1.5D useful thread engagement in aluminum or stainless threaded inserts in high-service locations;
- one common Torx/hex size preferred;
- defined tightening sequence to compress O-ring uniformly.

## O-ring candidate
A molded circular FKM 75A O-ring with circumference close to the racetrack groove is preferred over hand-spliced cord.

The current groove perimeter is expected to be in the ~620 mm class, giving an equivalent circular ID close to 198–200 mm. Therefore a **~200 x 3 mm FKM** molded ring is a useful procurement candidate for CAD sizing.

Final groove width/depth and ring stretch must be recalculated from the actual purchased seal; this is not yet a production part freeze.

## Wheel-profile relief
Rev.DL introduces a possible shallow annular outer-face relief around each wheel station to widen the Ø90 traction crown.

Rules for that relief:
- do not cut through the 5 mm minimum plate web outside local bosses without evidence;
- do not intersect the O-ring groove;
- do not reduce outer-bearing support wall below the machining requirement;
- maintain a local water-shedding fillet/chamfer rather than a dirt-trapping sharp pocket.

## Proof method
Before electronics are installed:
1. machine one representative body + side cover;
2. fit blank shafts/seals and production-intent O-ring;
3. preferably hydrostatic or otherwise low-energy shielded proof to 1 bar differential;
4. inspect permanent set and O-ring witness;
5. repeat open/close cycle 20 times;
6. repeat pressure-decay test.

Routine crawler operation remains only +0.20…+0.30 bar gauge.

## Decision
**5 mm Al cover remains the prototype baseline.**
Do not thicken it merely from intuition; preserve compact DN150 geometry. Add ribs/local bosses only where FEA or physical proof shows need.
