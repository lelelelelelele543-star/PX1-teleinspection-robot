# PX-1 current integrated crawler — Rev.B

Date: 2026-09-14
Status: **INTEGRATED MASTER BUILT / WHEEL PROFILE + PHYSICAL TEST HOLDS**

This is the single current crawler assembly. It intentionally stops creating new mechanical concepts where a recovered Proteus solution already exists.

## Assembly chain

`front crawler body -> 3 wheel stations/side -> 5 Z50/side -> rear X250 drive input -> 2 supported motor inputs -> manual lift -> fixed camera carrier -> sealed removable camera`

Service chain:

`dry pressure body -> removable PRESSURE/CAMERA cover -> compact flush pressure valve -> horizontal M12 gland -> 6-core camera harness -> lift-arm guard -> 6-pin SP13 -> camera`.

Rear tether chain follows the recovered Proteus functional stack:

`crawler connector -> spring/contact stack -> cable housing/nut -> seals/gland -> PU sleeve/crimp -> adhesive heatshrink -> cable cup -> reinforced tether`.

## Source-to-PX1 map

| PX-1 assembly | Recovered Proteus source | Current PX-1 implementation |
|---|---|---|
| Side drive | DRW-002-374 | 3 wheel stations/side; X50/X150/X250; five Z50/side; rear long axle |
| Crawler housing / bevel input | DRW-002-375 | dry pressure body; source-style shaft sealing; two Z40 input paths |
| Motor unit | DRW-002-386 | two motors total; supported Z16 shafts/bearings; purchasable motor/coupling candidates |
| Manual lift | DRW-002-744 | two side-link planes; manual lift; 150 N gas spring principle; M8 clamp principle |
| Lift housing / camera interface | DRW-002-752, ASS-002-890 | compact removable top service interface, M12 cable route, camera connector, protected harness |
| Pressure valve | DRW-002-745 / CAM026 valve family | compact protected valve; no tall automotive Schrader baseline |
| Crawler connector | ASS-002-090 | six electrical contacts/function interface reference |
| Tether connector / strain relief | ASS-002-364 | connector spring/housing/nut/seals/gland/PU sleeve/crimp/heatshrink/cable-cup functional stack |
| Wheel lock | ASS-002-103 | quick wheel mounting interface retained as source reference |
| 90 mm wheel for DN150 | MiniCam Proteus catalogue `QRW90SR/150` | official 150 mm compatibility accepted; exact outer profile still needs purchased/measured solid |

## Current hard geometry

- six wheel stations total, X50 / X150 / X250;
- ten m1 Z50 side gears total;
- two traction motors total;
- main body screen: 307 x 92 mm before rear motor extension;
- current motor housing end X384;
- lift body pivot X200;
- lift pivot heights Z92 / 109;
- lift links 90 mm;
- camera pressure shell Ø52 x 78 mm;
- service cover 86 x 44 x 6 mm;
- service opening 48 x 22 mm;
- compact pressure cap Ø12 x 1.5 mm envelope;
- local camera harness: exactly 6 insulated conductors, hard OD max 6.5 mm;
- lower-arm harness guard envelope 10 mm.

## Electrical local camera branch

Exactly six insulated conductors:

1. +12V_HEAD
2. GND_HEAD
3. UART_TX
4. UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

Overall braid, if used, is EMC shielding only.

Dry disconnect candidate: Molex Micro-Fit 3.0 `43025-0600` + `43020-0601`, contacts `43030-0007` / `43031-0007`.

Wet camera disconnect: WEIPU `SP1310/S6I-N` powered harness sockets -> `SP1312/P6-C` camera pins.

## Executed integrated check

The current master contains body, six wheel placeholders, ten Z50, wheel axles, both motor packages, four lift arms, fixed carrier, camera envelope, 150 N gas-spring envelope, service cover, M12 gland, flush pressure valve, dry six-way connector, six-core local harness/guard, SP13 and rear tether/strain-relief envelope.

No unintended collision was found between:

- pressure/service top package and wheel/gear/lift/camera groups;
- lift-harness guard and Z50/camera;
- traction motor bodies and camera envelope.

Current LOW ideal-DN150 clearances for released non-wheel envelopes:

- body: ~7.81 mm;
- service cover: ~7.37 mm;
- flush pressure cap: ~9.27 mm;
- M12 gland: ~13.86 mm;
- lift harness guard: ~27.78 mm;
- rear motor housing: ~18.36 mm.

The full camera TILT sweep remains governed by the already executed camera/lift validation rather than the simple LOW pose in this master.

## Wheel note — do not redesign the crawler around the placeholder

The master currently displays each wheel as a plain Ø90 x 16 cylinder only so the assembly is readable. That cylinder is **not** the real MiniCam wheel profile and therefore is not used for DN150 geometric release.

MiniCam's current wheel compatibility table explicitly specifies `QRW90SR/150` 90 mm soft-rubber wheels for a 150 mm pipe. The recovered drawing pack contains the wheel-lock assembly `ASS-002-103` but not a dimensioned production outer wheel/tire profile. Final DN150 release therefore requires either:

- a purchased QRW90SR/150 measured/modelled directly; or
- the exact missing wheel solid/drawing if recovered later.

Until then the wheel profile is a physical-geometry HOLD, not an architecture-change trigger.

## Files

- executable master: `mechanical/cadquery/PX1_Current_Master_RevB.py`;
- executed result: `mechanical/cadquery/PX1_CURRENT_MASTER_VALIDATION.json`;
- running the master exports `PX1_RevB_Current_Master.step`.

## Only remaining hard gates before machining release

1. exact 90 mm wheel solid/profile and physical DN150 jig;
2. purchased matched Z16/Z40 geometry/mounting distance;
3. actual pressure-cover seal groove from real elastomer;
4. pressure valve +0.25 bar decay/submersion test;
5. six-core cable flex/EMC test;
6. physical SP13/Micro-Fit orientation and pin-number drawing;
7. exact rear connector/tether-tail dimensions from purchased/source hardware;
8. final pressure and wet/grit crawler test.

No new crawler architecture is to be introduced to solve these gates unless source hardware or a physical test proves the current Proteus-derived arrangement impossible.
