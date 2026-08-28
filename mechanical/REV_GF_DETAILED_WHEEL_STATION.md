# PX-1 Rev.GF — detailed wheel station

Status: validated CAD packaging candidate for the active Rev.GE DN150 architecture; not a machining release.

## Why Rev.GF was required
The active Rev.GE side bay is only 8 mm deep (Y=38...46 on the left side) and must remain isolated from P0 by the 4 mm pressure membrane. A direct stack of a 61801 bearing (12x21x5) plus a source-like Z50 B4 gear needs more than the available 8 mm once assembly clearance is included.

A first attempt to recover the missing axial space with an approximately Ø53 mm shallow gear recess in the 5 mm side cover was rejected. The recess approaches/interferes with the large side-cover O-ring route and weakens the sealing land. The pressure/seal plane is therefore kept uncut.

## Rev.GF correction
The inboard wheel-shaft support becomes a standard thin 6701-2RS bearing, 12x18x4 mm. The next outboard support remains 61801-2RS 12x21x5 and the main outboard wheel-load bearing remains 61903-2RS 17x30x7.

The 6701 substitution is deliberate PX-1 geometry, not copied MiniCam geometry. JTEKT/Koyo data for 6701-2RS gives 12x18x4 mm, Cr 1.15 kN and C0r 0.530 kN. The inboard bearing is lightly loaded compared with the outboard pair and this rating is adequate for the prototype load envelope; exact purchased bearing brand/clearance remains a release gate.

## Left-side axial stack, global Y coordinates
- pressure membrane outer face / P1 inner boundary: Y=38.00;
- 6701-2RS: Y=38.10...42.10;
- 0.10 mm axial clearance;
- m1 Z50 gear, finished face 3.75 mm: Y=42.20...45.95;
- side-cover inner face: Y=46.00; no gear recess;
- 61801-2RS in axle flange: Y=46.15...51.15;
- 0.20 mm shoulder/gap;
- 61903-2RS in axle flange: Y=51.35...58.35;
- 0.20 mm shoulder/gap;
- X-ring running section: Y=58.55...61.95;
- 0.20 mm gap;
- keyed wheel seat: Y=62.15...69.15;
- recessed wheel-retaining hardware outer face: <=Y=69.80.

The right side is mirrored.

## Shaft / flange concept
Stepped shaft:
- Ø12 through the inner bearing, Z50 gear and 61801;
- Ø17 through 61903;
- Ø19 polished X-ring land;
- Ø17 keyed wheel seat;
- internal M8 thread for one recessed low-head wheel retaining screw.

Wheel torque is transmitted by a 4x4x7 key. The M8 screw provides axial retention only and is not used as the torque path.

The removable axle flange carries the 61801, 61903 and dynamic seal land while the inner 6701 bottoms against a local stationary boss attached to the P1 pressure membrane. The boss does not penetrate P0. Static flange sealing remains based on the 32x1.5 O-ring architecture.

## Wheel profile
The Ø90-class wheel remains dished/tapered rather than cylindrical. The inboard tread carries the full 45 mm radius near the cover and the profile tapers outward so the hub/retaining screw remain inside the DN150 cylinder.

Validated left-side outer-profile stations (Y, radius mm):
- 51.25, 45.00
- 53.00, 45.00
- 55.00, 43.80
- 58.00, 40.38
- 61.00, 36.45
- 64.00, 31.90
- 67.00, 26.50
- 70.00, 18.00
- 71.00, 15.50

The minimum analytical ideal-DN150 profile margin in the active Rev.GE pipe placement is about 0.12 mm. This is intentionally near-contact geometry for the elastic tread, not a debris/ovality allowance. The physical DN150 sweep test remains mandatory.

## CAD validation result
The local Rev.GF model passed:
- all solids valid;
- zero gear-to-inner-support collision;
- zero gear-to-side-cover collision;
- zero wheel-core/tire-to-flange collision;
- zero wheel-core/tire-to-cover collision;
- no P0 pressure-boundary breach;
- no fixed hardware outside the ideal DN150 cylinder;
- keyway does not cross the X-ring running land;
- the side-cover sealing plane remains full 5 mm thickness at the wheel station.

For a conservative 4 N*m wheel torque envelope:
- 4x4x7 wheel-key shear: about 16.8 MPa;
- wheel-key bearing stress: about 33.6 MPa;
- 4x4x7 gear-key shear: about 23.8 MPa;
- gear-key bearing stress: about 47.6 MPa;
- Ø12 shaft torsional shear: about 11.8 MPa.

These are screening calculations only. Final material, fits, fillets and purchased-part measurements must be frozen before machining drawings.

## Source architecture reference
Uploaded CRP150 drawing DRW-002-374 remains the architecture reference for the five-Z50 side train, 61801/61903 bearing family, axle flange, 18.72x2.62 X-ring, 32x1.5 static O-ring and keyed wheel shafts. Rev.GF changes the compact inboard bearing and exact axial geometry to make the PX-1 pressure architecture physically packageable.

## HOLD before machining release
1. Measure the actual purchased 6701-2RS, 61801-2RS, 61903-2RS and X-ring.
2. Freeze shaft/bearing fits and flange pocket tolerances from the selected manufacturers.
3. Validate X-ring groove against the selected elastomer datasheet and pressure direction.
4. Run body/cover FEA with the real wheel-flange holes and clamp pattern.
5. Print/machine one wheel-station mock-up and run radial-load, seal-drag and immersion tests.
6. Perform a full physical DN150 sweep with the real tread compound.