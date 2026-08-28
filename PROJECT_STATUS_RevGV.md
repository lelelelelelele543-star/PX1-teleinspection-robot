# PX-1 Rev.GV — sealed open wet-deck + revised electronics packaging

Status: CAD-VALIDATED PROTOTYPE BASELINE; not machining release.

## Major body correction
Rev.GV replaces the invalid old folded-camera `nose` subtraction with a real pressure boundary.

The folded camera/lift now sits above a continuous sealed structural roof. The wet zone is open to the robot nose and upward; P0 remains dry below it.

Active wet-deck roof profile (X,Z mm):
- (0,38)
- (120,42)
- (200,77)
- (220,90)

Structural roof thickness target: 5 mm.

This profile is intentionally monotonic toward the rear, so on a level crawler water/sludge has a continuous gravity path toward the open nose rather than a cup-shaped pocket. Final transitions require generous smooth radii and a physical sludge/drainage test.

## LOW camera / lift clearance
Using the active Rev.FN LOW camera geometry:
- camera OD 52 mm;
- camera axis X ~=83.557 mm, Z=75 mm;
- lens/front reference X ~=47.557 mm;
- wet-deck half-width +/-38 mm.

Validated clearances:
- side clearance around camera: 12 mm each side;
- gap below camera at front / center / rear: about 9.41 / 8.21 / 7.01 mm;
- minimum lower lift-arm to pressure-roof clearance: 6.0 mm;
- camera/body intersection: 0;
- all four lift-arm/body intersections: 0.

First-order open horizontal cone at the front plane is about 77.25 deg before the actual selected lens/FOV is applied.

## X200 compatibility
The rising roof reaches Z77 at X200, so the X200 bevel/output shaft and side input gear around Z45 stay fully below the wet zone. The Rev.GT dynamic-seal architecture is therefore not cut open by the camera-deck correction.

X200 remains the active side-train input because:
- all three wheel stations still rotate in the same direction;
- X250 is worse for mesh-path symmetry;
- X150 is symmetric but creates a substantially harder combined wheel/input shaft, bearing and sealing stack.

## Rear-top electronics saddle
Rev.GV adds a compact dry electronics saddle behind the lift pivot rather than lengthening the wheelbase or putting the controller in the wet-deck volume.

Outer CAD envelope:
- X 218..307 mm;
- Y +/-39 mm;
- Z 90..110 mm.

It remains inside ideal DN150 with about 5.15 mm geometric margin at its worst rectangular corner.

The full NUCLEO-F446RE is retained as the controller for this prototype packaging study, moved into the saddle. Packaging envelope is 82.5 x 70 x 12 mm. This assumes a low-profile installation with tall plug headers removed/replaced by a low-profile harness. Actual installed height is a release measurement gate.

## Revised dry-volume packaging
The following envelopes pass the current collision/containment validator simultaneously:
- AVD video transmitter 55x20x12;
- 48->24 V converter reserve 70x65x18;
- TB6612 camera-axis driver 50x25x19;
- input-protection reserve 22x60x22;
- compact dual traction H-bridge candidate about 28x46x12;
- NUCLEO-F446RE low-profile 82.5x70x12 in the top saddle;
- 2x traction motors Ø32x92;
- PTW1CM-class pressure sensor Ø24.4x25.

PASS:
- zero component/component intersections;
- zero component volume outside the modeled dry cavity;
- body remains inside ideal DN150;
- LOW camera and lift remain collision-free.

## Traction-driver packaging candidate
A Pololu Dual MC33926-class carrier is now the preferred compact packaging candidate for the prototype study because one board can drive both traction motors and the current motor-selection target keeps stall current around <=1.2 A per motor. Public/ChipDip-hosted documentation describes the dual board as 5..28 V and about 3 A continuous per channel, with a footprint about 1.10 x 1.8 inch.

This is NOT frozen BOM yet. Exact ChipDip purchasability/current article must be verified before replacing the two BTS7960 prototype modules in the BOM. If the finally measured motor stall current violates the target, the driver choice is reopened.

## CAD validator
`mechanical/cadquery/PX1_WetDeck_Packaging_RevGV.py`

The script exports:
- `PX1_PressureBody_WetDeck_RevGV.step`
- `PX1_RevGV_Packaging.step`
- `REV_GV_VALIDATION.json`

## Release gates
1. add manufacturing radii/fillets to the monotonic wet-deck roof and rerun LOW/MID/HIGH lift sweeps;
2. physical water + sludge drainage test, including representative pipe inclines;
3. actual selected camera lens/FOV optical-cone check;
4. actual NUCLEO board installed-height measurement with low-profile harness strategy;
5. exact compact dual traction-driver article and thermal test;
6. rebuild current viewer from Rev.GV CAD, not Rev.GC nose geometry;
7. full pressure-body/upper-saddle FEA and 1 bar dry structural proof before machining release.
