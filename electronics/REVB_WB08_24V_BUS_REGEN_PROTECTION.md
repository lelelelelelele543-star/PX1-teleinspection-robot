# PX-1 Rev.B — WB08 24 V bus / regenerative-energy / traction-driver protection

Date: 2026-09-11
Status: CONTROL STRATEGY FROZEN / HARDWARE PASS-SCREEN / MOTOR-BENCH HOLD

## 1. Scope

Protect the 24 V bus downstream of the isolated HV->24 V converter against:
- motor reversal and braking energy;
- wiring-inductance spikes;
- driver over-voltage;
- branch faults;
- uncontrolled torque commands that can damage the compact bevel stage.

No crawler drivetrain architecture is changed.

## 2. Important BTS7960 corrections

The active prototype still uses two BTS7960 full-bridge modules because they are already part of the approved prototype architecture. They are **not** silently replaced in Rev.B.

However the original Infineon BTS7960 device is obsolete. Infineon has publicly recommended newer NovalithIC devices such as BTN8982TA in replacement discussions. Therefore BTS7960/IBT-2 is a prototype-only sourcing choice and a Rev.C driver replacement gate.

Official BTS7960 limits that control WB08:
- absolute VS maximum: 45 V;
- over-voltage lockout begins in the 27.6...30 V region;
- setting INH low switches both internal power switches OFF (standby/high impedance at that half bridge);
- recommended local low-inductance supply capacitor: about 470 nF close to each device;
- current-sense output IS is proportional to forward high-side current only;
- nominal current-sense ratio kILIS ~8500, but the published spread is very wide, especially at lower current.

### Consequence

The BTS7960 native current sense is **not accurate enough to be the only torque-limit sensor** for PX-1's ~1 A-class normal motor current. It remains useful for diagnostics/gross fault recognition after per-module calibration.

Likewise the device's internal ~40+ A semiconductor current limit is far too high to protect a m1 bevel pair or the ISL gearmotor. Mechanical protection must occur much earlier in firmware/current supervision.

## 3. Primary regenerative-energy strategy

PX-1 does NOT intentionally use aggressive electrical braking with the present isolated DC/DC source.

The main strategy is to avoid creating large regenerative events:

1. commanded speed changes use acceleration/deceleration ramps;
2. normal STOP ramps PWM toward zero;
3. both bridge enable/INH controls then go LOW so the motor coasts;
4. direction reversal is blocked until a coast interval and low-current condition are satisfied;
5. no direct `+PWM -> -PWM` hard reversal is permitted;
6. E-STOP disables traction and the CCU tether-HV chain; it does not command dynamic braking;
7. a bus over-voltage event immediately disables both traction bridges and latches a fault until bus voltage returns to a safe range.

This protects the DC/DC, driver, gearbox and bevels simultaneously.

## 4. Why a TVS is not the braking system

A TVS is retained only as a fast transient clamp.

It is not sized or controlled as a continuous dump load. Repeatedly forcing motor kinetic energy into a TVS during every stop would create unnecessary thermal stress and unpredictable life.

The bulk capacitors absorb small short energy packets; motion control prevents large events; TVS catches the residual high-voltage spike.

## 5. Selected fast bus clamp

### Littelfuse 1.5KE30A

Part:
- manufacturer: Littelfuse;
- part number: `1.5KE30A`;
- package: axial DO-201;
- mounting: through-hole / point-to-point, suitable for the no-custom-PCB prototype;
- reverse standoff: 25.6 V;
- minimum breakdown: 28.5 V;
- maximum breakdown: 31.5 V;
- maximum clamp: 41.4 V at ~36.7 A, 10/1000 us pulse;
- peak pulse power class: 1.5 kW;
- active production part; high distributor stock exists.

Quantity: 2, one at each traction-driver supply branch.

Installation:
- connected directly across +24V/GND at the driver power terminals with the shortest practical leads;
- cathode to +24 V, anode to GND;
- insulated mechanically so the axial body/leads cannot touch chassis;
- not placed remotely at the converter where cable inductance would reduce effectiveness.

### Why 1.5KE30A, not 1.5KE27A

`1.5KE27A` has only 23.1 V reverse standoff, below the nominal 24 V rail; it is therefore too close to continuous conduction/leakage for a 24 V bus.

`1.5KE30A` has 25.6 V standoff, while its 41.4 V maximum clamp remains below the BTS7960 45 V absolute supply limit.

Note: BTS7960 over-voltage lockout occurs much earlier, around 27.6...30 V. The TVS does not prevent that protection event; it protects the silicon from a higher transient after the driver has already entered OV protection.

## 6. Local bulk capacitors

### Nichicon UHE1H102MHD6

Part:
- manufacturer: Nichicon;
- part number: `UHE1H102MHD6`;
- 1000 uF;
- 50 V;
- radial through-hole;
- 16 x 25 mm;
- 7.5 mm lead spacing;
- 10,000 h @105 C;
- impedance ~25 mOhm at 20 C / 100 kHz;
- ripple current ~2.555 A @100 kHz;
- active part with large distributor stock.

Quantity: 2, one per traction-driver branch.

Installation:
- each capacitor physically close to its BTS7960/IBT-2 module supply input;
- mechanically clamped, not hanging on leads;
- observe polarity;
- lead loop kept short;
- the two branch capacitors form ~2000 uF total on the common 24 V traction bus when branch wiring is low impedance.

### Energy screen

Total C = 2.0 mF.

Additional energy accepted by the bank above 24 V:
- to 27.5 V: ~0.180 J;
- to 28.5 V: ~0.236 J;
- to 30.0 V: ~0.324 J;
- to 41.4 V: ~1.138 J.

For perspective, a nominal 8.5 kg crawler moving at ~0.113 m/s has only ~0.054 J translational kinetic energy. **This is not a complete braking-energy proof** because motor rotor/gear inertia, external tether force and a downhill/back-driven crawler can add energy. Physical reversal/downhill testing is still mandatory.

## 7. High-frequency decoupling requirement

Infineon recommends ~470 nF ceramic capacitance from VS to GND close to each BTS7960 device.

Commodity IBT-2 modules vary in layout and component quality. Before release:
- inspect the actual purchased module;
- verify a low-inductance local capacitor exists at each half bridge;
- if absent/poorly located, add a 470 nF >=50 V low-ESR film/ceramic part directly across the module power terminals or replace the module.

Do not assume every marketplace `BTS7960 43A` board follows the Infineon application circuit.

## 8. 24 V bus measurement

Bus voltage is on the isolated low-voltage side, so it may be measured directly by the STM32 ADC.

Prototype divider:
- Rtop = 100 kOhm, 0.1%, >=50 V working-voltage class;
- Rbottom = 6.8 kOhm, 0.1%;
- ADC filter capacitor = 100 nF;
- divider full-scale check at 45 V -> ~2.865 V, below a 3.3 V ADC rail;
- at 24 V -> ~1.528 V.

Use long ADC sample time because divider Thevenin resistance is several kOhm.

Firmware thresholds are provisional until the real bus is logged:
- normal: <=26.0 V;
- warning / commanded ramp-to-zero: >26.5 V;
- immediate traction INH low / fault latch: >=27.0 V;
- re-enable allowed only below 25.5 V after a stable delay and deliberate command.

These thresholds intentionally act before the BTS7960 hardware over-voltage lockout range.

## 9. Motor-current measurement strategy

### Layer 1 — BTS7960 IS outputs
Use for:
- fast gross-current/fault indication;
- cross-checking left/right asymmetry;
- detecting open/failed driver behavior.

Do NOT use raw nominal kILIS alone to convert IS voltage into a precision torque value. Infineon's published spread is too wide at low current.

### Layer 2 — external per-side branch sensor
Prototype candidate:
- ready-made `INA226 R010 / XA-292` class module;
- marketplace source available with a 0.01 Ohm shunt and ~10 A-class measurement use;
- bus voltage capability of INA226 class: up to 36 V, suitable for the 24 V branch;
- two modules required, configured to different I2C addresses;
- locate one upstream of each traction H-bridge.

Purpose:
- calibrated motor branch current;
- branch voltage/power telemetry;
- sustained current/torque limit;
- test logging.

Status: PROTOTYPE CANDIDATE, not Rev.C freeze. Marketplace INA226 modules have inconsistent shunts/layouts, so each purchased board must be inspected and calibrated against a bench ammeter/load.

If the selected module cannot provide two reliable addresses or adequate sampling speed, move to an industrial current-sensor module rather than sharing one sensor between motors.

## 10. Torque/current control hierarchy

Final current values cannot be frozen from motor catalogue data alone.

Bench calibration must measure, per motor:
- no-load current;
- current at 0.2 / 0.4 / 0.6 / 0.8 / 1.0 N.m output torque where safe;
- rpm at those points;
- temperature rise;
- left/right differences after the whole side gear train is assembled.

Current-control logic then uses two levels:
- `I_CONT`: sustainable continuous traction current corresponding to thermal and normal torque target;
- `I_JAM`: higher short threshold with tens-of-ms timer, below the current that would exceed the bevel/gearbox mechanical gate.

WB03 mechanical target remains primary:
- ~0.60 N.m motor output for ~50 N total crawler pull;
- provisional 0.65...0.80 N.m operating ceiling before final hardened bevel validation;
- no command approaching motor theoretical stall torque.

## 11. Direction-change state machine

Per side:

`DRIVE_FWD -> RAMP_DOWN -> COAST -> ZERO_CONFIRM -> DRIVE_REV`

Rules:
- `RAMP_DOWN`: PWM reduces to zero over a calibrated interval;
- `COAST`: both half-bridge INH/enable paths disabled;
- minimum prototype coast dwell: 150 ms starting value;
- `ZERO_CONFIRM`: require branch current close to zero; if later wheel/motor speed sensing is available, require near-zero speed too;
- only then enable opposite direction.

The 150 ms value is a test starting point, not a final physical constant. Increase it if the unloaded side still back-generates enough to lift the bus.

## 12. Stop modes

Three distinct modes are defined:

### NORMAL STOP
Ramp down -> coast. Default operator stop.

### JAM STOP
Immediately remove PWM, INH low, coast. Log current, bus voltage and fault. No automatic reverse.

### E-STOP
Hardware disables traction and commands the CCU HV chain OFF. The crawler coasts. Restart requires deliberate operator reset.

No automatic plug-braking mode is released in Rev.B.

## 13. Branch fuses

Per-side traction fuse remains HOLD pending motor bench data.

Do not select a fuse from the BTS7960's advertised `43 A` number; that figure is unrelated to the safe current of the motor, m1 bevel train or thin internal wiring.

Preliminary expected fuse class is a few amperes per side, time-delay, but exact rating follows measured startup/jam current and wire gauge.

The converter output itself is limited to ~6.3 A class, but converter electronic OCP is not a substitute for branch wire/fault protection.

## 14. Driver lifecycle risk

Current Rev.B prototype:
- 2 x BTS7960/IBT-2 modules retained because the architecture is already approved and modules are readily available on marketplaces.

Rev.C gate:
- BTS7960 silicon is obsolete;
- marketplace boards may use remarked/cloned devices and undocumented copper/thermal design;
- final production must either qualify a controlled-source module batch or migrate to a current production integrated H-bridge while keeping the same 24 V / two-side / gear-drive mechanical architecture.

A driver replacement does not justify changing Z16/Z40, side gears, wheel stations or tether architecture.

## 15. Validation calculations

Script:
`electronics/analysis/PX1_24VBus_RevB.py`

Validation:
`electronics/REV_B_WB08_VALIDATION.json`

Current state: `PASS_SCREEN` for voltage ratings and passive energy buffering.

This means only that:
- 50 V bulk capacitors have large bus-voltage margin;
- 1.5KE30A transient clamp is below the 45 V absolute BTS7960 ceiling;
- the proposed divider remains within the STM32 ADC range;
- the 2 mF bank can absorb small braking-energy packets.

It does NOT prove repeated downhill braking or hard reversal is safe.

## 16. WB08 closure gates

Before Rev.C:
1. inspect actual BTS7960 modules and document PCB/capacitor/current-sense circuitry;
2. install one 1000 uF/50 V branch capacitor and one 1.5KE30A per drive side;
3. calibrate external left/right current sensors;
4. log 24 V bus at cruise, stop, direction change, skid-turn and jam;
5. tune ramp/coast timing so normal operation does not repeatedly enter BTS over-voltage lockout;
6. perform worst-case rolling downhill/back-drive test on a secured crawler;
7. prove TVS temperature remains near ambient in normal operation — it must not act as a routine brake dump;
8. freeze branch fuse values from measured current;
9. test E-STOP behavior with oscilloscope on 24 V bus;
10. decide/qualify Rev.C production H-bridge source.

## Change log

### 2026-09-11 — WB08
- retained BTS7960 only as a Rev.B prototype driver and formally recorded its obsolete lifecycle status;
- rejected hard direction reversal and routine dynamic braking;
- selected coast-stop as the normal/e-stop mechanical-safe behavior;
- selected active Littelfuse 1.5KE30A axial TVS per traction branch;
- selected 2 x Nichicon UHE1H102MHD6 1000 uF / 50 V branch capacitors;
- added 24 V ADC monitoring with 100k/6.8k divider;
- documented that BTS7960 IS current sense is too inaccurate to be the only torque-control sensor;
- added external per-side INA226-class measurement as the prototype calibration/telemetry layer;
- left exact branch fuse and current thresholds measurement-driven.
