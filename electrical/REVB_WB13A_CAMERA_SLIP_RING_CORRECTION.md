# PX-1 Rev.B — WB13A camera slip-ring correction

Date: 2026-09-11
Status: CAMERA ROTARY CANDIDATE CORRECTED / VIDEO QUALIFICATION HOLD

## 1. Reason for correction

WB13 conservatively assumed that camera PAN/lighting current crossed the continuous ROLL slip ring and therefore promoted the Ø22 mm `M220-0205-12S` mixed-current device for the camera.

WB14 re-audited the active mechanical architecture:
- LED annulus is fixed to the static outer shell;
- TILT/ROLL motors and their drivers are fixed-side relative to the ROLL interface;
- only the inner camera sensor/module rotates continuously.

Therefore the camera rotary current is far lower than WB13 assumed.

A second geometric conflict was also found:
- current ROLL bearing baseline is 6803 / 61803, ID 17 mm;
- the earlier camera rotary-transfer keepout was Ø12.5 mm;
- M220 OD is 22 mm and cannot pass through the existing 17 mm central bearing/spindle passage.

Conclusion: the WB13 M220 camera candidate was over-sized electrically and incompatible with the active central passage. It remains valid for the reel only.

## 2. Corrected camera candidate

Preferred engineering candidate:
- manufacturer: SenRing;
- model: `M125-06`;
- outside diameter: 12.5 mm;
- body length: 13.5 mm;
- six circuits;
- 1.5 A max per circuit;
- AWG30 silver-plated PTFE leads;
- gold-gold contact system;
- standard product family, manufacturer states stock availability;
- voltage class up to 240 VAC/VDC;
- electrical-noise figure <0.01 ohm;
- IP51 only — installation must remain inside the sealed camera head.

Packaging against 6803:
- bearing ID = 17.0 mm;
- slip-ring OD = 12.5 mm;
- diametral clearance = 4.5 mm;
- radial clearance = 2.25 mm before sleeve/retainer tolerances.

This restores the geometry already used in the old Rev.BJ packaging study.

## 3. Actual rotating functions

Only four circuits are presently required:
1. +12V_CAM
2. GND_CAM
3. CVBS_SIGNAL
4. CVBS_RETURN

Circuits 5 and 6 remain insulated spare.

No UART is required across the continuous ROLL joint for the Rev.B fixed-focus RunCam camera. Camera menu/setup is performed before deployment; TILT/ROLL and light control are handled on the fixed side.

## 4. Current margin

RunCam Phoenix 2 conservative design reservation:
- 12 V current <=120 mA until measured.

Even allowing additional camera-side service margin, this is far below the M125-06 1.5 A per-circuit rating.

Do not use spare rings in parallel for camera power. There is no need, and paralleling would complicate contact diagnostics.

## 5. Video limitation remains

M125-06 is not a controlled 75-ohm video rotary joint.

Therefore selection is still conditional on WB12 physical tests:
- raw CVBS through M125 while stationary;
- continuous rotation;
- direction reversal;
- Delta-Opti balun after the fixed side;
- 40 m tether + reel ring;
- 100/150 m tests;
- LED PWM / traction PWM operating simultaneously.

If CVBS quality through M125 is unacceptable, replace only the camera rotary transfer with a documented video-capable compact joint that still fits the <=17 mm central passage. Do not enlarge the entire Ø52 camera head by default.

## 6. Procurement status

Manufacturer current data identifies M125-06 as a standard stocked product family.

However an exact approved ChipDip/marketplace purchase route for genuine SenRing M125-06 has not yet been verified. Therefore:
- engineering selection: YES;
- procurement freeze: HOLD;
- do not machine a non-adjustable slip-ring pocket until exact sample/drawing is obtained.

## 7. Reel decision unaffected

The RMP300-style reel still benefits from the mixed M220 power/signal candidate because it must carry:
- ~120 VDC tether power;
- approximately 1 A-class long-line current;
- RS-485 pair;
- balanced video pair.

This correction applies only to the camera ROLL interface.

## Change log

### 2026-09-11 — WB13A
- removed fixed-shell LED and motor loads from the camera slip-ring current budget;
- discovered Ø22 M220 conflict with the active 17 mm 6803 passage;
- restored Ø12.5 x 13.5 mm M125-06 as the leading camera engineering candidate;
- reduced used rotary circuits to camera power + raw CVBS only;
- retained two spare rings;
- retained full CVBS-through-rotation qualification before production release.
