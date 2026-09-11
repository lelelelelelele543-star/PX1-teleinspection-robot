# PX-1 Rev.B — WB10 three-zone pressure / leak / temperature telemetry

Date: 2026-09-11
Status: PRESSURE SENSOR FAMILY FROZEN / PNEUMATIC PORT GEOMETRY HOLD / LEAK PROBE BENCH HOLD

## 1. Scope and unchanged mechanical baseline

WB10 implements the previously approved three dry pressure zones:
- `P0 BODY` — central electronics/motor body;
- `P1 LEFT DRIVE` — left side gear bay;
- `P2 RIGHT DRIVE` — right side gear bay.

Normal fill remains:
- +0.20...+0.30 bar gauge at surface;
- +0.25 bar typical target.

The three zones remain normally isolated after filling. WB10 does **not** create a permanent open manifold between them.

Required operator data:
- BODY pressure;
- LEFT DRIVE pressure;
- RIGHT DRIVE pressure;
- pressure-decay warning;
- pressure sensor temperature data;
- direct P0 liquid-ingress warning as a secondary protection layer.

## 2. Pressure sensing method correction

Do not use a simple 0...50 kPa gauge sensor inside a sealed zone with its reference port exposed to the same internal air. It would read incorrectly because both sides of the diaphragm would see the same pressure.

Rev.B uses **absolute digital pressure sensors**.

Gauge pressure shown to the operator is calculated from:

`P_gauge = P_zone_absolute - P_surface_ambient_absolute`

This avoids routing an atmospheric reference tube into each sealed crawler zone.

## 3. Selected pressure-sensor family

### Adafruit LPS28 (ST LPS28DFW) breakout

Selected ready module:
- manufacturer of breakout: Adafruit;
- product: `Adafruit LPS28 (LPS28DFW) Pressure Sensor - STEMMA QT / Qwiic`;
- Adafruit product ID: `6067`;
- sensing IC: STMicroelectronics `LPS28DFW`;
- IC lifecycle: active / volume production at the Rev.B check;
- absolute pressure sensor;
- selectable pressure full scale:
  - 260...1260 hPa;
  - 260...4060 hPa;
- absolute pressure accuracy class: ±0.5 hPa;
- pressure noise class: 0.32 Pa;
- 24-bit pressure output;
- integrated temperature compensation;
- embedded temperature output;
- 1...200 Hz output data rate;
- I2C / I3C sensor interface;
- breakout accepts 3.3 V / 5 V logic/supply use;
- default I2C address 0x5C, selectable 0x5D;
- small metal pressure port suitable for thin tube;
- breakout dimensions: 25.4 x 17.8 x 4.8 mm;
- breakout mass: ~1.8 g.

Official references:
- ST: `https://www.st.com/en/mems-and-sensors/lps28dfw.html`
- Adafruit: `https://www.adafruit.com/product/6067`

Approved marketplace route exists for Adafruit 6067 on Allegro.

Marketplace reference:
`https://allegro.pl/oferta/stemma-qt-lps28-lps28dfw-pressure-sensor-modul-z-czujnikiem-cisnienia-17755263747`

## 4. Mandatory full-scale mode

All crawler pressure sensors are configured in the **4060 hPa mode**.

Reason:
- normal atmosphere near sea-level is approximately 1013 hPa;
- adding the normal +0.25 bar fill gives approximately 1263 hPa absolute;
- this can already exceed the lower 1260 hPa full-scale mode before tolerances/weather are considered.

Therefore using 1260 hPa mode would create a hidden saturation risk at the normal fill target.

The 4060 hPa mode has ample range for the normal pressurized dry-body measurement.

## 5. Four identical pressure modules in the complete system

Use one sensor family everywhere:

Crawler:
- 1 x `P0 BODY` sensor;
- 1 x `P1 LEFT` sensor;
- 1 x `P2 RIGHT` sensor.

CCU:
- 1 x `PAMB` surface ambient sensor.

Total complete system:
- 4 x Adafruit 6067.

Field spare target:
- +1 x Adafruit 6067.

This is preferable to mixing a crawler gauge sensor with a different console barometer because service, calibration and firmware remain common.

## 6. Crawler I2C address conflict and selected solution

Three identical LPS28 sensors cannot all be placed directly on one I2C bus because the sensor offers only 0x5C/0x5D addressing.

Do not solve this with three separate software-I2C implementations or by modifying the NUCLEO hardware.

Selected ready module:
- Adafruit TCA9548A I2C Multiplexer;
- product ID `2717`;
- 8 downstream I2C channels;
- module I2C address configurable 0x70...0x77;
- supply/logic: 3...5 V class;
- dimensions: 30.6 x 17.6 x 2.7 mm;
- mass: ~1.8 g;
- ready module, no custom PCB.

Official reference:
`https://www.adafruit.com/product/2717`

Marketplace route exists on Allegro as Adafruit 2717/TCA9548A.

### Channel assignment

On crawler I2C1 PB8/PB9:
- INA226 LEFT remains on direct main I2C bus;
- INA226 RIGHT remains on direct main I2C bus;
- TCA9548A address 0x70 remains on direct main I2C bus;
- TCA channel 0 -> P0 LPS28 at 0x5C;
- TCA channel 1 -> P1 LPS28 at 0x5C;
- TCA channel 2 -> P2 LPS28 at 0x5C.

No pressure-sensor address straps are required. A replacement sensor can remain at its default 0x5C address.

## 7. Sensor physical location — keep electronics out of side gear bays

Rev.B preferred packaging keeps all three pressure sensor PCBs on one protected electronics carrier in P0.

P0 sensor:
- its pressure port samples P0 directly through a short protected opening/tube.

P1/P2 sensors:
- each pressure port receives its own **individual dead-ended pneumatic sense line** from the corresponding side-drive volume;
- the lines are not connected to each other;
- they are not connected to the fill manifold after the branch check valves;
- each line ends only at its own LPS28 sensing diaphragm.

Why:
- no I2C/power wires need to cross the P0/P1 or P0/P2 flood barriers;
- no electronic PCB sits beside wet/greased wheel gears;
- the pressure sensor board remains field-accessible with the main electronics cover removed.

## 8. Side-zone pressure sense line safety

The pneumatic sensing penetrations are a new fault path and therefore cannot be treated casually.

Requirements for each P1/P2 line:
- one dedicated sealed bulkhead passage;
- smallest practical bore/capillary consistent with acceptable pressure response time;
- no common tee between P1 and P2;
- no common open volume with P0;
- hose mechanically retained at both ends;
- pressure sensor port remains above the lowest expected water path where packaging allows;
- route includes a small flow-restricting capillary/orifice close to the side-zone boundary so a downstream hose failure does not instantly equalize zones;
- exact tube ID/OD, bulkhead article and restrictor bore remain a mechanical sample-fit gate.

If a side bay floods, water may enter its pressure sense tube and reach the water-resistant LPS28 port. This is acceptable as a fault indication only; after any water ingress, the affected sensor/tube is inspected and dried/replaced before return to service.

Do not rely on the sensor's water-resistant package as a structural flood barrier.

## 9. Pressure computation at the CCU

Crawler sends raw/filtered absolute pressure and temperature for P0/P1/P2.

CCU measures local ambient absolute pressure `PAMB` with its own Adafruit 6067.

Display values:

`P0_g = P0_abs - PAMB_abs`

`P1_g = P1_abs - PAMB_abs`

`P2_g = P2_abs - PAMB_abs`

Conversion:
- 1000 hPa = 1 bar;
- therefore 250 hPa difference = +0.25 bar gauge.

## 10. Accuracy screen

One LPS28 absolute accuracy class is approximately ±0.5 hPa.

Worst simple subtraction of crawler sensor and CCU ambient sensor gives an order-of-magnitude worst-case static error of approximately ±1 hPa before installation/calibration effects.

That equals approximately:
- ±0.001 bar;
- ±0.1 kPa.

This is far smaller than the current pressure alarm spacing:
- fill target ~+0.25 bar;
- warning ~+0.17 bar;
- stop/inspect ~+0.10 bar.

Thus sensor resolution/accuracy is not the limiting factor. Tubing, temperature gradients, sealing and calibration dominate the practical system.

## 11. Temperature compensation and leak detection

Pressure alone changes with gas temperature even in a perfectly sealed fixed volume.

Firmware must therefore record temperature with each pressure sample.

For trend diagnostics, use a normalized sealed-gas metric proportional to:

`P_abs / T_kelvin`

for each zone, with a stored reference after the crawler has thermally settled at fill time.

Do not interpret a slow pressure change during rapid cooling after immersion as an automatic seal failure without temperature context.

Alarm logic uses two layers:
1. absolute/gauge minimum threshold;
2. temperature-aware pressure-decay rate.

A rapid pressure loss remains a fault even if the absolute threshold has not yet been crossed.

## 12. Starting pressure alarm policy

Keep the earlier Rev.DH thresholds as initial engineering values:
- fill target: +0.25 bar typical;
- acceptable fill band: +0.20...+0.30 bar;
- warning: <+0.17 bar before deployment or unexpected temperature-corrected decay;
- stop/inspect: <+0.10 bar or rapid pressure loss.

These values remain firmware-configurable until submerged thermal tests are complete.

No automatic compressor is installed in the crawler. A falling pressure must identify a fault, not trigger continuous air injection.

## 13. Pressure sample rate

Pressure zones do not require 200 Hz telemetry.

Starting firmware settings:
- sensor acquisition: 10 Hz per zone;
- transmit operator pressure: 5...10 Hz;
- 1 s moving average for displayed pressure;
- maintain a faster raw trend buffer for rapid pressure-loss detection;
- store time-stamped pressure + temperature snapshots in the fault log.

## 14. Direct P0 water-ingress probe

Pressure decay is the primary early leak detector.

Add one independent conductivity probe at the lowest practical point of P0 as a final direct water-presence warning.

Mechanical electrodes:
- 2 x small 316/A4 stainless electrodes/screws;
- insulated from the aluminum body;
- electrode tips separated approximately 5...10 mm;
- positioned where leaked water would collect but normal condensation/splash from service cannot bridge them easily.

No exposed copper PCB water-sensor module is selected because sewer moisture and condensation would corrode it and make its threshold unreliable.

### Low-current sampled interface — no custom PCB

Harness-level components only:
- MCU `PB15` = leak excitation;
- 100 kOhm series resistor from PB15 to electrode A;
- electrode B -> `PC0 / ADC1_IN10`;
- 1 MOhm resistor from PC0 to logic GND;
- optional 10 nF ADC filter at the MCU end after bench testing.

Sampling:
- PB15 normally LOW/high-Z according to firmware safety implementation;
- drive excitation only for approximately 5...10 ms during a sample;
- sample at approximately 1 Hz;
- return excitation inactive after ADC conversion.

This keeps average electrolytic current extremely small.

Exact wet threshold is calibrated using clean water and representative dirty/ionic water. Any detected liquid is a latched warning/fault until inspected; the operator is not encouraged to continue operation merely because pressure remains positive.

## 15. Electronics temperature channel

LPS28 provides temperature associated with the pressure sensor electronics and is used for pressure trending.

The existing separate `PC2 / ADC1_IN12` electronics-temperature channel is retained for a later dedicated thermistor/temperature sensor on the main HV->24 V converter or heat spreader.

Do not substitute P0 air temperature for converter baseplate temperature when implementing thermal derating.

## 16. MCU map delta

Rev.B WB10 changes the previous logical map:
- old `PC0 PRESSURE_ADC` is retired because pressure is now digital I2C;
- PC0 becomes `LEAK_ADC`;
- PB15 becomes `LEAK_EXCITE`;
- PB8/PB9 remain I2C1 for INA226 + TCA9548A;
- P0/P1/P2 sensors are behind TCA9548A channels 0/1/2.

No traction, RS-485, camera UART or safety pin is moved.

## 17. Failure behavior

If one pressure sensor is missing/invalid:
- identify exact zone;
- show `PRESS SENSOR FAULT` for that zone;
- inhibit deployment until operator deliberate override/service mode;
- do not substitute another zone pressure numerically.

If TCA9548A is missing:
- all three crawler pressure channels fault;
- traction enable remains inhibited for normal field mode.

If ambient CCU sensor fails:
- crawler can still transmit absolute pressure;
- display gauge values as unavailable rather than assuming 1013 hPa;
- service mode may show raw absolute values.

If P0 leak probe becomes wet:
- latch leak warning/fault;
- command traction stop/coast according to fault policy;
- CCU removes tether HV after controlled stop/safety handling;
- require inspection before reset.

## 18. WB10 BOM delta

Crawler:
- 3 x Adafruit 6067 LPS28 pressure module;
- 1 x Adafruit 2717 TCA9548A I2C multiplexer;
- 2 x A4/316 stainless leak-probe electrodes;
- 1 x 100 kOhm resistor;
- 1 x 1 MOhm resistor;
- pneumatic sense tubing/fittings after mechanical sample qualification.

CCU:
- 1 x Adafruit 6067 LPS28 ambient pressure module.

Recommended spare:
- 1 x Adafruit 6067.

## 19. WB10 release gates

1. buy/measure one Adafruit 6067 sample;
2. verify operation on 5 V logic rail / NUCLEO I2C configuration;
3. verify 4060 hPa mode and raw temperature data;
4. bench three identical sensors through Adafruit 2717 at channels 0/1/2;
5. compare all three sensors at common atmospheric pressure and record offsets;
6. pressure all three lines to +0.25 bar gauge and verify calculated values against a reference gauge;
7. freeze pneumatic tube/port geometry only after physical sample fit;
8. perform 30 min sealed pressure/temperature trend test;
9. perform P1/P2 sense-line failure simulation and verify zones are not directly interconnected;
10. calibrate leak-probe ADC with dry, condensation and representative contaminated-water cases;
11. repeat submerged static and rotating-wheel pressure-decay tests;
12. verify CCU ambient-sensor subtraction over changing local barometric pressure.

## Change log

### 2026-09-11 — WB10
- selected current-production ST LPS28DFW via ready Adafruit 6067 modules;
- rejected low-range 1260 hPa mode because normal +0.25 bar fill can exceed it at normal atmospheric pressure;
- selected 4060 hPa mode;
- standardized four identical absolute pressure modules across crawler + CCU;
- selected Adafruit 2717 TCA9548A to avoid the three-identical-address conflict without custom PCB;
- kept all sensor electronics in P0 and moved P1/P2 pressure via independent dead-ended pneumatic sense lines rather than wiring through flood barriers;
- retained three-zone isolation and prohibited common pneumatic tees;
- added ambient subtraction and temperature-aware pressure-decay logic;
- replaced generic corrosive water-sensor boards with a sampled low-current stainless P0 conductivity probe;
- reassigned PC0 from obsolete analog pressure input to leak ADC and PB15 to leak excitation.
