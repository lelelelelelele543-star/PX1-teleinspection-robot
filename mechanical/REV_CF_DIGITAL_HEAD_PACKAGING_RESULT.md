# PX-1 Rev.CF — compact digital camera-head packaging result

Status: geometry candidate, not machining RELEASE.

## Current digital stack
- camera PCB candidate: 32x32 mm H.265/H.264 IP camera class;
- ROLL data transfer: miniature 100BASE-TX slip ring, Ø6.5 mm candidate;
- ROLL support: 2x 6803-2RS, 17x26x5;
- ROLL gearing: m0.5 z17/z51 candidate;
- long tether data: 10BASE-T1L after the fixed side of the ROLL joint;
- illumination remains on the fixed outer head, not on the rotating cartridge.

## Size result
The small Ethernet slip ring removes the need for 25 mm bore bearings and lets the design return to the 6803 architecture.

Head outside diameter remains **52 mm**.

A **72 mm overall cylindrical length is again plausible as a design target**, but it is not yet frozen. Exact length depends on:
1. real slip-ring body length and lead exit;
2. camera-board component height and connector direction;
3. lens and protective window stack;
4. rear service connector and retaining ring;
5. thermal spacing around the encoder/SoC.

## Critical radial margin
A 32x32 mm square board has a 45.25 mm diagonal. Inside a nominal Ø47 mm cavity this leaves only about **0.87 mm radial margin at each corner** when perfectly centered. Therefore:
- no tall connector may project from a board corner;
- board edge tolerance and shell concentricity matter;
- exact PCB drawing is mandatory before machining;
- if measured assembly margin drops below 0.5 mm, enlarge the head rather than forcing the fit.

## Digital architecture rule
Do not send 10BASE-T1L directly through the ROLL slip ring in the baseline design. Use ordinary 100BASE-TX across the short rotating interface, then convert to 10BASE-T1L on the stationary side for the 40–150 m tether.

## Next gate
1. obtain exact mechanical drawing for the selected miniature Ethernet slip ring;
2. obtain exact camera-board height/connector drawing;
3. freeze axial stack and real head length;
4. run thermal estimate for camera encoder inside sealed Ø52 shell;
5. repeat DN150 sweep with the resulting real external head length;
6. only then start detailed camera-head machining drawings.
