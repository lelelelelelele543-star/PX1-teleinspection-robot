# PX-1 Rev.FL — project status after source-locked drivetrain detail pass

Status: PROTOTYPE ENGINEERING, not machining/serial release.

## Major progress Rev.FE–FK
- side-drive bearing/seal architecture re-aligned directly to uploaded CRP150 `DRW-002-374`;
- source-size X-ring 18.72x2.62, axle-flange O-ring 32x1.5 and side-cover O-ring 190x1.5 adopted as the preferred prototype seal families;
- side-cover fastener logic corrected to compact CRP-like M3 service hardware;
- wheel shaft corrected to include a dedicated ~Ø19 polished X-ring land in addition to Ø12 and Ø17 bearing/drive journals;
- side-cover candidate enlarged to 286x86x5 to create usable seal/screw margins without worsening the critical DN150 lower-corner clearance;
- executable CadQuery Rev.FF created and successfully run to generate side-cover, flange, wheel-shaft and side-drive STEP solids;
- manufacturing drawing data created for the wheel shaft and axle flange/side cover;
- X200 bevel input re-aligned to uploaded `DRW-002-386` / `DRW-002-375`: 61801-supported pinion shaft plus 61800 and 18x30x7 sealed output shaft;
- executable CadQuery Rev.FI created and successfully run for pinion shaft, output shaft and P0 seal/bearing boss;
- first mechanical prototype BOM created.

## Current source-aligned traction architecture
Per side:
JGB37-555 -> own supported pinion shaft -> KHK 18/45 bevel pair candidate -> sealed Ø10/Ø18/Ø12 output shaft -> service coupling -> five equal m1 Z50 side gears -> three wheel shafts.

Wheel station:
61801 -> Z50 -> 61801 -> Ø17/61903 -> Ø19 X-ring land -> labyrinth -> wheel hub.

The bearing and seal count now deliberately mirrors the successful CRP150 service philosophy while keeping PX-1 geometry and modern electronics.

## Current side-cover/service hardware
Per side:
- 1 x 286x86x5 Al side cover candidate;
- 1 x 190x1.5 FKM main O-ring candidate;
- 12 x M3 perimeter screws;
- 3 x removable axle flanges;
- 4 x M3 screws per flange;
- 1 x 32x1.5 FKM static O-ring per flange;
- 1 x 18.72x2.62 FKM X-ring per wheel shaft.

## Current CAD execution status
Successfully executed locally with CadQuery 2.8.0:
- `mechanical/cadquery/PX1_SideDrive_RevFF.py`;
- `mechanical/cadquery/PX1_X200_Bevel_RevFI.py`.

Generated STEP geometry passed basic solid creation/bounding-box checks.
The old FreeCAD Rev.FC master remains useful as an integration reference, but the new CadQuery parts are the first actually executed machining-oriented solids in the current pass.

## Important engineering corrections now frozen for prototype
- no 4-wheel layout: crawler is six-wheel CRP150-style;
- no exposed/unsealed gear cover: P1/P2 are sealed positive-pressure side bays;
- no generic lip seal at the wheel by default: source-like X-ring architecture is preferred;
- no motor-shaft-only bevel support: each pinion gets its own 61801 support;
- no huge external flange protrusion: most bearing support enters the side bay, leaving only about 3 mm external flange disk projection;
- lower side-cover screw heads must remain flush for DN150.

## Still blocked before machining RELEASE
1. actual FKM X-ring 18.72x2.62 supplier data and sample;
2. actual FKM O-rings 32x1.5 and 190x1.5 supplier data and samples;
3. physical bearing brands/tolerance verification;
4. one machined wheel-station first article and rotating pressure test;
5. actual KHK bevel pair and contact-pattern setup;
6. actual JGB37 motor sample measurements/current/torque/RPM;
7. complete integrated body solid regenerated around the corrected Rev.FF/Rev.FI geometry;
8. exact camera PCB/rotary-transfer samples;
9. exact tether and rear connector;
10. physical DN150 tube sweep with deposits/ovality margin.

## Immediate next engineering block
- replace the wheel/side-drive placeholders in the integrated crawler master with the executed Rev.FF solids;
- replace the X200 envelopes with Rev.FI shaft/boss geometry;
- regenerate the main three-zone pressure body around the corrected pilots/bosses;
- run a complete DN150 interference/tolerance sweep;
- then derive the first real A3-style manufacturing drawing candidates in the MiniCam-document style.