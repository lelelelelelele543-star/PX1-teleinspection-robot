# PX-1 Rev.EA — sealed side cover and fastener layout

Status: prototype detail candidate. Replaces the vague rectangular-plate description in Rev.DX.

## Architecture
Each side drive P1/P2 is closed by one rigid rectangular aluminum cover, visually and functionally close to the proven CRP150 side-drive architecture while retaining PX-1 dimensions.

Nominal current envelope:
- cover visible size: 276 x 81 mm;
- thickness: 5 mm Al 6082-T6;
- three removable axle flanges installed through/onto the cover/body interface;
- five internal Z50 gears remain behind the cover;
- no drain holes because P1/P2 are dry pressurized cavities.

## Main cover static seal
Preferred geometry is a machined closed-loop O-ring groove around the gear cavity, completely inside the perimeter screw line.

Important source correction: the MiniCam part-list notation `O-Ring 190 x 1.5` means approximately 190 mm nominal inside diameter with 1.5 mm cross-section, NOT a 190 mm developed groove length. Its free circumference is roughly 597 mm before stretch.

PX-1 candidate family:
- FKM molded O-ring approximately 190 mm ID class;
- cross-section 1.5–2.5 mm to be selected from the actual groove/cover stiffness calculation;
- one-piece molded ring preferred over field-joined cord.

Do not freeze the groove from a guessed cross-section. Build the actual racetrack/rounded-rectangle path first, calculate installed stretch and compression, then select a standard molded ring.

Initial static-seal design targets:
- radial/planar installed stretch kept within the selected O-ring manufacturer's static-face guidance;
- static face squeeze around 20–25% as a starting target only;
- groove fill preferably <85%;
- surface finish on sealing lands Ra <=1.6 um target;
- no tool marks crossing the seal line.

## Cover location
The cover must not be positioned by screw clearance holes alone.

Use:
- one machined perimeter pilot/step around the cavity where practical;
- two dowel pins Ø3 or Ø4 located away from the O-ring and away from gear/bearing service paths;
- screws clamp the cover against the static seal;
- cover must return to the same location after service so gear-side bearing supports and wheel-flange geometry do not shift.

## Fasteners
Baseline:
- M4 A4-80 stainless where wall thickness permits;
- target 14–16 perimeter screws, finalized from the real cavity contour;
- anti-galling assembly paste compatible with aluminum/stainless and FKM;
- threaded inserts or helicoils preferred if repeated service damages direct aluminum threads.

No cover screw is allowed inside the pressure-seal boundary unless specifically sealed.

### DN150 screw-head correction
The lower outside corner of the current side cover is one of the tightest DN150 locations. A protruding screw head near the bottom edge can consume several millimetres of clearance.

Therefore:
- lower perimeter screws must be flush/countersunk or positioned higher on the safe screw line;
- do not use tall socket-head screws at the lowest cover edge;
- all screw-head solids are included in the final DN150 sweep;
- aim for >=4 mm nominal clearance at every non-traction solid after tolerance allowance.

## Flatness and stiffness
Prototype machining targets:
- cover sealing-face flatness <=0.10 mm over full cover before assembly;
- parent sealing land flatness <=0.08 mm preferred;
- cover must not visibly dish between screws at normal +0.25 bar;
- structural qualification target remains >=1 bar differential with safe test method.

If FEA or hydrostatic coupon testing shows local cover flex near the long unsupported spans, add shallow external ribs or internal bosses without reducing DN150 clearance.

## Axle-flange interaction
The three axle flanges have their own local static seals. The main cover seal and each wheel-flange seal are independent.

This allows:
- main cover removal for gear service;
- single wheel-flange removal for seal/bearing service;
- pressure testing of each service interface separately.

The main cover must have enough radial clearance around each flange so cover removal does not drag across the flange O-ring or shaft-seal journal.

## Pressure monitoring
P1 and P2 remain separately sensed. After any side-cover service:
1. isolate P0 and the opposite side;
2. fill serviced side to +0.25 bar;
3. record pressure and temperature for 30–60 min;
4. soap/bubble check external static joints if practical;
5. perform submerged static test before powered rotation.

## Release gates
- build the actual cover-groove path length in CAD;
- select a real standard molded FKM O-ring with acceptable installed stretch;
- groove coupon passes repeated assembly test;
- 20 cover open/close cycles without thread or sealing-land damage;
- 1 bar differential structural qualification on empty side bay;
- DN150 solid check includes all screw heads and flange protrusions;
- final drawing released only after real cover is pressure tested.
