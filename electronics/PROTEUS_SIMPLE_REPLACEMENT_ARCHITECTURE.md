# PX-1 — simplified electronics for the Proteus-like replacement

Status: ACTIVE ARCHITECTURE. Exact bought modules remain BOM gates.

## Goal
Keep the mechanical behaviour of CRP-150 / CAM026 / RMP300 while deleting proprietary electronics wherever possible.

The prototype must be repairable by replacing inexpensive modules and ordinary connectors rather than replacing a MiniCam main PCB.

## Crawler electronics — minimum set
1. One STM32 controller module.
2. One 2-channel traction H-bridge module, or two small single-channel H-bridges if the dual module is not readily available.
3. One 2-channel camera-axis H-bridge.
4. One isolated RS-485 transceiver module.
5. One pressure sensor.
6. One balanced analog-video transmitter/receiver pair.
7. Simple DC/DC power conversion only where the measured tether resistance requires it.
8. Fuses / transient suppression / reverse-polarity protection.

No proprietary motor-control PCB and no custom multilayer crawler main PCB are required for the first prototype.

## Camera electronics — minimum set
Keep CAM026 mechanical architecture, but simplify the inside:
- one compact fixed-focus CVBS/AHD board camera;
- LED illumination around the lens;
- one PAN motor;
- one ROTATE motor;
- slip ring only where required for continuous rotation;
- temperature/current protection where needed.

Deleted from baseline:
- motorised focus;
- focus motor PCB;
- proprietary angle-encoder PCBs unless a simple home/position sensor proves necessary;
- proprietary camera control boards.

The crawler controller drives the camera-axis H-bridge; the camera head itself should contain as little electronics as possible.

## Reel electronics — nearly passive
Preserve RMP300 mechanics:
- manual drum;
- brake;
- level wind;
- measuring wheel;
- slip ring.

Replace the proprietary meter-counter PCB with:
- a magnet + Hall sensor or small encoder on the measuring wheel;
- pulse counting in the console MCU.

The reel therefore has no complex control PCB.

## Console
- 7-inch CVBS monitor already selected for PX-1;
- simple MCU;
- joystick;
- traction-speed control;
- light control;
- PAN / ROTATE / HOME controls;
- distance zero;
- pressure indication;
- hardware E-stop that removes traction power independently of software;
- simple OSD over analog video.

## 6-core tether functional allocation
Retain the Proteus-like single reinforced six-core copper inspection cable.

Provisional functional allocation:
1. power +
2. power return
3. RS-485 A
4. RS-485 B
5. balanced video +
6. balanced video -

No coax, no optical fibre and no bundle of separate loose cables.

## Tether voltage rule
Do not freeze 24 V, 48 V or another feed voltage until the actual 40 m cable sample is measured end-to-end.

Measure:
- resistance of each conductor;
- round-trip resistance of the intended power pair;
- voltage at the crawler under representative drive/camera/light load.

If direct low-voltage feed is acceptable at 40 m, use it because it is simplest.
If voltage drop is excessive, use a higher DC tether voltage and one ready-made crawler DC/DC converter. Do not recreate the proprietary MiniCam high-voltage power board.

## Service rule
Every electronics module must be removable without machining the crawler and replaceable from a current commercial source or by a documented equivalent.