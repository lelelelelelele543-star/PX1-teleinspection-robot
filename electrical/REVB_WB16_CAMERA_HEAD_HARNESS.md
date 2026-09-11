# PX-1 Rev.B — WB16 camera-head external lift harness

Date: 2026-09-11
Status: PROTOTYPE CABLE ARTICLE SELECTED / ROUTING + CVBS QUALIFICATION HOLD

## 1. Scope

WB16 controls the flexible cable between:
- crawler/front-body camera electrical interface; and
- the removable camera-head SP13 connector mounted on the head assembly rear support / yoke-base interface.

This cable moves with the **manual lift**.

It is NOT the internal wiring that crosses the camera TILT pivot and it is NOT the six-core main inspection tether.

Internal TILT wiring/feedthrough is a separate work block because combining those two motions created false packaging conclusions in earlier notes.

## 2. Important mechanical correction

The WB15 SP13 panel connector belongs on the non-TILT rear support of the removable camera-head assembly, not on the Ø52 optical shell that sweeps through ±105 deg TILT.

Reason:
- SP1310 straight cable plug is approximately 49 mm long;
- placing that plug axially on the tilting optical shell would add a large rigid swept length behind the Ø52 camera;
- the existing DN150 camera-only check had only ~7.6 mm ideal minimum clearance and explicitly excluded connectors/cable loops;
- therefore treating the SP13 plug as a tilting-shell appendage would invalidate the DN150 claim.

The complete removable head assembly may include the yoke/support. Its external service connector stays fixed relative to that support while the optical shell performs TILT internally.

## 3. Selected cable article

Manufacturer: LAPP
Family: `UNITRONIC FD CY`
Exact article: `0027429`
Description: `UNITRONIC FD CY 7X0,25`
EAN route used by distributor: `4044773017502`

Manufacturer-controlled characteristics:
- 7 cores x 0.25 mm²;
- bare-copper extra-fine conductors;
- DIN 47100 core colours;
- tinned-copper overall braid shield;
- PVC outer sheath;
- nominal OD 6.7 mm;
- mass ~75 kg/km;
- maximum conductor resistance at 20 C: 79 ohm/km;
- conductor/conductor capacitance approx. 110 nF/km;
- conductor/shield capacitance approx. 171 nF/km;
- inductance approx. 0.725 mH/km;
- continuously-flexing/cable-chain product;
- dynamic minimum bending radius: 50.3 mm;
- fixed minimum bending radius: 26.8 mm;
- flexible temperature range -5...+70 C;
- not approved for torsional loading.

Current procurement route checked 2026-09-11:
- TME Czech symbol `UTR-FD-CY-7X0.25`;
- displayed stock at check: 200 m;
- sold by metre.

## 4. Why seven cores are accepted for a six-contact connector

The electrical interface still has six functions only:
1. +12V_HEAD
2. GND_HEAD
3. HEAD_UART_TX
4. HEAD_UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

The seventh cable core is an **unused physical spare**. It does not become a seventh system signal and does not alter the main architecture.

Rules:
- spare core is individually insulated at both ends;
- spare is not paralleled with power;
- spare is not used as shield/drain;
- spare is labelled `NC_SPARE_HEAD`.

## 5. Core-colour allocation

LAPP specifies DIN 47100 colour identification. Prototype harness allocation:
- white (WH) -> +12V_HEAD;
- brown (BN) -> GND_HEAD;
- green (GN) -> HEAD_UART_TX;
- yellow (YE) -> HEAD_UART_RX;
- grey (GY) -> CVBS_SIGNAL;
- pink (PK) -> CVBS_RETURN;
- blue (BU) -> NC_SPARE_HEAD.

This colour mapping is frozen as the intended build map but must be visually verified on the purchased cut before soldering.

Connector **numeric contact numbers remain HOLD** until the actual WEIPU pair is inspected from the defined mating/front view. Colour allocation and contact-number allocation are separate controls.

## 6. Shield rule

The LAPP overall braid is not an additional circuit and must never carry load current.

Forbidden:
- shield -> CVBS_RETURN;
- shield -> GND_HEAD as a normal return conductor;
- shield -> seventh SP13 contact (there is no seventh contact);
- shield used to compensate for a missing conductor.

Prototype termination:
- head/SP13 plug end: braid trimmed back, insulated and strain-relieved; no connection through the plastic SP13 shell;
- crawler fixed end: provide a labelled shield pigtail/clamp point for EMC A/B testing;
- final single-point bond/floating choice remains HOLD until the crawler chassis/logic-ground bonding rule and video-noise test are frozen.

No shield bond is allowed to create a parallel current-return path.

## 7. SP13 cable-plug correction

The previously selected `SP1310/S6I-N` accepts cable OD 4.0...6.5 mm.

LAPP 0027429 nominal OD is 6.7 mm, so forcing it into the I-version gland is prohibited.

Replace only the cable half with:
- WEIPU `SP1310/S6II-N`;
- female sockets;
- six contacts;
- 5 A/contact;
- 125 V class;
- cable range 5...8 mm;
- straight threaded cable connector;
- approx. Ø18.8 x 49 mm class.

The panel half remains:
- WEIPU `SP1312/P6-C` male six-pin rear-nut receptacle.

WEIPU SP1310 II differs in cable outlet range, not the six-contact mating architecture; SP1310 family mates SP1312.

## 8. Electrical drop screen

Use manufacturer maximum conductor resistance 79 ohm/km.

Until exact routing is frozen, maximum one-way prototype harness length is limited to 0.50 m.

At 0.50 m:
- one conductor R <= 0.0395 ohm;
- +12/GND loop R <= 0.079 ohm.

Calculated drops:
- 0.5 A -> <=0.040 V;
- 1.0 A -> <=0.079 V;
- 1.2 A -> <=0.095 V;
- 2.0 A -> <=0.158 V;
- 3.0 A short fault/transient screen -> <=0.237 V.

Pair copper loss:
- 1.2 A -> ~0.114 W total in +12/GND pair;
- 3.0 A -> ~0.711 W total, therefore 3 A is a transient/fault screen, not an approved continuous operating point.

The existing camera-branch fuse/current limits remain responsible for preventing sustained motor-stall current.

## 9. Mechanical lift-routing screen

Existing Rev.FN lift kinematics:
- body pivot midpoint approx. X200 / Z102;
- LOW camera axis approx. X83.557 / Z75;
- MID approx. X82.851 / Z130;
- HIGH approx. X135.2 / Z205.

Straight anchor distance from body pivot midpoint to head pivot region:
- LOW ~119.53 mm;
- MID ~120.45 mm;
- HIGH ~121.69 mm.

Total change LOW -> HIGH is only ~2.16 mm because the manual mechanism is a parallelogram.

Consequence:
- do not make a large hanging U-loop to absorb lift travel;
- route the cable alongside one 120 mm lift arm;
- use controlled relaxed bend/service arcs at the two pivot regions;
- clamp the jacket, not individual conductors;
- preserve cable orientation so motion is bending, not torsion.

## 10. Bend-radius rule

Manufacturer dynamic minimum = 50.3 mm.

PX-1 design minimum for WB16:
- `R_route >= 55 mm` wherever the cable repeatedly flexes;
- no kink directly behind SP1310 backshell;
- no zip tie/clamp inside the first bend that forces radius below 55 mm;
- cable may be fixed straighter along the middle of a lift arm.

The 55 mm routing envelope has **not yet passed full DN150 solid clearance**. Existing Rev.FN clearance results explicitly excluded flexible cable loops.

Therefore WB16 is electrically selected but mechanically HOLD until the R55 path is included in the LOW and DN150_SAFE assemblies.

## 11. Harness length and procurement

Prototype purchase:
- buy 3 m LAPP 0027429 minimum.

Reason:
- allows two trial harnesses plus destructive bend/termination samples;
- avoids locking final cut length before routing jig/CAD is verified.

Initial assembly rule:
- no field harness cut longer than 0.50 m until voltage-drop and routing are rechecked;
- determine final cut length from the physical lift jig with LOW/MID/HIGH positions and R55 templates;
- leave service allowance at connectors without forming a tight coil.

## 12. SP13 pin-number release procedure

Do not guess connector numbers from a front-view internet drawing.

On incoming sample:
1. photograph male and female mating faces;
2. photograph solder side;
3. record every moulded contact number;
4. continuity-map male pin N to female socket N;
5. define one controlled viewing convention;
6. then freeze numeric mapping in WB16B.

The colour/function map above is already fixed; only physical contact numbers remain HOLD.

## 13. CVBS / EMC qualification

LAPP 0027429 is a shielded low-frequency data/control cable, not a 75-ohm video cable.

The local raw-CVBS run is short, but acceptance still requires measurement.

Test sequence adds this exact harness to WB12:
- RunCam direct baseline;
- M125 internal ROLL interface;
- head internal wiring;
- SP1312/SP1310 connector pair;
- 0.5 m maximum LAPP 0027429 harness;
- Delta-Opti balun;
- main tether/reel chain.

Run with:
- TILT motor switching;
- ROLL motor switching;
- LED PWM;
- traction PWM.

Test shield at least in:
- head end isolated + crawler end floating;
- head end isolated + crawler end single-point bonded to the finally approved chassis/EMC reference.

Select the lower-noise configuration without creating a ground loop.

## 14. Serviceability

- SP1310 can be replaced without opening camera pressure shell;
- harness follows lift arm and is externally inspectable;
- clamps are captive/common fastener type;
- at least one clamp near each end is removable without dismantling the parallelogram;
- abrasion sleeve may be added only where it does not reduce bend radius below 55 mm;
- no adhesive-only strain relief.

## 15. WB16 release gates

1. buy exact LAPP 0027429 cut and SP1310/S6II-N;
2. measure cable OD at several points; reject if real OD cannot be safely clamped by II gland;
3. verify seven DIN47100 colours;
4. build 0.50 m bench harness and measure loop resistance;
5. run 1.2 A continuous thermal test in still air;
6. perform short protected 3 A transient/drop test;
7. verify UART with TILT/ROLL/LED PWM active;
8. verify raw CVBS through harness and SP13;
9. model/fit R55 route in LOW/MID/HIGH lift positions;
10. run DN150 LOW and DN150_SAFE solid sweep including actual cable OD and clamps;
11. cycle manual lift at least 500 prototype cycles and inspect jacket/shield migration;
12. only then freeze final cable cut length and clamp coordinates;
13. WB16B freezes numeric SP13 contact numbers after physical sample inspection.

## Change log

### 2026-09-11 — WB16
- separated external lift harness from internal TILT wiring;
- prevented SP13 plug from being modeled as an appendage on the ±105 deg tilting optical shell;
- selected current LAPP 0027429, 7x0.25 mm² shielded continuous-flex cable for prototype;
- used seventh conductor as insulated NC spare only;
- changed cable connector variant from SP1310/S6I-N to SP1310/S6II-N because 6.7 mm cable exceeds the I-version 6.5 mm maximum;
- preserved SP1312/P6-C panel connector and six electrical functions;
- added 0.50 m length cap, voltage-drop screen and R55 routing rule;
- left numeric SP13 contact numbering and shield-bond configuration as physical-test HOLD items.
