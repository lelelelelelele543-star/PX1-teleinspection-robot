# PX-1 Rev.GX — integrated wet-deck drainage and streamlined controller saddle

Status: CAD-VALIDATED PROTOTYPE BASELINE; not machining release.

## What Rev.GX closes
Rev.GX integrates the camera-view correction, real P0 pressure roof, sealed drainage scuppers, rear motor extension and revised electronics packaging into one body source.

The active source is:
`mechanical/cadquery/PX1_WetDeck_Drainage_RevGX.py`

## Wet-deck / camera
Pressure-roof profile (X,Z mm):
- 0,38
- 120,42
- 200,77
- 220,90

Roof thickness target: 5 mm.

LOW camera checks:
- Ø52 camera side clearance: 12 mm each side;
- clearance below camera front/centre/rear: ~9.41 / 8.21 / 7.01 mm;
- minimum lower lift-arm to roof: 6.0 mm;
- approximate unobstructed horizontal forward cone before actual lens FOV: ~77.25°;
- zero camera/body intersection;
- zero four lift-arm/body intersections.

The wet deck is open forward and upward. There is no closed front wall and no cup-shaped recess in front of the lens.

## Twin sealed scuppers
Two wet drains are integrated at the longitudinal local-low transition:
- X120;
- Y +/-26;
- Ø6 wet bore;
- Ø10 structural outer tube;
- 2 mm radial starting wall.

The tube body is fused into the pressure structure before the bore is cut, so the wet passage crosses the crawler without communicating with P0.

The shallow front deck is ~1.91° in body coordinates. If the crawler points nose-up beyond this, water can move rearward to the X120 transition and exit the scuppers instead of accumulating there. The following body ramp is ~23.63°, so the calculated local-low behaviour is retained for moderate nose-up attitudes below that range. Physical pitch/roll/sludge tests remain mandatory.

## Streamlined controller saddle
The rectangular Rev.GV top pod is superseded by a pipe-friendly trapezoidal/splayed section.

Outer section at the rear controller saddle:
- base Y +/-39 at Z90;
- vertical side to Z104;
- tapered upper wall to Y +/-34 at Z110.

This retains the required low-profile NUCLEO-F446RE cavity while improving ideal-DN150 geometric margin:
- around 10.0 mm near Y39/Z104 transition;
- around 7.8 mm at Y34/Z110 top edge.

The old rectangular worst corner was only ~5.15 mm, so the streamlined version is preferred.

## Electronics packaging PASS
Current dry-volume envelopes simultaneously fit without intersection:
- 48->24 V converter reserve 70x65x18 at X20..90;
- AVD video TX 55x20x12 at X95..150;
- TB6612 camera-axis driver 50x25x19;
- input protection reserve 22x60x22 moved rearward under the rising roof;
- compact dual traction H-bridge candidate ~28x46x12;
- NUCLEO-F446RE low-profile envelope 82.5x70x12 in the rear-top saddle;
- two Ø32x92 traction motors;
- PTW1CM-class pressure sensor Ø24.4x25.

PASS screen:
- zero component/component intersections;
- zero component volume outside the dry cavity;
- zero component/scupper structural-tube intersections;
- zero body volume outside ideal DN150.

## Driver note
The compact dual MC33926-class carrier remains a packaging/BOM candidate, not yet a frozen article. Its attraction is that one ready-made dual board replaces two very bulky BTS7960 modules while the current traction-motor target remains roughly <=1.2 A stall per motor. Exact procurement and thermal validation are still required before BOM freeze.

## Exports produced by the validator
- `PX1_PressureBody_WetDeck_RevGX.step`
- `PX1_RevGX_Packaging.step`
- `REV_GX_VALIDATION.json`

## Next block
1. replace sharp roof-profile breaks with manufacturable smooth radii/lofts without creating new water pockets;
2. run LOW/MID/HIGH full lift sweep against the revised roof and controller saddle;
3. update the real-CAD viewer to Rev.GX so the old invalid nose disappears;
4. prepare pressure/FEA load cases including the two scupper-tube penetrations and top saddle;
5. freeze actual controller installation height and traction-driver article only after physical parts are measured.
