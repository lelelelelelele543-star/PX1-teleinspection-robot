# PX-1 Rev.B — camera-head controlled BOM / WB16

Date: 2026-09-11
Status: PROTOTYPE PROCUREMENT LIST / SUPERSEDES WB15 BOM WHERE HARNESS OR CABLE-PLUG VARIANT DIFFERS

| Item | Qty | Exact article / family | Current source status | Controlled data | Installation | Release status |
|---|---:|---|---|---|---|---|
| Analog camera | 1 + 1 spare preferred | RunCam Phoenix 2 `PHOENIX2-SL` family | manufacturer/marketplace routes | ~19 x 19 x 19...20 mm; 5...36 V; CVBS | removable carrier inside integrated ROLL frame | SELECTED / SAMPLE HOLD |
| Internal ROLL slip ring | 1 + 1 spare | SenRing `M125-06` | manufacturer standard family | Ø12.5 x 13.5 mm; 6 x 1.5 A | non-structural coaxial transfer inside 6803 ID17 passage | SELECTED / VIDEO HOLD |
| ROLL bearings | 2 | 6803-2RS / 61803-2RS | exact brand HOLD | 17 x 26 x 5 mm | spaced seats in integrated ROLL spindle/carrier | GEOMETRY RETAINED |
| Head panel connector | 1 + 1 spare | WEIPU `SP1312/P6-C` | current active/orderable | 6 male; 5 A/contact; 125 V; IP68 family; OD ~19.5; M13x1; panel cutout Ø13 / 11.8 flat; panel <=3.5 | non-TILT rear support/yoke-base bulkhead, 3.0 mm land | SELECTED / PRESSURE+VIDEO HOLD |
| Lift-harness cable connector | 1 + 1 spare | WEIPU `SP1310/S6II-N` | active; current distributor/marketplace listings | 6 female; 5 A/contact; 125 V; cable OD 5...8 mm; ~Ø18.8 x 49 mm | cable side; powered harness uses recessed sockets | SELECTED / SAMPLE HOLD |
| External manual-lift harness cable | buy 3 m; final cut <=0.50 m each until routing freeze | LAPP `0027429` UNITRONIC FD CY 7X0.25 | current product; TME Czech displayed 200 m at latest check | 7 x 0.25 mm²; OD6.7; shielded; 79 ohm/km max/core; continuous-flex; dynamic Rmin50.3 | along one parallelogram arm, design R>=55; six used cores + one insulated spare | SELECTED / DN150 ROUTE+CVBS HOLD |
| Video balun | 2 system ends | Delta-Opti `TR-1D*P2`, EAN 5902887011313 | current route verified | body ~16 x 15 x 43 mm + local BNC lead | crawler fixed side after lift harness; CCU second end | SELECTED / COMPLETE LINK HOLD |
| White LEDs | 6 + 2 spares | Cree XP-G / XP-G3 family; prior target `XPGDWT-B1-0000-00LE2` where traceable | exact bin HOLD | 3535 class | six 8 mm MCPCB sites PCD40 | FAMILY SELECTED |
| Small LED MCPCB | 6 + spares | standard 8 mm 3535 aluminium MCPCB | marketplace | Ø8 class | shallow pocket + thermal compound + clamp | PROTOTYPE SOURCE |
| LED driver | 2 + 1 spare | `P4115adj` ready module | active marketplace route | ~29.3 x 15.1 x 9 mm | fixed-side head electronics; 1 per 3-LED string | SELECTED / THERMAL HOLD |
| Optical window | 1 + spare | tempered mineral glass or sapphire candidate | exact article HOLD | target Ø28 x 3 | static FKM-sealed mechanical retention | GEOMETRY TARGET |
| Camera lens | 1 | stock RunCam M12 2.1 mm initially | included | wide FOV | M12, locked after focus | DEMO BASELINE |
| Local controller | 1 | RP2040-Zero-class ready module | marketplace | ~18 x 23.5 mm class | fixed side relative to continuous ROLL | PACKAGING HOLD |
| Camera-axis motor | 2 | `DCGM-N20-12V-EN-200RPM` family | selected project article/source gate | 12 V; ~200 rpm; encoder; 1:150; stall <=1.1 A target | TILT and ROLL drive stations | SELECTED / SAMPLE HOLD |
| Camera-axis drivers | 2 | DRV8871-class ready modules | exact board source HOLD | module envelope sample-driven | one per axis | FAMILY RETAINED |
| Internal TILT electrical transfer | TBD | WB17 | not frozen | must accommodate ±105 deg without violating head pressure boundary | source-like integrated wiring/feedthrough, no cartridge | WB17 BLOCKER |

## WB16 external harness colour map

- WH = +12V_HEAD
- BN = GND_HEAD
- GN = HEAD_UART_TX
- YE = HEAD_UART_RX
- GY = CVBS_SIGNAL
- PK = CVBS_RETURN
- BU = NC_SPARE_HEAD

Numeric SP13 contact numbers remain HOLD until actual sample continuity mapping.

## Procurement action for first bench build

Buy first:
- 3 m LAPP 0027429;
- 2 x WEIPU SP1310/S6II-N;
- 2 x WEIPU SP1312/P6-C;
- one additional spare of each connector half if cost allows.

Do not buy `SP1310/S6I-N` for the LAPP 0027429 harness: its 6.5 mm maximum cable range is below the selected cable nominal 6.7 mm.

## Supersession note

WB15 BOM references to `SP1310/S6I-N` are superseded by this file because WB16 selected the real cable article after WB15 connector screening.

The panel connector, six electrical functions, pressure test requirement and mechanical register remain unchanged.
