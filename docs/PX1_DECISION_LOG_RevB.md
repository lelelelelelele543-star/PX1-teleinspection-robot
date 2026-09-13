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
| D-010 | WB21 Ø8 local CF99 harness geometry is not controlling | too bulky for source-like lift packaging; source uses compact M12 3.5–5 mm gland architecture | SUPERSEDED geometry |
| D-011 | WB23B R16 flex-fan / dual-flex-chamber concept stopped | over-engineered; repair photos and drawings show simpler local harness topology | REJECTED |
| D-012 | WB23C controls camera-lift service topology | Proteus evidence supports removable sealed cover + valve + M12 gland + lift cover + camera connector | CONTROLLED |
| D-013 | WB23C does not move lift pivot to X207.5 | no longer necessary after source topology correction | FROZEN X200 |
| D-014 | Local wet lift harness target <=5 mm OD, 8 insulated cores + shield preferred | fits M12 gland/source topology and supports paired power conductors + UART + CVBS | CONTROLLED target |
| D-015 | Cable pressure seal and electrical service disconnect are separate functions | gland should seal jacket; dry connector should provide replaceability | CONTROLLED |
| D-016 | PX-1 compact pressure/service cover uses 2 x M4 as prototype choice | practical small cover; direct pressure load is low; exact Proteus screw count not proven | PROTOTYPE HOLD |
| D-017 | M12 gland is horizontal / forward-facing in WB23C | avoids wasting DN150 roof clearance | CONTROLLED packaging |
| D-018 | Fill valve must remain low-profile, <=Ø14 x 6 mm hard envelope until exact part is selected | current DN150 limiting fixed item is pressure port | PROCUREMENT HOLD |
| D-019 | Only LOW lift position is required to remain inside DN150 | MID/HIGH are larger-pipe operating positions | FROZEN validation rule |
| D-020 | WB23A absolute one-sided Y coordinates are not manufacturing data | helper Y-sign ambiguity; WB23C supersedes routing | SUPERSEDED |
| D-021 | No final O-ring groove, cover torque or fill-valve thread is frozen before real samples | sealing depends on actual elastomer, flatness, boss and purchased part | HOLD |
| D-022 | Pressure/service interface must pass +0.25 bar decay + submersion before field release | IP ratings and CAD packaging do not prove crawler pressure sealing | REQUIRED |
| D-023 | Local harness must pass >=500, target 1000 lift cycles plus wet/grit repeat | catalog flexibility alone is not enough for this custom route | REQUIRED |

## Rule for future revisions

A new study may change a controlling decision only when it explicitly:

1. names the decision ID being reopened;
2. gives source/test evidence;
3. checks drivetrain, pressure boundary, DN150 and field service impact;
4. updates this log and the relevant master file.
