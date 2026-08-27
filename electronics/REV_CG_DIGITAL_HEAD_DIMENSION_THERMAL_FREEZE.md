# PX-1 Rev.CG — digital head dimensional and thermal freeze

Status: engineering candidate, not RELEASE.

## Ethernet rotary joint
Current preferred family: JINPAT LPMS-12 with 100 Mbps Ethernet integration, project candidate LPMS-12-0701-01E2.

Verified family data from current JINPAT documentation:
- LPMS-12 body OD: 6.5–7.6 mm depending configuration;
- LPMS-12 body length: approximately 17.4–19.4 mm depending family/drawing;
- Ethernet-integrated LPMS-12-0701-01E2 is listed as 1x 100 Mbps Ethernet + 7x 1 A circuits, OD 6.5 mm.

For CAD reserve until the exact supplier drawing is received:
- body envelope: Ø7.6 x 20.0 mm;
- straight lead-exit keepout: 10 mm each side before bend;
- no radial clamping on slip-ring shell;
- rotor/stator anti-rotation features must follow vendor drawing.

## Camera module
Current candidate: SMX-1E67E32 class, 32 x 32 mm board, 1080p30, H.265/H.264, 10/100 Ethernet.

The 32 x 32 mm board diagonal is 45.25 mm. With a nominal fixed-head internal diameter of 47 mm, corner clearance is only ~0.87 mm radially. Therefore:
- exact PCB outline and all connector/component protrusions are mandatory before machining;
- no board-edge connector may protrude beyond the 45.25 mm corner envelope;
- target local shell clearance is >=1.0 mm, therefore Ø52 mm is still HOLD until exact board drawing is known.

## Axial packaging target
Working head target returns to Ø52 x 72 mm.
Provisional axial budget:
- front window + seal/retainer: 5–7 mm;
- lens/sensor zone: 12–18 mm;
- 32 mm camera PCB/electronics zone: 12–16 mm depending actual component height;
- roll bearing/gear zone: 15–18 mm;
- LPMS-12 Ethernet rotary joint body: reserve 20 mm, partially overlapping bearing/gear axial region where mechanically possible;
- rear service closure: 5–7 mm.

This is a packaging budget, not a stacked sum: several zones must overlap radially/axially to stay within 72 mm.

## Thermal architecture
The digital camera/encoder dissipates heat continuously inside a sealed head. No fan is allowed.

Prototype heat path:
1. encoder/SoC thermal pad;
2. aluminium internal camera carrier;
3. direct metal contact/thermal pad to fixed outer aluminium shell;
4. shell rejects heat to surrounding air/water.

Do not thermally isolate the PCB on plastic standoffs only.

## Thermal acceptance test
Test complete sealed head at video maximum load, H.265 1080p30, Ethernet active, ROLL stationary then rotating.
Record:
- ambient temperature;
- outer-shell temperature near SoC thermal path;
- internal PCB/SoC temperature if telemetry is available;
- stream errors/frame drops;
- current consumption.

Test points:
- 25 °C ambient, 2 h continuous;
- 40 °C ambient equivalent test, 1 h minimum before production release;
- optional submerged-water test after leak testing, because water cooling will be substantially better than air.

Initial engineering limit: no thermal throttling, no stream loss, no connector/insulation damage. Exact component maximum junction temperature from the selected camera vendor overrides any project target.

## Release blockers
1. exact JINPAT drawing for LPMS-12-0701-01E2;
2. exact SMX-1E67E32 mechanical drawing including component heights and connector orientation;
3. measured camera power dissipation;
4. verified aluminium heat-spreader contact;
5. complete 2-hour thermal run;
6. combined DN150 sweep with final head dimensions.
