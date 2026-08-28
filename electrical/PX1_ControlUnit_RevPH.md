# PX1 Rev.PH — simplified Proteus-style control unit

## Design rule
Copy the successful Proteus operator workflow, not the proprietary CCU electronics/software stack.
Official Proteus control logic retained:
- left joystick = crawler movement
- right joystick = camera pan/rotate
- physical power control
- physical ALL STOP / emergency stop

Delete from PX1 baseline:
- survey/report computer
- proprietary keyboard
- Wi-Fi/file-sharing subsystem
- proprietary media/storage controller
- crawler/camera proprietary communication boards

## Front panel — baseline
1. 7 inch daylight-capable CVBS monitor
2. LEFT 2-axis joystick — crawler forward/reverse + left/right steering
3. RIGHT 2-axis joystick — camera tilt/pan + continuous rotate command mapping
4. red mushroom E-STOP / ALL STOP
5. POWER ON/OFF
6. CRAWLER ENABLE illuminated pushbutton
7. LIGHT rotary potentiometer
8. CAMERA HOME pushbutton
9. RECORD pushbutton only if chosen DVR module supports it
10. pressure/alarm indicator or buzzer

Manual camera lift means there is NO motorised lift control on the console.

## Simple electronics
Console controller candidate: readily available Arduino Nano-class or compact STM32 module.
Robot controller remains the serviceable STM32 module selected for the crawler.
Communication: RS-485, half duplex or full duplex as finally wired.
No CAN/Ethernet/proprietary bus required for first prototype.

## RS-485 command strategy
Console sends a compact fixed packet at 20-50 Hz:
- sequence number
- crawler joystick X/Y
- camera joystick X/Y
- light level
- camera home bit
- crawler enable bit
- spare function bits
- CRC16

Robot reply:
- pressure
- robot supply voltage
- left/right motor current
- fault flags
- camera state/home
- optional temperature
- CRC16

Fail-safe:
- if valid command packet is absent for >250 ms, both traction motors and camera motors command STOP
- restart requires a valid packet and CRAWLER ENABLE state

## E-STOP power architecture
The E-STOP is NOT software-only.
It directly removes coil power from the relay/contactor that energises the elevated tether supply.
Sequence:
24 V PSU -> fuse -> DC boost/isolation stage -> safety relay/contactor -> reel slip ring -> tether.

POWER ON powers the control electronics/monitor but does not automatically energise crawler power.
CRAWLER ENABLE energises the tether supply only if E-STOP is released and interlocks are healthy.
This mirrors the useful Proteus behaviour without reproducing proprietary electronics.

## Video / OSD
- camera video travels on the dedicated VIDEO+/VIDEO- conductors
- console receiver converts to CVBS for the 7 inch monitor
- external OSD overlays: distance, pressure, time, address/text
- optional simple CVBS DVR module records to SD/USB

No coax in the tether and no optical fibre.

## Reel interaction
RMP300 remains manual.
AS5600 meter data is read by the console controller through a short local cable at the reel/control station.
No motorised reel control or tension-control electronics in prototype 1.

## Status
Operator architecture frozen for prototype. Exact enclosure/panel dimensions and exact controller/DVR/video receiver modules remain BOM/CAD items.
