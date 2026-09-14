# PX1 Current BOM

Controlling tabular BOM in the release package: `PX1_Current_BOM.csv`.

| ID | Qty | Item | Article | Source | State | Notes |
|---|---:|---|---|---|---|---|
| MECH-001 | 1 | Main pressure body | PX1 custom EN AW-6082-T6 | Proteus-derived / PX1 adaptation | HOLD_MACHINING | exact cover/side interfaces remain open |
| BRG-61903 | 6 | Deep groove bearing | 61903-2RS | SKF/standard | BUY | 17x30x7 |
| BRG-61801-SIDE | 12 | Deep groove bearing | 61801-2RS | SKF/standard | BUY | 12x21x5; 6 per side source quantity |
| BRG-61801-Z16 | 2 | Z16 support bearing | 61801-2RS | SKF/standard | BUY | 12x21x5 |
| BRG-61800 | 2 | Z40 shaft bearing | 61800-2RS | SKF/standard | BUY | 10x19x5 |
| SEA-XRING | 6 | Dynamic X-ring | 18.72x2.62 | source size | BUY_SAMPLE | material compatibility test |
| SEA-SHAFT | 2 | Rotary shaft seal | 18x30x7 | source size | BUY_SAMPLE | lip material pressure/water test |
| GEAR-Z50 | 10 | Spur gear | m1 Z50 B4 | GEA-002-528/529 logic | HOLD_TOOTH_DETAIL | PA/bore/key details unresolved |
| GEAR-Z16 | 2 | Bevel pinion | m1 Z16 | GEA-002-531 logic | HOLD_SUPPLIER_DRAWING | matched pair required |
| GEAR-Z40 | 2 | Bevel gear | m1 Z40 | GEA-002-530 logic | HOLD_SUPPLIER_DRAWING | matched pair required |
| WHL-090 | 6 | 90 mm wheel | MiniCam QRW90SR/150 class | MiniCam | BUY_SAMPLE | exact outer profile/hub measurement required |
| MOT-032 | 3 | 24 V planetary gearmotor | ISL PGM-32P-24-100-60-02 / MOT-IG32PGM 100 | ISL Products | BUY_SAMPLE | 2 build + 1 spare; OD32 verified; length/flange measure |
| CPL-020 | 3 | Rigid coupling 6/6 | NBK MLR-20C-6-6 | NBK | BUY | OD20 L24; rated torque gate |
| GLD-M12 | 2 | Cable gland | LAPP 53112000 SKINTOP MS-M 12x1.5 | LAPP | BUY | 3.5-7 mm cable, SW16, L26.5 |
| CON-CAM-D | 1 | 6-way receptacle | Molex 43025-0600 | Molex | BUY | Micro-Fit 3.0 |
| CON-CAM-P | 1 | 6-way plug | Molex 43020-0601 | Molex | BUY | Micro-Fit 3.0 |
| CON-SP13-A | 1 | 6-way wet connector | WEIPU SP1310/S6I-N | WEIPU | BUY_SAMPLE | exact variant geometry measure |
| CON-SP13-B | 1 | 6-way panel connector | WEIPU SP1312/P6-C | WEIPU | BUY_SAMPLE | exact variant geometry measure |
| MCU-001 | 1 | Main controller | STM32 NUCLEO-F446RE | ST | BUY | 82.5x70 footprint |
| DRV-001 | 2 | Traction H-bridge module | BTS7960 / IBT-2 | marketplace module | BUY_SAMPLE | variant geometry/current validation required |
| DCDC-HV | 1 | HV to 24 V DC/DC | Cincon CQB150W-110S24 | Cincon | BUY | 43-160 V input class, quarter-brick 57.9x36.8x12.7 |
| CAP-HV | 1 | HV bulk capacitor | Nichicon UCS2D221MHD1TN | Nichicon | BUY | 220uF 200V D18x25 |
| VID-001 | 1 | Passive video balun | Delta-Opti TR-1D*P2 | Delta-Opti | BUY | 43x16x15; bench EMC/cable test required |
| DCDC-12 | 1 | 24 to 12 V module | LM2596 ready-made module | marketplace/ChipDip | BUY_SAMPLE | exact board variant dimensions required |
| DCDC-5 | 1 | 12 to 5 V module | MP1584 ready-made module | marketplace/ChipDip | BUY_SAMPLE | exact board variant dimensions required |
| RS485-01 | 1 | RS-485 interface module | MAX485 ready-made module | marketplace/ChipDip | BUY_SAMPLE | exact board variant dimensions required |
| PRS-001 | 1 | Pressure sensor | ТРЕБУЕТСЯ ВЫБОР АРТИКУЛА | marketplace/ChipDip | HOLD | 0..~0.5 bar gauge preferred, 5 V analog/digital module |
| GAS-001 | 1 | Gas spring | ACE GS-12-20-V4A class, 150 N target | ACE | BUY_SAMPLE | end fittings/length physical closure |
| CAB-LOC | 1 | Local camera cable | 6x0.25 mm2, OD<=6.5 | LAPP candidate 0028679 | BUY_SAMPLE | exactly six insulated conductors; flex/EMC test |
| CAB-TETH | 40 | Main reinforced tether | professional 6-core copper + aramid | HOLD exact article | HOLD | initial 40 m; no coax/fibre |
