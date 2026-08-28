# PX1 Rev.PK — Proteus-style simple control unit

Status: ACTIVE PROTOTYPE BASELINE.

## Operator workflow retained from Proteus
- LEFT joystick: crawler forward/reverse + left/right steering.
- RIGHT joystick: camera PAN/ROTATE command.
- physical POWER control.
- physical red ALL STOP / E-STOP.
- separate CRAWLER ENABLE.
- LIGHT level control.
- CAMERA HOME.
- DISTANCE ZERO.
- optional RECORD key.

Manual camera lift means there is no lift motor command on the console.

## Mechanical panel baseline
PX1 panel: 380 x 250 x 3 mm aluminium candidate.
Rear enclosure depth: 125 mm.
GF-AM071 complete monitor reference: 180 x 121 x 74 mm; final mounting holes/bracket remain HOLD until physical sample measurement.

Control centres in panel coordinates X/Y mm:
- left joystick: 80 / 67;
- right joystick: 300 / 67;
- ALL STOP: 190 / 67, standard 22 mm panel family;
- POWER: 135 / 25, 19 mm family;
- CRAWLER ENABLE: 245 / 25, 22 mm family;
- CAMERA HOME: 52 / 25, 19 mm family;
- DIST ZERO: 92 / 25, 19 mm family;
- RECORD: 288 / 25, 19 mm family, optional;
- LIGHT potentiometer: 330 / 25.

The Rev.PK CadQuery packing check fits all current module envelopes with zero AABB/solid collision and zero volume outside the rear enclosure.

## Standardise the controller
Use the same NUCLEO-F446RE family in the console and crawler where practical.
Benefits:
- one spare controller type;
- same programming/debug cable;
- same firmware toolchain;
- failed board can be swapped and reflashed for either role.

## Low-voltage control section
24 V external PSU feeds the console.
24 V directly feeds the GF-AM071 monitor and the tether-power input stage.
A replaceable 24->5 V buck feeds logic/OSD/video receiver as required.

Control/data modules:
- NUCLEO-F446RE;
- isolated RS-485 module;
- MAX7456-class ready OSD module;
- balanced-video-to-CVBS receiver;
- AS5600 reel distance sensor connected locally at the reel/control station;
- optional ready CVBS DVR module.

No custom PCB required.

## Hardware ALL STOP / crawler power
ALL STOP is independent of firmware.

Power path:
`24 V INPUT -> F1 -> K1 normally-open power relay -> TETHER BOOST -> reel slip ring -> tether`

K1 is a common replaceable 24 V / 40 A automotive-style relay with socket, because it switches the low-voltage 24 V input to the boost converter rather than trying to interrupt the elevated tether voltage directly.

K1 coil path:
`24 V -> ALL STOP NC contact -> CRAWLER ENABLE -> K1 coil -> 0 V`

Therefore pressing ALL STOP drops K1 even if either MCU has crashed.
POWER may leave the monitor/control logic alive while crawler power is removed.

The elevated tether output must have a discharge path. Final bleeder resistor value remains HOLD until the selected boost converter output capacitance is known. Release requirement: after K1 drops, exposed tether voltage must fall below the agreed safe service threshold within the specified discharge time.

Crawler/tether power must not auto-restart after an E-STOP event; operator re-enable is required.

## Communications
Console -> crawler command packet target 20–50 Hz:
- sequence;
- left joystick X/Y;
- right joystick X/Y;
- light level;
- camera HOME;
- crawler ENABLE state;
- auxiliary bits;
- CRC16.

Crawler -> console:
- internal pressure;
- robot input voltage;
- left/right traction current;
- faults;
- camera state/home;
- temperature optional;
- CRC16.

Fail-safe: no valid command for >250 ms commands both traction channels and both camera axes to STOP. Hardware ALL STOP remains independent of this software timeout.

## OSD
Minimum overlay:
- distance;
- crawler pressure;
- time;
- crawler power/fault state.

Job/address text remains a software UI item. It must not force a PC into the console; a simple service/configuration input method will be chosen later.

## Video
Dedicated tether VIDEO+/VIDEO- -> balanced receiver -> CVBS -> OSD -> GF-AM071.
No coax in the tether. No optical fibre.

## Power-module HOLD
The tether boost is deliberately represented only as a 200 W class packaging reserve. Exact 48/60 V output is NOT frozen until actual loop resistance of the real Proteus-style 6-core cable is measured.

## CAD
Active source:
`mechanical/cadquery/PX1_ControlUnit_RevPK.py`

Generated/validated locally:
- `PX1_ControlUnit_RevPK.step`
- `PX1_ControlUnit_FrontPanel_RevPK.step`
- `REV_PK_VALIDATION.json`

## Remaining gates
1. exact 2-axis joystick article and rear depth;
2. physical GF-AM071 bracket/hole measurement;
3. exact 24 V relay/socket and fuse holder;
4. actual tether loop resistance -> select boost voltage/module;
5. thermal test of boost converter in closed console;
6. cable/reel connector interlock and output discharge verification.
