# PX-1 field service procedure — camera/lift harness

Revision: Rev.B / WB23C draft
Status: **prototype service method; torque/leak acceptance values pending qualification**

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
3. Protect camera-side and harness-side connector from dirt/water.
4. Remove the two retained M4 screws from `PRESSURE / CAMERA SERVICE` cover.
5. Lift the cover only enough to access the internal connector; do not pull conductors.
6. Release dry internal `J_CAM_LIFT`.
7. Release internal cable clamp/strain relief.
8. Withdraw the complete cover + M12 gland + local lift-harness assembly as one service item.
9. Inspect cover seal, groove, gland seal, cable jacket and connector backshell.

## Installation

1. Verify replacement harness pinout before placing it in crawler.
2. Verify seal is clean, undamaged and not twisted.
3. Apply only a thin film of lubricant confirmed compatible with the chosen elastomer; do not fill the groove with sealant.
4. Connect `J_CAM_LIFT` inside the dry body.
5. Refit internal strain relief so connector contacts carry no cable tension.
6. Seat service cover squarely without trapping harness under the seal land.
7. Tighten both M4 screws progressively and evenly. Final torque comes from the released drawing after gasket-compression tests; do not invent a generic field torque.
8. Route local harness under lift-arm guard with free motion at both pivots.
9. Reconnect SP13 and perform continuity/video/control check.

## Mandatory leak check after opening

Prototype minimum:

1. pressurize to approximately +0.25 bar gauge;
2. allow temperature to stabilize;
3. record pressure decay for 30 min;
4. inspect cover perimeter, fill valve and gland for leakage with approved method;
5. cycle lift several times and repeat gland/cable inspection;
6. only then return crawler to wet operation.

## Reject criteria

Do not return crawler to service if any of the following is present:

- cut/flattened seal;
- damaged sealing land;
- cable jacket nick in gland clamp region;
- visible conductor tension at connector;
- loose gland body;
- pressure decay outside the qualified limit;
- continuous bubbles during controlled leak test;
- intermittent video/UART while moving the lift.
