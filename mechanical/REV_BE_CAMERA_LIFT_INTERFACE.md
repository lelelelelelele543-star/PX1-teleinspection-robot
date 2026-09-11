# PX-1 Rev.BE — front cover, manual lift and camera-head interface

Status: DRAWING-CANDIDATE architecture / synchronized with WB15.

## Manual lift
- one-hand manual parallelogram mechanism;
- no external hinge penetrates the dry pressure body;
- lift fastens to dedicated front-cover hard points;
- symmetric geometry so service parts are interchangeable left/right where possible;
- target locked positions: LOW / DN150 SAFE / HIGH;
- lock must be mechanical and self-holding; camera mass must not back-drive the lift.

## Front-cover interface
- EN AW-6082 T6, 10 mm prototype plate;
- centered pilot into main pressure body;
- dedicated M5 hard points for lift reaction loads;
- central service aperture reserved for camera harness/quick-release submodule;
- crawler P0 pressure boundary remains closed by its own sealed interface; removing the camera head must not open crawler P0.

## Camera head requirements
- TILT: -105 to +105 degrees;
- ROLL: continuous 360 degrees;
- camera head independently replaceable from crawler body;
- camera head is a separate sealed/pressurized assembly;
- electrical connector carries no structural head load;
- mechanical register/latch carries bending, impact and axial retention.

## Electrical quick connector — WB15 correction

The earlier LEMO `0K.304` placeholder is superseded because the controlled `0K.304` insert has only four low-voltage contacts while the active Rev.B head interface requires six functions.

Prototype connector baseline:
- camera-head panel side: WEIPU `SP1312/P6-C`, male pins, 6-way, rear-nut panel mount;
- crawler/lift harness side: WEIPU `SP1310/S6I-N`, female sockets, 6-way cable plug;
- 5 A/contact, 125 V class;
- SP13 family IP68 when correctly assembled/mated;
- panel cutout Ø13 with 11.8 mm anti-rotation flat dimension;
- local panel thickness candidate 3.0 mm, manufacturer max 3.5 mm.

Six external functions:
1. +12V_HEAD
2. GND_HEAD
3. HEAD_UART_TX
4. HEAD_UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

Exact numeric pin numbers remain sample-inspection HOLD.

## Rear head register

Current mechanical target:
- Ø36-class keyed cylindrical/spigot register;
- connector centered inside register envelope;
- connector front OD ~19.5 mm leaves ~8.25 mm nominal radial mechanical protection inside Ø36;
- one retained mechanical latch/pin or captive clamp provides axial retention;
- anti-rotation key/register prevents connector or cable from carrying head torque.

The connector panel seal is pressure-qualified by WB15 testing; IP68 alone is not treated as proof of the camera-head positive-pressure boundary.

## Mechanical service rule

Removal sequence target:
1. disable camera-head 12 V branch;
2. unscrew/withdraw SP1310 cable plug;
3. release one retained mechanical clamp/pin;
4. remove camera head without opening crawler dry body;
5. lift remains attached to crawler.

Electrical connector remains tool-less but threaded. One-hand requirement applies to normal manual lift operation, not to a live one-motion head swap.

## Service clearance

Rev.B CAD reserves:
- ~49 mm plug-body envelope behind panel;
- >=55 mm solid axial keep-out;
- >=60 mm practical axial withdrawal/service clearance before fixed obstruction;
- cable bend clearance based on final 4...6.5 mm OD six-core head harness.

If the straight plug conflicts with the yoke/lift in the final solid model, connector orientation is revisited deliberately; no ad-hoc sharp cable bend is allowed.

## Design holds
1. exact camera-head mass and center of gravity;
2. exact TILT/ROLL motor/gearbox purchased dimensions;
3. exact SP13 purchased sample dimensions and moulded pin numbering;
4. WB15 pressure/leak result;
5. WB12 video result through SP13;
6. locking-pin diameter after bending/shear check;
7. arm thickness and pivot bearing/bushing selection;
8. front-cover perimeter O-ring groove after final fastener pattern;
9. full DN150 solid sweep with mated SP13 plug and harness envelope.

## Target fabrication philosophy
All lift arms remain simple 2D-profile parts or turned spacers/bushings. No hidden castings, custom hinges, cartridges/cassettes or inaccessible fasteners. Field assembly should use common M4/M5 fasteners and one retained lock pin wherever possible.

## Change log

### Rev.BE original
- established manual lift/front-cover/camera service interface;
- carried LEMO 0K.304 as an unverified placeholder.

### 2026-09-11 — WB15 synchronization
- identified 0K.304 as four-contact and electrically insufficient;
- replaced placeholder with exact six-pin WEIPU SP13 pair;
- added Ø36/Ø13 rear-register geometry and service-clearance requirements;
- separated connector ingress rating from actual camera-head pressure qualification;
- preserved mechanical quick-release and crawler P0 isolation.
