# PX-1 Rev.PF — CRP150 lift integration gate

Status: IMPORTANT CORRECTION / HOLD.

## What was checked
Rev.PD reproduced the CRP150 lift topology from DRW-002-744, but several key dimensions were not present in the available source drawing and were therefore represented parametrically.

A conservative integration check against the current Rev.PB crawler body shows that those provisional Rev.PD dimensions intersect the body. Therefore the provisional dimensions MUST NOT be treated as the CRP150 geometry and MUST NOT be propagated into machining CAD.

## Source-controlled facts that remain valid
From DRW-002-744:
- 1x SPR-002-524 gas spring, 150 N;
- 2x FSS-002-068 lever side;
- 1x FSS-002-073 lever sheet plate;
- M8 clamping lever;
- 3x DIN2093 20x10.2x1.1 Belleville washers;
- 2x 15x2.5 O-rings;
- 4x 8x0.8 circlips;
- M6x18 pin;
- lift housing FAL-002-067;
- lever-arm assembly ASS-002-723.

The assembly drawing also clearly shows the compact folded arrangement with the gas spring nested alongside/below the side lever, not an external tall parallelogram.

## Why Rev.PD geometry is on HOLD
The available DRW-002-744 is an assembly/parts drawing and does not dimension:
- pivot-to-pivot lever length;
- vertical pivot spacing;
- exact lever-side profile;
- lift-housing mounting datum relative to crawler body;
- gas spring closed/open length and mounting centers;
- exact camera-top connector datum.

Those dimensions cannot be recovered reliably from the raster view without introducing scaling error.

## Required physical/detail dimensions to freeze the lift
Minimum measurement set from an existing CRP150 or original detail drawings:
1. centre distance: lower body pivot -> lower camera-side pivot;
2. centre distance: upper body pivot -> upper camera-side pivot;
3. vertical spacing between body pivots;
4. vertical spacing between camera-side pivots;
5. body pivot X/Z location from a repeatable crawler datum;
6. gas spring eye-to-eye length CLOSED;
7. gas spring eye-to-eye length at full raised position;
8. gas spring body diameter and stroke;
9. camera connector axis position in fully folded state;
10. side lever plate thickness and maximum outline height.

Once these ten values are available, the CRP150 lift can be rebuilt essentially one-for-one and the CAM026 folded/raised sweeps can be checked correctly.

## Design rule
Do NOT redesign the lift to solve missing dimensions. The objective is to preserve the proven CRP150 mechanism. Until detail dimensions are available, development continues on crawler drive, camera internals, reel and control electronics without changing the lift architecture.
