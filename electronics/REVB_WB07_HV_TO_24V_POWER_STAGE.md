# PX-1 Rev.B — WB07 tether HV -> 24 V crawler power stage

Date: 2026-09-11
Status: COMPONENT / PACKAGING BASELINE FROZEN — THERMAL & HV QUALIFICATION HOLD

## 1. Architecture check

This work block does not change the approved electrical architecture.

Active chain remains:

`CCU controlled 100-120 VDC -> reel/slip ring -> six-core tether HV+/HV- -> sealed tail connector -> local fuse/inrush/protection -> isolated commercial DC/DC -> 24 V crawler bus`

The first bench crawler is still permitted to run directly from a protected 24 V bench supply before the tether-HV stage is installed.

No custom high-voltage PCB is introduced. The selected converter is a complete commercial potted module. Wiring around it is serviceable point-to-point harness / insulated support hardware.

## 2. Previous power-study errors formally corrected

The following old studies are historical where they conflict with Rev.PP + WB06:

- `REV_CI_TETHER_POWER_VOLTAGE_DROP.md`: 48 V tether baseline — superseded.
- `REV_CK_DC_DC_SELECTION.md`: RSD-200C-24 from a 48 V tether — superseded.
- `REV_DJ_COMPACT_48_TO_24_POWER_CORRECTION.md`: CHB200W-48S24, 18-75 V input — physically useful class but electrically incompatible with the active 100-120 V long-tether bus.
- `REV_GS_TWO_MOTOR_POWER_BUDGET.md`: the corrected two-motor power budget remains useful, but its 60 V long-cable study voltage is superseded by WB06.

The active long-run source point is now approximately 120 VDC within the already approved 100-120 VDC system class.

## 3. Proteus comparison

The CRP-150 P01 repair archive confirms that the original crawler main board has a distinct `HIGH VOLTAGE` area, one 220 uF / 200 V electrolytic and two 330 uF / 50 V electrolytics. This supports the same high-level architecture: high-voltage cable-side power followed by local low-voltage power conversion.

It does **not** reveal enough information to copy MiniCam's converter topology, switching frequency, transformer, protection or exact bus voltage. PX-1 therefore intentionally uses a replaceable commercial converter instead of reproducing P01.

## 4. Main DC/DC selection — frozen Rev.B candidate

### Cincon CQB150W-110S24

Manufacturer: Cincon Electronics
Part: `CQB150W-110S24`
Quantity: 1 crawler + 1 spare preferred for first build
Distributors currently verified: DigiKey / Mouser

Manufacturer-controlled electrical data:
- input operating range: 43...160 VDC;
- nominal input: 110 VDC;
- input absolute continuous maximum: 160 VDC;
- 100 ms input surge maximum: 200 VDC;
- output: 24 VDC;
- output current: 6.3 A;
- rated output power: ~151 W class;
- efficiency at 110 V / full load: 89%;
- input-output isolation: 3000 VDC / 1 min;
- input-case isolation: 2250 VDC / 1 min;
- output-case isolation: 500 VAC / 1 min;
- OCP: hiccup, auto recovery;
- OVP: approximately 115...140% nominal;
- continuous short-circuit protection;
- UVLO turn-on around 40.5...42.5 V;
- OTP center-baseplate shutdown around 110 C, recovery around 100 C;
- fixed switching frequency ~270...330 kHz;
- weight ~68 g;
- potted UL94V-0 construction;
- aluminum base plate.

Mechanical:
- quarter-brick industrial format;
- 57.9 x 36.8 x 12.7 mm body;
- two M3 x 0.5 mounting inserts;
- 50.80 mm insert center spacing;
- input/output pins according to Cincon mechanical drawing.

Current stock check at audit time:
- DigiKey: 43 units;
- Mouser: 7 units.

### Why selected

It solves all of the current primary gates simultaneously:
1. 43-160 V input covers the WB06 hot 150 m crawler voltage (~99 V normal screen) with large undervoltage margin.
2. 160 V continuous maximum gives reasonable headroom above a regulated 120 V source.
3. 24 V / 6.3 A directly matches the local crawler bus.
4. 150 W matches the active Rev.PP preferred minimum and the Rev.GS short-controlled system budget.
5. 57.9 x 36.8 x 12.7 mm fits the existing compact power-module reserve; old Mean Well RSD solutions do not.
6. The part is commercially stocked now, not merely manufacturer-RFQ.

## 5. Why RSD-100D / RSD-150D are not the crawler choice

Mean Well RSD D-input models are electrically compatible with approximately 100-120 VDC tether voltage, but their enclosed railway package is much larger than the quarter-brick Cincon.

`RSD-100D-24` also supplies only about 100.8 W, leaving inadequate margin for the active 120-145 W controlled peak study.

Therefore RSD remains useful as an external/bench comparison device, not the embedded crawler converter.

## 6. Power / tether interaction

The converter's 89% full-load efficiency means the tether sees more power than the 24 V loads consume.

For Rev.B planning:

| 24 V output load | Approx. converter input power at 89% |
|---:|---:|
| 60 W | 67.4 W |
| 90 W | 101.1 W |
| 100 W | 112.4 W |
| 120 W | 134.8 W |
| 145 W | 162.9 W |
| 150 W | 168.5 W |

Using the WB06 hot 150 m AWG22 loop screen (18.573 ohm at ~60 C) and 120 V source:
- 100 W output -> crawler converter input ~98.9 V, line current ~1.14 A, cable loss ~24.0 W;
- 120 W output -> ~93.1 V, ~1.45 A, cable loss ~39.0 W;
- 145 W short output -> ~84.0 V, ~1.94 A, cable loss ~69.9 W;
- 150 W continuous at 150 m hot is electrically possible but inefficient and is **not** a desired operating point.

Decision:
- design the crawler converter for 150 W capability;
- target normal total crawler power <=100 W;
- permit 120-145 W only as short controlled transients until the real cable/thermal data exist;
- do not interpret a 150 W converter rating as permission to draw 150 W continuously through a 150 m lightweight tether.

## 7. Input bulk capacitor

Cincon recommends an external 220 uF input capacitor for this series.

Selected purchasable candidate:
- manufacturer: Nichicon;
- part: `UCS2D221MHD1TN`;
- 220 uF;
- 200 VDC;
- 18 mm diameter;
- 25 mm length;
- 7.5 mm lead spacing;
- -40...+105 C;
- 10,000 h class;
- ripple current ~2.365 A;
- current Mouser stock in the thousands at the audit date.

Installation:
- mounted horizontally in P0 to fit the low front dry-volume height;
- mechanically clamped with a nonconductive saddle; leads do not carry vibration load;
- installed close to converter input with short insulated conductors;
- minimum 200 V rating retained even though nominal tether is 120 V.

Architecture note: the original Proteus P01 also contains one 220 uF / 200 V capacitor. This numerical coincidence is useful as a sanity check, not evidence that the circuits are equivalent.

Energy stored at 120 V:
`E = 0.5*C*V^2 ~= 1.58 J`.

That stored energy makes inrush and service-discharge behavior mandatory design items.

## 8. Input fuse

### Crawler local fuse

Selected fuse family:
- Eaton Bussmann `S505H`;
- candidate article: `BK1-S505H-3-15-R` / S505H-3.15-R;
- 3.15 A;
- time-delay;
- ceramic 5 x 20 mm;
- rated 400 VDC for the 0.5-5 A family;
- high breaking capacity;
- currently stocked in large quantity through Mouser.

Reason for 3.15 A rather than blindly using Cincon's generic 6 A recommendation:
- our source is controlled around 120 V rather than the converter's 43 V lower-input extreme;
- normal long-line current is around 1.0-1.2 A;
- the current WB06 hot 150 m 145 W short-peak screen is ~1.94 A;
- 3.15 A time-delay gives useful cable/harness protection while preserving startup/transient margin.

This remains a prototype fuse value. It must be checked against the actual external capacitor inrush, source current limit and measured operating current.

### Service holder

Preferred internal service holder:
- SCHURTER `FIZ` family;
- example order number `0031.2203`;
- 5x20 mm;
- panel/internal-bracket mount;
- solder / 6.3 x 0.8 quick-connect terminals;
- UL/CSA rated up to 600 VAC/DC;
- IP40/IP67 variant family.

Install on an **internal dry service bracket** reachable after opening the crawler service cover. It does not penetrate the external P0 pressure boundary.

## 9. Inrush control

The 220 uF / 200 V capacitor stores ~1.58 J at 120 V. The system must not rely on connector contact resistance to limit charging current.

Rev.B strategy is two-layer:
1. CCU HV source must start with a controlled/current-limited ramp;
2. crawler input includes a local passive inrush limiter during prototype qualification.

Prototype passive candidate:
- Songtian PS-series `10D-13`;
- exact family article `MF1310004M4EN0CSB0`;
- 10 ohm at 25 C;
- 13 mm class disc (15 mm max finished diameter in supplier table);
- 4 A max steady current at 25 C;
- -40...+200 C family range.

Status: **TEST CANDIDATE, NOT PRODUCTION-FROZEN**.

Reasons for hold:
- an NTC is weak for rapid OFF/ON because it remains hot and low-resistance;
- its pulse-energy capability must be verified for our 220 uF / 120 V capacitor and worst-case source impedance;
- final production may use an active/precharge arrangement if repeated restart testing requires it.

E-STOP and fault clearing must not automatically re-enable HV while the NTC is still hot. Deliberate operator re-enable remains mandatory.

## 10. Converter mounting without a custom PCB

The project rule `no custom PCB` is preserved.

The CQB module is not soldered onto a newly designed PCB. Instead:
- module is mechanically mounted by its M3 inserts to a machined aluminum thermal carrier;
- converter pins receive short insulated point-to-point pigtails;
- pigtails are strain-relieved in a machined/printed insulating terminal guide;
- all exposed HV solder joints receive individual high-temperature heatshrink plus a secondary rigid insulating cover;
- input and output harnesses use service connectors outside the immediate HV pin area;
- no wire tension is allowed on converter pins.

Final carrier part:
`PX1-460-HV24-THERMAL-CARRIER`.

Material candidate:
- EN AW-6082 T6;
- thermal interface pad to converter base plate as required by the verified mounting orientation;
- carrier conducts heat to the crawler aluminum pressure body using blind internal fasteners only.

No screw penetrates the wet pressure boundary.

## 11. Thermal requirement

At 89% efficiency, full 150 W output corresponds to about 18.5 W converter dissipation.

Approximate dissipation screen:
- 60 W output: ~7.4 W;
- 90 W: ~11.1 W;
- 100 W: ~12.4 W;
- 120 W: ~14.8 W;
- 145 W: ~17.9 W;
- 150 W: ~18.5 W.

This is too much heat to leave in stagnant P0 air.

Rules:
- aluminum base plate must have a direct thermal path into the crawler housing;
- thermal carrier/body interface must be flat and repeatable;
- converter base temperature sensor is required for prototype testing;
- firmware derates traction before converter OTP;
- sealed-body soak test at realistic 90-100 W total output is mandatory;
- 120-145 W short load is tested only after normal-load temperature stabilizes acceptably.

Manufacturer data allow case operation to +105 C and OTP around 110 C, but PX-1 shall use a substantially lower normal thermal limit after prototype test rather than running near shutdown.

## 12. Output 24 V bus

The CQB output is the single main 24 V bus.

Branches remain:
- LEFT traction driver;
- RIGHT traction driver;
- camera/lighting conversion;
- 5 V logic conversion;
- sensors/telemetry.

Per-side motor current limiting remains mandatory because converter OCP is not a bevel-gear protector.

Motor reversal/regeneration warning:
- an isolated DC/DC converter is not assumed to sink energy returned by the H-bridges;
- BTS7960 reversal/braking can raise the local 24 V bus;
- acceleration/deceleration/reversal ramps remain mandatory;
- local 24 V bulk capacitance and a bus clamp/dump strategy are a separate WB08 release item.

Do not add a random TVS and call the regenerative-energy problem solved without measuring the motor/gear inertia and repeated braking energy.

## 13. HV sensing / isolation

The DC/DC isolation is useful and must not be casually bypassed.

Therefore:
- crawler MCU ground remains on the 24 V/output side;
- direct resistor divider from tether HV to MCU ADC is prohibited because it defeats galvanic isolation;
- tether-input voltage telemetry requires an isolated voltage-sensing solution if retained;
- this is a later instrumentation selection item and is not required to operate the first protected prototype.

## 14. Packaging screen

Existing Rev.PR reserved roughly `80 x 58 x 18 mm` for the HV-to-24 converter block.

Bare CQB150W-110S24:
- 57.9 x 36.8 x 12.7 mm.

It therefore fits the existing converter envelope with substantial X/Y margin.

The 220 uF / 200 V capacitor is 18 x 25 mm and is installed horizontally adjacent to the module rather than vertically in the low front roof.

The rear local fuse remains near the tail connector so a short in the long internal HV harness does not remain unfused from the crawler entry.

Final full-solid packaging remains HOLD until the thermal carrier and insulating pin cover are drawn.

## 15. Safety sequence

Mandatory high-voltage sequence remains:
1. CCU low-voltage logic ON, tether HV OFF.
2. Cable/reel/crawler connection state checked by safe method.
3. Operator requests crawler enable.
4. Hardware E-STOP chain must be healthy.
5. CCU HV source ramps/current-limits toward nominal.
6. Crawler input capacitor charges through qualified inrush path.
7. CQB converter starts and 24 V bus rises.
8. STM32 boots and sends valid heartbeat.
9. Only then traction may enable.
10. E-STOP / line overcurrent / connector fault / lost heartbeat -> CCU HV OFF.
11. Re-enable after a trip requires deliberate operator action.

No exposed disconnected tether connector may be live.

## 16. Release gates

WB07 does not become Rev.C-ready until:
1. purchase one CQB150W-110S24 and verify exact dimensions/pins;
2. purchase the exact 220 uF / 200 V capacitor and measure package;
3. build a non-PCB insulated harness/carrier prototype;
4. test 24 V output at 0 / 25 / 50 / 90 / 100 / 120 / 145 W;
5. log converter base temperature and crawler-body temperature;
6. test at equivalent 40 / 100 / 150 m source impedances from WB06;
7. qualify fuse/inrush behavior cold and during repeated OFF/ON;
8. verify source ramp and E-STOP drop-out;
9. test insulation resistance HV-to-body / HV-to-24 V after wet-pressure cycling;
10. integrate final 24 V bus clamp/regeneration solution from WB08;
11. rerun full CAD with thermal carrier, pin cover, capacitor, fuse holder and harness bend radii.

## Change log

### 2026-09-11 — WB07
- retired old 48/60 V converter selections from the active architecture;
- selected a currently stocked 43-160 V -> 24 V / 150 W quarter-brick converter;
- preserved commercial-module / no-custom-PCB rule;
- selected a real 220 uF / 200 V 18x25 mm capacitor;
- selected a DC-rated 3.15 A time-delay fuse family and service holder;
- defined NTC only as a prototype inrush candidate, not an untested production fix;
- quantified normal/peak converter dissipation and long-cable interaction;
- explicitly protected the DC/DC isolation from being bypassed by a direct MCU voltage divider;
- left 24 V regeneration/clamp and final thermal carrier as the next release work.
