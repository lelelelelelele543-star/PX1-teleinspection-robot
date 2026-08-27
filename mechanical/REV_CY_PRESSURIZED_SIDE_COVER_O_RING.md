# PX-1 Rev.CY — pressurized side cover / O-ring / locating system

Status: detailed prototype design basis for the CRP150-style six-wheel side bays.

## Cover architecture
Each side has one long removable aluminum cover over the complete three-wheel gear train.

The cover is NOT a cassette. Shafts, inner bearings, motor and inner wall remain part of the crawler structure.

Starting cover envelope for CAD:
- length: 276 mm;
- height: 82 mm;
- basic plate thickness: 5 mm;
- local bearing/seal bosses: 8–10 mm total local thickness;
- material: Al 6082-T6 or 6061-T6;
- hard anodize after final machining preferred.

Exact outside contour follows wheel and body clearance and remains parametric.

## Primary static seal
One continuous O-ring seals the complete cover perimeter.

Starting prototype:
- elastomer: FKM 75 Shore A preferred; NBR 70 acceptable for early dry bench prototype only;
- cross-section: 3.0 mm candidate;
- groove: rounded-rectangle/racetrack path with no sharp corners;
- groove depth target: 2.30–2.40 mm;
- groove width target: 3.8–4.0 mm;
- static axial squeeze target: approximately 20–23%;
- groove fill must be checked against the actual purchased O-ring before RELEASE.

Use a molded standard-size O-ring stretched only slightly around the racetrack path where possible. Do not use a hand-glued cord joint as the production seal.

## Cover location
Perimeter screws do not define the bearing geometry.

Use:
- machined peripheral locating step/pilot;
- 2x precision dowel pins, nominal Ø4 mm, widely separated;
- the outer 6000 bearing bosses are machined in the same setup as the locating features.

This keeps the outer and inner wheel bearings coaxial after repeated service.

## Fasteners
Starting pattern:
- M4 stainless cap screws;
- approximately 35–40 mm perimeter spacing;
- local additional screws around regions of high cover flexibility if FEA/pressure test requires;
- thread engagement >=1.5D in aluminum or use stainless threaded inserts where repeated service is expected;
- all screws accessible with one common hex/Torx size where practical.

## Pressure design
Normal operating overpressure: +0.20…+0.30 bar gauge.

The cover and O-ring joint are designed mechanically for at least **1.0 bar differential pressure** in either direction as the prototype structural target. Positive internal pressure is a leak-detection and ingress-resistance aid, not the sole waterproofing method.

One Ø4–5 mm internal passage connects each side bay to the central dry volume so the entire crawler is filled and monitored from one pressure port.

No drain holes and no atmospheric vent in normal service.

## Cover stiffness target
At 1.0 bar differential:
- no permanent deformation;
- no local O-ring unloading;
- target maximum central deflection <=0.20 mm before prototype qualification.

Final thickness/boss ribs may change after CAD/FEA, but do not reduce the basic plate below 5 mm without evidence.

## Bearing/seal bosses
At each of 3 wheel stations the cover carries:
- Ø22 seal bore for 10x22x7 FKM rotary seal;
- Ø26 H7 outer-bearing bore for 6000-2RS;
- concentricity of seal bore to bearing bore <=0.03 mm target;
- seal entry chamfer 0.5x20°;
- labyrinth counterbore outside the seal sized to overlap the wheel-hub shield without contact.

## Service rules
- cover must come off after wheels are removed;
- no adhesive/gasket maker as the primary perimeter seal;
- O-ring groove remains visible and cleanable by hand;
- spare side-cover O-rings and 6 shaft seals belong in the field service kit;
- after every cover opening: visual inspection, lubrication compatible with FKM, pressure test.

## Release gates
- actual O-ring size selected and squeeze/fill recalculated;
- bolt preload check;
- cover FEA or conservative deflection calculation;
- 1.0 bar bench proof test on empty body;
- repeated open/close service test >=20 cycles;
- pressure decay after thermal cycling;
- submerged rotating-wheel test.
