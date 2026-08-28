# PX1 Rev.PG — RMP300 reel electrical simplification

## Rule
Keep the proven RMP300 mechanical architecture. Replace only proprietary/unavailable electrical parts.

## Source basis
- ASS-004-097 RMP300 reel assembly
- ASS-004-094 left/slip-ring side
- ASS-004-092 meter counter assembly
- ASS-002-696 measure unit

## Slip ring replacement
Preferred prototype candidate: **SenRing M220-0605**
- capsule OD: 22 mm
- length: 40 mm
- 6 circuits
- 5 A per circuit
- voltage range: 0..240 VAC/VDC
- contact: precious metal / gold-gold
- electrical noise: <0.01 ohm manufacturer figure
- standard stock model
- IP51: mount inside the protected RMP300 left-side enclosure; it is NOT a water-pressure boundary

PX1 six-core mapping through reel:
1. PWR+
2. PWR-
3. RS485_A
4. RS485_B
5. VIDEO+
6. VIDEO-

No coax, no optical fibre, no separate loose twisted-pair cable architecture.

## Meter counter replacement
Delete proprietary meter-counter PCB.
Retain original mechanical measure unit: rollers, spring loading, measuring wheel, shaft and 618/8 bearings.
Preferred sensor architecture: **AS5600 magnetic angle sensor module** with diametrical magnet on the measuring-wheel shaft.
- contactless, no encoder-wheel wear
- 12-bit absolute angle
- I2C / analog / PWM class interface
- firmware unwraps successive 0..360 degree readings into cumulative distance
- calibration constant is measured wheel circumference under actual cable compression, not nominal CAD diameter

Distance equation:
`distance = accumulated_turns * calibrated_effective_circumference`

Calibration procedure:
1. Load the real tether through the RMP300 measure unit at normal spring pressure.
2. Mark exactly 10.000 m of tether.
3. Record accumulated AS5600 angle/turns over that length.
4. Store effective mm/rev in console settings.
5. Repeat forward/backward; reject if hysteresis exceeds 0.5% before investigating roller pressure/slip.

## Interface
Reel itself remains manual and mechanically passive.
Only these low-complexity electronics live on/near reel:
- slip ring
- AS5600 sensor module
- optional small sealed junction box

No proprietary reel controller PCB and no reel motor.

## Status
Prototype architecture frozen. Exact purchased AS5600 carrier board and mechanical magnet holder remain BOM/detailing items.
