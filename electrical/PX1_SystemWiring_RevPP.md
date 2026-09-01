# PX-1 SYSTEM WIRING — Rev.PP

Date: 2026-09-01
Status: ACTIVE END-TO-END ELECTRICAL BASELINE
Supersedes `electrical/PX1_SystemWiring_RevPN.md` where tether voltage or system partition differs.

## 1. System partition

```text
AC / external supply
        |
        v
PX1 CCU
  24 V control bus
  operator controls
  video receiver / OSD / display
  RS-485 master
  HV source + hardware disconnect
        |
        v
PX1 MANUAL REEL
  HV pass-through
  RS-485 pass-through
  balanced-video pass-through
  distance A/B encoder
  serviceable slip ring
        |
        v
6-core reinforced copper tether
        |
        v
PX1 CRAWLER
  HV input protection
  HV -> 24 V isolated/non-isolated DC/DC as selected
  24 V traction bus
  STM32 controller
  LEFT/RIGHT traction channels
  sensors
  camera interface
        |
        v
CAM026-inspired camera node
```

## 2. Tether conductor assignment

The main tether has exactly six copper conductors:

| Core | Function |
|---|---|
| 1 | HV+ |
| 2 | HV return |
| 3 | RS485_A |
| 4 | RS485_B |
| 5 | VIDEO+ |
| 6 | VIDEO- |

No coaxial core, fibre or Ethernet cable is introduced into the main tether.

The tensile aramid/Kevlar member is terminated mechanically and is not an electrical current path.

## 3. CCU power architecture

Prototype control-power branch:

```text
mains/external supply
      |
      +--> 24 V regulated supply
               |
               +--> 7 in monitor
               +--> controller / OSD / RS-485 / video RX
               +--> camera/control auxiliaries as required
               +--> HV source input
```

Long-tether crawler-power branch:

```text
24 V source
   |
  F1
   |
E-STOP / K1 hardware safety chain
   |
HV converter, 100-120 VDC design class
   |
current sensing + output fuse
   |
reel/slip ring
   |
HV+ / HV return tether conductors
```

The exact commercial HV converter is OPEN until a serviceable unit is selected and bench-tested.

### Mandatory hardware safety
- E-STOP must remove the dangerous tether supply independently of firmware.
- An MCU output may request HV ON but may not override a broken hardware safety chain.
- HV output must discharge to a defined safe state after disable; discharge implementation depends on the selected converter capacitance.
- exposed service connectors are not to remain energized when disconnected.
- fault state defaults to HV OFF.

## 4. HV enable sequence

1. CCU logic powers at low voltage; tether HV remains OFF.
2. RS-485/reel/crawler detection logic starts using the approved detection arrangement.
3. Operator requests CRAWLER ENABLE.
4. Hardware safety chain must be healthy.
5. CCU closes K1/enables the HV source.
6. Crawler local power starts and sends a valid heartbeat/telemetry stream.
7. CCU supervises line current and heartbeat.
8. E-STOP, overcurrent, connector/reel fault or lost crawler heartbeat causes HV OFF.
9. Automatic restart after a safety trip is prohibited; deliberate re-enable is required.

The exact pre-power crawler-detection method is OPEN. It may use a safe low-energy detection voltage or a reel/interlock continuity path; it must not require the full tether HV to remain continuously energized merely to discover an unplugged crawler.

## 5. Manual reel wiring

The reel contains no 100 W-class converter.

It provides:
- rated HV wiring/pass-through;
- RS-485 pair pass-through;
- balanced-video pair pass-through;
- slip ring;
- measuring wheel encoder A/B;
- optional local status/interlock board.

Distance encoder A/B remains outside the six tether cores because it measures reel payout on the surface side. It may connect directly to the CCU controller through a short local harness.

A 12-circuit slip-ring class remains convenient because power circuits can be paralleled and spare rings retained. Exact slip ring remains OPEN pending voltage/current/contact-noise qualification.

## 6. Crawler HV input

Cable/tail sequence:

```text
jacket strain relief
 -> aramid structural termination
 -> relaxed six-core service loop
 -> sealed electrical bulkhead/connector
 -> input fuse
 -> surge/transient protection
 -> inrush control
 -> HV DC/DC
 -> local 24 V bus
```

The connector contacts never carry towing/recovery load.

### HV DC/DC target
Input design class: 100-120 VDC nominal system class.
Output: regulated 24 VDC.
Required prototype output envelope: approximately 150 W minimum preferred, with margin selected after actual motor/camera power is known.

The converter must be a replaceable commercial module for the prototype. A custom copy of Mini-Cam `PCB-001-982` is explicitly not required.

## 7. Crawler low-voltage distribution

```text
24 V MAIN BUS
 |
 +-- F-L --> LEFT traction driver --> LEFT geared motor
 |
 +-- F-R --> RIGHT traction driver --> RIGHT geared motor
 |
 +-- 24->12 V --> camera / lighting as required
 |
 +-- 24->5 V --> STM32 / sensors / RS-485 / video electronics
 |
 +-- current/voltage/pressure monitoring
```

Per-side current sensing is retained.

The first low-voltage bench crawler may run directly from a current-limited 24 V supply with the HV converter absent. The HV input stage is integrated only after traction, camera and control are proven at 24 V.

## 8. Traction interface

Mechanical architecture:
- two motors total;
- one motor per side;
- each motor drives the rear long-axle input through Z16 -> Z40 bevel reduction;
- five Z50 gears distribute rotation to all three wheels of the side.

Electrical prototype:
- two independent reversible motor-driver channels;
- PWM speed control;
- acceleration/deceleration ramp;
- per-side fuse;
- per-side current measurement;
- jam limit;
- communications watchdog.

The previously selected BTS7960 modules remain valid only for brushed DC motor candidates. If the final traction motor is BLDC, use a commercially available sensored BLDC controller/driver instead. Motor technology is therefore frozen only after the exact purchased motor is selected.

## 9. RS-485 control network

CCU is master; crawler is the primary remote node.

Baseline:
- half-duplex differential RS-485;
- CRC and sequence number;
- command update target 20-50 Hz;
- fail-safe bias/termination sized for the actual line;
- galvanic isolation at the CCU interface preferred;
- crawler watchdog stops traction on loss of valid command.

Minimum crawler telemetry:
- pressure;
- 24 V bus voltage;
- tether/HV input voltage if safely sensed by the selected converter/interface;
- left/right motor current;
- temperature(s);
- fault bits;
- camera status;
- heartbeat.

## 10. Video path

No digital encoder is required in the crawler for the prototype.

```text
fixed-focus CVBS camera
 -> balanced differential video transmitter
 -> camera rotating interface
 -> crawler direct pair
 -> tether VIDEO+/VIDEO-
 -> reel slip ring
 -> balanced differential receiver in CCU
 -> OSD
 -> 7 in CVBS monitor
```

The selected balanced-video transmitter/receiver must be proven through the final slip ring and 40 m tether before release; then through a 100-150 m equivalent.

## 11. Camera local electrical interface

Preferred camera quick-interface / rotating-interface functional set:
1. camera power +
2. camera power return
3. local control TX/A
4. local control RX/B
5. VIDEO+
6. VIDEO-

A small camera MCU controls PAN/ROTATE/lighting locally so the main crawler MCU does not route individual motor/encoder wires through the whole robot.

Exact camera local protocol may be UART or short local RS-485; this does not change the main six-core tether allocation.

## 12. Pressure system

Crawler pressure sensor remains inside the dry body. A service pressurization port is external but sealed/valved. Pressure value is transmitted to CCU over RS-485 and shown to the operator.

The camera remains a separately sealed body.

## 13. Fault hierarchy

Hardware faults with immediate power effect:
- E-STOP;
- tether/HV overcurrent;
- critical insulation/power-module fault where available;
- open safety chain.

Crawler software faults:
- command timeout;
- overcurrent/jam;
- undervoltage/overvoltage;
- pressure outside configured band;
- thermal fault;
- camera communication fault.

Traction must default to STOP on MCU reset or communications loss.

## 14. Prototype bring-up order

1. 24 V bench crawler: MCU + two drivers + motors + pressure + camera control.
2. Direct short-wire RS-485 and balanced CVBS proof.
3. Reel encoder and slip ring proof at low voltage.
4. 40 m six-core cable proof with low-energy/low-voltage tests.
5. HV source and dummy-load qualification in CCU.
6. HV->24 V crawler converter qualification on dummy load.
7. Integrate HV through reel/tether with crawler disconnected first and appropriate enclosed test load.
8. Integrate crawler and verify E-STOP/fault drop-out.
9. Thermal and current logging.
10. Only then extend toward 100-150 m.

Rev.PP is the active electrical architecture. Component part numbers that are still OPEN must not be silently frozen by older experimental documents.
