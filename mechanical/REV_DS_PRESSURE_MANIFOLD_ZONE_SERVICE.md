# PX-1 Rev.DS — three-zone pressure manifold / service architecture

Status: prototype mechanical/pneumatic architecture; exact valve and sensor articles remain procurement gates.

## Zones retained
- P0 BODY — electronics, DC/DC, traction motors;
- P1 LEFT DRIVE — left three-wheel sealed gear bay;
- P2 RIGHT DRIVE — right three-wheel sealed gear bay.

Normal surface fill target: approximately +0.25 bar gauge, operating window +0.20…+0.30 bar.

## One external fill point, isolated after fill
Rear service port feeds a compact three-branch manifold.
Each branch has its own check valve:
- fill -> check -> P0;
- fill -> check -> P1;
- fill -> check -> P2.

After the compressor/fill gun is removed, loss of P1 or P2 must not vent P0 through the manifold.

## Service layout
Put the fill manifold immediately behind the rear service cover/tail area where it can be replaced without removing the traction motors.

Use short rigid/flexible pneumatic connections only inside the dry body. Avoid long small-bore hoses routed through moving mechanisms.

## Pressure sensing
Each pressure zone needs its own sensor channel.

Preferred system topology:
- one sensor physically exposed to each zone air volume;
- sensor electrical output crosses the zone boundary through a sealed electrical feedthrough or sealed PCB/header area;
- do not route an open pneumatic tube from a side bay into the electronics volume because a failed wheel seal could then carry water directly into P0.

Sensor range target:
- absolute pressure sensor around 0…200 kPa absolute or equivalent;
- enough resolution to detect small pressure-decay rates around the 100–130 kPa absolute operating region;
- temperature measured near each zone or compensated in firmware.

Gauge sensors that require an atmospheric reference vent through the pressure boundary are not preferred.

## Fill hardware
Rear fill interface target:
- compact Schrader-style or industrial pneumatic service valve;
- protective screw cap;
- separate non-return valve inside so dirt in the external valve does not become the only pressure barrier;
- accessible with crawler sitting on wheels;
- does not project beyond the rear recovery/tether protection envelope.

## Relief / overpressure protection
A small mechanical relief element is retained as a safety device.

Prototype set-point target remains approximately 0.35–0.40 bar gauge, to be finalized after body proof testing.

The operator must not use the relief valve as a pressure regulator. Fill pressure is controlled by the service regulator/gauge.

## Console diagnostics
Display separately:
- BODY pressure;
- LEFT pressure;
- RIGHT pressure;
- pressure trend/decay rate.

Initial warning logic:
- normal filled state ~+0.25 bar;
- warning below ~+0.17 bar or abnormal decay;
- stop/inspect below ~+0.10 bar or rapid loss.

Absolute thresholds are corrected for temperature and sensor offset after calibration.

## Leak localization
Examples:
- only LEFT falls: investigate three left wheel seals, left cover O-ring, left sensor/feedthrough;
- only RIGHT falls: symmetric right-side fault;
- only BODY falls: top/rear/electrical cover, tail connector, camera/lift body boundary, central-output seals;
- all three fall together after fill: fill manifold/check-valve or common service-port fault is likely.

## Qualification
- leak-test each zone separately before full assembly;
- fill all three, disconnect service line, record 60 min pressure/temperature;
- submerge static;
- run all six wheels submerged;
- heat/cool cycle and repeat;
- intentionally vent P1 and verify P0/P2 remain pressurized;
- verify relief operates without damaging O-rings or sensor ports.
