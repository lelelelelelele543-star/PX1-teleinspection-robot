# PX-1 Rev.EA — wheel axle flange / seal solid definition

Status: detailed prototype geometry for all six wheel exits.

## Design basis
The uploaded CRP150 side-drive drawing uses three separate axle flanges on each side, each locally sealed to the side cover. PX-1 adopts that service architecture with its own dimensions and FKM lip-seal stack.

## Visible flange
Per wheel station:
- flange OD: 48 mm candidate;
- flange total axial length: 14 mm;
- outer visible plate thickness: 6 mm;
- locating pilot into side cover: 8 mm;
- material: Al 6082-T6 hard-anodized or AISI 316 if field wear/corrosion testing justifies it;
- 3x M3 A4/A2 Torx screws on PCD 40 mm;
- flange located by pilot, not by screw clearance.

## Static flange seal
Candidate:
- FKM O-ring 30x1.5 mm;
- axial face-seal groove in flange or side cover;
- starting groove width 2.0 mm;
- starting groove depth 1.15 mm;
- target axial squeeze about 23%;
- final groove verified against actual seal manufacturer data.

Do not use RTV/gasket maker as the primary seal.

## Rotating seal and bearing stack
Outer-to-inner around a normal front/rear wheel station:
1. wheel retaining disk + M6 screw + spring/Schnorr washer;
2. keyed/recessed wheel hub;
3. non-contact labyrinth overlap around flange nose;
4. FKM TC double-lip shaft seal 12x22x7;
5. outer bearing 61801-2RS, 12x21x5;
6. Z50 wheel gear, m1, face 8 mm;
7. inner bearing 61801-2RS, 12x21x5;
8. shaft shoulder/circlip or locknut.

The wheel hub is recessed around the protruding flange, so the flange/bearing/seal package may occupy Y beyond the nominal side-cover plane without forcing the Ø90 traction shoulder farther outboard.

## Axial packaging target, positive-Y side
Nominal planes used by the master model:
- inner structural bearing seat: Y≈36…41 mm;
- gear working width: Y≈41…49 mm;
- outer bearing: Y≈49…54 mm;
- shaft seal: Y≈54…61 mm;
- wheel traction envelope: Y≈51…67 mm with a recessed central hub around the flange.

The negative-Y side is mirrored.

This is a packaging definition, not a machining dimension chain.

## Shaft
Common front/rear wheel shaft:
- main bearing/gear/wheel diameter: Ø12 h6;
- material preferred: 40X13/AISI 420 stainless, hardened/ground seal journal;
- seal journal Ra <=0.4 um;
- no keyway/thread/flat beneath the seal lip;
- 4x4 mm parallel key candidate for wheel and driven gear;
- M6 axial thread in shaft end only.

## Middle wheel station
The middle station carries the bevel input as well as the side Z50 gear.

Use a stepped one-piece or rigidly coupled shaft:
- Ø10 section in P0 for KHK Z45 bevel gear and compact P0 bearing;
- clean-side rotary seal at P0-to-side-bay boundary;
- Ø12 section in P1/P2 for Z50 gear, outer 61801 bearing, outer wheel seal and wheel.

This gives two independent water barriers before water could reach P0:
1. outer wheel seal;
2. central P1/P2-to-P0 shaft seal.

## Flange stiffness / fastening
Three M3 screws on PCD 40 leave about 2.3 mm nominal radial edge land in a Ø48 flange when using ~Ø3.4 clearance holes. This is acceptable for the prototype only if countersinks do not break the edge.

If the chosen screw head/countersink requires more radial material, enlarge flange OD to 50 mm rather than reducing the sealing land.

## Service sequence
1. depressurize affected side zone;
2. remove wheel M6 retainer and wheel;
3. remove 3 flange screws;
4. withdraw flange with outer bearing/seal where practical;
5. replace seal/bearing/O-ring on bench;
6. clean O-ring land and labyrinth;
7. reinstall with controlled screw torque;
8. pressure-test only the affected side zone before full robot deployment.

## Qualification gates
- actual flange O-ring compression check;
- press-fit / slip-fit bearing strategy frozen;
- shaft runout <=0.03 mm at seal journal;
- 2 h submerged powered rotation;
- mud/sand exposure + pressure wash;
- 20 flange removal/refit cycles;
- pressure-decay comparison before/after endurance;
- verify no flange or M3 head contacts DN150 wall through full crawler yaw/roll tolerance.