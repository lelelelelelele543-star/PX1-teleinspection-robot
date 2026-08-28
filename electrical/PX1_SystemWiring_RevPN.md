# PX1 Rev.PN — simplified end-to-end Proteus-style system wiring

Status: ACTIVE SYSTEM ARCHITECTURE.

## Design objective
Keep the successful Proteus system split:
`CONTROL UNIT <-> MANUAL REEL <-> 6-CORE TETHER <-> CRAWLER <-> CAM026-LIKE CAMERA`
while deleting proprietary processing boards wherever a direct signal path or standard module is sufficient.

---

## 1. Main six-core tether
One reinforced Proteus-style six-core copper inspection cable.
No coax, optical fibre or collection of separate loose twisted-pair cables.

Main tether pin/function assignment:
1. PWR+
2. PWR-
3. RS485_A
4. RS485_B
5. VIDEO+
6. VIDEO-

Aramid/Kevlar strength path is terminated mechanically in the reel/crawler tail structure. Electrical contacts carry no tensile load.

---

## 2. Control unit Rev.PK/PL
External 24 V PSU -> console.

Control branch:
`24V -> monitor`
`24V -> 5V buck -> NUCLEO-F446RE + isolated TTL TO RS485(C) + OSD/video receiver`

Crawler-power branch:
`24V -> F1 -> K1 hardware safety relay -> TETHER POWER CONVERTER -> reel slip ring -> PWR+/PWR-`

K1 coil is physically interrupted by normally-closed ALL STOP.
No firmware can override a pressed ALL STOP.

Exact tether converter output voltage remains HOLD until real cable loop resistance is measured.

---

## 3. Manual reel Rev.PJ
Reel carries no system computer.

Standard slip-ring candidate: Senring M220-1205, 12 circuits.
Proposed mapping:
- rings 1+2 -> PWR+
- rings 3+4 -> PWR-
- ring 5 -> RS485_A
- ring 6 -> RS485_B
- ring 7 -> VIDEO+
- ring 8 -> VIDEO-
- rings 9..12 -> spare / future diagnostics

Distance measurement:
mechanical Proteus-style measuring wheel -> magnet -> AS5600 ready module -> short local cable to console MCU.
The distance sensor does not consume tether conductors.

Layering remains fully mechanical: 06B-1 chain, Z30/Z16 PX1 replacement set.

---

## 4. Crawler tail/input
Cable entry sequence:
`aramid strain termination -> water seal -> electrical connector -> input protection`

Electrical input block:
- fuse;
- transient clamp/TVS;
- reverse polarity protection;
- inrush limiting as required by selected DC/DC;
- line DC/DC -> local 24 V bus.

The exact line DC/DC remains HOLD with tether voltage.

---

## 5. Crawler electronics — deliberately small
Local 24 V bus feeds:
- LEFT traction driver -> left motor;
- RIGHT traction driver -> right motor;
- 24->12 V camera supply;
- 24->5 V logic supply;
- pressure sensor/current sensing as required.

Logic:
- NUCLEO-F446RE;
- isolated TTL TO RS485(C), same spare module as console.

The crawler MCU:
- interprets left joystick commands;
- drives the two traction channels;
- controls the fixed-side camera ROTATE motor;
- sends PAN/light commands to the camera-side MCU;
- reports pressure/voltage/current/faults to console.

There is no video digitiser, recorder or proprietary camera computer in the crawler.

---

## 6. Video path — no crawler processing
`fixed-focus CVBS camera board`
-> `balanced video transmitter inside rotating camera assembly`
-> `CAM026 6-way slip ring VIDEO+/VIDEO-`
-> `camera quick connector VIDEO+/VIDEO-`
-> `crawler internal direct pair`
-> `main tether VIDEO+/VIDEO-`
-> `reel slip ring`
-> `console balanced receiver`
-> `MAX7456-class OSD`
-> `GF-AM071 monitor`

This is the shortest useful electronic path and keeps main-tether video balanced.

---

## 7. Camera connector / six-way rotating interface
Crawler-to-camera quick connector functions:
1. +12 V
2. GND
3. UART crawler TX -> camera RX
4. UART camera TX -> crawler RX
5. VIDEO+
6. VIDEO-

The same six functions continue across the camera continuous-rotation slip ring.

Rotating side:
- RP2040-Zero ready MCU module;
- PAN DRV8871 ready H-bridge;
- PAN magnetic angle sensor;
- LED PWM/current module;
- fixed-focus CVBS camera;
- balanced video transmitter.

Fixed side:
- ROTATE DRV8871;
- ROTATE angle/reference sensor.

Thus two DRV8871 modules are used per complete camera system, but only one is on the continuously rotating side.

---

## 8. Control/fail-safe hierarchy
Hardware level:
- ALL STOP removes crawler power regardless of MCU state.

Console software level:
- sends command packet 20–50 Hz with CRC/sequence.

Crawler software level:
- >250 ms without valid command -> traction STOP + ROTATE STOP + PAN STOP command.

Camera software level:
- local UART timeout -> PAN STOP;
- invalid/out-of-range PAN sensor -> PAN STOP;
- mechanical PAN stop remains independent of software.

Power restoration after ALL STOP requires deliberate CRAWLER ENABLE action.

---

## 9. What was removed compared with proprietary Proteus electronics
Removed from PX1 architecture:
- proprietary crawler main PCB equivalent;
- dedicated focus motor and focus PCB;
- separate proprietary PAN/ROTATE controller PCBs;
- proprietary reel meter PCB;
- proprietary reel slip-ring PCB;
- PC/WinCan/Wi-Fi stack in control unit.

Functions preserved:
- six-wheel crawler drive;
- pressure supervision;
- manual camera lift;
- continuous camera rotate;
- +/-135 degree PAN target;
- six camera LEDs;
- distance counter;
- manual level-wind reel;
- two-joystick Proteus operator workflow;
- hardware ALL STOP;
- live video and OSD.

---

## 10. Remaining system gates
1. Measure actual power-conductor loop resistance of the real six-core tether.
2. Freeze line voltage and line DC/DC only after that measurement.
3. Select/test balanced video TX/RX through camera slip ring + 150 m cable.
4. Measure/close CRP150 lift dimensions from physical source because detail drawings are absent.
5. Freeze exact traction motors/drivers and verify current/thermal margin.
6. Pressure/water test camera, crawler and tail independently.
