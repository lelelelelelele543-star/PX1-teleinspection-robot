# PX-1 field service procedure — six-core camera/lift harness

Revision: Rev.B / WB23G draft
Status: **prototype service method; torque/leak acceptance values pending qualification**

## Controlled harness

The replaceable wet lift harness has exactly six insulated conductors:

1. +12V_HEAD
2. GND_HEAD
3. UART_TX
4. UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

Overall shield, if present, is EMC only and is not DC return.

Current dry service connector candidate is a six-way Molex Micro-Fit 3.0 pair. Camera quick disconnect remains six-pin WEIPU SP13.

## Safety / preparation

The crawler must be de-energized and fully depressurized before opening any pressure-boundary cover. Never loosen the service cover while the body is pressurized.

Required state:

- crawler power OFF;
- head 12 V OFF;
- crawler pressure = ambient;
- exterior washed and dried around service cover;
- camera connector dry enough to open without carrying dirty water into the interface.

## Removal

1. Put camera/lift in a convenient low/service position.
2. Unscrew and disconnect the external SP13 camera plug.
3. Protect both SP13 halves from dirt/water.
4. Remove the two retained M4 screws from `PRESSURE / CAMERA SERVICE` cover.
5. Lift the cover only enough to access the internal six-way connector; do not pull conductors.
6. Release dry internal `J_CAM_LIFT` Micro-Fit connector by its latch, not by the wires.
7. Release internal cable clamp/strain relief.
8. Withdraw the complete cover + M12 gland + six-core local lift-harness assembly as one service item.
9. Inspect cover seal, groove, gland seal, cable jacket, guard-contact areas and SP13 backshell.

## Replacement harness pre-check

Before installation, verify 1:1 continuity of all six functions from dry connector to SP13. No combining or splitting of +12 V/GND is permitted in the local wet harness.

Also verify:

- no short between any insulated core and shield;
- cable OD is within the released gland/SP13 range;
- shield termination matches the current EMC test configuration;
- strain-relief parts clamp the jacket, not individual cores.

## Installation

1. Verify service-cover seal is clean, undamaged and not twisted.
2. Apply only a thin film of lubricant confirmed compatible with the chosen elastomer; do not fill the groove with sealant.
3. Connect dry six-way `J_CAM_LIFT` inside the body.
4. Refit internal strain relief so Micro-Fit contacts carry no cable tension.
5. Seat service cover squarely without trapping cable under the seal land.
6. Tighten both M4 screws progressively and evenly. Final torque comes from the released drawing after gasket-compression tests.
7. Route the six-core cable under the removable drain-open lift-arm guard with free motion at both ends.
8. Reconnect SP13 and perform continuity/video/control check before repressurizing.

## Mandatory leak check after opening

Prototype minimum:

1. pressurize to approximately +0.25 bar gauge;
2. allow temperature to stabilize;
3. record pressure decay for 30 min;
4. inspect cover perimeter, fill valve and M12 gland;
5. cycle lift several times and repeat gland/cable inspection;
6. only then return crawler to wet operation.

## Electrical return-to-service check

With crawler dry and safe:

- confirm camera supply voltage at the head;
- confirm UART commands both directions;
- confirm stable raw CVBS image;
- move lift and camera while watching for intermittent image/control;
- switch LEDs and traction motors to expose PWM/noise problems.

## Reject criteria

Do not return crawler to service if any of the following is present:

- cut/flattened pressure-cover seal;
- damaged sealing land;
- cable jacket nick in gland clamp or flex region;
- visible conductor tension at Micro-Fit or SP13;
- loose gland body;
- damaged connector latch/contact;
- pressure decay outside the qualified limit;
- continuous bubbles during controlled leak test;
- intermittent video/UART/power while moving the lift.
