# PX-1 Rev.BH — camera head internal layout

Status: PROTOTYPE ARCHITECTURE. Final motor/gearbox and connector part numbers remain HOLD until exact purchased dimensions are verified.

## Target external envelope
- camera head OD: <=52 mm
- cylindrical body length target: 72 mm maximum excluding quick-release nose
- separate dry/pressurized camera head from crawler main body
- front optical window flush/protected

## Functional stack
Front to rear:
1. protective front bezel + optical window;
2. LED ring / illumination PCB carrier;
3. camera module volume;
4. TILT axle/yoke bearings;
5. compact TILT actuator and reduction;
6. continuous ROLL bearing set;
7. ROLL drive gear/motor;
8. rotary electrical transfer/slip-ring or equivalent continuous-roll service interface;
9. rear quick-release connector and mechanical latch.

## TILT architecture
- range: -105..+105 deg
- hard mechanical stops outside commanded range
- target pivot shaft: 5–6 mm stainless
- two miniature radial bearings preferred over plain aluminium-on-steel pivot
- drive must be self-holding enough to prevent head droop when power is removed, or use a mechanical brake/friction preload that does not prevent service

## ROLL architecture
- continuous 360 deg
- no cable winding allowed
- two-bearing support preferred to resist camera head side load
- electrical path must tolerate unlimited rotation; no fixed pigtail through the roll axis
- index/home sensing allowed but must not mechanically limit rotation

## Illumination
- LEDs arranged symmetrically around optical window where practical
- LEDs and driver thermally coupled to metal head shell
- illumination module replaceable independently of camera module
- avoid placing high-current PWM wiring immediately adjacent to CVBS path

## Sealing
- camera head is independently sealed from crawler body
- static joints use FKM O-rings
- rotating joints require dedicated rotary seals or fully isolated internal rotary arrangement
- quick-release connector must remain behind its own environmental seal boundary

## Serviceability
Target service sequence:
1. disconnect rear quick connector;
2. release one positive latch/retainer;
3. remove complete head;
4. bench-service bezel/window/LED/camera/TILT/ROLL as submodules.

## Release holds
- exact camera module dimensions;
- exact TILT motor/gearbox dimensions;
- exact ROLL motor/gearbox dimensions;
- exact slip-ring/rotary-transfer part;
- final front window material/thickness;
- exact quick-release connector shell and insert;
- thermal test at full LED power;
- full DN150 clearance re-check after real purchased part envelopes are inserted.
