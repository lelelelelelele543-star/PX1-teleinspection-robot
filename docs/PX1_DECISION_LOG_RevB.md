# PX-1 Rev.B engineering decision log

Updated: 2026-09-14

This file records controlling decisions so exploratory studies do not silently become architecture changes.

| ID | Decision | Reason / evidence | State |
|---|---|---|---|
| D-001 | Crawler remains 3 wheel stations per side / 6 wheels total at X50/X150/X250 | CRP150 source drive drawings + hard architecture lock | FROZEN Rev.B |
| D-002 | Five m1 Z50 side gears per side, rear X250 long-axle drive input, 2 traction motors total | Proteus side-drive source architecture | FROZEN Rev.B |
| D-003 | No mechanical cassettes/cartridges | field repairability and user directive; source Proteus body is integrated/service-cover based | FROZEN Rev.B |
| D-004 | Main crawler is dry and positively pressurized; wheel shafts use proper dynamic seals | user requirement + Proteus architecture | FROZEN principle |
| D-005 | Manual camera lift retained; no powered lift added | source manual lift is proven and simpler | FROZEN Rev.B |
| D-006 | WB22A body pivot remains X200, pivots Z92/109, 90 mm links | corrected lift/camera integration passes current screen | CONTROLLED |
| D-007 | Camera is separated from four-bar by rigid fixed carrier | corrects WB20/WB21 arm/camera collision | CONTROLLED |
| D-008 | Removable camera uses six electrical functions through SP13 family | six required functions; old four-contact LEMO placeholder was insufficient | CONTROLLED prototype |
| D-009 | Powered lift harness side uses female sockets | safer when camera is removed | CONTROLLED |
| D-010 | WB21 Ø8 local CF99 harness geometry is not controlling | too bulky for source-like lift packaging; source uses compact M12 gland architecture | SUPERSEDED geometry |
| D-011 | WB23B R16 flex-fan / dual-flex-chamber concept stopped | over-engineered; repair photos and drawings show simpler local harness topology | REJECTED |
| D-012 | WB23C controls camera-lift service topology | Proteus evidence supports removable sealed cover + valve + M12 gland + lift cover + camera connector | CONTROLLED |
| D-013 | Service topology does not move lift pivot to X207.5 | no longer necessary after source topology correction | FROZEN X200 |
| D-014 | Local wet lift harness is exactly 6 insulated conductors: +12V, GND, UART TX/RX, CVBS signal/return; optional overall shield is EMC only | matches six-function SP13 interface and user-confirmed six-core architecture; avoids pointless wet splices | FROZEN Rev.B |
| D-015 | Cable pressure seal and electrical service disconnect are separate functions | gland seals jacket; dry connector provides replaceability | CONTROLLED |
| D-016 | PX-1 compact pressure/service cover uses 2 x M4 as prototype choice | practical small cover; direct pressure load is low; exact Proteus screw count not proven | PROTOTYPE HOLD |
| D-017 | M12 gland is horizontal / forward-facing | avoids wasting DN150 roof clearance | CONTROLLED packaging |
| D-018 | Exposed fill-valve procurement was limited to <=Ø14 x 6 mm by WB23F; WB24A now replaces the tall-valve baseline with a flush capped service port | source MiniCam uses cap + screw-on adaptor and current CAD gives better DN150 margin with flush port | SUPERSEDED by D-030 |
| D-019 | Only LOW lift position is required to remain inside DN150 | MID/HIGH are larger-pipe operating positions | FROZEN validation rule |
| D-020 | WB23A absolute one-sided Y coordinates are not manufacturing data | helper Y-sign ambiguity; newer service topology supersedes routing | SUPERSEDED |
| D-021 | No final O-ring groove, cover torque or fill-valve thread is frozen before real samples | sealing depends on actual elastomer, flatness, boss and purchased part | HOLD |
| D-022 | Pressure/service interface must pass +0.25 bar decay + submersion before field release | IP ratings and CAD packaging do not prove crawler pressure sealing | REQUIRED |
| D-023 | Local harness must pass >=500, target 1000 lift cycles plus wet/grit repeat | catalog flexibility alone is not enough for this custom route | REQUIRED |
| D-024 | Local cable target is 6 x 0.25 mm² class, preferred OD about 5.4...6.0 mm, hard package maximum 6.5 mm | electrical drop is acceptable on short local run and both M12 gland/SP13 S6I support this OD class | CONTROLLED target |
| D-025 | Dry J_CAM_LIFT prototype connector is 6-way Molex Micro-Fit 3.0; housings 43025-0600 / 43020-0601; prototype contacts 43030-0007 female / 43031-0007 male | exact six-way service architecture and 20...24 AWG contact class match current cable target | CONTROLLED prototype |
| D-026 | Lower-arm guard conservative envelope is 10 mm for WB23G | gives service/abrasion allowance around <=Ø6.5 cable while retaining ~27.8 mm LOW ideal-DN150 clearance | CONTROLLED packaging |
| D-027 | Historical 8-core WB21/WB23A executed validation remains archived only; it cannot control procurement or wiring | preserves engineering traceability without rewriting past executed data | SUPERSEDED |
| D-028 | Primary physical local-cable sample is LAPP UNITRONIC FD P plus A `0028679`, exactly 6 x 0.25 mm², nominal OD 5.4 mm | best current exact-six-core continuous-flex/PUR mechanical fit; production use still depends on raw-CVBS/UART EMC test because cable is unshielded | PRIMARY SAMPLE / EMC HOLD |
| D-029 | LAPP LiYCY `0034406` remains a shielded six-core A/B comparator, not automatic production winner | fits geometry but has weaker continuous-flex claim; screen alone does not outweigh flex-life requirement | TEST COMPARATOR |
| D-030 | PX1 pressure port uses Proteus-like low-profile capped service topology rather than a permanently tall Schrader body | source drawings show valve shaft/cover/ball/O-rings/spring and official manual uses removable cap + screw-on pressure adaptor | CONTROLLED FUNCTIONAL ARCHITECTURE |
| D-031 | WB24A driving protection-cap target is <=Ø12 x 1.5 mm exposed, with internal valve envelope <=Ø10 x 18 mm at X273/Y0 | executed CAD gives ~9.27 mm cap DN150 clearance and no collision with dry connector/gland; WB23E cover becomes limiting top feature | CONTROLLED PACKAGING / DETAIL HOLD |
| D-032 | Valve service adaptor is removable, mechanically opens the check valve and includes/permits controlled purge before cover opening | mirrors documented Proteus service logic and keeps bulky pneumatic fittings off crawler roof | CONTROLLED TOOL CONCEPT |
| D-033 | Original MiniCam valve dimensions are not reverse-invented; only confirmed topology and explicitly visible source dimensions are reused | individual FSS-001-843/FSS-001-844 detail drawings are not in current source set | FROZEN EVIDENCE RULE |
| D-034 | Source spring geometry `d0.5 / De3.7 / L0 7.9` is a real standard DIN-size candidate but spring force/preload is not frozen from geometry alone | exact same geometry is commercially catalogued; valve adaptor will open check mechanically and bench tests determine preload | PROTOTYPE HOLD |

## Rule for future revisions

A new study may change a controlling decision only when it explicitly:

1. names the decision ID being reopened;
2. gives source/test evidence;
3. checks drivetrain, pressure boundary, DN150 and field service impact;
4. updates this log and the relevant master file.
