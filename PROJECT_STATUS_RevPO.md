# PX-1 PROJECT STATUS — Rev.PO

Date: 2026-09-01
Status: ACTIVE SYSTEM ARCHITECTURE BASELINE

## Purpose
Rev.PO converts the CRP-150 / RMP / CCU reverse-engineering results into the baseline architecture for the buildable PX-1 system.

PX-1 is not a literal clone of Mini-Cam electronics. It preserves the proven Proteus system topology and mechanical logic while replacing proprietary electronics with serviceable, commercially available modules.

## 1. System architecture frozen for PX-1

```text
230 VAC / external power
        |
        v
PX1 CONTROL UNIT (CCU)
        |
        |-- operator controls / 7 in monitor / OSD
        |-- crawler master controller
        |-- hardwired emergency stop
        |-- HV enable + current/voltage monitoring
        |-- 24 V -> HV tether supply
        |
        v
PX1 MANUAL REEL
        |
        |-- manual crank
        |-- mechanical brake
        |-- mechanical level-wind
        |-- measuring wheel + A/B encoder
        |-- serviceable slip ring
        |
        v
6-core reinforced copper inspection tether
        |
        v
PX1 CRAWLER
        |
        |-- HV input protection
        |-- HV -> 24 V main DC/DC
        |-- 24 V traction bus
        |-- 12/5/3.3 V auxiliary rails as required
        |-- crawler MCU
        |-- LEFT traction driver
        |-- RIGHT traction driver
        |-- pressure / voltage / current / IMU
        |-- balanced video interface
        |-- camera network interface
        |
        v
CAM026-inspired sealed PAN/ROTATE camera
```

## 2. Power philosophy

The original Proteus architecture is now treated as the correct system-level reference:

- high-voltage DC is generated in the control unit, not on the reel;
- the reel passes and supervises power but is not the main traction power converter;
- the long tether transports power at substantially higher voltage than the crawler motor bus;
- the crawler converts tether power locally to approximately 24 V-class internal power;
- dangerous tether power is normally OFF until the system is valid and explicitly enabled;
- emergency stop removes tether HV in hardware.

Original CRP-150 reference evidence indicates approximately 120 VDC nominal crawler supply and approximately 100 W crawler power. PX-1 therefore adopts a 100-120 VDC design class as the target for the long-tether architecture.

### Prototype release rule
The actual selected CCU boost module and crawler HV->24 V module must be commercially available, enclosed or safely mountable, current-limited, thermally adequate and service-replaceable. No custom multilayer power PCB is required for the prototype.

A lower-voltage bench supply may be used during subsystem testing, but the released tether architecture must remain compatible with the 100-120 VDC class required for 100-150 m operation.

## 3. Six-core tether allocation

Baseline electrical allocation:

1. HV+
2. HV return
3. differential control/data A
4. differential control/data B
5. differential analog video +
6. differential analog video -

Rules:
- no coax in the main tether;
- no optical fiber;
- no bundle of unrelated loose twisted-pair cables;
- use one professional reinforced six-core inspection cable;
- aramid/Kevlar tensile path must terminate mechanically and must not load electrical contacts;
- field retermination remains mandatory.

Initial cable length: 40 m.
System architecture must scale to 100-150 m after conductor resistance and loss are confirmed on the selected cable.

## 4. Crawler mechanics — preserve Proteus

Source architecture remains the master mechanical reference.

Per side:
- 3 wheel stations;
- 2 idlers;
- 5 equal Z50 module-1 spur gears;
- adjacent gear centers 50 mm;
- wheel centers 100 mm;
- front-to-rear wheelbase 200 mm;
- rear wheel long axle is the drive input.

Crawler total:
- 2 traction motors, one per side;
- Z16 -> Z40 straight-bevel reduction, 2.5:1;
- manual camera lift integrated into the main housing;
- 150 N lift gas spring;
- M8 clamp architecture;
- sealed dry main body;
- conventional serviceable shafts, bearings, covers and seals; no cartridge/cassette mechanical modules.

Historical CAD that conflicts with the confirmed rear-input/module-1 geometry remains rejected and must not be released for machining.

## 5. Traction drive baseline

The original CRP-150 uses one geared motor per side and a local three-phase BLDC power stage. PX-1 preserves the one-motor-per-side mechanical architecture but does not require proprietary FAULHABER electronics.

Prototype baseline:
- 24 V-class motor bus;
- two traction channels;
- one available geared motor per side;
- driver modules individually replaceable;
- current sensing per side;
- firmware current limit;
- hardware fuse for each traction branch.

Existing JGB37-520 family remains a packaging candidate, not a released motor. Exact ratio is selected only after bench torque/speed/current testing against the reconstructed total drive ratio and wheel size.

The original 66:1 gearhead and Z16:Z40 pair are retained as the performance reference, not as mandatory purchased parts.

## 6. Crawler controller

Baseline main controller remains STM32 NUCLEO-F446RE or a functionally equivalent serviceable STM32 module.

Responsibilities:
- command reception over differential bus;
- left/right traction command;
- pressure sensing;
- crawler voltage/current/temperature monitoring;
- IMU;
- camera-node command routing;
- fault handling;
- heartbeat to CCU;
- telemetry to OSD.

The prototype does not reproduce the multiple proprietary HCS08 processors of the original CRP-150 unless there is a demonstrated reliability need. Distributed intelligence is retained only where it simplifies the camera or a motor controller module.

## 7. Camera architecture

Preserve CAM026 mechanical/function principle:
- separately sealed camera module;
- continuous ROTATE target;
- PAN target approximately +/-135 degrees;
- useful image at low lift position;
- white LED illumination;
- fixed-focus modern imaging module where practical.

Electrical architecture:
- small camera controller located in/near the camera assembly;
- PAN/ROTATE motor driver modules local to the camera subsystem;
- one local network/control interface between crawler and camera node;
- do not route every individual camera control wire back to the crawler MCU;
- video leaves the camera as CVBS-compatible analog video and is converted to a balanced differential pair for the tether;
- camera slip-ring circuit count is selected from the actual final camera wiring, with six-way Proteus logic as the reference.

## 8. Reel architecture

Preserve RMP300 principles:
- manual drum;
- hand crank;
- mechanical brake;
- mechanical level-wind;
- measuring roller;
- A/B quadrature encoder for direction and distance;
- slip ring in the main shaft path.

PX-1 simplification:
- no proprietary reel PCB is required;
- distance A/B may terminate directly at the CCU controller or at a small replaceable reel interface module;
- reel electronics must not be responsible for the main 100 W-class HV conversion;
- HV power simply passes through appropriately rated wiring, connector and slip-ring circuits;
- optional reel status/interlock is permitted, but must fail safe.

## 9. Control unit architecture

The PX-1 CCU is the master and contains:
- fused AC input or external DC input as selected;
- 24 V internal control bus;
- 7 inch video monitor;
- joystick;
- momentary control buttons;
- speed/light controls;
- crawler master MCU;
- balanced-video receiver -> CVBS monitor path;
- distance counter input from reel;
- OSD generator;
- tether HV supply module;
- contactor/relay or equivalent hardware HV disconnect;
- precharge/discharge where required by the selected HV module;
- E-stop that removes HV independent of software.

HV enable state machine:
1. CCU logic ON, HV OFF.
2. Reel/interface valid.
3. Crawler communication heartbeat valid or approved detection sequence valid.
4. Operator explicitly enables crawler power.
5. HV contactor/enable closes.
6. CCU supervises tether current and crawler heartbeat.
7. Any E-stop, connector loss, overcurrent or lost heartbeat -> HV OFF.

## 10. Video and data

Control/data baseline: RS-485 for the prototype.

Video baseline:
- CVBS-class camera;
- differential/balanced analog line driver at crawler/camera side;
- two tether conductors for video;
- differential/balanced receiver in CCU;
- no coaxial conductor in the main tether.

This deliberately copies the Proteus system principle of separating power, control and video functions while keeping the physical cable to six reinforced copper conductors.

## 11. Pressure and sealing

Crawler main body:
- dry internal volume;
- serviceable pressurization port;
- internal pressure sensor;
- pressure telemetry displayed at CCU;
- dynamic shaft seals on output shafts;
- replaceable static O-rings on covers/flanges;
- no external hinge into the dry pressure volume.

Camera remains separately sealed so a camera service event does not open the traction-electronics pressure volume.

## 12. Development order from Rev.PO

1. Rebuild the crawler mechanical master CAD with the audited module-1/rear-input architecture.
2. Freeze wheel diameter and required crawler ground-speed range.
3. Bench-test candidate 24 V traction motors and choose the exact ratio.
4. Freeze Z16/Z40 geometry and motor adapter.
5. Freeze main body, seals, bearings and integrated lift pivots.
6. Build one complete side-drive prototype before releasing the second side.
7. Build crawler low-voltage bench electronics at 24 V first.
8. Build and test camera PAN/ROTATE node and balanced CVBS link.
9. Build manual reel, encoder and slip-ring path.
10. Select and bench-test CCU HV source and crawler HV->24 V converter using dummy loads before connecting the crawler.
11. Integrate 40 m tether.
12. Only after the 40 m system passes thermal/current/fault tests, validate 100-150 m operation.

## 13. Immediate engineering freeze

Frozen now:
- Proteus-derived six-wheel mechanical layout;
- one motor per side;
- rear long-axle side-drive input;
- module-1 five-Z50 train;
- Z16/Z40 2.5:1 bevel concept;
- manual 150 N lift;
- six-core reinforced copper tether;
- high-voltage tether / local 24 V crawler power principle;
- separate differential data and differential analog-video pairs;
- CCU-side hardware HV disconnect;
- manual reel with level-wind and A/B meter encoder;
- separately sealed PAN/ROTATE camera.

Not frozen yet:
- exact traction motor and gear ratio;
- exact tether cable conductor size;
- exact HV voltage within the 100-120 V class;
- exact CCU HV converter module;
- exact crawler HV->24 V converter module;
- exact slip ring;
- exact camera module and PAN/ROTATE motors;
- final connector family;
- released machining dimensions of the crawler housing and bevel pair.

Rev.PO is the system architecture baseline for all following PX-1 work.
