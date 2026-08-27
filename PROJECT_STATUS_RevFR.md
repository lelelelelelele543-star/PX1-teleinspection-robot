# PX-1 Rev.FR — project status after lift/camera/tail production pass

Status: PROTOTYPE ENGINEERING BASELINE, not machining/serial release.

## Newly completed in Rev.FM–FQ
- true four-bar manual camera lift instead of the earlier single-link envelope;
- 150 N gas-spring balance geometry calculated across LOW/MID/HIGH;
- mechanical DN150 stop policy tied to real hardware;
- executable CadQuery lift/camera/yoke model `mechanical/cadquery/PX1_LiftCamera_RevFN.py`;
- executed numeric validation for lift positions, gas-spring length/torque and DN150 camera sweep;
- camera yoke/front-window/internal-ROLL service architecture aligned with lessons from uploaded CAM026 documentation;
- layered rugged tether termination aligned with uploaded Proteus cable-end documentation;
- complete DN150 clearance policy including fasteners, lift pivots, yoke and cable loop.

## Current lift geometry
- body pivot X = 200 mm;
- body pivots Z = 92 / 112 mm;
- link length = 120 mm;
- camera-side pivot spacing = 20 mm;
- LOW camera axis X≈83.557 / Z75;
- MID axis X≈82.851 / Z130;
- HIGH axis X≈135.200 / Z205.

## Gas spring baseline
- one 150 N spring first prototype;
- fixed pin X220/Z35;
- moving pin 80 mm from lower lift pivot;
- geometric center-distance range ~104.6…139.5 mm;
- required stroke ~34.8 mm;
- assist torque drops from ~6.9 N*m LOW to ~1.2 N*m HIGH;
- M8 clamp remains the actual holding device.

## Current DN150 numeric hard points
- camera full TILT at LOW: ~7.64 mm ideal minimum;
- upper lift-pivot envelope: ~7.51 mm nominal;
- side-cover lower region: ~5.6 mm ideal and remains the current hard point.

Therefore all lower side-cover hardware must remain flush/recessed.

## Camera baseline
- fixed outer shell target Ø52 x 72 mm;
- whole shell TILT -105..+105 deg;
- internal camera cartridge continuous ROLL 360 deg;
- replaceable mechanically retained front window;
- separate LED light ring;
- two-bearing internal ROLL cartridge;
- digital rotary transfer non-structural;
- complete head removable without opening P0.

## Tail baseline
- rugged PUR/TPU robotic tether, not Ethernet patch cable;
- 48 V power + balanced digital pair(s);
- separate aramid/UHMWPE tensile member;
- layered jacket/gland/boot/sleeve termination;
- structural tensile anchor independent from electrical connector;
- field-retermination required.

## Frozen drivetrain baseline carried forward
- six Ø90-class profiled wheels;
- three per side, pitch 100 mm;
- five equal m1 Z50 gears per side;
- X200 bevel input, 2.5:1 candidate;
- source-aligned 61801/61903 wheel support philosophy;
- X-ring dynamic wheel sealing baseline;
- 61800 + 18x30x7 central bevel-output boundary;
- P0/P1/P2 independent positive-pressure zones.

## Next production work
1. merge Rev.FN lift/yoke solids into the Rev.FC/FF drivetrain body master;
2. replace camera shell envelope with real front retainer, rear closure, bearing seats and internal cartridge solid;
3. model the complete top-cover O-ring path and screw coordinates;
4. model the rear connector adapter + tensile anchor + pressure-fill boss as machinable solids;
5. run one combined DN150 collision script including side covers, screws, yoke, lift and tail;
6. derive prototype 2D drawings for wheel shaft, wheel flange, X200 output shaft, lift arm and camera front retainer;
7. freeze exact purchased bearings/seals/gears/motors/camera/rotary transfer before tolerance release.

## Physical gates still mandatory
- actual JGB37-555 sample dimensions/current/RPM/torque;
- KHK bevel contact-pattern setup;
- exact wheel X-ring and static O-rings;
- exact camera PCB/lens/rotary-transfer parts;
- exact rugged tether and connector;
- DN150 physical tube sweep;
- P0/P1/P2 pressure tests with wheel shafts rotating;
- 1 kN-class tether pull qualification;
- camera thermal and tilt/roll endurance tests.