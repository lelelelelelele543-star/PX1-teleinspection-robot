# PX-1 Rev.CS — side gearbox for gear-only 4WD

Status: engineering candidate, not machining RELEASE.

## Architecture
One motor per side. The JGB37-520 drives the rear axle gear. Front and rear wheels on the same side are mechanically linked by an enclosed spur-gear train. No belts or chains.

Required property: front and rear wheel on one side must rotate in the same direction. Therefore the number of external gear meshes between rear and front axle gears must be even.

## First geometry candidate
- pressure angle: 20°;
- module: m = 1.0;
- rear axle gear: z40;
- front axle gear: z40;
- intermediate gears: candidate z30, quantity chosen from actual wheelbase;
- axle ratio rear:front = 1:1;
- face width target: 8–10 mm;
- prototype gear material: POM-C or PA6G for idlers, steel/aluminium hub where needed;
- final material remains HOLD after contamination and wear testing.

At m1.0:
- z40 pitch diameter = 40 mm, OD ≈42 mm;
- z30 pitch diameter = 30 mm, OD ≈32 mm;
- z40/z30 center distance = 35 mm;
- z30/z30 center distance = 30 mm.

Example only: rear z40 -> 3x z30 idlers -> front z40 gives 4 meshes, same axle rotation direction, and nominal axle spacing 35+30+30+35 = 130 mm. This is NOT frozen; exact idler count and tooth counts must be solved from final crawler wheelbase.

## Motor input
Do not cantilever a large wheel gear directly on the JGB37 output shaft. Preferred serviceable layout:
1. JGB37 motor pinion / coupling drives rear axle gear or a short supported input stage;
2. rear wheel axle is supported by its own bearings in the side gearbox;
3. gearbox loads are carried by the chassis, not by the motor gearbox output bearing alone.

Exact motor-to-rear-axle gearing remains HOLD until motor shaft dimensions and required wheel torque are measured.

## Idler support
Each idler runs on a replaceable shoulder bolt or hardened pin with replaceable bushing/bearing. Idler pins must be accessible after removing one outer side cover. No press-fit pin that requires stripping the whole crawler.

## Dirt/water protection
The spur train sits inside a closed side cassette. Outer cover uses a perimeter gasket/O-ring and captive screws. This is a splash/dirt barrier, not the main crawler pressure boundary. If water enters the cassette, it must not enter the dry electronics body.

Add a small drain/inspection feature at the lowest point of the cassette unless later pressure testing shows a fully sealed oil/grease-filled cassette is preferable.

## Lubrication
Prototype: compatible water-resistant grease applied sparingly. Avoid exposed sticky grease that traps abrasive grit. Material/lubricant pair must be validated after muddy-water cycling.

## Service target
A field technician with hex keys, spanners and a small puller should be able to:
- remove a wheel;
- remove the side cover;
- replace one idler gear or bearing;
- replace the motor;
- reassemble without opening the main pressure body.

Target side-cassette service time: <=30 min after cleaning.

## Release gates
- exact wheelbase;
- exact rear/front axle positions;
- measured JGB37 shaft geometry;
- measured motor torque/current;
- gear tooth root strength and wear check;
- backlash and shaft tolerance stack;
- mud/sand/water endurance test;
- full DN150 external-envelope check.
