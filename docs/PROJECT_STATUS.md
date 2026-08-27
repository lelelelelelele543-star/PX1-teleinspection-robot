# PX-1 Project Status

Current working engineering revision: Rev.AJ.

## Frozen architecture
- body 250 x 94 x 76 mm
- 4WD external geared transmission
- two sealed rear output shafts
- wheelbase 160 mm
- nominal wheel diameter 90 mm
- manual camera lift
- TILT -105..+105 degrees
- continuous ROLL
- universal waterproof quick-release interfaces
- 24 V power bus
- two NUCLEO-F446RE controllers
- isolated/protected RS-485 target architecture
- CVBS 75 ohm video path

## Prototype-dependent holds
1. Exact traction motor and final adapter-hole pattern.
2. Exact tether outside diameter and LEMO cable collet.
3. Exact camera-side LEMO shell suffix.
4. Final pressure, undervoltage and thermal thresholds after prototype measurements.
5. Final sealing and traction acceptance values after first physical crawler.

## Toolchain
- FreeCAD — mechanical CAD
- KiCad — electrical design
- STM32CubeIDE — firmware
- LTspice — power/EMC simulation
- OrcaSlicer — printed fixtures and prototypes
- GitHub — source/revision control
