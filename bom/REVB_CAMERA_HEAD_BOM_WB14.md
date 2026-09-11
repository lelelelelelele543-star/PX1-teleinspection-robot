# PX-1 Rev.B — camera-head controlled BOM / WB14

Date: 2026-09-11
Status: PROTOTYPE PROCUREMENT LIST / RELEASE HOLDS SHOWN EXPLICITLY

| Item | Qty | Article / family | Source status | Controlled dimensions | Installation | Release status |
|---|---:|---|---|---|---|---|
| Analog camera | 1 + 1 spare preferred | RunCam Phoenix 2, `PHOENIX2-SL` family | RunCam manufacturer active; AliExpress marketplace listings for standard Phoenix 2 currently indexed | ~19 x 19 x 19...20 mm; M12 lens; ~9 g | M2-based removable carrier inside integrated ROLL frame; real sample controls holes | SELECTED / SAMPLE HOLD |
| Camera slip ring | 1 | SenRing `M125-06` | Manufacturer standard-stock family; exact approved marketplace route still HOLD | Ø12.5 x 13.5 mm; 6 x 1.5 A; AWG30 leads | Coaxial non-structural rotary interface inside 17 mm ID ROLL bearing passage; retained by normal holder, not used as bearing | ENGINEERING SELECTED / PROCUREMENT+VIDEO HOLD |
| ROLL bearings | 2 | 6803-2RS / 61803-2RS family | exact brand/source HOLD | 17 x 26 x 5 mm | spaced bearing seats in ordinary integrated ROLL carrier | GEOMETRY RETAINED / BRAND HOLD |
| Video balun | 1 crawler-side half + matching CCU half | Delta-Opti `TR-1D*P2` pair, EAN 5902887011313 | current marketplace route verified | body ~16 x 15 x 43 mm plus local BNC lead | fixed side after camera slip ring; mechanically clipped/strain relieved | SELECTED / COMPLETE-LINK TEST HOLD |
| White LED emitter | 6 + 2 spares | Cree XP-G / XP-G3 white family; previous exact target `XPGDWT-B1-0000-00LE2` retained when traceable | exact controlled-bin source still HOLD; marketplace 8 mm XP-G3 assemblies exist for prototype | emitter 3535 class on 8 mm-class MCPCB | six separate thermally clamped positions on PCD40 | FAMILY SELECTED / EXACT BIN HOLD |
| Small LED MCPCB | 6 + spares | standard 8 mm 3535 aluminium MCPCB compatible with XP-G family | AliExpress marketplace families currently indexed in 8/10/12/14/16/20 mm sizes | 8 mm-class; actual thickness sample-driven | shallow front-carrier pocket + thermal compound + removable clamp ring | PROTOTYPE SOURCE / SAMPLE HOLD |
| LED current driver | 2 + 1 spare | `P4115adj` ready module | current Allegro marketplace listing | PCB 29.3 x 15.1 x 9 mm | fixed-side electronics carrier; one module per 3-LED string; screw/terminal service access | SELECTED / DROPOUT+THERMAL HOLD |
| Front optical window | 1 + spare | tempered mineral glass or sapphire candidate | exact article/source HOLD | current target Ø28 x 3 mm | static mechanically retained window with dedicated FKM seal; not adhesive-only | GEOMETRY TARGET / SOURCE+GLAND HOLD |
| Camera lens | 1 | stock RunCam 2.1 mm M12 for first test | included with camera | ~155 deg class FOV | threaded M12, focus locked only after pipe test | DEMO BASELINE / FINAL FOV HOLD |
| Narrower lens reference | 1 test article if required | 5 mm M12, 1/2 in sensor-compatible class | controlled manufacturer examples exist; approved marketplace exact article still HOLD | engineering target ~75 deg horizontal, lens OD ~17 mm class | replace stock M12 only after BFL/image-circle/focus check | OPTICAL TARGET / PROCUREMENT HOLD |
| Fixed-side local controller | 1 optional | RP2040-Zero class ready module | marketplace/official routes available; exact article not yet repurchased for WB14 | ~18 x 23.5 mm class | fixed side only; never on continuous ROLL carrier | ARCHITECTURE OPTION / PACKAGING HOLD |
| Camera-axis drivers | 2 | DRV8871-class ready modules | exact board/source HOLD | reference ~26 x 20 x 8 mm class | fixed-side carrier, one per TILT/ROLL motor | FAMILY RETAINED / EXACT MODULE HOLD |

## Procurement rule

A line marked `HOLD` is not permission to buy an arbitrary substitute of similar appearance.

Before machining around a purchased module, record:
- actual supplier/listing;
- photo/label;
- measured X/Y/Z dimensions;
- mounting-hole positions;
- connector/lead exit;
- electrical revision where applicable.

## Camera-specific errors now closed

- larger 34 mm CCTV board camera is not adopted because RunCam already meets the analog/packaging requirement;
- Ø16 star LED boards are not used in the Ø52/Ø28 front geometry;
- Ø22 M220 is not used in the camera because it conflicts with the 17 mm central ROLL passage;
- fixed-shell lighting does not cross the camera ROLL slip ring;
- no cartridge/cassette camera module is permitted;
- old digital/Ethernet Rev.FA camera path is historical and does not control this BOM.
