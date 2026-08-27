# PX-1 Rev.GC — Group B pressure structure

Status: CAD-validated prototype candidate; not machining release.

## Source-aligned architecture
The uploaded CRP150 documentation shows a dedicated side-cover drive assembly using 61801/61903 bearings, X-rings and a large cover O-ring, while the crawler housing drawing shows separate bevel-output shaft seals and 61800 bearings. PX-1 therefore retains three pressure zones:
- P0 central electronics/motor cavity;
- P1 left side drive;
- P2 right side drive.

All three are filled from one service point but are isolated with check valves so a damaged wheel seal cannot immediately dump P0.

## Main body
- overall body datum envelope: 307 x 92 x 82 mm, Z=8..90;
- P0 internal width: 68 mm;
- side-wall thickness: 12 mm nominal;
- side-drive pocket depth: 8 mm;
- remaining P0/P1 and P0/P2 membrane: 4 mm nominal;
- floor: 6 mm class;
- top roof/land: 5 mm class;
- rear structural wall: 8 mm class;
- front roof recess retained for folded camera.

## Side bays
Left side bay: Y=38..46 mm.
Right side bay: Y=-46..-38 mm.

Five Z50 gears per side fit entirely in the bay at nominal gear-face center Y=+/-42 mm with 8 mm face width.

Revised side cover candidate:
- 286 x 80 x 5 mm;
- Z=6..86;
- outer Y=+/-51 mm;
- 12 x M3 cover fasteners;
- three axle-flange pilots;
- 190 x 1.5 source-size FKM O-ring-derived racetrack groove candidate.

The lower ideal DN150 corner clearance is ~6.29 mm in the current body position, improving the previous ~3.5 mm hard point.

## Side-cover seal calculation
For 1.5 mm cross-section and current candidate groove 1.9 mm wide x 1.2 mm deep:
- nominal face squeeze: 20%;
- approximate gland fill: 77.5%;
- centerline racetrack: ~264.204 x 60 mm.

Final groove follows the exact selected O-ring manufacturer standard/sample.

## Top service cover
- 158 x 74 x 5 mm;
- 14 x M4 clearance positions;
- two dowel candidates;
- 2.5 mm FKM custom/molded loop candidate;
- candidate groove 3.2 x 2.0 mm gives 20% squeeze and ~76.7% fill.

## Rear structure
- separate structural towing/recovery clevis tied to main body;
- replaceable 52 x 52 x 6 connector adapter;
- main body receives only a generic pilot + mounting interface;
- final connector cutout stays in the inexpensive replaceable adapter;
- separate pressure fill and pressure sensor/service bosses.

## CAD validation
`mechanical/cadquery/PX1_GroupB_RevGC.py` executes successfully in CadQuery 2.8.0.

Validation results:
- all Group-B solids valid;
- motor/body intersection: 0 mm^3 left and right;
- all Group-B non-wheel solids outside ideal DN150: 0 mm^3;
- current 32 mm motor package side clearance: 1.5 mm each side.

## Holds
- exact O-ring/X-ring suppliers;
- exact 32 mm motor;
- exact connector;
- pressure proof depth/pressure rating;
- FEA/local stress around 4 mm pressure membranes and X200 cartridge seats;
- physical pressure cycling.
