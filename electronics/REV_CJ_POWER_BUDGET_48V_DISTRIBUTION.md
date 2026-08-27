# PX-1 Rev.CJ — provisional power budget and 48 V distribution

Status: engineering candidate. Drive-motor current values remain HOLD until the exact JGB37-520 SKU is frozen and measured.

## Architecture
- tether bus: 48 VDC nominal;
- local crawler conversion: isolated/non-isolated 48->24 V high-power rail for traction;
- local 48->12 V rail for TILT/ROLL motors and camera auxiliaries where required;
- local 48/24->5 V rail for logic/PHY/control;
- all branch rails fused separately;
- no traction motor current is routed through camera-head slip-ring circuits.

## Current load budget
Known/selected values:
- TILT N20: 12 V, stall-current reference 1.1 A => 13.2 W electrical worst-case per motor;
- ROLL N20: same class => 13.2 W worst-case;
- digital camera/encoder: reserve 4 W until exact module measurement;
- lighting: reserve 12 W first-article target;
- controller + 10BASE-T1L PHY + sensors: reserve 6 W.

Traction motors are still the dominant unknown. Until the exact JGB37-520 24 V SKU is frozen, use a provisional design envelope:
- 4 traction motors continuous budget: 60 W total candidate;
- 4 traction motors short peak budget: 140 W total candidate.

This produces approximately:
- normal crawler budget: ~85-90 W;
- short electrical peak envelope: ~185-190 W.

These are sizing values, not measured consumption.

## Converter sizing candidate
- main 48->24 V traction DC/DC: >=200 W continuous candidate, >=250 W preferred for margin and transient handling;
- 48->12 V auxiliary DC/DC: >=40 W;
- 5 V logic rail: >=15 W.

A single monolithic 48->24 converter may be used for prototype traction, but camera/logic should remain on separately filtered rails so motor current steps do not reset the digital video path.

## 48 V tether current
At 90 W total load and 90% local conversion efficiency, source power is ~100 W and 48 V tether current is ~2.1 A.
At 190 W peak and 90% efficiency, source power is ~211 W and 48 V tether current is ~4.4 A.

Therefore the previously selected 2x1.5 mm2 copper power conductors remain plausible for normal operation, but the short-peak drop at 150 m must be checked against real traction-motor stall behavior before RELEASE.

## Protection candidate
- console-side main DC fuse: 6 A slow-blow candidate for first prototype;
- crawler-side 48 V input protection: reverse-polarity protection + TVS + branch fusing;
- traction 24 V branch: fuse/breaker sized after measured motor stall current;
- camera/logic branches: independent lower-current fuses;
- emergency stop should remove traction power while preserving diagnostics/video where practical.

## Mandatory first-article measurements
1. current of one exact traction motor unloaded at 24 V;
2. current of one motor driving one wheel on bench load;
3. stalled/near-stalled current with a current-limited supply;
4. four-motor crawler current on flat dry surface;
5. four-motor current while towing 40 m tether;
6. converter efficiency and case temperature;
7. 48 V voltage measured at console and crawler ends during acceleration.

Only after these measurements may converter power and fuse values move from CANDIDATE to RELEASE.
