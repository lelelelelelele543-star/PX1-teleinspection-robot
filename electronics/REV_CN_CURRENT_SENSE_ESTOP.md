# PX-1 Rev.CN — traction current sensing and hardware E-STOP

Status: engineering candidate.

## Current sensing
Preferred sensor family for each traction side: Allegro ACS770, bidirectional ±50 A variant.

Candidate part:
- ACS770LCB-050B-PFF-T;
- ±50 A measurement range;
- 5 V supply;
- Hall-effect isolated measurement;
- 100 µΩ primary conductor;
- 120 kHz typical bandwidth;
- operating range -40..+150 °C.

Reasoning: traction motors can generate bidirectional current during braking/reversal, so a bidirectional sensor is preferred. The low-resistance integrated conductor minimizes loss and does not require a shunt in the motor return path.

Two sensors are used: one for LEFT traction branch and one for RIGHT traction branch.

## Hardware E-STOP architecture
The mushroom E-STOP does not depend on firmware. It interrupts the coil/control path of a dedicated traction contactor/relay. When pressed, traction power is removed from the BTS7960 stage while camera, communication and controller rails may remain powered for recovery and diagnostics.

Preferred contact arrangement:
- latching red mushroom, twist/pull release;
- minimum 2 normally-closed contacts;
- one NC contact in traction-contactor control path;
- second NC contact into controller safety input for telemetry/state logging;
- industrial panel style, IP65/IP67 class preferred.

## Traction contactor
Do NOT use an EV200-class 500 A contactor: it is electrically excellent but grossly oversized for PX-1.

Target traction contactor specification:
- DC-rated switching, not an AC-only relay;
- contacts >=30 A continuous at 24 VDC;
- coil 24 V preferred (from protected 24 V rail);
- normally-open main contacts;
- sealed automotive/industrial type preferred;
- suppression diode/TVS across coil, placed locally;
- manual replacement without soldering.

Exact contactor SKU remains HOLD until measured JGB37-520 stall current is known.

## Safety behavior
E-STOP pressed:
- traction contactor opens;
- BTS7960 enable lines are also forced LOW by hardware;
- camera/network/controller remain alive;
- software records E_STOP_ACTIVE;
- restoring the mushroom does NOT automatically restart traction: operator re-enable command is required.

## Release gates
1. measure stall and reverse-current peaks on both JGB37-520 traction groups;
2. choose contactor with >=2x measured continuous-current margin and verified DC interrupt rating;
3. verify contactor opening under worst-case motor current;
4. verify controller cannot re-enable BTS7960 while E-STOP loop is open;
5. validate current-sensor calibration and overcurrent thresholds.
