# PX-1 Rev.B — camera-head controlled BOM / WB15

Date: 2026-09-11
Status: PROTOTYPE PROCUREMENT LIST / SUPERSEDES WB14 BOM FOR ACTIVE HEAD INTERFACE

| Item | Qty | Article / family | Source status | Controlled dimensions / ratings | Installation | Release status |
|---|---:|---|---|---|---|---|
| Analog camera | 1 + 1 spare preferred | RunCam Phoenix 2, `PHOENIX2-SL` family | manufacturer active; marketplace routes exist | ~19 x 19 x 19...20 mm; 5...36 V; M12 lens | removable carrier inside integrated ROLL frame | SELECTED / SAMPLE HOLD |
| Internal ROLL slip ring | 1 + 1 spare | SenRing `M125-06` | manufacturer standard-stock family | Ø12.5 x 13.5 mm; 6 x 1.5 A; AWG30 leads | coaxial non-structural transfer inside 6803 ID17 passage | SELECTED / VIDEO TEST HOLD |
| ROLL bearings | 2 | 6803-2RS / 61803-2RS | exact brand/source HOLD | 17 x 26 x 5 mm | spaced seats in integrated inner ROLL spindle/carrier | GEOMETRY RETAINED / BRAND HOLD |
| Head panel connector | 1 + 1 spare | WEIPU `SP1312/P6-C` | exact active distributor stock verified | 6 pin; 5 A/contact; 125 V; IP68 family; OD ~19.5 mm; M13x1; panel cutout Ø13 with 11.8 flat; panel <=3.5 mm | centered in 3.0 mm rear bulkhead within Ø36 mechanical register; rear-nut mount | SELECTED / PRESSURE+VIDEO HOLD |
| Crawler/lift cable connector | 1 + 1 spare | WEIPU `SP1310/S6I-N` | exact active distributor stock verified | 6 socket; 5 A/contact; 125 V; IP68 family; OD ~18.8 mm; L ~49 mm; cable OD 4...6.5 mm | straight cable plug; female powered side; >=60 mm extraction clearance | SELECTED / HARNESS HOLD |
| Video balun | one camera-side + one CCU-side pair | Delta-Opti `TR-1D*P2`, EAN 5902887011313 | current marketplace route verified | body ~16 x 15 x 43 mm plus local BNC lead | crawler/lift fixed side after SP13; not inside continuous ROLL | SELECTED / COMPLETE-LINK TEST HOLD |
| White LED emitter | 6 + 2 spares | Cree XP-G / XP-G3 white family; prior target `XPGDWT-B1-0000-00LE2` where traceable | exact controlled-bin source HOLD | 3535 emitter class | six separate 8 mm MCPCB sites on PCD40 | FAMILY SELECTED / EXACT BIN HOLD |
| Small LED MCPCB | 6 + spares | standard 8 mm 3535 aluminium MCPCB | marketplace families indexed | 8 mm class; thickness sample-driven | shallow pocket + thermal compound + removable clamp ring | PROTOTYPE SOURCE / SAMPLE HOLD |
| LED current driver | 2 + 1 spare | `P4115adj` ready module | active marketplace route | ~29.3 x 15.1 x 9 mm; adjustable constant current | fixed-side head electronics; one per 3-LED string | SELECTED / DROPOUT+THERMAL HOLD |
| Front optical window | 1 + spare | tempered mineral glass or sapphire candidate | exact article/source HOLD | target Ø28 x 3 mm | static mechanically retained FKM-sealed window | GEOMETRY TARGET / SOURCE+GLAND HOLD |
| Camera lens | 1 | stock RunCam M12 2.1 mm for first test | included | ~155 deg class FOV | threaded M12; final focus/FOV test-driven | DEMO BASELINE / FINAL FOV HOLD |
| Narrower lens test | 1 if required | 5 mm M12, 1/2 in-compatible class | exact marketplace article HOLD | target ~75 deg horizontal class | substitute only after BFL/image-circle test | OPTICAL TARGET / PROCUREMENT HOLD |
| Fixed-side local controller | 1 optional | RP2040-Zero-class ready module | marketplace routes available | ~18 x 23.5 mm class | fixed head side only; never on continuous ROLL carrier | ARCHITECTURE OPTION / PACKAGING HOLD |
| Camera-axis drivers | 2 | DRV8871-class ready modules | exact board/source HOLD | board envelope sample-driven | fixed-side carrier, one per TILT/ROLL motor | FAMILY RETAINED / EXACT MODULE HOLD |
| Local six-core head harness | 1 | exact flexible 6-core cable TBD in WB16 | not frozen | must fit SP1310 version-I cable OD 4.0...6.5 mm | crawler/lift fixed harness to head connector | WB16 HOLD |

## External head logical allocation

The active six functions are:
- +12V_HEAD
- GND_HEAD
- HEAD_UART_TX
- HEAD_UART_RX
- CVBS_SIGNAL
- CVBS_RETURN

Numeric contact numbers remain HOLD until the first SP13 pair is physically inspected and front/rear-view numbering is confirmed.

## Procurement rule

A `HOLD` line is not permission to buy an arbitrary visual substitute.

Before machining around a purchased module, record:
- exact supplier/listing;
- manufacturer article;
- photo/label;
- measured X/Y/Z dimensions;
- mounting/lead exit;
- electrical revision where applicable.

## Errors closed through WB15

- larger CCTV board is not adopted because RunCam already satisfies analog/size requirement;
- Ø16 LED stars are rejected for Ø52/Ø28 front geometry;
- Ø22 M220 is rejected for camera internal ROLL because it cannot pass 6803 ID17;
- fixed-shell lighting and camera-axis drive currents do not cross internal ROLL;
- LEMO 0K.304 placeholder is retired because it has only four LV contacts;
- connector ingress rating is not treated as camera-head pressure proof;
- no cartridge/cassette camera mechanics are permitted.

## Next controlled BOM gate — WB16

Freeze:
- exact six-core local cable article/source;
- cable OD/bend radius;
- conductor cross-section;
- SP13 numeric contact map;
- local video/UART pairing and strain-relief geometry.
