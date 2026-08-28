# PX-1 Rev.PB — Proteus replacement mechanical reset

Status: ACTIVE MASTER BASELINE; not machining release.

## What is now corrected
PX-1 has been reset from the experimental custom-crawler branch to a CRP-150 replacement architecture.

The active side-drive reconstruction now follows the uploaded CRP-150 source assemblies:
- five Z50 B4 gears per side;
- three axle gears and two idlers;
- three wheel stations;
- one long wheel axle per side;
- one 61801 support and three 61903 wheel supports per side;
- three 18.72x2.62 X-rings per side;
- three 32x1.5 flange O-rings per side;
- one 190x1.5 side-cover O-ring per side;
- two motors total;
- Z16 -> Z40 bevel handoff.

The previous PX-1 separate fourth-gear/X200 input concept is superseded.
The long axle is reconstructed at the rear/end wheel gear, so the rear Z50 is both a wheel gear and the drivetrain input.

Gear direction from rear input:
- rear wheel Z50: +
- rear idler: -
- middle wheel Z50: +
- front idler: -
- front wheel Z50: +

All three wheels therefore rotate in the same direction.

## CAD
New active sources:
- `mechanical/cadquery/PX1_ProteusSideDrive_RevPA.py`
- `mechanical/cadquery/PX1_ProteusCrawler_RevPB.py`

Rev.PB full crawler skeleton:
- target external reference: CRP-150 307 x 133 x 110 mm;
- current mechanical skeleton bounding box: about 307 x 133 x 101 mm before final lift/camera hardware;
- six Ø90-class wheel envelopes;
- 10 side Z50 gears total;
- rear-wheel long input axle each side;
- two internal Z40 bevel envelopes;
- two compact traction-motor envelopes;
- no custom top controller pod;
- no separate fourth input shaft.

Fixed body/cover parts pass the ideal DN150 geometry screen. Wheel tread is intentionally at the pipe-contact boundary and will be seated using the final physical tyre profile.

## Camera reset
The new camera target is CAM026-like rather than the experimental compact Ø52 camera.

Published CAM026 reference target:
- about 120 x 73 x 73 mm;
- continuous 360-degree rotation;
- +/-135-degree pan;
- 75-degree FOV class;
- pressurised construction.

Keep the source mechanical layout and external appearance; replace proprietary electronics, focus system and control boards with simple current components.

## Electronics reset
Active document:
`electronics/PROTEUS_SIMPLE_REPLACEMENT_ARCHITECTURE.md`

Key rule: mechanically similar to Proteus, electronically much simpler.
The crawler prototype uses replaceable ready-made controller/H-bridge/RS485/video/power modules; the camera has minimum internal electronics; the RMP300-like reel is nearly passive.

## Source reference values now used as controls
CRP-150 published crawler reference:
- 307 x 133 x 110 mm;
- 9.25 kg;
- DN150-class entry;
- manual elevator;
- 150 W published power-consumption class;
- 0...500 mbar internal pressure range.

## Next autonomous block
1. rebuild the manual lift using DRW-002-744 components and 150 N gas spring rather than the experimental indexed lift;
2. reconstruct the CAM026 side-frame / pan worm / rotate bearing architecture from ASS-001-801/802/803;
3. keep the LOW camera sightline open exactly as required by the user;
4. then reconstruct RMP300 reel geometry from ASS-004-097 and its subassemblies;
5. only after those real source-based assemblies exist, replace the outdated viewer with a Proteus-replacement viewer.