# PX-1 Teleinspection Robot

Open engineering project for a modular pipe-inspection crawler inspired by professional systems such as Minicam Proteus CRP-150 and Rovver 125, but designed around inexpensive, replaceable, serviceable components.

## Current design baseline
- Sealed crawler body: 250 x 94 x 76 mm
- Two dynamic rear shaft seals only
- External geared 4WD, 160 mm wheelbase
- Wheels: nominal 90 mm
- Manual camera lift with LOW / DN150 SAFE / HIGH positions
- Camera TILT: -105..+105 deg
- Camera ROLL: continuous 360 deg
- Tail connector: LEMO EGG.5K.870.CLL5
- Camera quick-release architecture: LEMO K-series 0K.304
- Main controller: STM32 NUCLEO-F446RE
- Console controller: STM32 NUCLEO-F446RE
- RS-485 control link, CVBS video on 75 ohm coax
- Output-shaft metering: AS5600 / MIKROE Angle 7 Click

## Project structure
- `mechanical/` FreeCAD, STEP, STL, DXF and mechanical drawings
- `electronics/` KiCad schematics, harnesses, pinouts and protection
- `firmware/crawler/` crawler firmware
- `firmware/console/` operator-console firmware
- `firmware/common/` shared protocol and utilities
- `simulation/` LTspice power and EMC models
- `manufacturing/` machining, assembly and inspection instructions
- `bom/` current purchasable parts and alternates
- `tests/` prototype verification and acceptance tests
- `docs/` controlled PDF documentation
- `release/` manufacturing release only

## Rule
Files in `release/` are the only files intended for manufacturing. Historical and experimental material must not be treated as released production data.
