# PX-1 Rev.DH — three sealed pressure zones

Status: reliability architecture. Supersedes the earlier permanently open pressure passage between side gear bays and the electronics body.

## Reason for the change
A single open dry volume is simple, but if a side-cover O-ring or one wheel seal is damaged, water can eventually migrate directly into the electronics compartment.

The uploaded Proteus crawler housing drawing shows a useful proven principle: the central crawler housing has dedicated shaft seals on the bevel-output axles. PX-1 keeps that system-level idea and combines it with the user's sealed, pressurized side covers.

## Pressure zones
PX-1 now has three normally isolated dry volumes:

- **P0 BODY** — electronics, DC/DC, traction motors, controller;
- **P1 LEFT DRIVE** — left three-wheel gear train;
- **P2 RIGHT DRIVE** — right three-wheel gear train.

Normal initial pressure target in each zone: **+0.20…+0.30 bar gauge at surface**.

## Fill arrangement
One external service/fill port feeds a small three-way manifold.

Each branch contains a one-way fill valve/check valve:
- manifold -> P0;
- manifold -> P1;
- manifold -> P2.

After filling, the three zones do not have a permanently open air passage between them.

This means a damaged wheel seal can depressurize one side drive bay without immediately depressurizing/flooding the electronics body.

## Dynamic sealing boundaries
### Central body to side-drive bays
Two transverse bevel-output half-shafts cross the P0/P1 and P0/P2 boundaries.

Each uses a replaceable clean-side rotary shaft seal. Starting PX-1 shaft diameter remains Ø10 mm; final seal dimension follows the detailed bevel/output carrier design.

These two seals normally see nearly zero differential pressure because all three zones are filled to the same nominal pressure. They function primarily as a secondary flood barrier.

### Side bays to sewer
Each of the six wheel shafts has its own outer rotary seal in the removable side cover.

Total rotating water barriers:
- 6 primary wheel shaft seals;
- 2 secondary central-output seals.

## Static seals
- P0 top/electronic cover: continuous O-ring;
- P1 side cover: continuous FKM O-ring;
- P2 side cover: continuous FKM O-ring;
- tail connector and pressure fill port: dedicated O-rings/sealing washers;
- camera/lift interfaces remain separate sealed assemblies.

## Pressure sensing
Professional target: monitor all three zones separately.

Display on the operator console:
- BODY pressure;
- LEFT DRIVE pressure;
- RIGHT DRIVE pressure;
- pressure-decay warning for each zone.

This makes field diagnosis immediate: a falling LEFT pressure points toward left cover/wheel seals rather than electronics-body leakage.

Exact pressure-sensor part number remains an electronics selection gate.

## Alarm philosophy
Initial prototype thresholds, subject to thermal compensation:
- fill target: +0.25 bar typical;
- warning: < +0.17 bar before deployment or unexpected decay during operation;
- stop / inspect: < +0.10 bar or rapid pressure loss;
- pressure drop rate is more informative than a single absolute value.

No automatic compressor is fitted to the crawler. A leak must be repaired, not hidden by continuously feeding air.

## Pressure proof and leak test
Normal operation is not a pressure-vessel test.

Prototype qualification:
1. proof the empty body/side covers using the safest practical method, preferably hydrostatic or shielded low-energy test;
2. normal dry leak test at approximately +0.25 bar;
3. record P0/P1/P2 for 30 min with temperature compensation;
4. submerged static test;
5. submerged wheel-rotation test;
6. repeat pressure-decay test after endurance cycling.

The side-cover mechanical target of >=1 bar differential remains a structural qualification target; routine pneumatic operation remains only +0.20…+0.30 bar.

## Field-service advantage
A technician can isolate the fault by zone, remove only the affected side cover, replace common seals/bearings and re-pressure-test that zone. The central controller housing does not need to be opened for normal drivetrain service.
