# PX-1 Rev.B — WB04 motor coupling / supported pinion interface

Date: 2026-09-11
Status: PACKAGING PASS / DRAWING HOLD

## 1. Purpose

Close the missing mechanical chain between the selected Ø32 traction motor and the supported Z16 bevel-pinion shaft without changing the proven CRP-150 drivetrain topology.

The active Rev.PR master contained only a motor envelope and screening bevel solids. It did **not** explicitly model:
- the motor output shaft;
- a serviceable coupling;
- the exact 61801 support bearing location;
- coupling insertion length;
- motor mounting face;
- rear service clearance.

Therefore the earlier Rev.PR packaging PASS must not be treated as a manufacturing proof for the motor input assembly.

## 2. CRP-150 architecture comparison

Source `DRW-002-386` confirms per crawler:
- two motors total;
- two small bevel gears GEA-002-531 Z16;
- two FSS-002-083 bevel-pinion shafts/coupling elements;
- two 61801-2RS bearings 12x21x5;
- one common motor holder.

The important architecture rule remains:
**the Z16 bevel load is supported by a dedicated 61801 in the holder; the bevel gear is not simply hung cantilevered from the motor gearbox output shaft.**

PX-1 keeps this rule.

## 3. Leading motor interface

Part:
- manufacturer: ISL Products International;
- part: `PGM-32P-24-100-60-02 / MOT-IG32PGM 100`;
- quantity: 2 crawler + 1 spare preferred;
- source: ISL / DigiKey Marketplace;
- nominal voltage: 24 V;
- motor/gearbox OD: 32 mm;
- published total `shaft and bearing` length: 92 mm;
- output shaft: Ø6 mm;
- mounting-hole spacing: 26 mm;
- rated speed: 49 rpm;
- rated torque: 1.765 N.m.

The IG-32PGM family manufacturer drawing shows a 12 mm output-shaft projection and four M3 x 5.5-deep holes on Ø26 PCD. These dimensions are accepted for **packaging screening only** until the exact purchased ISL article is physically measured.

Do not cut the final motor holder from the family drawing alone.

## 4. Coupling selection

### Baseline — NBK MLR-20C-6-6

Part:
- manufacturer: NBK / Nabeya Bi-tech Kaisha;
- part number: `MLR-20C-6-6`;
- type: rigid one-piece clamping coupling;
- bore: 6 mm / 6 mm;
- outside diameter A: 20 mm;
- overall width W: 24 mm;
- rated torque: 2.5 N.m;
- mass: 18 g;
- clamp screw: M2;
- clamp-screw tightening torque: 0.5 N.m;
- recommended mating-shaft tolerance: h6 or h7.

Why this is selected for the source-like prototype:
- its 2.5 N.m rated torque exceeds the Rev.B short bevel-input gate of 2.0 N.m;
- it is zero-backlash and compact;
- it preserves the CRP-150 principle in which the dedicated 61801 and the motor/gearhead bearing together support the aligned input train;
- it does not require a second pinion bearing or a larger gearbox compartment.

The motor D-flat/clamp orientation must follow NBK mounting guidance and a physical slip test is mandatory before load release.

### Fallback — NBK MOM-20C-6-6

If the actual motor sample cannot be repeatably centered well enough for a rigid coupling, the approved fallback study is:
- Oldham clamp coupling `MOM-20C-6-6`;
- Ø20 x 28 mm envelope;
- rated torque 7.7 N.m;
- max torque 15.4 N.m;
- published slip torque for 6 mm bore: 6 N.m;
- lateral misalignment capability up to 0.4 mm;
- angular misalignment up to 2 degrees.

However this flexible coupling must **not** simply replace the rigid coupling with the existing single 61801. It removes the useful radial support contribution of the motor shaft. If MOM-20C is selected, PX-1 must add a second pinion-shaft bearing and rerun the holder/length calculations.

Therefore MOM-20C is a controlled fallback, not the current baseline.

## 5. Pinion support bearing

Prototype premium bearing selected for purchase/measurement:
- manufacturer: FAG;
- part: `61801-2RSR-HLC` / 61801-2RSR family;
- dimensions: 12 x 21 x 5 mm;
- quantity for motor-input stage: 2 + spares;
- Czech distributor examples: RS / ProPrumysl;
- dynamic rating class: approximately 1.9 kN;
- normal internal clearance / double contact seal.

A JTEKT/Koyo 6801-2RS 12x21x5 is a fully dimensional alternative and publishes Cr 2.40 kN, C0r 1.05 kN.

Rev.B bearing screen uses conservative C = 1.74 kN. Even with a 1.5 reaction multiplier, the 2.0 N.m pinion-load screen remains far below the bearing static/dynamic capacity. Exact L10 is not a release proof until final pinion overhang and motor support reaction are known.

## 6. Pinion shaft — PX1-441 candidate

Project part: `PX1-441-Z16-INPUT-SHAFT`
Quantity: 2.

Material candidate:
- preferred 1.4542 / 17-4PH stainless;
- alternate 42CrMo4 QT with corrosion protection compatible with grease and bearing fits.

Current rear half of the shaft can be frozen only as an interface candidate:
- coupling stub: Ø6 h6;
- coupling engagement target: >=7 mm in the WB04 screen, never below NBK minimum installation requirement;
- 61801 bearing journal: Ø12 k6 candidate, 5.0 mm long;
- bearing retaining groove: DIN 471-compatible 12 mm external-circlip geometry;
- no thread or cross hole through the bearing journal;
- transition fillets to follow bearing chamfer limit and stress calculation.

The Z16 front seat/bore/key is **HOLD** until the hardened matched bevel supplier controls hub/bore geometry and mounting distance.

Nominal Ø6 stub torsional shear screen:
- 0.60 N.m -> ~14.1 MPa;
- 0.80 N.m -> ~18.9 MPa;
- 1.00 N.m -> ~23.6 MPa;
- 2.00 N.m -> ~47.2 MPa;
- motor-gearbox published ~3.923 N.m mechanical limit -> ~92.5 MPa.

These nominal values are acceptable for the proposed steel classes but final shoulder/groove stress concentration still requires drawing review.

### Retaining ring candidate

Commercial item:
- DIN 471 external circlip;
- shaft size 12 mm;
- ring thickness 1.0 mm;
- stainless candidate;
- example Czech source: Killich item `293009012`, 12x1.0, stainless, DIN 471.

This circlip is a **PX-1 adaptation** for positive inner-ring retention. The CRP-150 motor-unit assembly sheet does not explicitly list it, so it must not be presented as copied MiniCam hardware.

## 7. Holder alignment rule

Project part: `PX1-440-TWIN-MOTOR-HOLDER`
Material candidate: EN AW-6082 T6.

The holder remains an ordinary removable bracket/holder, not a cartridge/cassette module.

Rigid-coupling release requires:
- motor centering register and 61801 bearing bore machined from one datum setup;
- bearing bore candidate Ø21 H7;
- bearing-axis to motor-axis concentricity target <=0.02 mm before sample validation;
- motor mounting-face perpendicularity target <=0.03 mm over 25 mm;
- screws provide clamp only; the motor must be located by a real register/pilot or a validated repeatable fixture, not by M3 clearance alone;
- four M3 motor screws per motor remain provisional until the exact purchased motor front face is measured.

If the purchased motor has no repeatable precision register, do **not** force the rigid coupling. Promote the two-bearing + Oldham fallback instead.

## 8. Rear-body packaging correction

The active Rev.PR rear extension used approximately:
- outer width 80 mm;
- internal width 72 mm;
- rear end X ~358 mm.

With two real Ø32 motors that leaves only about 2 mm side clearance and does not explicitly reserve the coupling/holder chain. That is not sufficient for manufacturing/service release.

WB04 candidate envelope therefore changes only the rear extension:
- X = 242...384 mm;
- outer width = 92 mm, matching the main-body width class;
- outer Z = 19...71 mm;
- dry cavity X = 246...378 mm;
- dry cavity width = 80 mm;
- dry cavity Z = 24...66 mm.

This is a justified Rev.B geometry correction, **not a drivetrain architecture change**.

Calculated hard clearances in the WB04 screen:
- between the two Ø32 motor bodies: 4.0 mm;
- motor to cavity side wall: 6.0 mm;
- motor to top/bottom cavity wall: 5.0 mm;
- motor rear to cavity end: 5.0 mm;
- candidate rear hard envelope to ideal DN150: minimum ~18.36 mm;
- all modeled motor/coupling/bearing/holder envelopes remain inside the dry cavity and ideal DN150 cylinder;
- unintended solid collisions: zero.

The extra axial length is approximately 26 mm relative to the old Rev.PR rear-end screen. Axial length does not create a DN150 radial conflict, but elbow/bend negotiability and tail geometry remain separate system gates.

## 9. Pressure / sealing consequence

Widening the rear dry extension cannot be treated as free packaging volume.

Rules:
- P0 remains one sealed dry positive-pressure volume;
- no motor-holder fastener may create a through-hole to the wet exterior;
- rear wall / service cover requires a normal static O-ring and positive register;
- tether strain must terminate mechanically at the tail and must not load the rear pressure-cover seal;
- the enlarged rear extension must be included in pressure FEA/proof testing;
- exact rear-cover O-ring and tail connector are deferred to the next pressure/tail work block rather than invented in WB04.

At normal +0.30 bar gauge, the pressure load on a rear internal projected area near 80 x 42 mm is only about 101 N, but local cover bending, connector holes, screw spacing and proof pressure still control the actual design.

## 10. Thermal/service consequence

Two rated 9 W-class gearmotors are inside P0. Motor outer cases must not be left floating thermally in air.

The final holder must provide:
- metal contact path from each gearbox/motor mount into the 6082 holder and pressure body;
- service removal without disturbing wheel-shaft seals;
- direct tool access to coupling clamps;
- visible witness marks on coupling/shaft after torque setting;
- wire routing clear of the 4 mm inter-motor gap;
- no wire trapped between motor body and pressure wall.

A sealed-body thermal soak at commanded traction current is mandatory before Rev.C.

## 11. Executable CAD screen

Script:
`mechanical/cadquery/PX1_MotorInput_RevB.py`

Validation:
`mechanical/REV_B_WB04_VALIDATION.json`

Current result: `PASS_SCREEN`.

This PASS means only:
- commercial motor/coupling/bearing envelopes can coexist;
- proposed rear extension fits ideal DN150;
- required service clearances exist at screening level.

It does **not** release the motor holder or pinion shaft for machining.

## 12. WB04 closure gates

WB04 becomes drawing-ready only after:
1. physically obtain and measure at least two ISL motors;
2. measure shaft OD, flat, runout, shaft projection, face register and actual M3 pattern;
3. obtain/buy the NBK coupling or a documented equivalent and run a clamp-slip test on the real motor shaft;
4. receive final hardened Z16/Z40 matched-pair drawing and mounting distance;
5. freeze the pinion front interface;
6. choose rigid one-bearing source-like route or two-bearing flexible fallback based on measured alignment repeatability;
7. finish the structural holder, outer-bearing retention and tool access in CAD;
8. rerun the complete master including rear cover/tail and LOW/MID/HIGH lift.

## Change log

### 2026-09-11 — WB04
- identified that Rev.PR did not include the real motor coupling chain;
- selected NBK MLR-20C-6-6 as the source-like rigid-coupling candidate;
- defined MOM-20C-6-6 only as a controlled two-bearing fallback;
- selected a real purchasable FAG 61801-2RSR-class pinion bearing;
- added a commercial DIN 471 12x1 retaining-ring candidate;
- screened a real Ø32 x 92 mm motor package;
- enlarged only the rear pressure-extension candidate to obtain manufacturing/service clearance;
- obtained PASS_SCREEN with zero modeled hard collisions and >18 mm ideal-DN150 rear-envelope margin;
- kept final motor register, final pinion interface, rear seal and holder machining on HOLD pending physical parts and supplier drawings.
