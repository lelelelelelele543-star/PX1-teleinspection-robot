# PX-1 Rev.B — WB22A lift/camera integration correction

Date: 2026-09-13  
Status: **PASS_SCREEN / MANUFACTURING HOLD / PROCUREMENT HOLD**

## 1. Why WB22A exists

WB22A is a corrective work block inserted before the previously planned static head-harness work.

Two integration faults were found while auditing WB20/WB21 against the controlled CRP-150 drawings and the user's 2025-03-14 Proteus service photographs:

1. one WB20 audit model extruded the wet-bay cut in the wrong `Y` direction; the intended `-38...+38 mm` open wet channel was therefore not represented by that audit solid;
2. WB21 placed the four-bar end pivots effectively on the camera TILT axis. Exact solid intersection checks then showed the lift plates occupying the same volume as the moving camera package.

The service photographs show the useful source topology more clearly: the lift linkage terminates in a separate rigid head-support structure and the camera is mounted ahead of that structure. The photographs are used only as topology/packaging evidence; no dimension has been scaled from a photograph.

WB22A therefore changes the active sequence to:

`pressure body -> four-bar lift -> fixed head carrier -> sealed TILT camera`.

This correction supersedes the WB20/WB21 lift geometry wherever they conflict. It does **not** change the hard crawler architecture.

## 2. Architecture retained

Unchanged Rev.B locks:

- 3 wheel stations per side / 6 wheels total;
- wheel stations `X50 / X150 / X250`;
- 100 mm station pitch / 200 mm front-to-rear wheelbase;
- five module-1 Z50 gears per side / ten total;
- two traction motors total;
- rear `X250` input on each side;
- dry pressurised body;
- manual camera lift;
- sealed Ø52 camera package;
- no mechanical cartridges/cassettes.

## 3. Corrected wet bay

The WB20 profile is retained:

- floor/pressure-roof outer profile points: `(X0,Z22)`, `(140,26)`, `(200,77)`, `(220,90)`;
- wet-bay half width: `38 mm`;
- nominal pressure-roof thickness: `5 mm`.

CadQuery `XZ` positive extrusion runs toward `-Y`. WB22A therefore starts the wet cut at `Y=+38 mm` and extrudes 76 mm. An explicit assertion now requires:

- wet cut `Ymin = -38.000 mm`;
- wet cut `Ymax = +38.000 mm`.

This prevents the previous sign error from silently returning.

## 4. Corrected lift geometry

Controlled WB22A values:

- body pivot X: **200.0 mm**;
- lower body pivot Z: **92.0 mm**;
- upper body pivot Z: **109.0 mm**;
- pivot separation: **17.0 mm**;
- link length: **90.0 mm**;
- arm centre planes: **Y = ±31.0 mm**;
- arm plate section: **4.0 x 14.0 mm**;
- vertical edge gap between lower/upper plates at the pivots: **3.0 mm**.

The arm section is an engineering screen, not a released material/thickness decision. Final material, fatigue, buckling and abuse-load checks remain on HOLD.

### Why the WB21 120 mm links were not retained

With WB21's end pivot at the TILT axis, the four plates physically intersect the camera. Merely moving the plates sideways forced them into the yoke/Z50 corridor and left poor dirty-service margins.

WB22A instead uses a shorter 90 mm parallelogram and places a rigid carrier between the lift and camera. This preserves the LOW optical-axis position without moving the Z50 side gear planes.

## 5. Fixed head carrier

The carrier is rigid with the four-bar and does not TILT with the camera.

Derived carrier offset from the lift end pivot to camera axis:

- **30.7474 mm forward in X**.

This value is derived so the WB20 LOW camera axis remains exactly:

- `X = 83.5569 mm`;
- `Z = 75.0000 mm`.

Carrier screen:

- side cheek inner face: `|Y| = 35.0 mm`;
- side cheek outer face: `|Y| = 37.5 mm`;
- side cheek thickness: `2.5 mm`;
- pivot pin diameter screen: `8 mm`;
- rear/upper cross tie relative to camera axis: `+48 mm X / +30 mm Z`;
- cross-tie envelope: `8 x 75 x 5 mm`.

The carrier side structure remains outside the moving head. The cross tie is positioned outside the complete radial envelope of the TILT package.

Calculated cross-tie margin to the full moving radial envelope:

- **5.0147 mm**.

## 6. LOW/MID/HIGH kinematics

### LOW

- lift angle: `-17.7916 deg`;
- camera axis: `X83.5569 / Z75.0000 mm`;
- lift-end pivots: `X114.3043 / Z64.5` and `X114.3043 / Z81.5 mm`.

### MID

- lift angle: `+17.7916 deg`;
- camera axis: `X83.5569 / Z130.0000 mm`;
- lift-end pivots: `X114.3043 / Z119.5` and `X114.3043 / Z136.5 mm`.

### HIGH

- lift angle: `+66.4435 deg`;
- camera axis: `X133.2838 / Z185.0000 mm`;
- lift-end pivots: `X164.0313 / Z174.5` and `X164.0313 / Z191.5 mm`.

HIGH is a large-pipe/service position and is not a DN150 operating position.

## 7. Executed solid collision checks

CadQuery 2.8.0 was executed against:

- corrected body/wet-bay solid;
- all four lift arms;
- fixed carrier;
- all ten Z50 solids;
- Ø52 x 78 mm moving camera package;
- TILT package from `-105...+105 deg` in 1-degree steps for pipe/floor sweep;
- one 150 N gas spring envelope.

For LOW, MID and HIGH:

- lift arms vs body: **0 mm3**;
- lift arms vs all Z50: **0 mm3**;
- lift arms vs fixed carrier structure: **0 mm3**;
- carrier vs body: **0 mm3**;
- carrier vs all Z50: **0 mm3**;
- gas spring vs body: **0 mm3**;
- gas spring vs Z50: **0 mm3**;
- gas spring vs carrier: **0 mm3**;
- gas spring vs lift arms: **0 mm3**.

All-angle moving-head separation is additionally controlled by invariant envelopes about the TILT Y axis:

- arm-to-shell lateral gap: **3.00 mm**;
- negative-side arm to TILT-pod lateral gap: **3.25 mm**;
- minimum arm-end radial gap to TILT boss: **14.43 mm**;
- carrier inner face to camera boss: **1.00 mm**.

The 1.00 mm boss/carrier value is acceptable only for the current CAD screen; manufacturing tolerance, grit and axial play must be resolved before release.

## 8. DN150 LOW gate

Ideal DN150 screen at LOW:

- moving camera minimum clearance over the full 1-degree TILT sweep: **3.0405 mm** at about `-61 deg`;
- moving camera minimum wet-floor clearance: **3.7214 mm** at about `-58 deg`;
- lift-arm minimum ideal-pipe clearance: **4.9300 mm**;
- fixed carrier minimum ideal-pipe clearance: **8.0585 mm**;
- gas spring minimum ideal-pipe clearance: **37.17 mm**.

These are ideal-cylinder CAD values, not dirty/oval-pipe release values. The moving camera remains the DN150 limiting hard part.

## 9. Gas spring

The MiniCam source package confirms the use of one **150 N gas spring** in the manual lift (`DRW-002-744`). WB22A keeps that source principle.

Current prototype candidate retained for packaging screen:

- ACE `GS-12-20-V4A`;
- force screen: `150 N`;
- body OD screen: `12 mm`;
- stroke: `20 mm`;
- nominal extended length screen: `72 mm`;
- nominal retracted length screen: `52 mm`.

WB22A geometry:

- fixed base: `X195.0 / Y0 / Z84.0 mm`;
- moving attachment: `62.5 mm` from the lower body pivot.

Calculated spring lengths:

- LOW: **55.629 mm**;
- MID: **60.874 mm**;
- HIGH: **68.280 mm**.

Minimum margin from either stroke end: **3.629 mm**.

Assist torque at 150 N:

- LOW: **1.026 N m**;
- MID: **1.408 N m**;
- HIGH: **1.068 N m**.

This proves geometry, not final hand force. Final camera/carrier mass and CG are still required before the spring force is released.

## 10. Effect on WB21 harness

WB21's cable article, electrical allocation and body-gland study remain useful technical work, but its lift-arm coordinates are no longer controlling because WB22A changes:

- link length;
- upper pivot height;
- arm Y plane;
- arm section;
- camera-to-link interface;
- moving carrier geometry.

Therefore the WB21 `52.8 ±0.5 mm` flex length and `Y=-13` moving-clamp solution must **not** be released or manufactured from the old coordinates.

The next harness work is renumbered **WB23** and must be re-solved on WB22A geometry.

## 11. Remaining HOLDs

Before manufacturing release:

1. assign final material to the 4 x 14 mm lift arms and run bending/fatigue/abuse-load calculations;
2. dimension real pivot bushes, washers, circlips and axial float using purchasable parts;
3. increase or tolerance-control the 1.0 mm carrier-to-camera-boss lateral gap;
4. add dirt relief/drainage and anti-snag radii to the carrier webs;
5. calculate carrier stiffness with camera mass and cable pull;
6. verify the physical gas-spring article and end fittings from an allowed procurement source;
7. weigh the actual camera/carrier and tune spring force for one-hand operation;
8. run a printed/metal LOW jig in a real DN150 pipe, including ovality, grit and cable drag;
9. re-solve the complete body-to-camera harness on WB22A geometry;
10. do not machine from this work block yet.

## 12. Next work block

**WB23 — corrected lift harness and final serviceable head connector.**

WB23 must:

- retain a serviceable straight six-contact SP13-class connector unless a better field-repairable part is proven;
- route the local head cable on the corrected 90 mm lift;
- define both body-pivot flex and camera-carrier transition explicitly;
- avoid a hidden second uncontrolled flex zone;
- retain field camera replacement without opening the pressurised crawler body;
- re-check all LOW/MID/HIGH collisions against all ten Z50 and the gas spring.

## Change log

### 2026-09-13 — WB22A

- audited the user's Proteus repair photographs against the source drawings;
- recorded photographs as topology evidence only;
- found and corrected the WB20 wet-cut extrusion-direction mistake;
- found the previously missed WB21 four-bar/camera solid collision;
- rejected the attempted cure of simply pushing the arms out toward the Z50 gears;
- introduced a rigid head carrier between four-bar and sealed camera;
- changed lift link length from 120 to 90 mm;
- changed upper body pivot from Z112 to Z109 mm;
- selected a screened 4 x 14 mm arm section on `Y=±31 mm`;
- preserved the WB20 LOW optical-axis position;
- re-screened all ten Z50, body, carrier, gas spring and DN150;
- achieved `PASS_SCREEN / MANUFACTURING HOLD / PROCUREMENT HOLD`;
- declared WB21 harness coordinates superseded and moved harness work to WB23.
