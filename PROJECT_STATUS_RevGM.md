# PX-1 Rev.GM — independent pressure / rear-tether structural screen

Status: PRE-FEA STRUCTURAL SCREEN PASSED; not machining release.

## Purpose
Rev.GL closed the integrated DN150/drivetrain geometry. Rev.GM independently screens the current wall/cover thicknesses before spending time on a full 3D FEM model.

The calculation is intentionally separate from CadQuery geometry checks. It uses a Navier simply-supported rectangular-plate series and elementary rectangular-tube axial/bending calculations. A 3x stress/deflection multiplier is applied to the plate results as a coarse pre-FEA allowance for edge condition, holes and local geometry.

This is NOT a substitute for FreeCAD/CalculiX 3D FEA.

## Pressure cases
Worst preliminary differential used: 0.060 MPa = 0.60 bar.

This covers the important reverse-pressure direction: approximately 10 m external water pressure while the crawler retains about +0.4 bar internal positive pressure, as well as one-zone pressure-loss fault cases.

## Current plate results
All values below include the 3x screening multiplier where stated.

### P0 top cover
Effective clear span 144 x 60 mm, thickness 5 mm:
- calculated center deflection ~0.0109 mm;
- calculated center von Mises screen ~5.03 MPa;
- 3x stress screen ~15.1 MPa;
- 3x deflection screen ~0.033 mm.

### P0/P1 or P0/P2 4 mm pressure membrane
Deliberately pessimistic full-bay span 286 x 80 mm, ignoring the local wheel/idler bosses that stiffen the real wall:
- center deflection ~0.0753 mm;
- center von Mises screen ~15.48 MPa;
- 3x stress screen ~46.44 MPa;
- 3x deflection screen ~0.226 mm.

This is the highest plate result and is the first area to inspect in 3D FEA.

### P0 floor
291 x 68 mm effective screen, thickness 6 mm:
- 3x stress screen ~15.16 MPa;
- 3x deflection screen ~0.036 mm.

### P0 sidewall
291 x 71 mm screen, thickness 4 mm:
- 3x stress screen ~37.1 MPa;
- 3x deflection screen ~0.142 mm.

### P1/P2 side cover local panel
54 x 70 mm, thickness 5 mm:
- 3x stress screen ~7.95 MPa;
- 3x deflection screen ~0.012 mm.

### Rear pressure extension wall
68 x 33 mm, thickness 4 mm:
- 3x stress screen ~6.62 MPa;
- 3x deflection screen ~0.0053 mm.

## Pressure resultants
At 0.60 bar differential:
- top 144 x 60 clear span: ~518 N total pressure force;
- one full 286 x 80 side-bay projected area: ~1.37 kN;
- rear 68 x 36 cavity end area: ~147 N.

These values are small relative to the intended fastener/structural system but bolt preload, local bearing and O-ring compression are still separate release checks.

## Rear tether structural screen
Current rear pressure extension section is approximated as a 76 x 44 mm outer / 68 x 36 mm inner rectangular tube:
- metal area ~896 mm2;
- section modulus ~12,505 mm3.

Results:
- 2 kN centered pull: ~2.23 MPa axial;
- 2 kN pull at 30 mm offset: ~7.03 MPa combined;
- 2 kN pull at 50 mm offset: ~10.23 MPa combined;
- deliberately abusive 5 kN pull at 30 mm offset: ~17.58 MPa combined.

Therefore the gross rear tunnel section is not the likely tether-load weakness. The release-critical locations are the real strength-member anchor, its fasteners/contact, and the filleted transition from the narrow rear extension into the main body.

## Decision
Do not thicken the whole body at this stage.

The current 4/5/6 mm wall architecture passes the pre-FEA screen with useful margin. Global thickening would increase mass and hurt DN150 packaging without evidence that it is required.

## Next FEA priorities
1. P0/P1 and P0/P2 4 mm membranes around X200 cartridge seat and wheel/idler bosses;
2. top-opening corners and cover fastener regions;
3. transition at X299 from 92 mm full-width body to 76 x 44 rear motor extension;
4. rear tether anchor under 2 kN proof load plus off-axis moment;
5. X200 cartridge-seat local stress under bevel/gear reactions;
6. repeat complete DN150 validation after any fillet/rib changes.

## Release gates
- true 3D FreeCAD/CalculiX FEA;
- exact aluminium alloy/temper and allowable stress;
- realistic bolt preload/contact and local notch geometry;
- purchased seal/bearing fits;
- hydrostatic/pressure-cycle testing;
- 2 kN-class tether proof test on the built rear anchor.
