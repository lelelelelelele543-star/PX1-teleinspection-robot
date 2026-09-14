# PX-1 project status — Rev.B snapshot — 2026-09-14

## Controlling architecture

PX-1 remains a Proteus-inspired, serviceable six-wheel inspection crawler:

- 3 wheel stations per side / 6 wheels;
- X50 / X150 / X250;
- 10 x m1 Z50 side gears;
- 2 traction motors;
- rear X250 long-axle input;
- dry pressurized body;
- manual camera lift;
- separately sealed removable camera;
- no mechanical cassette/cartridge architecture;
- no custom PCB required for first working prototype.

## Mechanical state

### WB22A — lift/camera integration

Status: **PASS_SCREEN / MANUFACTURING HOLD / PROCUREMENT HOLD**.

Controls:
- corrected symmetric wet-bay cut;
- four-bar separated from TILT axis by rigid fixed carrier;
- body pivot X200;
- pivots Z92/109;
- link 90 mm;
- arms Y±31, 4 x 14 mm;
- camera Ø52 x 78;
- LOW optical axis X83.5569 / Z75.

### WB23E — current pressure/service cover geometry

Status: **PASS_SEAL_LAND_AND_FULL_INTEGRATION_SCREEN / SEAL_TEST_HOLD / PROCUREMENT_HOLD**.

- cover 86 x 44 x 6 mm;
- service opening 48 x 22 mm;
- 2 x M4 centres X226 / X296;
- provisional groove centre path 4 mm outside opening;
- provisional groove width 2.5 mm;
- minimum M4 hole-edge to groove outer edge 3.5 mm;
- minimum screw-head edge to cover end 4.0 mm;
- minimum groove outer edge to cover Y edge 5.75 mm;
- horizontal LAPP M12 gland packaging retained.

The exact original Proteus small-cover screw count is not claimed. Two M4 screws are a PX-1 prototype choice pending seal/flatness testing.

### WB23F — pressure-port DN150 rule

Status: **PACKAGING RULE FROZEN / VALVE ARTICLE PROCUREMENT HOLD**.

The fill valve is the limiting fixed roof item in LOW. Preferred exposed valve+cap envelope is **<=Ø12 x 5 mm**. The current prototype hard screen is **<=Ø14 x 6 mm** (~4.70 mm ideal-DN150 clearance). Ø14 x 8 mm would fall below the current 3 mm screen and is not acceptable as baseline.

### WB23G — six-core local camera/lift harness

Status: **PASS_SIX_CORE_PACKAGING_SCREEN / SEAL_TEST_HOLD / FLEX_TEST_HOLD / CABLE_SAMPLE_HOLD / PROCUREMENT_HOLD**.

The local wet harness is now explicitly **six insulated conductors**, not eight:

1. +12V_HEAD
2. GND_HEAD
3. UART_TX
4. UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

Overall shield is EMC only, never DC return.

Packaging target:
- conductor target 0.25 mm² class;
- preferred finished OD 5.5...6.0 mm;
- hard package maximum 6.5 mm;
- conservative arm-guard outside envelope 10 mm;
- WB22A X200 lift geometry and WB23E cover remain unchanged.

Executed WB23G result:
- 6 wheels / 10 Z50 retained;
- fixed service package vs wheels/Z50/lift/camera: 0 mm³ unintended collision;
- 10 mm guard vs Z50: 0 mm³;
- 10 mm guard vs camera: 0 mm³;
- LOW guard ideal-DN150 clearance ~27.78 mm;
- 48 x 22 service opening accepts the new compact six-way dry connector envelope.

Only LOW is required to fit DN150; MID/HIGH are larger-pipe lift positions.

## Electrical camera/lift state

Controlled local chain:

`camera/control electronics -> dry 6-way service connector -> six-core shielded cable -> WEIPU SP13 6-pin -> sealed removable camera`.

Dry service candidate is now Molex Micro-Fit 3.0:
- `43025-0600` receptacle housing, 6 circuits;
- `43020-0601` plug housing, 6 circuits;
- female contact candidate `43030-0007`, 20/22/24 AWG class;
- exact mating male contact article held until cable conductor/insulation dimensions are measured.

The old JST VH 8-way candidate and parallel +12/GND local-core scheme are superseded.

Camera wet quick disconnect remains:
- head: WEIPU `SP1312/P6-C`, male pins;
- powered lift harness: WEIPU `SP1310/S6I-N`, female sockets.

Size/electrical cable benchmark: LAPP UNITRONIC LiYCY `0034406`, 6 x 0.25 mm², shielded, nominal OD 6.0 mm. It is **not** a final flex-life release; it must pass the same lift-cycle/wet/grit qualification as any other candidate.

Current copper-only screen at 2.92 A peak shows that one 0.25 mm² +12V core and one 0.25 mm² GND core are reasonable for the short local run. At 0.4 m, the +20% resistance screen is ~0.196 V drop (~1.64% of 12 V); at 0.6 m it is ~0.294 V (~2.45%). Purchased cable resistance and camera-terminal voltage must be measured.

## Pressure/service state

Current roof/service package:
- WB23E cover 86 x 44 x 6 mm;
- opening 48 x 22 mm;
- 2 x M4 at X226/X296;
- horizontal LAPP `53112000` M12 gland candidate;
- preferred fill-valve hard envelope <=Ø12 x 5 mm;
- current fixed ideal-DN150 clearances: cover ~7.37 mm, Ø14 x 6 pressure-port screen ~4.70 mm, gland ~13.86 mm, M4 heads ~7.93 mm.

Pressure release still requires purchased parts, final groove, decay/submersion tests and physical DN150 tolerance validation.

## Source/evidence correction

Repair photographs and MiniCam drawings control the service topology. They support a compact lift housing/cover, M12 cable fitting, camera connector and dedicated lift-arm cover. The project therefore no longer invents large local cable loops where the source demonstrates a compact protected harness.

Historical WB21/WB23A executed files may contain old 8-core/Ø8 studies. They remain archived for traceability but **do not control procurement, wiring or current mechanical packaging**.

## Immediate procurement samples — not bulk release

1. 1–2 x LAPP `53112000` M12 glands;
2. one short sample of six-core shielded cable in the 0.25 mm² / OD <=6.5 mm class;
3. 2 x WEIPU SP13 six-pin working pairs;
4. Molex Micro-Fit 3.0 six-way housings + test crimp contacts;
5. 2–3 candidate very low-profile fill valves, preferably <=Ø12 x 5 mm exposed with cap;
6. FKM 2 mm cord / candidate molded seal material.

## Immediate physical prototypes

1. 3D-print dummy WB23E pressure cover and 10 mm-envelope arm guard on Anycubic Chiron for fit/access only.
2. Machine first aluminium cover coupon after real gland/valve arrive.
3. Build a pressure-box coupon reproducing cover/gland/valve geometry before risking the complete crawler body.
4. Build a lift-cycle fixture with actual six-core cable, SP13 and guard.

## Qualification gates before machining release

- exact purchased-part measurement;
- +0.25 bar pressure decay;
- submerged leak test;
- >=500 lift cycles, target 1000;
- wet/grit repeat;
- post-cycle pressure test;
- raw CVBS + UART + power under simultaneous motor/LED interference;
- measure cable resistance and camera voltage under maximum load;
- physical DN150 jig with final pressure cap/gland/screw heads;
- final full-master tolerance/collision check;
- only then freeze manufacturing drawing/BOM and STL/STEP handoff.

## Next controlled work blocks

- WB24A: select and dimension real fill valve/gland/seal, then release exact pressure-service boss/groove study;
- WB24B: buy/measure six-core cable + Micro-Fit/SP13 samples, then freeze numeric six-pin table;
- WB25: complete crawler master with purchased connector/fastener/valve envelopes;
- release candidate: prototype body/lift drawings, arm guard, service cover and assembly/service documentation.
