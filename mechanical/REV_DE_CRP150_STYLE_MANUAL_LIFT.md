# PX-1 Rev.DE — CRP150-style manual camera lift

Status: detailed architecture candidate based on the uploaded original Proteus crawler lift drawings, adapted to PX-1 geometry.

## Reference features taken from the uploaded drawings
The original Proteus crawler lift documentation shows:
- two side lever arms;
- a manual clamping lever M8;
- a 150 N gas spring;
- dedicated lever axles/pins;
- disc springs in the clamp stack;
- circlips and thin thrust washers for service adjustment;
- O-rings around selected lift housing interfaces.

These are architecture references only; PX-1 uses its own dimensions and parts.

## PX-1 lift concept
Keep the user-required one-hand manual parallelogram lift.

Functions:
- operator releases one M8 clamping lever;
- 150 N-class gas spring partly balances the camera head;
- camera height is moved by hand;
- lever is re-clamped at the desired height;
- hard mechanical LOW and DN150-SAFE stops prevent accidental over-height in small pipe;
- HIGH position is available only for larger pipe.

## Packaging candidate
Coordinate system: pipe floor / wheel contact plane Z=0, crawler front X=0.

Current candidate:
- lift base pivot zone X=55–115 mm;
- lower pivot axis Z≈82–88 mm;
- paired arms length 78–88 mm candidate;
- arm plate thickness 4 mm stainless or 5 mm Al 7075/6082 after stiffness check;
- pivot pins Ø8 mm baseline;
- replaceable polymer/bronze bushings rather than running aluminum directly on pins.

Camera head stays in front of the main body in LOW position so its centerline can sit below the body top without collision.

## Camera height targets
The uploaded MiniCam documentation and current PX-1 DN150 requirements support a wide manual height range, but exact positions must be collision-checked.

PX-1 starting targets:
- LOW camera axis: Z≈80–85 mm;
- DN150-SAFE axis: Z≈95–105 mm;
- HIGH: Z≈180–220 mm initially, final maximum after stability test.

The LOW camera head is intentionally forward-overhanging. The body nose is shaped/recessed around the folded head and lift links rather than forcing the entire camera above the roof.

## Gas spring
Prototype target: 150 N class, matching the proven order of magnitude in the MiniCam lift drawing.

Do not order exact stroke/length until linkage CAD is solved.
Required selection fields:
- extended length;
- stroke;
- end fitting type;
- force 120–180 N adjustment window;
- corrosion-resistant rod/body or protective boot;
- operating temperature suitable for sewer work.

## Clamp stack
Use a field-serviceable manual clamp rather than a proprietary locking mechanism:
- M8 adjustable clamping lever;
- hardened/stainless clamp axle;
- Belleville/disc spring stack to maintain clamp preload;
- thrust washers;
- replaceable friction washer if required.

The clamp must hold camera position with power removed and after wet contamination.

## Pivot service
- common Ø8 pins where practical;
- circlips or shoulder screws for axial retention;
- thin shims available for play adjustment;
- grease grooves only where they cannot pump dirt into seals;
- no welded permanent pivots.

## DN150 safety
Firmware does not make the lift safe; the lift is manual.

Therefore DN150 protection is mechanical:
- removable/indexed stop pin or stop screw blocks the HIGH range;
- LOW/SAFE positions remain reachable;
- camera TILT still operates within the allowed pipe envelope.

## Acceptance tests
- one-hand raise/lower with complete camera head installed;
- hold 10 min at each angle without clamp slip;
- 500 lift cycles;
- wet/muddy clamp test;
- measured handle force;
- side-play check before/after cycling;
- DN150 physical tube sweep;
- rollover/stability check at HIGH position.

## Next CAD gate
Build the four-bar linkage and gas-spring line-of-action parametrically, then sweep the actual Ø52x72 digital camera-head envelope through LOW/DN150-SAFE/HIGH and TILT -105…+105°.
