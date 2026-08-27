# PX-1 Rev.EF — central bevel output / side-drive coupling

Status: prototype architecture, source-aligned but PX-1-specific geometry.

## Source-derived architecture
The CRP150 crawler housing drawing shows, per crawler:
- 2x big bevel gear Z40;
- 2x bevel-gear axle;
- 2x shaft seal 18x30x7;
- 2x bearing 61800-2RS (10x19x5);
- local O-rings/axle rings around the bevel-output assembly.

The side-drive drawing separately shows one long wheel axle, two short wheel axles, five Z50 gears, 61801/61903 bearings and local axle flanges.

PX-1 adopts that separation: the center bevel transmission remains in P0 and transfers torque across the P0/P1 or P0/P2 pressure boundary to the side drive.

## PX-1 transfer shaft
Per side, one transfer shaft is centered on the middle-wheel station X=150 / Z=45.

Prototype stepped shaft candidate:
- large bevel gear seat: Ø10 h6;
- 61800 bearing journal: Ø10 h6;
- seal journal at body wall: Ø18 h8 / polished;
- side-bay drive stub: Ø12 h6;
- material candidate: 17-4PH / 40Cr13 / equivalent corrosion-resistant high-strength stainless after machining trial;
- no thread or keyway under the dynamic seal lip.

The Ø18 seal journal deliberately follows the proven 18x30x7 shaft-seal class seen in the source housing drawing.

## Large bevel gear
Current catalog candidate remains KHK SB1.5-4518H:
- m1.5;
- Z45;
- bore 10 mm;
- paired with SB1.5-1845H Z18;
- ratio 2.5:1.

The production torque connection between the KHK gear and PX-1 shaft is HOLD until the actual gear hub is measured. Preferred order:
1. existing catalog keyway if supplied and suitable;
2. machine a short keyway after hub-wall check;
3. clamp hub only if a positive keyed solution is not practical.

No adhesive-only torque transfer.

## Bearing / seal support
Each side transfer shaft uses:
- one 61800-2RS in P0 close to the large bevel gear;
- one 18x30x7 FKM shaft seal at the P0-to-side-bay wall;
- the side-drive middle axle bearing stack provides the second radial support after the service coupling is engaged.

This is deliberately similar at system level to the source CRP arrangement, which uses one 61800 and one 18x30x7 seal per bevel axle.

## Service coupling to middle wheel axle
PX-1 does not make the bevel-output shaft and the complete wheel axle one permanent part. The two are joined inside P1/P2 with a short positive dog coupling.

Prototype coupling target:
- transfer shaft side: Ø12 male stub;
- middle wheel axle side: matching removable female/half coupling;
- outside diameter <=22 mm;
- axial engagement 8–10 mm;
- two opposed dogs or cross-slot geometry;
- light running axial clearance so the side plate can be removed without pulling the bevel gear from P0;
- torque is carried by metal faces, not a clamp screw;
- no elastomer spider in the sealed gear bay.

A keyed sleeve is an acceptable fallback if it proves simpler to machine and service.

## Strength sanity check
At the current controlled side-torque target ~3.38 N*m:
- a solid Ø10 torsion section is only about 17.2 MPa nominal torsional shear;
- Ø12 is about 9.9 MPa.

Therefore the design is not shaft-strength limited at the current prototype torque. Gear tooth contact, coupling face pressure, bearing alignment and sealing are the controlling gates.

## Axial control
Use shoulders + circlips/retaining rings where possible. The bevel mesh must not set axial position by itself.

Target axial float after assembly: 0.05–0.15 mm at the transfer shaft, then adjust bevel contact with defined shims if required.

## Pressure-zone rule
The 18x30x7 seal is the dynamic boundary between P0 and P1/P2.
All three zones are normally filled to nearly equal +0.20..+0.30 bar, so this seal normally sees very small differential pressure. It remains a secondary flood barrier if a side bay loses pressure.

## Release gates
- actual KHK gear received and hub measured;
- transfer shaft drawing with all shoulders/radii finalized;
- 61800 seat and seal bore coupon checked;
- coupling prototype survives repeated 3.5 N*m reversals without fretting;
- bevel contact pattern checked after 20 remove/refit cycles of side drive;
- P0 remains pressure-tight with P1 intentionally vented;
- final machining drawing only after these checks.