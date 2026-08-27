# PX-1 Rev.FM — manual lift balance and mechanical stops

Status: prototype geometry baseline, not machining release.

## Source basis
Uploaded Proteus crawler lift drawing DRW-002-744 shows the architecture we intentionally retain:
- 150 N gas spring;
- M8 manual clamping lever;
- three DIN2093 disc springs 20x10.2x1.1 in the clamp stack;
- separate side arms and lever axles;
- Ø6 pin and Ø8/circlip service hardware;
- selected 15x2.5 O-rings at the lift housing interfaces.

PX-1 uses its own linkage dimensions and body geometry.

## Corrected PX-1 parallelogram
The previous single-link envelope is superseded by a true four-bar arrangement.

Body-side pivots:
- X = 200 mm;
- lower Z = 92 mm;
- upper Z = 112 mm;
- vertical pivot spacing = 20 mm.

Camera-side pivots retain the same 20 mm vertical spacing.
Both links are 120 mm center-to-center.

This keeps the camera cradle orientation substantially constant while height is changed manually.

## Height positions
With camera-axis offset +2 mm from the camera-side pivot midpoint:
- LOW / DN150: camera axis Z = 75 mm; arm angle about -13.985 deg; camera axis X about 83.557 mm;
- MID: Z = 130 mm; arm angle about +12.513 deg; camera axis X about 82.851 mm;
- HIGH: Z = 205 mm; arm angle about +57.317 deg; camera axis X about 135.200 mm.

Only LOW is allowed in DN150 until the physical-tube gate is passed.

## Gas spring study
Use one 150 N gas spring as the first prototype, matching the successful CRP-class order of magnitude.

Current geometry candidate:
- body-side spring pin X=220, Z=35 mm;
- moving spring pin located 80 mm from the lower lift pivot along the lower arm.

Calculated center-to-center spring lengths:
- LOW: 104.64 mm;
- MID: 123.08 mm;
- HIGH: 139.47 mm;
- required geometric stroke: about 34.83 mm.

Calculated ideal assisting torque about the lower pivot:
- LOW: ~6.90 N*m;
- MID: ~5.00 N*m;
- HIGH: ~1.20 N*m.

This is deliberately an assist, not a position lock. The M8 clamp must hold the lift with the spring removed or depressurized.

## Mechanical stops
DN150 safety is hardware-based.

Required stops:
1. LOW stop defines the folded working height;
2. removable DN150 stop physically blocks movement above LOW while the robot is configured for 150 mm pipe;
3. HIGH travel is available only after that stop is removed for larger pipes;
4. stop impact must react into the lift housing/body bosses, not into the camera connector or gas spring rod.

Preferred implementation:
- retained Ø6 hardened/stainless stop pin inspired by the source architecture;
- secondary adjustable M6 stop screw for prototype tuning;
- production stop position transferred to a fixed machined face after the physical DN150 sweep.

## Clamp
Prototype clamp stack:
- M8 adjustable hand lever;
- hardened/stainless clamp axle;
- 3x DIN2093 20x10.2x1.1 disc springs;
- thrust/friction washers;
- replaceable friction element if wet contamination lowers holding torque.

Acceptance:
- no slip for 10 min in LOW/MID/HIGH with complete camera installed;
- repeat after wet mud contamination;
- 500 raise/lower cycles;
- clamp still holds with gas spring disconnected.

## DN150 consequence
Moving the upper body pivot down to Z112 materially improves pipe clearance compared with the earlier Z118 candidate. The full low-position camera/yoke/fastener sweep remains a separate validation gate.