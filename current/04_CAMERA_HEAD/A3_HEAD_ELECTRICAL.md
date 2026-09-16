# A3 head electrical architecture

Status: BENCH WIRING FROZEN / PAN-ROTATE MOTOR ARTICLES STILL H08.

## Local supply
Crawler provides `+12V_HEAD` and `GND_HEAD` to the removable camera head.

Initial head current budget:
- RunCam Phoenix 2 family: use 0.20 A design allowance at 12 V;
- LED string A: 0.35 A;
- LED string B: 0.35 A;
- local MCU / logic / future two small motor drivers: reserve 0.40 A average for bench planning;
- total initial continuous planning allowance: **1.30 A at 12 V**.

Bench supply current limit starts at 1.5 A and may be raised only when pan/rotate motor stall/current measurements exist. The crawler head branch should ultimately have its own protection independent from traction.

## Power tree
```text
+12V_HEAD
  |
  +-- camera branch filter --> RunCam Phoenix 2
  |
  +-- LED driver A --> 3x white XP-G series string
  |
  +-- LED driver B --> 3x white XP-G series string
  |
  +-- 12->5V ready-made regulator --> head MCU / sensors
  |
  +-- future motor-driver branch --> PAN + ROTATE motors

GND_HEAD -------------------------- common power reference
CVBS_SIGNAL / CVBS_RETURN -------- separately routed video pair
```

For the first bench, keep the camera branch physically separated from LED-driver switching loops. Place local bulk capacitance near the camera and test both LED PWM frequency and harness routing for visible bands/sync loss.

## Lighting
Candidate driver family: ready-made PT4115 adjustable constant-current modules, one per three-LED string.

PT4115 device limits useful to the bench:
- buck constant-current topology;
- 6…30 V input class;
- up to 1.2 A device current class;
- DIM accepts PWM; published PWM range extends from roughly 100 Hz to >20 kHz;
- current relation at device level is approximately `ILED = 0.1 / Rsense`.

PX1 does not require changing module sense resistors if adjustable modules are used. Set **350 mA** by ammeter/current-limited bench supply and record the setting before installation.

Two independent drivers are mandatory for the two 3-LED strings; no uncontrolled parallel LED strings.

## Camera
RunCam Phoenix 2 family is used because it directly supplies CVBS, accepts a wide DC input and fits a ~19 mm package. For PX1 Rev.A:
- set PAL unless the console/video receiver requires NTSC;
- set 4:3 initially because it is the conventional inspection-monitor format;
- mechanically set M12 focus during assembly;
- lock the lens after focus verification;
- **remote focus motor is omitted from Rev.A** unless pipe tests prove it necessary.

This deliberately removes the source CAM026 focus motor/gear/PCB while preserving pan, rotate and lighting. It reduces head volume and failure modes without changing crawler mechanics or the six-wire harness.

## Six-pin quick-disconnect numbering
Logical numbering is frozen now so firmware/wiring can progress; physical connector contact numbering is released only after the exact SP13 sample/datasheet is confirmed.

| PX1 logical pin | Net | Direction |
|---|---|---|
| H1 | +12V_HEAD | crawler -> head |
| H2 | GND_HEAD | return |
| H3 | UART_TX_CRAWLER_TO_HEAD | crawler -> head |
| H4 | UART_RX_HEAD_TO_CRAWLER | head -> crawler |
| H5 | CVBS_SIGNAL | head -> crawler |
| H6 | CVBS_RETURN | video return |

Never infer physical pin numbers from this logical table. `H1..H6` are PX1 net identifiers until the real connector is frozen.

## Head controller
`RP2040-Zero` remains a compact ready-made candidate for A3 pan/rotate control. It provides more than enough UART, PWM, ADC/I2C and GPIO resources. It is not needed for the static camera/light test, so A3.0 can proceed even if the controller is not yet purchased.

## Pan/rotate drivers
The source CAM026 used separate DC motors and separate control electronics for focus/rotate; PX1 uses its own electronics. If the selected PAN/ROTATE motors are small brushed DC gearmotors, two DRV8871-class ready-made modules are acceptable for the bench. Exact motor current/stall current must be known before final driver release.

## EMC rules for A3 bench
- LED-switch current loops short and away from CVBS conductors;
- motor wires twisted locally where practical;
- add suppression directly at brushed motor terminals when motors are selected;
- route CVBS signal and return together through the dynamic harness;
- do not share CVBS return with LED/motor current;
- PWM edges are tested at multiple duty cycles while viewing a dark and bright scene;
- verify video with traction motors operating, not only on a clean desktop supply.

## Bench test points
- TP1: +12V_HEAD at quick disconnect;
- TP2: camera 12 V after branch filter;
- TP3: LED string A current;
- TP4: LED string B current;
- TP5: 5 V head logic rail;
- TP6: CVBS signal/return at crawler-side end of local harness.

Record voltage/current and thermal values in A3 test sheet before moving the circuit into a sealed metal head.
