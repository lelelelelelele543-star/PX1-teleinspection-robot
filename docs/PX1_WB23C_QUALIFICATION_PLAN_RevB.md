# PX-1 WB23C qualification plan — pressure/service cover and local lift harness

Date: 2026-09-14
Status: **test plan**

## Q1 — dimensional incoming inspection

Record measured dimensions of:

- LAPP 53112000 gland: thread, OD, nut flats, thread length and supported cable OD;
- chosen local cable OD at five positions;
- chosen fill valve exposed OD/height/thread;
- SP13 plug/panel pair;
- O-ring cord diameter/hardness;
- machined cover flatness and body seal-land flatness.

Acceptance: dimensions fit released CAD without interference and with required seal compression.

## Q2 — dry continuity and load

- measure every conductor end-to-end;
- measure insulation between conductors and shield/chassis;
- run maximum expected head load;
- record supply voltage at dry connector and at camera connector;
- operate UART and raw CVBS simultaneously;
- toggle LEDs and camera motors while observing video.

No intermittent contact, sync loss or excessive voltage drop is accepted.

## Q3 — +0.25 bar pressure-decay

Assembly must include production-intent cover, seal, two M4 screws, gland, fill valve and local cable.

1. Pressurize to +0.25 bar gauge.
2. Stabilize temperature.
3. Record pressure and ambient temperature for 30 min.
4. Inspect cover perimeter, valve and gland.

Final numerical decay limit is established after instrument repeatability is measured. No visible leak/bubble stream is allowed.

## Q4 — submerged static leak

With the same assembly at +0.25 bar gauge, submerge the service interface for at least 30 min. No continuous bubbles and no water intrusion after drying/opening inspection.

## Q5 — 1 bar proof gate

Run only after the crawler pressure-body release formally retains a 1 bar rating. Use a controlled fixture/procedure with personnel protection. Passing Q3 does not automatically authorize Q5.

## Q6 — lift dry-cycle endurance

Run:

- minimum 500 LOW-HIGH-LOW cycles;
- target 1000 cycles;
- speed representative of manual field operation;
- real camera connector and gland installed.

Monitor power-core resistance, UART, CVBS and shield continuity.

## Q7 — wet/grit lift cycles

After dry cycling, repeat a representative subset with water and realistic pipe grit/sludge around the lift guard. The guard must not pack debris into a hard pinch point.

## Q8 — post-cycle pressure test

Repeat Q3 and Q4 after flex cycling to catch gland/jacket damage that a fresh-assembly test misses.

## Q9 — service-replacement trial

A technician unfamiliar with assembly should be able to replace the local harness without removing the main electronics.

Record:

- service time;
- tools;
- connector accessibility;
- seal/conductor damage risk;
- whether two cover screws provide enough alignment during reassembly.

Recurring misalignment justifies adding locating features or changing fastener count before production release.

## Q10 — DN150 physical jig

Test final hardware in representative ID150 pipe with:

- LOW lift position;
- final pressure cap;
- final screw heads;
- final horizontal gland;
- final arm guard;
- representative wheel tread loading.

Confirm the ~4.7 mm ideal-CAD limiting fixed clearance is not consumed by real tolerance, ovality, welds or debris.

## Release condition

WB23C leaves HOLD only when Q1–Q4, Q6–Q10 pass and selected parts have controlled articles. Q5 is additionally required if the final crawler is formally released to a 1 bar pressure rating.
