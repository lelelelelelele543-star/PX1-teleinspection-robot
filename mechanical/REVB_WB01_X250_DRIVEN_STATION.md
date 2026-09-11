# PX-1 Rev.B Work Block 01 — X250 driven rear wheel station

Date: 2026-09-11
Status: ACTIVE REVB CANDIDATE / NOT MACHINING RELEASE

## 1. Purpose

Close the highest-risk mechanical gap in Rev.A: the rear X250 station must simultaneously be:
- the rear wheel station;
- the side-drive Z50 input;
- the torque handoff from the Z40 bevel output;
- a sealed boundary between the central dry pressure volume and the side-drive dry bay;
- serviceable without converting the design into a cartridge/cassette module.

This work block does not change the frozen six-wheel CRP-150-derived topology.

## 2. Source facts rechecked from the Library

### DRW-002-374 — one CRP-150 side-drive assembly
Explicit parts-list evidence:
- 1 side cover FAL-002-062;
- 2 idler gears GEA-002-528, Z50 B4;
- 3 axle gears GEA-002-529, Z50 B4;
- 1 long axle FSS-002-064;
- 2 short axles FSS-002-063;
- 6 bearings 61801-2RS, 12x21x5;
- 3 bearings 61903-2RS, 17x30x7;
- 3 axle flanges FSS-002-061;
- 3 X-rings 18.72x2.62;
- 3 static O-rings 32x1.5;
- 1 side-cover O-ring 190x1.5;
- 1 short key 4x4x7;
- 3 keys 4x4x12.

Important correction: source quantity is SIX 61801 bearings per side-drive assembly. Older repository wording that reduced this to one side-drive 61801 was wrong and has been corrected in the reference register documents.

### DRW-002-375 — central housing / large bevel path
Explicit evidence:
- 2 x Z40 large bevel gears;
- 2 x FSS-002-066 bevel-output axles;
- 2 x 61800-2RS bearings, 10x19x5;
- 2 x dynamic shaft seals 18x30x7.

### DRW-002-386 — motor / pinion path
Explicit evidence:
- 2 x Z16 bevel pinions;
- 2 x FSS-002-083 pinion shafts;
- 2 x 61801-2RS bearings, one supported pinion bearing per motor;
- 2 x motor/gear units.

### ASS-002-103 — wheel retention
Explicit evidence:
- wheel disk FSS-002-065;
- M6x14 A2 button screw;
- M6 spring washer;
- 10x1.8 O-ring.

## 3. Source versus PX-1 adaptation

Do not mix the two columns.

| Function | CRP-150 source evidence | PX-1 Rev.B direction |
|---|---|---|
| Rear side-drive input | long axle FSS-002-064 | rear X250 long axle |
| Side gears | Z50 B4, five per side | m1, Z50, 20 deg, five per side |
| Large bevel | Z40 | Z40, exact commercial/machined geometry still HOLD |
| Pinion | Z16 | Z16, supported separately from motor output bearing |
| P0-to-side seal | 18x30x7 shaft seal on bevel-output path | retain 18 mm-class polished dynamic seal land |
| Wheel dynamic seal | X-ring 18.72x2.62 | retain X-ring architecture, FKM preferred |
| Outer wheel bearing | 61903-2RS | retain 61903-2RS class |
| Compact inboard wheel support | source has six 61801 per side | PX-1 may use a thinner bearing where packaging requires it, but substitution must be explicit |

## 4. Conflict found in older PX-1 drawing candidates

Two old files cannot both define the current station:

- `REV_FG_WHEEL_SHAFT_DRAWING_DATA.md` uses two 61801 bearings per station and an 18 mm wheel seat;
- later `REV_GF_DETAILED_WHEEL_STATION.md` changes the inboard support to 6701-2RS and uses a much shorter compact axial stack.

Therefore Rev.FG remains useful for material, finish, datum and inspection philosophy, but its axial dimensions are **not** the active Rev.B rear-station chain.

A second conflict exists in `REV_FH_AXLE_FLANGE_SIDE_COVER_DRAWING_DATA.md`: its approximately 12 mm flange envelope was created before the later compact station placed both a 61801 and a 61903 plus the X-ring function in/around the removable flange. The Rev.B flange must be redrawn; the old 12 mm total envelope is not a release dimension.

## 5. Packaging problem at X250

The active Rev.PR master has approximately 12 mm of dry side-bay depth between the central dry-volume boundary and the side-cover inner plane.

A conventional serial stack of:
- keyed bevel-output coupling;
- inboard bearing;
- Z50 gear;

cannot fit into 12 mm with useful assembly clearances if every element receives its own axial segment.

Therefore Rev.B requires an **overlapped coupling/bearing geometry** rather than simply making the crawler wider.

## 6. Preferred Rev.B X250 coupling candidate

### 6.1 Functional layout

From P0 outward toward one side:

1. Z40 bevel-output shaft in P0;
2. 61800-2RS support on the Z40 path;
3. dedicated polished Ø18-class running land through an 18x30x7 shaft seal;
4. shaft steps down to a keyed male stub after the seal;
5. the male stub enters a blind female bore in the rear long axle;
6. the rear long axle has an enlarged inboard hub that is supported **around the coupling overlap** by a thin-section bearing;
7. the shaft steps down to the Z50 gear seat immediately after that bearing;
8. the usual outboard wheel-bearing / X-ring / wheel stack follows.

The important packaging trick is that the coupling engagement and the inboard support occupy the same axial region.

### 6.2 Thin bearing candidate

Candidate: **6704-2RS / 61704-2RS, 20x27x4 mm**.

Why this size:
- 20 mm bore allows a robust Ø20 inboard hub around a smaller keyed internal coupling bore;
- 27 mm OD remains well inside the radial envelope of a Z50 m1 gear;
- 4 mm width preserves the compact side bay;
- current market check confirms this is a real, purchasable standard bearing size, including EZO/JTEKT/generic supply.

Published examples give dynamic capacity approximately 1.0-1.3 kN and static capacity around 0.7 kN class. Exact purchased brand and internal clearance remain a procurement gate.

This bearing is proposed **only for the rear X250 coupling hub**. Front and centre stations may keep the later Rev.GF 6701 approach.

### 6.3 Preliminary local axial screen

Use local coordinate `Y=0` at the outer face of the P0 seal carrier and `Y=12.0 mm` at the current side-cover inner plane.

Candidate:
- female long-axle hub: Y=0.0...7.5 mm, OD Ø20;
- male output-stub engagement: about 6.8-7.0 mm;
- 6704-2RS around the outer part of the hub: approximately Y=3.5...7.5 mm;
- axial clearance: ~0.10-0.15 mm;
- custom Z50 B4 gear tooth face: approximately Y=7.65...11.65 mm;
- remaining nominal clearance to cover inner plane: ~0.35 mm.

This is a packaging screen, not a tolerance stack release.

## 7. Coupling geometry candidate

To keep the female hub wall robust, use a smaller keyed internal coupling than the source-scale 4x4 key unless the final CAD proves enough wall thickness.

Prototype screen:
- bevel-output male stub: Ø10 class;
- long-axle blind bore: Ø10 sliding fit candidate;
- key: 3x3, useful engagement approximately 7 mm;
- long-axle coupling hub OD: Ø20;
- bearing journal on hub: Ø20 for 6704-2RS;
- positive axial location supplied by the complete bearing/flange stack, not by key friction.

The Ø10 class is mechanically coherent with the source 61800-2RS bearing bore on the Z40 output path. It is a PX-1 adaptation, not a claimed MiniCam dimension.

### 4 N.m screening loads

For a 3x3x7 mm key at d=10 mm and T=4 N.m:
- key shear stress ≈ 38.1 MPa;
- key bearing stress ≈ 76.2 MPa.

For a Ø12 solid shaft at 4 N.m:
- maximum torsional shear ≈ 11.8 MPa.

These values are modest for a hardened/stainless steel prototype but do not replace fatigue, keyway stress-concentration or first-article testing.

## 8. Z50 gear decision for packaging

Do **not** assume that `B4` proves the complete source gear hub is only 4 mm long. `B4` confirms the tooth-face width; the source also lists 4x4x12 keys, so source hub geometry is not fully known from the available parts list.

PX-1 therefore uses its own gear geometry:
- m = 1.0;
- z = 50;
- pressure angle = 20 deg;
- tooth face = 4.0 mm nominal;
- compact hubless or minimal-hub prototype form at X250;
- Ø12-class seat on the long axle;
- positive key drive;
- gear axial retention by shoulders/spacers/cover-side hardware, not by adhesive alone.

At the current 4 N.m screen, even a short 4x4x4 mm steel key on a Ø12 seat gives approximately:
- shear ≈ 41.7 MPa;
- bearing ≈ 83.3 MPa.

Therefore a compact PX-1 gear key is mechanically plausible; exact key length is frozen only with the finished gear hub and shaft drawing.

## 9. Outboard flange stack — redraw required

The Rev.B removable rear axle flange must package, in functional order:
- 61801-2RS class intermediate support, 12x21x5;
- axial shoulder/gap;
- 61903-2RS wheel-load bearing, 17x30x7;
- axial shoulder/gap;
- stationary X-ring gland acting on the dedicated Ø19-class polished wheel-seal land;
- static 32x1.5 axle-flange O-ring;
- four-screw clamp pattern with a positive pilot/register.

Minimum pure functional axial sum before end walls is already roughly:
`5 + 0.2 + 7 + 0.2 + 3.4 = 15.8 mm`.

Therefore the old 12 mm total flange envelope is not credible for the later three-support wheel station. Rev.B target part envelope is expected to be roughly 17-18 mm class, with part of the first bearing region overlapping the side-cover thickness so the full amount does not become external projection.

Exact flange envelope remains a CAD/DN150 gate.

## 10. P0 shaft-seal rule

The 18x30x7 seal and the wheel X-ring perform different jobs and both remain:
- 18x30x7 keeps P0 isolated from a side-drive bay around the bevel-output path;
- 18.72x2.62 X-ring keeps water/sludge out at the external wheel-shaft path.

Positive internal pressure does not replace either seal.

Seal-running surfaces:
- hardened/corrosion-resistant steel;
- no keyway, circlip groove, thread or shoulder edge under the contact band;
- polished finish target remains Ra <=0.4 um until checked against the exact selected seal manufacturer.

## 11. Traction numbers with the current motor gate

For the active motor target of 45-65 rpm geared output and the 2.5:1 bevel reduction:
- wheel speed ≈ 18-26 rpm;
- with a 90 mm wheel, theoretical crawler speed ≈ 0.085-0.123 m/s before slip.

At motor rated torque:
- 1.0 N.m motor -> 2.5 N.m ideal side-input torque;
- 1.3 N.m motor -> 3.25 N.m ideal side-input torque.

At 45 mm wheel radius this corresponds to about 56-72 N ideal tractive force per side before losses. The existing 4 N.m shaft/key screening envelope therefore retains useful torque margin.

## 12. What is frozen by this work block

Frozen for Rev.B CAD development:
- X250 is the rear driven wheel/input station;
- P0 Z40 path remains separately sealed with an 18x30x7-class shaft seal;
- side-drive wheel path retains separate external X-ring sealing;
- rear long axle remains a serviceable separate part from the motor/pinion unit;
- coupling and inboard support must overlap axially rather than widening the whole crawler;
- 6704-2RS 20x27x4 is the preferred rear coupling-hub support candidate pending exact purchased-brand freeze;
- the old Rev.FG shaft length chain and old Rev.FH 12 mm flange envelope are not manufacturing-release data for X250.

## 13. HOLD before Rev.B promotion

1. Model the complete X250 shaft, Ø20 coupling hub, 6704 bearing, custom Z50 B4 gear, 61801, 61903, X-ring gland and wheel as solids.
2. Add the actual 18x30x7 P0 shaft seal and Z40-output shaft.
3. Verify male/female coupling assembly path and tool access.
4. Verify no coupling bottoming: retain controlled axial clearance.
5. Verify bearing shoulders and circlip/retention can actually be machined and assembled.
6. Rebuild the axle flange to the required 17-18 mm class functional stack.
7. Rerun full DN150 solid clearance with the tapered wheel, complete flange and all screw heads.
8. Freeze real bearing brands and fits after procurement.
9. Build **one X250 side-drive first article** and test torque, radial load, seal drag, pressure decay and submerged rotation before duplicating the opposite side.

## Change log

### 2026-09-11
- started Rev.B Work Block 01;
- reconciled source bearing quantities;
- identified Rev.FG/Rev.GF and Rev.FH/Rev.GF axial conflicts;
- introduced compact overlapping coupling/bearing concept for X250;
- selected 6704-2RS size as the preferred purchasable rear coupling-hub support candidate;
- retained all source-derived sealing layers and rear-input topology.
