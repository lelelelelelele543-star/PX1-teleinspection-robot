# PX-1 SYSTEM WIRING — Rev.B

Date: 2026-09-11
Status: ACTIVE REV.B END-TO-END ELECTRICAL BASELINE
Supersedes `PX1_SystemWiring_RevPP.md` where exact tether construction, source voltage, converter selection or 24 V protection differs.

## 1. System chain

```text
AC / external CCU supply
        |
        v
PX1 CCU
  low-voltage controls / display / OSD
  isolated RS-485 master interface
  balanced-video receiver
  120 VDC-class crawler supply
  current-limited soft start
  hardware E-STOP disconnect
        |
        v
PX1 MANUAL REEL
  6 functional tether circuits through qualified slip ring
  local payout encoder A/B -> CCU only
        |
        v
ONE reinforced 6-functional-core tether
  22AWG HV+
  22AWG HV-
  24AWG RS485_A/B pair
  24AWG VIDEO+/- pair
  aramid tensile reinforcement
        |
        v
PX1 CRAWLER TAIL
  jacket support
  aramid structural termination
  relaxed copper service loop
  sealed 6-pin H-D 1.6 connector
        |
        v
CRAWLER HV INPUT
  3.15A time-delay HV fuse candidate
  qualified inrush limiter / controlled source ramp
  220uF / 200V input capacitor
  commercial isolated HV->24V converter
        |
        v
24 V MAIN BUS / STAR
  bus-voltage ADC
  LEFT traction branch
  RIGHT traction branch
  24->12 V camera/axis branch
  24->5 V logic/communications branch
  lighting constant-current branch
```

## 2. Main tether — active Rev.B construction

Replacement-cable target:
- exactly 6 functional copper conductors;
- 2 x 22 AWG for HV power;
- 2 x 2 x 24 AWG differential signal pairs;
- aramid/Kevlar-class strength member;
- no coax;
- no fibre;
- no additional electrical core required for shield/drain;
- target OD <=8.0 mm, absolute prototype gate <=8.5 mm;
- target mass <=60 g/m;
- breaking load >=1.5 kN, >=3 kN preferred.

First 40 m demonstrator may use the existing professional Proteus-class cable only after measurement/qualification.

## 3. Tether pinout

| Pin | Function | Replacement conductor |
|---:|---|---|
| 1 | HV+ | 22 AWG |
| 2 | RS485_A | 24 AWG pair A |
| 3 | RS485_B | 24 AWG pair A |
| 4 | HV- | 22 AWG |
| 5 | VIDEO- | 24 AWG pair B |
| 6 | VIDEO+ | 24 AWG pair B |

Gold H-D 1.6 contacts for the 22/24AWG replacement cable:
- crawler male: LAPP 13162500;
- cable female: LAPP 13163500;
- 0.14...0.37 mm²;
- strip 8 mm.

Exact contact barrel for the existing Proteus cable remains sample-driven.

## 4. Tether voltage

Active long-run source target: approximately 120 VDC, within the already approved 100-120 VDC system class.

Reason:
- lightweight 22 AWG power conductors are compatible with ~1 A cable current;
- 40 m and 100 m have good margin;
- 150 m remains feasible if normal crawler power is kept around <=100 W and higher power is short-duration only.

The 48 V and 60 V long-cable studies are historical and no longer control the active design.

## 5. Crawler HV input sequence

```text
sealed H-D connector
 -> local HV fuse
 -> inrush element / source-ramp interaction
 -> 220uF 200V bulk capacitor
 -> isolated 120V-class to 24V DC/DC
 -> 24V bus
```

Current primary engineering converter:
- Cincon CQB150W-110S24;
- 43-160 VDC input;
- 24 V / 6.3 A;
- ~151 W;
- ~57.9 x 36.8 x 12.7 mm;
- isolated.

### Procurement restriction note
The Cincon module is the current **engineering reference** because its controlled datasheet and current distributor inventory are verified. It is not considered procurement-frozen under the project's earlier `ChipDip / marketplace` sourcing restriction until an approved purchasing route is confirmed.

ChipDip's current technical library includes electrically compatible 150 W / 24 V / high-input modules, including:
- Murata `Q-24/6.25-W80` / IRQ-W80 family, 16-160 V input, 24 V / 6.25 A, ~61.21 x 39.62 x 13 mm;
- RECOM `RPA150Q-11024SRUW/P`, 14.4-170 V, 24 V / 6.25 A, but that RECOM article is now an EOL/obsolete risk and is not selected as the new freeze.

Before purchase, WB07 must be closed with an article actually available through an approved source. Electrical/CAD architecture is not changed by choosing an equivalent quarter-brick in this envelope.

## 6. HV input capacitor

Engineering candidate:
- Nichicon UCS2D221MHD1TN;
- 220 uF / 200 V;
- ~18 x 25 mm;
- mount horizontally;
- mechanically clamped.

Stored energy at 120 V is ~1.58 J. Inrush and discharge handling are mandatory.

## 7. HV input fuse

Prototype class:
- 3.15 A time-delay;
- 5 x 20 mm ceramic;
- DC rating comfortably above 120 V;
- internal dry service holder.

Current engineering article: Eaton Bussmann S505H-3.15-R class.

Final article/source is frozen together with the selected HV converter purchasing route.

## 8. 24 V main bus

The isolated converter output powers the local 24 V bus.

Normal total-output target:
- <=100 W.

Short controlled transient:
- 120...145 W class after thermal/long-line qualification.

Continuous 150 W through a hot 150 m lightweight tether is explicitly not the normal design condition.

Distribution rule:
- use one explicit 24 V star point immediately downstream of the main DC/DC;
- traction, 12 V converter, 5 V converter and lighting branch leave this star separately;
- aluminum structure is not a normal current return conductor.

## 9. Traction branches

Two branches only:

```text
24V BUS
  |
  +-- LEFT branch -> current sensor -> local bulk/TVS -> BTS7960 module -> LEFT motor
  |
  +-- RIGHT branch -> current sensor -> local bulk/TVS -> BTS7960 module -> RIGHT motor
```

Per branch Rev.B hardware:
- one 1000 uF / 50 V Nichicon UHE1H102MHD6 close to driver;
- one Littelfuse 1.5KE30A TVS directly at driver power terminals;
- verify/add ~470 nF low-inductance local decoupling;
- branch fuse value HOLD until motor bench measurements;
- external calibrated current measurement required.

## 10. Traction-driver status

BTS7960 / IBT-2 remains the approved Rev.B prototype H-bridge only.

Important:
- original Infineon BTS7960 silicon is obsolete;
- marketplace module build quality is not controlled;
- hardware current limit is far above the safe mechanical drivetrain current;
- native IS current sense is not accurate enough to be the sole precision torque sensor.

Rev.C must qualify a controlled-source driver or migrate to a current production bridge without changing mechanical drive architecture.

## 11. Traction motion policy

Normal stop:
`PWM ramp down -> INH/enable low -> COAST`.

Direction change:
`drive -> ramp down -> coast -> zero-current confirmation -> opposite direction`.

Hard instant reversal is prohibited.
Routine dynamic braking is not released.

Starting bus thresholds:
- >26.5 V: ramp toward zero / warning;
- >=27.0 V: immediate traction inhibit + latched fault;
- re-enable below 25.5 V only after stable delay and deliberate command.

## 12. 24 V bus telemetry

STM32 ADC divider candidate:
- 100 kOhm top;
- 6.8 kOhm bottom;
- 100 nF ADC filter;
- ~1.53 V at 24 V bus;
- ~2.87 V at 45 V bus.

This measurement is on the isolated low-voltage side and does not defeat HV isolation.

Direct tether-HV-to-MCU resistor divider remains prohibited.

## 13. Current telemetry

Layer 1:
- BTS7960 IS outputs for gross/fault diagnostics after calibration.

Layer 2:
- one external ready-made bidirectional current/power sensor per drive side;
- INA226 R010-class module is the Rev.B prototype candidate;
- sensor silicon measures 0...36 V bus class and supports programmable I2C addressing;
- two modules use I2C1 on PB8/PB9;
- calibrate every purchased module against a bench reference because generic module shunts/traces vary.

Final current/torque thresholds remain motor-test data, not catalog guesses.

## 14. Auxiliary low-voltage branches — WB09 freeze

### 12 V camera / camera-axis rail

Selected service module:
- Pololu `D42V55F12`;
- item `5577`;
- input 12...60 V;
- output fixed 12 V;
- typical continuous current class 4.5 A;
- 25.4 x 25.4 x 9 mm;
- soft-start, reverse-input, over-current and thermal protection;
- EN and PG available.

Loads:
- camera electronics;
- TILT/ROLL 12 V motor-driver branches;
- balanced-video transmitter if its final article uses 12 V.

The two current camera-axis motors have a combined stall-current screen of about 2.2 A. This is below the converter's current envelope, but motor stall is still fault-only operation.

Preliminary branch protection:
- 24 V converter-input fuse: 3.15 A time-delay;
- 12 V camera-harness fuse: 3.15 A time-delay;
- both values remain physical-test driven.

### 5 V logic rail

Selected service module:
- Pololu `D42V55F5`;
- item `5571`;
- input 5...60 V;
- output fixed 5 V;
- typical continuous current class 6 A;
- 25.4 x 25.4 x 9 mm;
- same mechanical family as the 12 V converter;
- soft-start, reverse-input, over-current and thermal protection;
- EN and PG available.

Loads:
- NUCLEO-F446RE through E5V;
- crawler-side isolated RS-485 TTL side;
- current sensors;
- low-voltage sensors/interfaces.

This converter is intentionally oversized; 60 V input rating was selected to keep margin above WB08's common 24 V bus transient envelope rather than relying on old 35/36 V hobby buck modules.

Preliminary branch protection:
- 24 V converter-input fuse: 1.0 A time-delay;
- NUCLEO E5V harness protection starting class: <=0.75 A after real-load measurement.

### NUCLEO power rule

- `5V_LOGIC -> NUCLEO E5V`;
- follow ST UM1724 external-supply jumper and USB power-sequence requirements;
- do not connect the crawler 24 V bus directly to E5V;
- other 5 V loads connect in parallel to the 5 V rail, not through the NUCLEO board.

## 15. Main RS-485 physical layer — WB09

Selected module family:
- Waveshare `TTL TO RS485 (C)`;
- SKU `27479`;
- same module at crawler and CCU ends;
- half duplex;
- isolated power and signals on-board;
- TVS/protection on-board;
- optional 120 ohm termination;
- approximately 42.8 x 15.2 x 4.75 mm;
- automatic ready-module direction handling; no external MCU DE GPIO is required.

Crawler MCU allocation:
- PC10 / USART3_TX;
- PC11 / USART3_RX;
- PA2/PA3 kept for NUCLEO ST-LINK VCP debug.

Local camera UART reservation:
- PC12 / UART5_TX;
- PD2 / UART5_RX.

### RS-485 common-mode HOLD

The tether intentionally has only A/B for RS-485 and no seventh reference conductor.

Therefore galvanic isolation is required but is not by itself proof of unlimited common-mode margin.

Rules:
- never bond isolated RS-485 line-side reference/PE to tether HV-;
- never consume VIDEO+/VIDEO- as a temporary reference in the released harness;
- do not claim 150 m production release from the Waveshare distance rating alone;
- scope/test differential and common-mode behavior at 40 m, then 100/150 m equivalent, while traction/camera motors and lighting are switching.

If common-mode margin is inadequate, revise the physical layer deliberately. Do not silently alter the six-core pinout.

Termination:
- only at the two physical tether endpoints;
- match the measured characteristic impedance of the final signal pair;
- use onboard 120 ohm only if the pair measurement justifies it;
- no termination in the reel middle.

## 16. Ground/return routing

Rules:
- motor returns use short high-current paths back to the 24 V star;
- LEFT motor return does not flow through RIGHT current sensor;
- camera/video/logic return does not carry traction motor current;
- balanced-video and RS-485 pair routing remains physically separated from BTS7960 switching loops;
- auxiliary buck heat and traction-driver heat are coupled to the aluminum body/carrier where practical, not stagnant air only;
- RS-485 TTL-side ground belongs to logic ground while line side remains galvanically isolated.

## 17. Hardware safety

CCU hardware E-STOP must disable tether HV independently of the crawler MCU.

Crawler firmware cannot override:
- open E-STOP chain;
- source overcurrent;
- line/connector safety fault.

On lost command/heartbeat:
- traction INH low;
- motor coast;
- camera-axis commands stop;
- CCU subsequently removes HV according to fault policy.

No disconnected tether connector may remain energized.

## 18. Bring-up sequence

1. 24 V bench crawler only.
2. Verify 12 V and 5 V rails on dummy loads.
3. Power NUCLEO through E5V and verify USB/ST-LINK power sequencing.
4. One motor side at a time: motor -> supported bevel -> side drive.
5. Calibrate current versus torque and calibrate both INA226-class modules.
6. Add second traction side and bus transient logging.
7. Prove isolated RS-485 and balanced CVBS at low voltage through 40 m.
8. Exercise RS-485 common-mode/noise with traction, camera axes and LED PWM active.
9. Build HV converter carrier/harness on dummy load.
10. Qualify inrush, fuse and E-STOP without crawler attached.
11. Integrate crawler at 40 m.
12. Emulate 100/150 m loop resistance and repeat RS-485 common-mode tests.
13. Only then order/operate long tether.

## 19. Controlled document references

- `tether/REVB_WB06_TETHER_POWER_SIGNAL_FREEZE.md`
- `mechanical/REVB_WB05_TAIL_CONNECTOR_AND_STRAIN_RELIEF.md`
- `electronics/REVB_WB07_HV_TO_24V_POWER_STAGE.md`
- `electronics/REVB_WB08_24V_BUS_REGEN_PROTECTION.md`
- `electrical/REVB_WB09_LOW_VOLTAGE_COMMS.md`
- `electrical/PX1_CommonServiceModules_RevB.md`
- `electrical/REV_B_WB09_VALIDATION.json`
- `mechanical/REVB_WB03_BEVEL_MOTOR_TORQUE_GATE.md`
- `firmware/crawler/board_map_f446.h`

## Change log

### 2026-09-11 — Rev.B promotion
- promoted 120 V long-tether architecture;
- promoted 22/24 AWG six-functional-core replacement tether;
- promoted sealed H-D 1.6 tail connector architecture;
- added 150 W-class 120V->24V quarter-brick stage;
- added 24 V regenerative/transient protection and coast-stop policy;
- recorded BTS7960 lifecycle/current-sense limitations;
- explicitly restored the approved-source procurement gate for the HV DC/DC rather than treating DigiKey/Mouser availability alone as final procurement approval.

### 2026-09-11 — WB09 integration
- froze Pololu 5577 as the 12 V camera/axis converter and Pololu 5571 as the 5 V logic converter for Rev.B;
- replaced old 35/36 V-class auxiliary-buck assumptions with 60 V-input modules;
- fixed NUCLEO power at regulated E5V;
- froze Waveshare 27479 as the Rev.B isolated ready-made RS-485 module family;
- moved main tether UART to USART3 PC10/PC11 and removed the external DE requirement;
- reserved UART5 PC12/PD2 for the local camera node and I2C1 PB8/PB9 for current sensors;
- recorded two-wire/no-reference RS-485 common-mode behavior as a physical qualification HOLD.
