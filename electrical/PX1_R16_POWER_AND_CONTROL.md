# PX-1 R16 — power and motor-control baseline

This is the component baseline matched to the R16 dry-bay reserve.  It is not
an electrical safety approval and is not a substitute for the final tether,
fusing, creepage or thermal drawings.

## Selected modules

| Function | Selected part | R16 placement/status |
|---|---|---|
| HV tether to crawler bus | Mean Well RSD-60H-24 | Body reserve 128×60×25 mm; 40…160 VDC input, 24 V/2.5 A, 60 W candidate |
| Traction motors | 2× Pololu 4695, 24 V, 100:1, encoder | Two 37D envelopes staggered along X in the sealed body |
| Traction/camera bridges | 4× Adafruit 3190 DRV8871 | Four carriers on the high service rail; two traction and two camera channels |
| Body controller | NUCLEO-F446RE | 82.5×70 mm reserve on the rear tray |
| Camera | RunCam Phoenix 2 SE V2 | Board stays in the separate armoured pod |
| Command link | Isolated TTL→RS485 module | Body reserve beside the video transmitter |

## Power budget for the first 40 m demonstrator

The R16 mechanical reserve is based on the traction drivers being configured
for a **0.64 A/channel bench current limit** and the two camera channels being
limited to the lower candidate in the inherited BOM.  At 24 V, the two traction
channels consume at most about 30.7 W under that *electronic* limit.  The camera
12 V rail, imager, LEDs, MCU, RS485 and video transmitter have to be measured;
they are not granted the motor stall current.  The RSD-60H-24 60 W rating is
therefore a bounded prototype target with thermal logging, not an unlimited
stall-power allowance.

The Pololu 4695 page explicitly gives 24 V/100 RPM/100 mA no-load and a 3 A
extrapolated stall current, and warns that stall values are not continuous
ratings.  The firmware must stop on timeout, over-current, undervoltage and
loss of tether interlock; current limiting is a protection layer, not a torque
specification.

## Firmware mapping

The existing `firmware/crawler/r12/` host-tested drive core remains the starting
point.  R16 must carry a new hardware-profile revision before flashing:

- the two traction channels keep the R12 PA6/PA7 and PB0/PB1 PWM allocation;
- encoder inputs remain PA0/PA1 and PB6/PB7 only after confirming 3.3 V levels;
- the two camera channels are driven through the second DRV8871 pair and a
  separate lift/pod harness;
- timeout, explicit re-arm, reverse dwell and emergency stop remain mandatory;
- no code is flashed or claimed tested on hardware in this CAD-only gate.

The nominal pin allocation is recorded in
`firmware/crawler/r16/hardware_profile.json`.  It keeps the tested R12 traction
and encoder map, reserves TIM1 PA8..PA11 for four independent camera-driver
inputs, and moves the optional camera UART to PC6/PC7.  This file is a harness
and packaging contract only; verify alternate functions, connector breakout,
encoder voltage and the purchased carrier revision before producing a BIN.

## Required electrical gates

1. Prove the RSD-60H-24 input/output isolation and surge protection with the
   actual six-core tether and connector.
2. Log bus voltage, RSD temperature, both motor currents and camera load under
   wet/blocked-wheel tests.
3. Verify DRV8871 current-limit resistor values and thermal rise on the real
   copper/heat-spreader arrangement.
4. Add a hardware contactor/precharge/discharge path at the surface source;
   do not rely on firmware for high-voltage isolation.
5. Update the flashable hardware profile only after pin, encoder, connector and
   E-stop continuity are measured.

References: [Mean Well RSD-60 datasheet](https://www.meanwell.com/Upload/PDF/RSD-60/RSD-60-SPEC.PDF),
[Pololu 4695](https://www.pololu.com/product/4695).
