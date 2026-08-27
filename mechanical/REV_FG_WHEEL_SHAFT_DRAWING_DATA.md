# PX-1 Rev.FG — wheel shaft manufacturing drawing data

Status: drawing-candidate for first machined prototype; not serial release.

## Reference architecture
The uploaded CRP150 side-drive assembly `DRW-002-374` confirms the bearing/seal architecture used as the basis for PX-1:
- two 61801-2RS bearings per wheel station;
- one 61903-2RS outer wheel bearing;
- X-ring 18.72x2.62 at each axle flange;
- 4x4 keying;
- separate removable axle flange.

PX-1 keeps that architecture but uses its own shaft dimensions.

## Part
Suggested project part number: `PX1-431-WHEEL-SHAFT`.

Quantity: 6.

Material candidate:
- preferred: 1.4542 / 17-4PH stainless, precipitation hardened after rough machining;
- alternate prototype: 42CrMo4 QT with corrosion-resistant surface treatment compatible with the seal.

Do not use soft untreated aluminum for a rotating seal journal.

## Datum system
- Datum A: common axis established by the two Ø12 bearing journals and Ø17 outer bearing journal;
- Datum B: inboard axial shoulder;
- Datum C: wheel-keyway angular center plane.

All concentric diameters are turned in one setup where practical.

## Prototype dimensional chain
Starting from inboard end:

1. Bearing journal J1:
   - Ø12 k6 candidate;
   - length 5.0 mm;
   - for 61801 inner ring.

2. Z50 gear seat:
   - Ø12 h6;
   - length 8.0 mm;
   - keyway 4 mm, DIN 6885-A style, effective length about 7 mm candidate;
   - gear must be removable with normal puller force, not press-welded to shaft.

3. Bearing journal J2:
   - Ø12 k6 candidate;
   - length 5.0 mm;
   - for second 61801 inner ring.

4. Spacer/shoulder transition zone:
   - nominal 5.0 mm axial budget;
   - shoulder diameter chosen to provide positive bearing abutment without contacting bearing seals;
   - fillet radius compatible with bearing chamfer.

5. Outer wheel-load bearing journal:
   - Ø17 k6 candidate;
   - length 7.0 mm;
   - for 61903 inner ring.

6. Dynamic X-ring seal land:
   - Ø19.00 h8 candidate;
   - axial polished band >=4.0 mm;
   - Ra <=0.4 um, target 0.2...0.4 um;
   - circularity <=0.01 mm target;
   - total runout to Datum A <=0.02 mm target;
   - absolutely no keyway, thread, circlip groove or machining witness line across contact band.

7. Labyrinth/excluder collar:
   - OD about Ø21 mm;
   - width 2.0 mm candidate;
   - chamfered to avoid cutting the X-ring during assembly.

8. Wheel seat:
   - Ø17 h6 candidate;
   - length 18.0 mm;
   - keyway 4x4, useful key length 12 mm candidate;
   - no keyway breakout into seal land.

9. Axial wheel retention:
   - internal M6x1 thread, minimum full thread depth 10 mm;
   - target prototype screw M6x14 A4 with separate wheel disk/washer architecture;
   - thread entry chamfer 0.5x45 deg.

Current modeled overall shaft length is approximately 54 mm before any final circlip/end-face allowance.

## Bearing-seat details
- bearing shoulder runout to Datum A <=0.02 mm;
- shoulder face roughness Ra <=1.6 um;
- edge radius under bearing inner ring <= bearing manufacturer permissible chamfer;
- assembly lead-in chamfer 0.3x30...45 deg.

Final k6/h6 choice is confirmed after the actual bearing brands are purchased and the service-removal force is checked.

## Gear/wheel keyways
Use separate keyways for gear torque and wheel torque unless the final wheel hub provides another positive drive feature.

Key material:
- stainless/hardened steel compatible with shaft;
- no soft aluminum key.

Keyways must not create a stress riser directly beside the dynamic seal land.

## Surface protection
If 17-4PH is used:
- passivate after final machining/polish;
- protect polished seal track from bead blasting.

If 42CrMo4 is used:
- seal land surface treatment must not flake or produce a rough coating;
- final seal track is ground/polished after hardening/coating process as appropriate.

## General drawing requirements
- unmarked dimensions: DIN ISO 2768-fH style baseline, matching the reference drawing philosophy;
- critical fits/tolerances shown individually override general tolerance;
- deburr all edges;
- no burr allowed in keyways or thread start;
- laser mark part/revision only on a non-bearing, non-sealing surface.

## First article inspection
Record:
- Ø12 J1/J2 diameters at 3 angular positions;
- Ø17 bearing diameter;
- Ø19 seal-land diameter/roundness;
- seal-land Ra;
- runout of seal land and wheel seat to Datum A;
- keyway width/depth;
- overall length;
- M6 thread gauge result.

The first three shafts are inspected 100% before the remaining three are machined.