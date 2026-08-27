# PX-1 Rev.FV — prototype drawing release queue

Status: active drawing plan after Rev.FS integrated solid validation.

The first drawing pack will be released in the following order so critical fits are fixed before cosmetic/external parts.

## Group A — rotating/sealing parts
1. DRW-PX1-431 wheel shaft, Rev.FS geometry.
2. DRW-PX1-432 axle flange, 61903 pocket + static seal + X-ring gland interface.
3. DRW-PX1-433 side-drive cover, 286x86x5, 3 pilots, main face seal, flush lower screw line.
4. DRW-PX1-434 X200 bevel output shaft.
5. DRW-PX1-435 X200 bearing/seal boss.
6. DRW-PX1-436 supported bevel pinion shaft.

Required on sheets:
- datums;
- bearing/seal fits;
- surface finish at seal lands;
- runout/coaxiality;
- keyway positions;
- heat treatment/material where applicable;
- inspection characteristics marked CTQ.

## Group B — main pressure structure
7. DRW-PX1-100 P0 main pressure body.
8. DRW-PX1-101 P0 top cover and seal path.
9. DRW-PX1-102 rear structural bulkhead / tether anchor bosses.
10. DRW-PX1-103 replaceable rear connector adapter plate.

## Group C — lift
11. DRW-PX1-210 lower lift arm.
12. DRW-PX1-211 upper lift arm.
13. DRW-PX1-212 body pivot block.
14. DRW-PX1-213 camera-side lift bridge.
15. ASS-PX1-220 manual lift assembly including M8 clamp, Belleville stack, gas spring and DN150 mechanical stop.

## Group D — camera head
16. DRW-PX1-310 fixed camera outer shell.
17. DRW-PX1-311 front window retainer.
18. DRW-PX1-312 rear service closure.
19. DRW-PX1-313 yoke cheek.
20. ASS-PX1-320 digital TILT/ROLL camera assembly.

Final bearing seats and internal ROLL geometry remain blocked by the exact camera PCB and rotary-transfer sample.

## Group E — general assemblies
21. ASS-PX1-001 complete crawler.
22. ASS-PX1-002 longitudinal section through P0 and X200 drive.
23. ASS-PX1-003 transverse section through wheel station / P0 / P1 / P2.
24. ASS-PX1-004 side-drive exploded assembly.
25. ASS-PX1-005 rear tether termination.

## Drawing style
Final sheets must use factory-style engineering drawing conventions:
- true CAD-derived orthographic views and sections;
- centerlines and section hatching;
- item balloons and PARTLIST on assemblies;
- fit/tolerance callouts only where justified;
- ISO-style title block/revision field;
- no cartoon/schematic geometry presented as manufacturing drawing.

## Release gates
A drawing may move from CANDIDATE to PROTOTYPE RELEASE only after:
- corresponding Rev.FS/next solid recomputes without error;
- no DN150 interference in full solid test;
- exact bearing/seal/gear sample or authoritative drawing is available for every fit shown;
- dimensions are not copied from proprietary MiniCam geometry; uploaded documentation is used only as architecture/service reference.

Serial release remains blocked until pressure, traction, thermal, tether-pull and DN150 physical tests pass.