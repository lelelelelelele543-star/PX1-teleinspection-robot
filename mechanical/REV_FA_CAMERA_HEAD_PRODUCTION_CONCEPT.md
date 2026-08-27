# PX-1 Rev.FA — digital camera head production concept

Status: prototype mechanical architecture; exact camera/slip-ring articles remain procurement gates.

## External envelope
Target remains approximately Ø52 x 72 mm for DN150 compatibility.
Outer shell is fixed relative to the tilt yoke; ROLL occurs inside the sealed outer shell.

## Outer shell
Material: EN AW-6082 T6 candidate.
- OD 52 mm target;
- wall 2.5–3.0 mm class;
- removable front retainer;
- rear service closure;
- no rotating external pressure seal for ROLL if the internal cartridge architecture is retained.

## Front window
- clear aperture suitable for selected lens;
- current window candidate approximately Ø28 x 3 mm;
- sapphire or tempered mineral glass;
- static FKM O-ring seal;
- mechanically retained front ring, not adhesive-only retention.

## Lighting
LEDs form a separate annulus around the optical window.
- aluminum MCPCB;
- direct thermal path into fixed shell;
- optical black separator between lens and LED cavity to prevent flare;
- LED wiring does not use video/data return as power return.

## Internal ROLL cartridge
Rotating cartridge contains:
- digital camera board/lens carrier;
- ROLL gear;
- two small radial bearings;
- compact Ethernet/data-capable rotary transfer;
- thermal bridge from camera SoC region to rotating aluminum carrier, then controlled path to outer shell where feasible.

The slip ring/rotary transfer is not structural and carries no bearing load.

## Bearings
Use two spaced miniature bearings rather than one cantilever bearing.
Exact bearing family depends on the final cartridge diameter; previously modeled 6803/6805 families are not considered frozen until the 32 mm camera PCB and rotary-transfer sample are physically available.

## ROLL drive
- continuous 360 deg;
- small geared motor mounted in fixed yoke/shell rear zone;
- spur/worm candidate chosen after packaging;
- absolute/home reference retained;
- mechanical wiring path never twists because electrical transfer crosses the rotating interface.

## TILT
Whole fixed shell rotates in the lift yoke around the transverse tilt axis.
- range: -105…+105 deg;
- hard stops slightly beyond software operating limit;
- tilt axis uses bearings/bushings independent from cable guidance;
- yoke protects front window from direct side impact.

## Quick removal
Camera head should be field-removable without opening P0.
Mechanical target:
- keyed spigot into lift cradle;
- retained latch or captive fastener;
- static O-ring at the head/cradle interface if that interface carries a sealed electrical cavity;
- electrical connector mechanically unloaded.

## Digital path
No CVBS, PAL, NTSC or coax is part of the current architecture.
Camera -> local Ethernet electronics -> Ethernet-capable rotary transfer -> crawler digital network -> long-tether physical layer.

## DN150 gate
The Ø52 x 72 envelope remains only a target until the following are included in a full sweep:
- real front retainer;
- yoke cheeks;
- tilt fasteners;
- rear motor bulge if any;
- cable/service loop;
- LOW lift arms;
- pipe ovality/deposits allowance.

## Release blockers
1. actual camera PCB and lens dimensions;
2. actual rotary-transfer drawing/sample;
3. thermal test at 1080p maximum load;
4. full tilt/roll endurance test;
5. 1 bar-class proof of the empty head shell using safe test procedure;
6. repeated window removal/seal test;
7. DN150 solid sweep.