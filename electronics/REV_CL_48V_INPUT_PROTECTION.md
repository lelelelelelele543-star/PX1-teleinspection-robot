# PX-1 Rev.CL — 48 V tether input protection and distribution

Status: architecture candidate; exact protection-module part numbers remain HOLD until bench surge and motor-current tests.

## Design objective
The crawler must tolerate field connection mistakes, long-cable transients and motor noise without turning the main pressure body into a fragile custom-PCB system.

Project rule remains: use replaceable ready-made modules / serviceable discrete assemblies, not a custom main PCB.

## Input chain
Tether +48 V / 0 V -> service fuse -> reverse-polarity / ideal-diode protection -> surge clamp -> EMI input filter -> protected 48 V bus -> separate fused branches.

## Main service fuse
Prototype candidate: 7.5 A time-delay automotive blade fuse in a sealed holder.

Reasoning:
- expected normal line current about 2.1 A;
- present estimated short peak about 4.4 A;
- fuse must survive motor acceleration but open on sustained cable/branch faults.

7.5 A is NOT production-frozen until JGB37-520 stall current and converter inrush are measured.

## Reverse-polarity protection
Preferred implementation: ready-made high-side ideal-diode / reverse-battery module rated:
- continuous input >=60 V;
- transient device voltage rating preferably >=80 V;
- continuous current >=8 A;
- low forward drop, no ordinary series silicon diode for the traction supply.

If a suitable sealed module cannot be sourced, a serviceable MOSFET module may be mounted on an aluminium carrier, but it must remain individually replaceable.

## Surge suppression
Do not rely on a single generic TVS chosen only by a '48 V' label. The clamp voltage must be coordinated with the actual maximum input rating of all downstream DC/DC converters.

Prototype strategy:
1. suppress large switching transients at the console/source side;
2. add a crawler-side surge suppressor after the fuse;
3. verify the worst transient at the crawler with an oscilloscope before freezing the TVS / surge-module rating.

Target protected-bus rule: measured repetitive transients must remain below the lowest absolute input limit of the installed converters with engineering margin.

## Input EMI filter
Serviceable two-stage candidate:
- common-mode choke or ready-made DC EMI filter rated >=8 A;
- local film/ceramic bypassing for high-frequency motor noise;
- bulk low-ESR capacitor on protected 48 V bus;
- physical separation between traction wiring and digital/video pair.

Exact capacitance is HOLD because converter inrush and cable inductance must be checked together; do not simply fit the largest capacitor available.

## Protected 48 V branch distribution
Use separate replaceable fuses for:
- 48->24 V traction converter;
- 48->12 V camera / auxiliaries;
- 48->5 V logic / networking;
- service/spare branch if fitted.

A fault in camera electronics must not disable traction power, and a motor-driver short must not burn the complete tether.

## Grounding
- tether power return is the DC power reference;
- cable shields / digital-pair shields terminate according to the final 10BASE-T1L interface design, not randomly to multiple chassis points;
- aluminium body/chassis bonding point is singular and documented;
- motor return currents must not share narrow logic-ground wiring.

## Mechanical/service requirements
- fuse accessible after one service cover removal;
- protection and filter modules labelled and replaceable individually;
- no soldered inline fuse hidden inside harness;
- crimped ferrules / sealed automotive or industrial connectors preferred for power branches;
- all high-current wires mechanically restrained before electrical terminals.

## Release gates
1. measure actual JGB37-520 running, acceleration and stall currents;
2. measure 48 V converter inrush;
3. measure crawler-input transient during forward/reverse/braking over 40 m prototype tether;
4. repeat with representative 100-150 m tether impedance;
5. freeze fuse ratings;
6. freeze surge suppressor/clamp part;
7. thermal test complete sealed pressure body at maximum continuous load.
