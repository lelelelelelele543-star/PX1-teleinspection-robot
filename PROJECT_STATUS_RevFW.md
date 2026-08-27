# PX-1 Rev.FW — integrated project status

Status: PROTOTYPE ENGINEERING BASELINE. Not machining/serial release.

## Major result of Rev.FS–FV
The previously separate drive, lift, camera and tail models have now been merged into one executable integrated CadQuery master:
`mechanical/cadquery/PX1_FullCrawler_RevFS.py`

The script executed successfully in CadQuery 2.8.0 and generated the complete crawler STEP plus separate major machining candidates.

## Current integrated architecture
- CRP150-inspired six-wheel crawler with own PX-1 geometry;
- body length 307 mm class;
- 6 x Ø90-class profiled wheels;
- wheel centers X50/X150/X250, pitch 100 mm;
- five equal m1 Z50 gears per side;
- X200 bevel traction input, 2.5:1 candidate;
- paired JGB37-555 traction motors aft of folded camera zone;
- P0 central body + P1/P2 side-drive pressure zones;
- side covers 286 x 86 x 5 mm;
- source-aligned 61801/61903 wheel support philosophy and wheel X-ring sealing baseline;
- 61800 + 18x30x7 central output boundary;
- true four-bar manual lift, 120 mm arms;
- LOW camera axis X83.557 / Z75;
- digital Ø52x72 camera target, TILT ±105°, internal continuous ROLL;
- structural tether anchor independent from electrical connector;
- rugged PUR/TPU tether with separate strength member, 48 V and balanced digital data pair(s).

## DN150 integrated result
In the current ideal solid model:
- body, covers, flanges, lift arms and yoke are fully contained inside the ideal DN150 cylindrical envelope;
- camera shell remains contained through sampled TILT -105..+105 deg;
- modeled wheel crown protrusion beyond the ideal air-cylinder is about 1.89 mm^3 per wheel, representing nominal traction contact;
- lower side-cover corner is now the smallest calculated hard clearance at about 3.55 mm;
- upper lift hardware remains about 7.51 mm nominal clearance.

Therefore flush/recessed lower side-cover fasteners are mandatory.

## Manufacturing definition added
- Rev.FT datum/tolerance candidate table;
- Rev.FU integrated prototype mechanical BOM;
- Rev.FV ordered drawing-release queue.

The first critical drawings will cover wheel shaft, axle flange, side cover, X200 output shaft/boss and supported pinion shaft before body/camera cosmetic details.

## Physical/procurement gates still open
1. exact JGB37-555 sample dimensions/current/RPM/torque;
2. exact KHK bevel pair sample/contact pattern;
3. exact wheel X-ring and static O-rings;
4. final traction driver;
5. camera PCB/lens mechanical drawing/sample;
6. Ethernet/data-capable rotary transfer sample;
7. exact rugged tether and qualified rear connector;
8. actual gas spring article and end fittings;
9. complete screw-head/cable-loop DN150 physical sweep;
10. P0/P1/P2 leak/pressure tests with rotating wheel shafts;
11. 1 kN-class tether pull test;
12. thermal and camera endurance tests.

## Immediate engineering direction
Proceed from integrated CAD to the first real prototype manufacturing drawings and inspection dimensions. Do not freeze any purchased-part interface from a marketplace image or generic family name.