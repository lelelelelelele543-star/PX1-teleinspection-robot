# PX-1 Rev.BC — rear cover and tether interface

Status: DRAWING-CANDIDATE architecture; connector cutout remains HOLD until exact LEMO dimensional drawing is verified.

## Selected architecture
- removable rear pressure cover;
- universal waterproof quick-disconnect tether interface;
- project baseline connector family: LEMO EGG.5K.870.CLL5;
- connector is carried by the rear cover, not the main body;
- separate mechanical strain-relief/towing structure carries cable pull; connector contacts must not carry crawler towing load;
- cover remains replaceable as one service module.

## Rear cover candidate
- material: EN AW-6082 T6;
- plate thickness: 10 mm prototype;
- piloted into body end land;
- static FKM face O-ring around dry-volume perimeter;
- cover screws outside sealing line wherever practical;
- connector centered high enough to clear drivetrain and internal motor envelopes;
- lowering/towing eye mechanically tied to cover/body fasteners or dedicated load path, never to connector shell alone.

## Electrical allocation target
Tether must support at minimum:
1. +24 V supply;
2. 0 V return;
3. RS-485 A;
4. RS-485 B;
5. CVBS signal/coax center;
6. CVBS shield/return;
7. spare/service conductors where connector/cable configuration permits.

Final pin numbers are HOLD until the exact insert/contact arrangement for the purchased connector is verified from manufacturer documentation and matched to the selected tether cable.

## Service requirements
- disconnect tether without opening pressure body;
- replace rear cover/connector module independently;
- field re-termination must not require soldering directly to the main controller;
- internal connector harness terminates to a documented service connector/terminal interface;
- strain relief must tolerate repeated bending and cable pull independently of electrical contacts.

## Release holds
1. exact LEMO shell/insert dimensions;
2. matching cable-side plug and collet for actual tether OD;
3. pressure/water ingress rating of complete mated pair;
4. final pinout/current derating;
5. cover O-ring size/groove after connector and screw pattern are frozen;
6. towing-eye proof-load target.
