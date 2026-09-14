# PX-1 Rev.B WB23G — six-core local camera/lift harness correction

Date: 2026-09-14
Status: **PASS_SIX_CORE_PACKAGING_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / CABLE_SAMPLE_HOLD / PROCUREMENT_HOLD**

## Correction

The local wet lift/camera harness is **six insulated conductors**, not eight.

Controlled functions are one conductor each:

1. `+12V_HEAD`
2. `GND_HEAD`
3. `UART_TX`
4. `UART_RX`
5. `CVBS_SIGNAL`
6. `CVBS_RETURN`

An overall braid/shield may be present for EMC, but it is not counted as a seventh circuit and is never used as DC power return.

The previous idea of two parallel +12 V conductors and two parallel GND conductors is superseded. It added cable diameter, splice points and service complexity without a demonstrated need on the short local lift harness.

## Cable target

- exactly 6 insulated cores;
- target conductor section: `0.25 mm²` class;
- preferred finished OD: `5.5...6.0 mm`;
- hard packaging maximum: `6.5 mm` because the current SP13 S6I plug is a 4.0...6.5 mm cable class and the M12 gland candidate is 3.5...7 mm;
- overall shield preferred for the mixed CVBS/UART/power environment;
- no loose individual wires across the wet lift.

A current size/electrical benchmark is LAPP `UNITRONIC LiYCY 0034406`, 6 x 0.25 mm², shielded, nominal OD 6.0 mm. It is **not released as the final flex cable** because its published application includes fixed installation/occasional flexing rather than a guaranteed lifetime for the PX-1 lift route. It may be bought only as a prototype/sample benchmark and must pass PX-1 flex/wet/grit testing.

## Dry service disconnect

The previous JST VH 8-way candidate is superseded for this local interface.

Reason: JST VH is a useful power family but its normal published conductor range starts around 0.33 mm²; the current local cable target is 0.25 mm².

Prototype dry wire-to-wire candidate:

- receptacle housing: Molex Micro-Fit 3.0 `43025-0600`, 6 circuits;
- plug housing: Molex Micro-Fit 3.0 `43020-0601`, 6 circuits, no panel ears;
- female crimp contact candidate: `43030-0007`, 20/22/24 AWG class;
- male contact: corresponding `43031` family, exact bag/reel article held until the real cable conductor and insulation OD are measured.

This connector is inside the dry pressure body. It is not a pressure seal and does not replace the M12 gland.

## Camera quick disconnect

WB15 remains unchanged:

- sealed camera panel: WEIPU `SP1312/P6-C`, male pins;
- powered lift harness: WEIPU `SP1310/S6I-N`, female sockets;
- six functions map 1:1 through the local cable.

Numeric pin numbers remain HOLD until physical connectors are inspected from the correct mating/front/rear view.

## Mechanical re-screen

WB23G retains:

- WB22A lift geometry and body pivot X200;
- WB23E service cover 86 x 44 x 6 mm;
- WB23E 48 x 22 mm service opening;
- all 6 wheels and all 10 Z50 gears.

To accommodate a real 6 x 0.25 mm² cable, the local cable hard envelope is increased from 5.0 to 6.5 mm and the conservative removable arm-guard envelope from 7 to 10 mm.

Executed CadQuery result:

- fixed package vs all ten Z50: `0 mm³`;
- fixed package vs all six wheel envelopes: `0 mm³`;
- fixed package vs lift arms: `0 mm³` unintended collision;
- fixed package vs camera: `0 mm³`;
- 10 mm guard vs Z50: `0 mm³`;
- 10 mm guard vs camera: `0 mm³`;
- LOW guard ideal-DN150 clearance: about `27.78 mm`;
- service opening still easily accepts the smaller six-way dry connector envelope.

Only LOW is required to fit DN150; MID/HIGH are lift positions for larger pipes.

## Electrical screen

At the current conservative camera-head peak screen of 2.92 A, 0.25 mm² copper remains reasonable for the short local harness. For a 0.4 m local run the copper-only round-trip screen is about 0.164 V drop at room-temperature resistivity, about 1.36% of 12 V; a +20% resistance screen remains about 1.64%. At 0.6 m the +20% screen is about 2.45%.

These are not cable datasheet guarantees. The purchased cable core resistance must be measured and the real voltage at the head recorded under simultaneous camera, LED and motion load.

## Release gates

1. buy one short sample of candidate six-core cable;
2. measure finished OD and individual conductor copper/insulation dimensions;
3. measure resistance per metre of all six cores;
4. verify the real cable fits both M12 gland and SP13 S6I strain relief;
5. crimp the chosen Micro-Fit contacts and perform pull test;
6. run >=500 LOW-HIGH-LOW cycles, target 1000;
7. repeat after wet/grit exposure;
8. inspect jacket, continuity and shield;
9. run raw CVBS + UART while traction/LED PWM are active;
10. only after this freeze exact cable article and numeric six-pin table.

Controlled files:

- `cadquery/PX1_WB23G_SixCoreHarness_RevB.py`;
- `cadquery/REV_B_WB23G_VALIDATION.json`.
