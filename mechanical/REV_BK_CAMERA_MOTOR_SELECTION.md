# PX-1 Rev.BK — exact camera-axis motor selection and drive concept

Status: engineering selection for prototype; not yet machining release.

## Selected common motor
Use one motor type for both TILT and ROLL to simplify spares:

**DCGM-N20-12V-EN-200RPM**
- 12 V
- no-load speed: 200 rpm
- gearbox ratio: 1:150
- Hall encoder: 1050 PPR at output according to supplier datasheet
- stall torque: >=1.2 kg·cm (~0.118 N·m)
- stall current: <=1.1 A
- all-metal geartrain

This motor is preferred over an unknown generic 30–60 rpm N20 because it has a documented encoder, torque and current specification and fits the existing N20-class envelope.

## TILT drive decision
Use a **worm reduction** after the N20 gearbox rather than a simple spur pair.

Prototype target:
- worm ratio: ~20:1
- motor output at 200 rpm -> camera tilt output ~10 rpm nominal before PWM control
- expected available torque is far above the static camera gravity torque requirement even after conservative worm losses
- worm stage is selected primarily for compactness and resistance to back-driving, not because raw motor torque is insufficient

Self-locking is NOT assumed from ratio alone. Final worm lead angle, materials, lubrication and efficiency must be checked physically. If the built worm is back-drivable, add a positive holding brake/detent rather than relying only on powered motor braking.

## TILT torque budget
Conservative first packaging estimate:
- moving camera/head mass acting about TILT axis: 0.25 kg maximum target
- center-of-mass eccentricity: 30 mm maximum target
- static gravity torque = m*g*r ≈ 0.25*9.81*0.03 = 0.074 N·m
- design target with 3x static margin: >=0.22 N·m holding torque at TILT axis

The selected motor has ~0.118 N·m stall torque before the added worm stage, so torque capacity is not the limiting factor. Gear strength, backlash, sealing and holding behavior are the key design items.

## ROLL drive decision
ROLL remains spur-geared because it must rotate continuously and should remain efficient/reversible.

Prototype pair:
- module: 0.5
- pressure angle: 20°
- pinion: z17
- driven gear: z51
- ratio: 3:1
- pitch diameters: 8.5 / 25.5 mm
- nominal center distance: 17.0 mm
- theoretical output speed at full motor speed: ~67 rpm; normal commanded speed will be lower under encoder/PWM control

z17 is used to avoid the severe undercut problem of a tiny 12-tooth standard pinion.

## Electrical implication
Each camera-axis motor can approach ~1.1 A stall current. Driver sizing must therefore allow at least 2 A peak per motor with margin, current limiting and fault shutdown. Do not drive either motor directly from STM32 pins.

## Release gates
1. obtain/measure exact physical dimensions of purchased DCGM-N20-12V-EN-200RPM;
2. bench-measure motor no-load current, stall/limited torque and backlash;
3. make first worm/wheel pair and test back-driving over temperature/lubrication;
4. verify TILT axis holding >=0.22 N·m without overheating;
5. generate exact z17/z51 involute gear CAD;
6. re-run Ø52 camera-head and DN150 clearance checks.
