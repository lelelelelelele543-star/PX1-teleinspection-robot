# PX-1 Rev.FD — project status after production-solid pass

Status: PROTOTYPE ENGINEERING, not machining/serial release.

## Newly completed in Rev.EY–FC
- detailed X200 bevel-stage architecture;
- explicit bearing/seal/coaxiality requirements for pinion and output shafts;
- static-seal and cover-fastener policy for P0/P1/P2;
- production-oriented digital camera-head shell architecture;
- structural rear bulkhead / tether anchor / connector adapter / pressure fill layout;
- new production-oriented FreeCAD source master `mechanical/freecad/PX1_Production_Master_RevFC.py`.

## Current mechanical baseline
- 6 x Ø90-class profiled wheels;
- wheel pitch 100 mm;
- five equal m1 Z50 gears per side;
- X200 bevel input, 2.5:1 candidate;
- paired JGB37 traction motor holder aft of the folded camera region;
- wheel stations with Ø12/Ø17 stepped shaft philosophy, 61801 inner and 61903 outer support;
- P0 central body, P1 left drive, P2 right drive independently sealed/pressurized;
- manual camera lift with DN150 mechanical low stop;
- Ø52 x 72 mm digital camera target, TILT ±105°, continuous ROLL;
- rugged non-Ethernet-patch tether with tensile member and 48 V + balanced digital pairs.

## Current machining-oriented body concept
- Al 6082 milled pressure body/tray;
- ~6 mm floor and side-wall class, local thick bosses;
- front upper recess for folded camera;
- top service opening behind camera recess;
- side covers 5 mm class with closed-loop FKM face seals;
- local removable wheel flanges;
- structural rear bosses independent from service/connector plate.

## Still blocked before drawing RELEASE
1. physical JGB37-555 sample dimensions/current/RPM/torque;
2. physical KHK gear pair and contact-pattern setup;
3. final traction driver module/implementation;
4. exact wheel-seal articles and molded cover O-rings;
5. exact camera PCB, lens and component heights;
6. exact Ethernet-capable rotary transfer sample;
7. exact rugged tether and qualified rear connector;
8. full FreeCAD execution/solid check of Rev.FC;
9. DN150 physical tube sweep with complete screws/yoke/cable loop;
10. pressure and rotating-shaft qualification.

## Next engineering work
- execute and repair Rev.FC CAD until all solids recompute;
- derive real 2D manufacturing drawings for wheel shaft, axle flange, X200 output shaft and side cover;
- freeze screw coordinates and O-ring paths from the actual solid;
- build full camera yoke and front window retainer solids;
- integrate rear connector adapter as soon as one actual connector is selected;
- generate prototype machining BOM and tolerance table.
