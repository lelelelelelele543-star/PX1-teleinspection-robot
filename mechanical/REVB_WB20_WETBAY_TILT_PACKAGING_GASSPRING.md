# PX-1 Rev.B — WB20 full-crawler correction: wet bay / TILT stack / electronics packaging / gas spring

Date: 2026-09-11  
Status: **PASS_SCREEN / MANUFACTURING HOLD**

## 1. Why WB20 exists

WB20 was opened after integrating the WB18/WB19 camera model with the complete Rev.PR crawler geometry.

An important omission was found in the previous validation chain:
- WB18 validated the camera moving/fixed parts internally and against the ideal DN150 cylinder;
- WB19 added the controller-saddle / external-harness routing problem;
- neither release screen had made the **fixed TILT yoke cheeks a mandatory collision pair against the complete Rev.PR pressure body and the side Z50 gear train**.

When those solids were combined, the previous wide yoke occupied the same upper-side region as the crawler body/gear envelope in LOW.

A second integration problem was exposed at the same time: the previous high front wet-deck/roof did not provide useful full `-105...+105 deg` TILT clearance in LOW.

Therefore it would have been incorrect to continue freezing harness coordinates around WB19. WB20 corrects the underlying crawler geometry first.

**WB19 remains historical design evidence, but its body-side harness coordinates are superseded for manufacturing by WB20.**

## 2. Architecture that is NOT changed

WB20 does not change the active PX-1 Rev.B architecture:
- three wheel stations per side;
- six wheels total;
- wheel centers X50 / X150 / X250;
- rear X250 is the traction input station;
- five Z50 module-1 side gears per side at X50 / X100 / X150 / X200 / X250;
- ten Z50 side gears total;
- one traction motor per side;
- manual camera lift;
- separate sealed camera pressure zone P3;
- fixed TILT pivots, rotating camera shell;
- continuous rotation only on internal ROLL;
- no mechanical cartridge/cassette concept;
- six-core main inspection tether architecture is unchanged.

Changing any of the above requires a separate architecture change revision.

## 3. Corrected Proteus-like front wet bay

The front wet camera bay is lowered rather than shrinking the camera or deleting TILT travel.

WB20 screen roof/wet-floor centerline profile:

| X, mm | wet floor / pressure-roof outer Z, mm |
|---:|---:|
| 0 | 22 |
| 140 | 26 |
| 200 | 77 |
| 220 | 90 |

Other screen values:
- wet-deck half width: 38 mm;
- nominal pressure-roof thickness: 5 mm;
- camera LOW axis remains approximately `X83.557 / Z75`;
- pipe reference remains ideal DN150, `R=75 mm`, axis `Z=52.048 mm`.

This is deliberately consistent with the original Proteus/Rev.PF lesson: the camera needs a genuinely low, open wet bay. The camera is not forced to clear an unnecessarily high front dry floor.

The first WB20 trial used a higher `Z25 -> Z29` front profile. It produced only about 0.72 mm camera-to-floor clearance around TILT -58 deg and was rejected. The accepted screen lowers that front profile by 3 mm.

### Body result

Executed CadQuery 2.8.0 screen:
- pressure body solid is valid;
- minimum ideal body-to-DN150 clearance from the detailed mesh: about **7.81 mm**;
- no body enlargement beyond the active DN150 master is introduced.

This is still an ideal-cylinder result. Pressure FEA/proof and a real pipe gate remain mandatory.

## 4. Narrow/recessed TILT side stack

The previous camera side stack placed too much hardware outboard.

WB20 keeps the WB17 functional architecture but moves the bearing farther into P3:

wet -> dry side, each side:
1. fixed Ø8 pivot;
2. compact external/wet retainer region;
3. 8x16x7 FKM radial shaft seal;
4. controlled spacer/shoulder;
5. 618/8 open bearing, 8x16x4, recessed into dry P3;
6. internal shoulder/retainer.

Current screen coordinates:
- bearing axial region: approximately `|Y| = 22...26 mm`;
- seal axial region: approximately `|Y| = 26...33 mm`;
- camera boss outer face: `|Y| = 34.0 mm`;
- boss-to-yoke gap: 0.5 mm;
- yoke inner face: `|Y| = 34.5 mm`;
- yoke thickness: 3.0 mm;
- yoke outer face: `|Y| = 37.5 mm`.

The side Z50 gear inner face in the active screen is at approximately:
- `|Y| = 40.125 mm`.

Therefore:
- fixed yoke to Z50 lateral screen gap: **2.625 mm**;
- moving camera hard-envelope to Z50 lateral screen gap: **6.125 mm**;
- fixed yoke to wet-deck side edge: **0.5 mm**.

The 0.5 mm deck-side value is a packaging clearance, not a released dirty-service gap. Exact cheek profile, fillets, fastener heads and manufacturing tolerances must be added before drawing release.

## 5. Full LOW TILT validation

WB20 does not use a few selected camera angles.

The detailed WB18 moving-camera mesh is sampled through:
- TILT minimum: -105 deg;
- TILT maximum: +105 deg;
- increment: 1 deg.

Executed results:
- minimum moving-camera ideal DN150 clearance: **3.0405 mm**;
- worst pipe-clearance angle: approximately **-61 deg**;
- minimum moving-camera clearance to corrected wet floor: **3.721 mm**;
- worst floor-clearance angle: approximately **-58 deg**;
- fixed-yoke ideal DN150 clearance: **10.928 mm**;
- fixed-yoke minimum floor clearance: **21.607 mm**;
- moving-to-Z50 lateral screen gap: **6.125 mm**;
- fixed-yoke-to-Z50 lateral screen gap: **2.625 mm**.

Interpretation:
- the previous body/yoke collision is removed at screen level;
- full nominal LOW TILT geometry is restored without changing the Ø52 optical-shell target;
- the ~3.04 mm ideal pipe margin is too small to call production-safe in an oval, dirty or damaged real DN150 pipe.

Therefore physical DN150 qualification remains a hard release gate.

## 6. Electronics repack after lowering the camera bay

Lowering the camera bay removes some of the old generic front electronics reserve. WB20 does **not** respond by enlarging the crawler.

Instead the already selected real components are repacked into the remaining dry volume.

Current validation envelopes:

### Main HV -> 24 V converter
- manufacturer: Cincon;
- article: `CQB150W-110S24`;
- actual body: approximately 57.9 x 36.8 x 12.7 mm;
- WB20 converter + thermal-carrier reserve: 65 x 45 x 16 mm;
- screen location: approximately X260 / Y0 / Z70.

### Input bulk capacitor
- manufacturer: Nichicon;
- article: `UCS2D221MHD1TN`;
- 220 uF / 200 V;
- approximately Ø18 x 25 mm;
- installed horizontally in the screen around X205 / Y+24 / Z30.

### Video balun
- Delta-Opti `TR-1D*P2`;
- body approximately 43 x 16 x 15 mm;
- screen location around X205 / Y-22 / Z42.

### Main controller
- STM32 NUCLEO-F446RE;
- low-profile reserve 82.5 x 70 x 12 mm;
- retained in the upper controller saddle around X262.25 / Y0 / Z98.

### Other reserves
- two traction-driver reserves remain inside P0;
- input-protection reserve remains inside P0;
- pressure-sensor reserve remains inside P0.

Executed result:
- every tested component outside the dry union: **0.0 mm3**;
- pairwise tested component intersections: **none**.

The electrical architecture is therefore not changed merely to create camera clearance.

## 7. ROLL consequence of the recessed TILT bearing

Moving the 618/8 bearing inboard consumes some P3 axial packaging space.

The current ROLL package can still be retained, but the ROLL N20 motor/pinion position may need to move approximately a few millimeters toward the camera front.

Release gate:
- exact purchased N20 body/shaft dimensions;
- useful output-shaft length with bearing/gear/pinion stack installed;
- pinion retention and service access.

Do not freeze a generic N20 shaft dimension from marketplace photographs.

## 8. Gas spring correction

The older Rev.FM candidate body anchor near `X220 / Z35` is superseded. In the integrated crawler it passes through/inside the pressure-body volume and cannot be propagated to production CAD.

WB20 retains the successful Proteus principle:
- manual lift;
- M8 mechanical friction clamp carries static holding;
- gas spring is only an assist/counterbalance;
- approximately 150 N starting force class.

### Current purchasable prototype article

Manufacturer: ACE Controls  
Family/article: `GS-12-20-V4A`  
Type: stainless push-type industrial gas spring.

Manufacturer geometry used for the screen:
- body OD: 12 mm;
- rod OD: 4 mm;
- stroke: 20 mm;
- extended L: 72 mm class;
- adjustable/available force class up to about 180 N;
- PX-1 first prototype target: **150 N**.

Manufacturer page:
`https://www.ace-ace.com/com/products/motion-control/industrial-gas-springs-push-type/gs-8-v4a-to-gs-40-va/gs-12-v4a/gs-12-20-v4a.html`

### WB20 screen pins

Body-side fixed pin:
- `X = 194.0 mm`;
- `Z = 82.9 mm`.

Moving pin:
- 63.0 mm from the lower body lift pivot along the lower lift link.

Lateral screen position:
- center Y = 16 mm, inboard of the side lift arm.

### Calculated positions at 150 N

LOW:
- eye/pin center distance ≈ **55.472 mm**;
- assisting torque ≈ **1.257 N.m**;
- moving pin ≈ X138.867 / Z76.775;
- OD12 envelope floor gap ≈ **5.0 mm**.

MID:
- length ≈ **59.985 mm**;
- assisting torque ≈ **1.604 N.m**;
- moving pin ≈ X138.497 / Z105.650;
- floor gap ≈ **5.0 mm**.

HIGH:
- length ≈ **68.151 mm**;
- assisting torque ≈ **1.382 N.m**;
- moving pin ≈ X165.980 / Z145.025;
- floor gap ≈ **5.0 mm**.

Using the nominal 72 mm extended / 20 mm stroke geometry only as the first article screen:
- nominal retracted length = 52 mm;
- minimum used length = 55.472 mm;
- maximum used length = 68.151 mm;
- used geometric span ≈ 12.680 mm;
- compression-end margin ≈ **3.472 mm**;
- extension-end margin ≈ **3.849 mm**.

The gas spring is **not** a lift lock. The M8 clamp must still hold LOW/MID/HIGH with the gas spring disconnected or depressurized.

Exact end fittings change pin-to-pin geometry. Therefore the purchased ACE spring plus selected rod/body end fittings must be measured before the two pin coordinates become machining dimensions.

## 9. WB19 harness consequence

The external-head harness is deliberately not frozen in WB20.

Reason:
- wet-floor/body geometry changed;
- fixed yoke width changed;
- the correct location of the body-side strain relief/guide changes with those solids;
- WB19 proved the old harness assumptions were wrong but its candidate path was still built around the pre-WB20 body/yoke package.

Rules retained:
- LAPP `0027429 UNITRONIC FD CY 7X0.25` remains the current prototype baseline unless a later work block proves a better stocked article;
- nominal OD remains 6.7 mm;
- design dynamic bend radius remains R55 until formally superseded;
- the external head connector remains serviceable;
- no torsional accumulation is allowed in the harness;
- the shield is not a current-return conductor.

`SP1324` 90-degree WEIPU SP13 remains a candidate only. The exact six-contact overmolded procurement article is not yet frozen.

## 10. Manufacturing / release holds

WB20 is **not machining release**.

Hard holds:
1. physical DN150 tube sweep including real pipe ovality, joint steps, deposits and debris;
2. pressure FEA and hydro/pneumatic proof of the lowered front roof and transition region;
3. actual machined yoke, retainer and fastener geometry;
4. measured 618/8 bearing and 8x16x7 seal samples, final fits and seal lands;
5. exact N20 ROLL motor shaft/body sample and pinion retention;
6. purchased ACE GS-12-20-V4A plus exact end fitting stack measured pin-to-pin;
7. gas-spring brackets, pivots, corrosion and 500-cycle lift test;
8. M8 clamp wet creep test with gas spring disconnected;
9. constant-length camera harness re-solved on WB20 geometry;
10. physical camera P3 +0.25 bar pressure/submersion test;
11. CVBS/UART/lighting qualification through the actual camera harness;
12. all outstanding WB18 physical component measurements.

The exact CRP150 lift dimensions also remain under the older Rev.PF source/physical measurement gate. WB20 dimensions are PX-1 design datums, not claimed original MiniCam dimensions.

## 11. Next controlled work block — WB21

WB21 shall solve the **constant-length external camera harness on the corrected WB20 geometry**.

It must evaluate:
- actual moving connector exit LOW/MID/HIGH;
- routing relative to one lift arm / both lift pivots;
- one constant physical cut length;
- controlled slack storage without entering wheel/Z50/body/TILT envelopes;
- R55 for LAPP 0027429 unless cable article is formally changed;
- body-side jacket clamp / sealed feedthrough position;
- straight SP1310 versus 90-degree SP1324 only with procurement evidence;
- wet-cycle abrasion/service access;
- DN150 LOW sweep including the actual cable diameter and clamps.

No drivetrain, main-tether or camera-pressure architecture change is authorized to solve WB21.

## 12. Change log

### 2026-09-11 — WB20
- discovered and recorded the missing fixed-yoke vs complete crawler body/Z50 integration check in WB18/WB19;
- rejected the first `Z25 -> Z29` wet-floor trial because TILT-to-floor margin fell below 1 mm;
- lowered front wet bay to `Z22 -> Z26` before the rear rise;
- recessed 618/8 bearings into P3 and reduced yoke outboard width;
- restored full screen TILT -105...+105 deg at 1-degree resolution;
- retained the six-wheel / ten-Z50 / X250-drive hard lock;
- repacked the real Cincon, Nichicon, Delta and NUCLEO envelopes without enlarging the body;
- superseded the old gas-spring body anchor;
- selected ACE GS-12-20-V4A as the current real prototype spring family and found a compatible 150 N geometry screen;
- explicitly superseded WB19 harness machining coordinates pending WB21;
- kept status at PASS_SCREEN / MANUFACTURING HOLD.
