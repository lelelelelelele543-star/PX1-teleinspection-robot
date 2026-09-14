# PX-1 WB23E/F/G qualification plan — pressure/service cover and six-core lift harness

Date: 2026-09-14
Status: **test plan**

## Q1 — dimensional incoming inspection

Record measured dimensions of:

- LAPP 53112000 gland: thread, OD, nut flats, thread length and supported cable OD;
- chosen **6-core** local cable OD at five positions, conductor diameter and insulation OD;
- chosen fill valve including protective cap exposed OD/height/thread;
- Micro-Fit six-way dry connector housings/contacts;
- SP13 six-pin plug/panel pair;
- O-ring cord diameter/hardness;
- machined cover flatness and body seal-land flatness.

Acceptance: dimensions fit released CAD without interference and with required seal compression. Local cable must be <=6.5 mm OD; preferred target is 5.5...6.0 mm.

## Q2 — six-core continuity and load

Verify exactly six insulated circuits end-to-end:

1. +12V_HEAD
2. GND_HEAD
3. UART_TX
4. UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

Additionally verify overall shield continuity separately. Shield must not be used as DC return.

Then:
- measure resistance of every core per metre and complete harness end-to-end;
- measure insulation between conductors and shield/chassis;
- run maximum expected head load;
- record supply voltage at dry connector and at camera connector;
- operate UART and raw CVBS simultaneously;
- toggle LEDs and camera motors while observing video;
- record temperature rise at +12 V and GND crimp/solder contacts.

No intermittent contact, sync loss, excessive temperature rise or unacceptable voltage drop is accepted.

## Q3 — +0.25 bar pressure-decay

Assembly must include production-intent cover, seal, two M4 screws, gland, fill valve and actual six-core local cable.

1. Pressurize to +0.25 bar gauge.
2. Stabilize temperature.
3. Record pressure and ambient temperature for 30 min.
4. Inspect cover perimeter, valve and gland.

Final numerical decay limit is established after instrument repeatability is measured. No visible leak/bubble stream is allowed.

## Q4 — submerged static leak

With the same assembly at +0.25 bar gauge, submerge the service interface for at least 30 min. No continuous bubbles and no water intrusion after drying/opening inspection.

## Q5 — 1 bar proof gate

Run only if the final crawler pressure-body release formally retains a 1 bar proof/operating requirement. Use a controlled fixture and personnel protection. Passing Q3 does not authorize Q5.

## Q6 — lift dry-cycle endurance

Run:

- minimum 500 LOW-HIGH-LOW cycles;
- target 1000 cycles;
- speed representative of manual field operation;
- real six-core cable, 10 mm-envelope guard, SP13 and gland installed.

Continuously or periodically monitor +12/GND resistance, UART, CVBS and shield continuity. Inspect the cable where it exits the gland, enters the guard and bends near both ends.

## Q7 — wet/grit lift cycles

After dry cycling, repeat a representative subset with water and realistic pipe grit/sludge around the lift guard. The guard must drain and must not pack debris into a hard pinch point.

## Q8 — post-cycle electrical + pressure test

Repeat Q2, Q3 and Q4 after flex cycling. This catches conductor/crimp degradation and gland/jacket damage that a fresh-assembly test misses.

## Q9 — service-replacement trial

A technician unfamiliar with assembly should be able to replace the complete cover + M12 gland + six-core lift harness without removing the main electronics.

Record service time, tools, Micro-Fit accessibility, SP13 accessibility, seal damage risk and whether two cover screws provide enough alignment during reassembly.

## Q10 — DN150 physical jig

Test final hardware in representative ID150 pipe with:

- LOW lift position;
- final pressure valve and cap;
- final screw heads;
- final horizontal gland;
- final 10 mm-envelope arm guard;
- representative wheel tread loading.

The preferred pressure-valve envelope is <=Ø12 x 5 mm. The current Ø14 x 6 screen leaves ~4.70 mm ideal-CAD clearance; real tolerance/ovality/debris must not consume this to contact.

## Q11 — connector pull/service cycling

- Micro-Fit: at least 30 mate/unmate prototype cycles plus conductor pull inspection; do not exceed catalog durability without separate justification;
- SP13: at least 50 service mate/unmate cycles as previously required by WB15;
- repeat continuity and video checks after cycling.

## Release condition

The WB23E/F/G service interface remains on HOLD until Q1–Q4 and Q6–Q11 pass with controlled purchased articles. Q5 is additionally required only if the final crawler pressure specification formally calls for it.
