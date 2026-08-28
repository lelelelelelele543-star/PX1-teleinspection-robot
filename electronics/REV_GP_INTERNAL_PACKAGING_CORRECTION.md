# PX-1 Rev.GP — current internal packaging correction

Status: active packaging baseline; supersedes the obsolete longitudinal zoning in Rev.EP where traction motors were assumed in the center of P0.

## Why correction was required
Current Rev.GJ/GL drivetrain places the two traction motors at the rear:
- Ø32 mm motor envelope;
- length 92 mm;
- axes Y=+/-16.5 mm, Z=45 mm;
- X=237...329 mm;
- rear narrow pressure extension carries the last 30 mm of the motor envelopes.

The active main P0 cavity is approximately X=8...307, Y=+/-34 and Z=14...85 mm, with rear extension X=299...332, Y=+/-34, Z=27...63 mm.

Therefore the old Rev.EP statement that the NUCLEO could be placed arbitrarily/horizontally and that motors occupied X≈100...200 is no longer valid.

## Rev.GP validated envelope packing
Executable model: `mechanical/cadquery/PX1_Internal_Packaging_RevGP.py`.

The following bounding envelopes fit inside the active cavity with zero modeled intersection:

### Front integrated control tray X≈15...98
NUCLEO-F446RE:
- board footprint reference 82.5 x 70 mm;
- installed thickness/header reserve 22 mm;
- long dimension along X;
- board carried diagonally about the X axis at 45 degrees;
- resulting Y-Z projected envelope ~65 x 65 mm inside the 68 x 71 mm cavity.

This diagonal mounting is mandatory in the current envelope. A flat horizontal NUCLEO does not fit the 68 mm internal width.

The two remaining cross-section corner voids are reserved for:
- TB6612 PAN/TILT driver envelope 51 x 25 x 19 mm;
- compact data/PHY/pressure/service reserve 55 x 20 x 18 mm.

These three items should be treated as one removable front tray assembly rather than three independently trapped modules.

### Traction-driver zone X≈105...210
Two full-size prototype BTS7960 / IBT-2 envelopes are retained:
- each 50 x 43 x 50 mm in the chosen installed orientation;
- first X=105...155;
- second X=160...210;
- 5 mm axial gap between modules.

They require a metal carrier/heat-spreader. The envelope test does not prove thermal adequacy.

### Protection zone X≈212...234
Reserve ~22 x 60 x 22 mm for:
- 48 V input protection interface after rear feed;
- traction branch disconnect/current-sense/fuse elements as final parts permit.

There is approximately 3 mm axial envelope gap to the motor fronts at X237.

### Rear traction zone X≈237...329
Two Ø32 x 92 motors remain the dominant rear volume.

The 48→24 V half-brick envelope is placed above the motor fronts:
- X≈220...290;
- Y≈-32.5...+32.5;
- Z≈65...83;
- ~4 mm modeled vertical gap above the Ø32 motor envelope;
- only ~2 mm to the current inner roof, therefore the real thermal pad, tolerances and connector height must be measured before release.

The half-brick must conduct heat into the body/top thermal land and cannot rely on sealed-air cooling.

## Ballast-boss keep-outs
Rev.GP adds four blind ballast bosses at:
- X105, Y+/-18;
- X245, Y+/-18.

The bosses protrude only near the floor. Current checks give:
- ~7.5 mm axial gap from the front boss pair to the NUCLEO envelope;
- ~10 mm or more vertical clearance below the rear motor envelopes in the final boss concept.

All trays must include these boss keep-outs. Do not delete the bosses by drilling through P0 to simplify tray mounting.

## Harness routing rule after repack
Preferred separation remains:
- left/right traction power and motor leads low/central;
- camera/data link biased to the opposite side/corner of the front tray;
- data routing does not run parallel immediately beside BTS7960 motor outputs;
- DC/DC input/output wiring kept short in the rear/mid power zones;
- every removable tray has plug-in harness interfaces.

## Current release gates
1. measure the actual selected BTS7960 modules including heatsinks and terminals;
2. measure the actual half-brick plus mounting plate/connector height;
3. insert exact NUCLEO connector/header envelope, not PCB dimensions only;
4. add exact 10BASE-T1L PHY/interface module;
5. add real fuse/current-sensor/contact-disconnect parts;
6. model harness connector plug bodies and minimum bend radii;
7. prove front tray extraction with camera lift installed;
8. sealed 60 min thermal test at representative traction load.

## Decision
Current geometry demonstrates that the active controller, two prototype BTS7960 modules, rearward Ø32 motors and a compact half-brick can coexist in the current pressure envelope without enlarging the crawler. This is still an envelope proof, not an electronics release.
