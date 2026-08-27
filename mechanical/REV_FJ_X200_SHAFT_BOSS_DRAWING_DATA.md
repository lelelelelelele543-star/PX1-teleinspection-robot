# PX-1 Rev.FJ — X200 bevel shaft / bearing boss manufacturing drawing data

Status: prototype drawing candidate.

## Source basis
Uploaded CRP150 documentation shows the same functional separation that PX-1 now uses:
- `DRW-002-386`: each small bevel gear is carried on its own axle and supported by a 61801-2RS (12x21x5), rather than loading only the motor output bearing;
- `DRW-002-375`: each large bevel/output axle uses a 61800-2RS (10x19x5) and an 18x30x7 shaft seal at the crawler housing boundary.

PX-1 uses different gears/motors but deliberately retains this proven mechanical arrangement.

# A. PINION SHAFT `PX1-441`

Quantity: 2.

Material:
- 17-4PH / 1.4542 preferred;
- 42CrMo4 QT acceptable for prototype with corrosion protection.

Prototype chain:
- motor coupling seat: Ø6 class x 12 mm, exact D-flat/bore after actual JGB37 measurement;
- KHK small bevel gear seat: Ø8 h6 candidate x 14 mm;
- positive shoulder: 2 mm axial class;
- 61801 bearing journal: Ø12 k6 candidate x 5 mm;
- retained end: 6 mm axial budget with M5-class screw/circlip solution after real KHK hub is measured;
- current total modeled length: 39 mm.

Critical requirements:
- pinion gear seat and 61801 journal coaxiality <=0.02 mm;
- shoulder runout <=0.02 mm;
- bearing journal Ra <=0.8 um;
- gear-seat runout <=0.02 mm;
- no direct bevel radial/thrust load is to be carried solely by the JGB37 gearbox output bearing.

The final axial gear position is set by shim/spacer after the actual KHK mounting distance is checked.

# B. OUTPUT SHAFT `PX1-442`

Quantity: 2.

Prototype chain from bevel-gear side toward side drive:
1. KHK large bevel gear seat:
   - Ø10 h6 candidate;
   - 16 mm axial budget;
   - key/retention after exact gear hub measurement.

2. 61800 bearing journal:
   - Ø10 k6 candidate;
   - 5.0 mm length.

3. bearing/seal shoulder spacer:
   - 2 mm axial class;
   - diameter large enough for positive bearing abutment.

4. dynamic seal land:
   - Ø18 h8 candidate;
   - 7.0 mm minimum polished length;
   - Ra <=0.4 um;
   - circularity <=0.01 mm target;
   - total runout to bearing datum <=0.02 mm.

5. service coupling journal into P1/P2:
   - Ø12 h6 candidate;
   - 12 mm length;
   - D-flat or keyed coupling geometry outside the seal contact track;
   - current overall shaft model length: 42 mm.

Important: the seal land remains free of keyways, threads and circlip grooves.

# C. X200 BODY BOSS / P0 BOUNDARY

Quantity: 2 integrated bosses, one per side.

Current machined boss envelope:
- OD about Ø38 mm local reinforced material;
- axial material budget about 15 mm.

Coaxial internal features:
- inboard 61800 bearing pocket: Ø19 H7 candidate, depth 5.0 +0.05/0 mm;
- outboard FKM shaft-seal pocket: Ø30 H8 candidate, depth 7.0 +0.10/0 mm;
- through shaft clearance around Ø18.4 candidate.

Critical geometric control:
- Ø19 bearing bore and Ø30 seal bore coaxial within 0.02 mm target;
- both machined from one datum/setup where possible;
- bearing shoulder and seal shoulder perpendicular to shaft axis within 0.02 mm;
- seal entry chamfer polished/no sharp edge.

# D. DYNAMIC SEAL

Source architecture: 18x30x7.

PX-1:
- FKM preferred;
- spring-loaded rotary shaft seal or equivalent selected only after exact supplier review;
- lip faces toward external/side-drive water-risk side according to selected seal architecture;
- compatible grease applied only if seal manufacturer permits it;
- no assembly tool may drag seal lip over a keyway or sharp shoulder.

# E. BEVEL MESH SETTING

Do not dimension the KHK pair by generic pitch-cone theory on the production drawing.
Use the actual purchased KHK mounting-distance dimensions.

Provide:
- replaceable shim stack on pinion or output side;
- contact-pattern blue check;
- backlash measurement at four angular positions;
- left/right no-load motor-current comparison after assembly.

Acceptance requires:
- centered tooth contact;
- no binding over 360 degrees;
- no measurable seal heating during unloaded 30 min run;
- no abnormal bearing temperature;
- equal left/right current within an engineering tolerance established from the actual motors.

# F. TEMPORARY TORQUE LIMIT

Until real JGB37 stall/current data are measured:
- bevel-pinion mechanical input cap remains about 1.5 N*m;
- estimated post-pair torque with 2.5 ratio and 0.90 efficiency is about 3.375 N*m.

CadQuery sanity check at that limit:
- Ø8 pinion torsional shear ~14.9 MPa;
- Ø10 output section ~17.2 MPa;
- Ø12 coupling section ~9.95 MPa.

Therefore shaft strength is not the limiting factor in the current prototype; gear contact, bearings, seals and actual motor overload control dominate.

# G. DRAWING STANDARD

- general untoleranced dimensions: DIN ISO 2768-fH style baseline to match the reference documentation philosophy;
- critical fits/runout shown explicitly;
- deburr 0.2...0.5 mm unless otherwise stated;
- no coating on polished seal track unless specifically qualified;
- part/revision marking on non-functional surface only.