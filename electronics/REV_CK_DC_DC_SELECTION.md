# PX-1 Rev.CK — DC/DC converter selection

Status: component-selection candidate. Final purchase list requires current ChipDip stock check.

## Power architecture
Tether bus: 48 VDC nominal.

Branches inside crawler:
1. 48 -> 24 V, traction and actuator rail;
2. 48 -> 12 V, camera / selected auxiliaries;
3. 24 -> 5 V or 48 -> 5 V, logic / communications.

## 48 -> 24 V main converter
Preferred industrial candidate: Mean Well RSD-200C-24.
- output: 24 V, 8.4 A;
- rated power: about 200 W;
- input family: 48 V nominal, wide-range railway DC/DC;
- protections include short circuit, overload, over-voltage, over-temperature and input reverse polarity;
- isolated output;
- convection cooled.

For PX-1 this is the minimum acceptable class for the current Rev.CJ budget. If motor-current measurements show repeated peak demand above the converter transient capability, move to the 250–300 W class instead of relying on overload operation.

## 48 -> 12 V auxiliary converter
Candidate class: TracoPower TEN 40-4812WI.
- input: 18–75 V;
- output: 12 V;
- output current: 3.35 A;
- power: 40 W;
- efficiency about 87%;
- operating temperature class down to -40 C;
- shielded metal case;
- short-circuit / over-voltage / over-temperature protections.

This branch is intended for camera electronics and other low-noise loads. Do not connect traction motors to this converter.

## 5 V logic converter
Two acceptable prototype routes:
A. 48 -> 5 V isolated converter, about 15 W, e.g. Mean Well MDS15C-05 class (36–75 V input, 5 V / 3 A output).
B. 24 -> 5 V automotive/industrial buck after the main 24 V converter.

Route A gives better electrical separation from the motor rail. Route B is cheaper and simpler. For the first prototype, prefer isolated 48 -> 5 V if it fits the enclosure and budget.

## Distribution rules
- each branch gets its own replaceable fuse near the 48 V entry;
- camera/logic ground routing must not share high-current motor return paths physically;
- add TVS and input bulk capacitance at the crawler 48 V entry;
- add LC filtering before camera and digital communications;
- DC/DC modules must be mounted to a metal heat-spreading plate where required;
- use pluggable service connectors so a converter can be changed without unsoldering the harness.

## Release holds
- measure actual JGB37-520 stall and normal current;
- check RSD-200C-24 derating at expected internal temperature;
- verify startup/inrush of BTS7960 + motor branches;
- confirm exact ChipDip availability and package dimensions;
- freeze fuse values only after current measurements.
