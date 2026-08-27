# PX-1 Rev.DY — centre wheel/input shaft and bevel stack

Status: detailed prototype geometry candidate. Supersedes the loose coaxial assumption in Rev.DX.

## Design decision
The middle wheel station remains the torque-input station for each side. The large bevel gear and the middle Z50 spur gear share one stepped transverse shaft so the torque path is short and serviceable.

Per side torque path:

`JGB37-555 -> short coupling/pinion shaft -> KHK SB1.5-1845H pinion -> KHK SB1.5-4518H large bevel -> stepped middle shaft -> Z50 -> four remaining Z50 gears -> 3 wheels`

## Why stepped shaft
The selected large bevel candidate has a nominal 10 mm bore while the wheel/side-drive shaft family has moved to Ø12 mm. Do not bore the hardened bevel gear to Ø12 for the prototype.

Use a stepped shaft:
- inner bevel seat: Ø10 h6;
- transition shoulder: R0.4 max, relieved against gear chamfer;
- side-drive/bearing/gear working section: Ø12 h6;
- outer seal-running section: Ø12 h8 or better, ground/polished;
- wheel torque section: Ø12 with key or positive drive feature;
- axial wheel retainer: M6 internal thread.

Preferred material: 40Cr13 / 1.4034 or equivalent corrosion-resistant hardenable stainless, hardened only as required for the seal journal. AISI 316 is acceptable for early fit prototypes but is not preferred for the final seal-running surface without a wear sleeve.

## Large bevel torque attachment
Preferred serviceable solution: keyed Ø10 bevel seat rather than adhesive-only retention.

Prototype key candidate:
- parallel key approximately 3 x 3 mm;
- effective engaged length >=10 mm;
- axial retention by shaft shoulder plus locknut / tab washer on the inner end where packaging permits.

At the current control-limited pinion torque 1.50 N·m and 2.5:1 reduction with 0.90 mechanical efficiency, nominal side output is about 3.38 N·m.

A 3x3 key with 10 mm effective length on a Ø10 seat has approximate conservative stresses:
- key shear ~22.5 MPa;
- bearing/crushing ~45 MPa.

This is acceptable as a prototype starting point but the exact key/keyway is not RELEASE until the actual KHK hub machining condition is checked. If the purchased H gear cannot be keyed without damaging its heat treatment, use a non-destructive split-clamp/taper adapter or order a semi-custom finished-bore gear. Do not drill random radial grub-screw holes as the primary torque path.

## Bearing arrangement — middle station
The middle shaft carries both bevel and wheel-train loads.

Preferred stack from P0 centre toward outside:
1. large bevel gear on Ø10 keyed seat;
2. inner bearing supporting the Ø10 section, 6000/61800 class selected after exact space check;
3. P0-to-P1 secondary rotary seal on a dedicated polished journal;
4. shaft step to Ø12;
5. middle Z50 spur gear on Ø12 positive-drive seat;
6. outer 61801-2RS bearing in the removable axle flange;
7. primary FKM 12x22x7 rotary seal;
8. labyrinth/dirt exclusion geometry;
9. wheel hub;
10. retaining disk + M6 screw.

The large bevel must be supported close to its mesh. Do not cantilever it from the wheel-flange bearing alone.

## Bevel-force check
For m1.5, z18 pinion, nominal pitch diameter about 27 mm and 1.50 N·m pinion torque:
- tangential force Ft ~111 N;
- pinion pitch angle ~21.8 deg for 18/45 pair;
- approximate radial component ~37.5 N;
- approximate axial component ~15.0 N.

These loads are small compared with normal miniature bearing ratings; geometry, stiffness, alignment and sealing are more critical than static bearing capacity.

## Backlash/alignment
Use catalog backlash as the starting condition; do not preload the bevel pair tight.

Mechanical provisions:
- motor/pinion carrier has controlled axial shim adjustment;
- large-gear shaft position is fixed by shoulders and bearing seats;
- tooth contact checked with marking compound after final cover torque;
- acceptable contact must stay centered on the tooth face without edge loading.

## Release gates
1. inspect actual SB1.5-1845H/SB1.5-4518H hub hardness and machining allowance;
2. measure exact bore, face, hub and mounting offsets;
3. decide keyed gear vs semi-custom finished bore;
4. run tooth-contact test under hand load;
5. run 30 min loaded bench test;
6. confirm no measurable pressure leakage through P0/P1 shaft boundary;
7. freeze manufacturing drawing only after the purchased pair is in hand.
