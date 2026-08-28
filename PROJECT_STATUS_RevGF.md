# PX-1 Rev.GF — wheel-station packaging correction

Status: PROTOTYPE ENGINEERING BASELINE; not machining release.

## What changed from Rev.GE
The detailed wheel-station pass found an axial packaging conflict that was hidden by the previous envelope model. A 61801 (12x21x5) plus a Z50 B4 gear cannot share the 8 mm P1/P2 side bay with real assembly clearance.

A shallow Ø~53 mm gear recess into the 5 mm side cover was modelled and rejected because it compromises the large side-cover O-ring sealing land. Rev.GF therefore preserves the full side-cover sealing plane and changes only the compact inboard support.

## Active Rev.GF wheel station
- inner support: 6701-2RS, 12x18x4;
- gear: m1 Z50, 3.75 mm finished face, entirely inside P1/P2;
- next support: 61801-2RS, 12x21x5;
- main outboard support: 61903-2RS, 17x30x7;
- dynamic seal: X-ring 18.72x2.62 on Ø19 polished land;
- axle-flange static seal architecture: O-ring 32x1.5;
- wheel seat: Ø17 with 4x4x7 key;
- wheel retention: one recessed M8 low-head screw;
- full Ø90-class rolling radius remains on the inboard tread, with the wheel tapering outward for DN150 clearance.

The inboard 6701 is a deliberate PX-1 substitution. It preserves the source-inspired three-support concept while fitting the independent dry side bay without cutting the pressure/seal plane.

## Validation completed
Local CadQuery 2.8.0 validation passed:
- solids valid;
- no gear/support or gear/cover collision;
- no wheel/flange or wheel/cover collision;
- P0/P1 pressure membrane remains intact;
- fixed hardware remains inside ideal DN150;
- tapered tread profile remains inside ideal DN150 with ~0.12 mm minimum analytical margin at the near-contact zone;
- keyways do not cross the X-ring land;
- full 5 mm side-cover thickness is retained at the wheel station.

Screening at 4 N*m wheel torque gives low shaft/key stresses (wheel-key shear ~16.8 MPa, gear-key shear ~23.8 MPa, Ø12 shaft torsional shear ~11.8 MPa).

## Documentation correction
`PROJECT_STATUS_RevGE.md` referenced `mechanical/cadquery/PX1_FullCrawler_RevGD.py`, but that file is not present on the current main branch. Rev.GF does not treat that missing file as an executable release artifact. The verified Group-B Rev.GC CAD and the new Rev.GF wheel-station work are the current reproducible basis.

## Current HOLD items
- exact purchased 6701/61801/61903 bearing brands and fits;
- exact X-ring compound and gland dimensions from purchased seal data;
- integrated six-station side-cover/body CAD using the Rev.GF stack;
- real X200 bevel-output section and motor sample dimensions;
- physical DN150 sweep and pressure/immersion testing.

## Next autonomous work
1. mirror Rev.GF station to all six wheel positions;
2. integrate it into the full 286x80x5 side covers without disturbing the 190x1.5 cover seal;
3. build the real X200 bevel-output section and verify its bearings/seals against the Ø32 motor geometry;
4. then regenerate the full crawler STEP and run complete ideal-DN150 collision checks.