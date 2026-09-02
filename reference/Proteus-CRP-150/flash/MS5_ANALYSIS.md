# Proteus MS5 service image analysis

Status: source evidence extracted from the customer-provided Proteus flash-drive image. This record documents observations; it is not permission to copy proprietary firmware.

## Image and filesystem

- original archive: `MS5.z01` ... `MS5.z29` + `MS5.zip`;
- reconstructed image: HDD Raw Copy Tool 1.20 IMGC, 7.40 GiB logical source;
- source descriptor: `Mass Storage Device`, revision 1.00, serial `212102612040`;
- filesystem: ext3, label `linux_ltib`, ARM Linux application image;
- extraction tools: open-source `shizmob/unimgc`, `fdisk`, `debugfs`;
- image was processed read-only until a disposable extracted copy was made.

## Relevant contents

| Evidence | Engineering use |
|---|---|
| `/root/Help/Adjusting the camera elevator.avi` and text | Confirms external twin-arm lift and fore/aft manual lock operation. |
| `/root/Help/Changing the wheels.avi` and text | Confirms field wheel change with one accessible central fastener and indexed hub/cam engagement. |
| `/root/Help/Pressurizing products.avi` | Confirms pressure-test/service workflow is an essential product function. |
| `/root/Help/Connecting crawler to control unit.avi` | Confirms a single serviceable crawler tether interface. |
| `/root/Help/Connecting camera to crawler.avi` | Confirms separately serviceable camera head interface. |
| `/root/Help/Cable drum friction brake.avi` | Confirms manual reel with mechanical friction brake. |
| `/root/ProteusApp` | ARM executable with debug symbols; indicates camera, serial, video, drum and RS-485 functions. |
| `TW9912_Proteus_tvin.ko` startup reference | Confirms an analogue-video decoder in the source CCU. |
| `/dev/ProteusFPHub` startup reference | Confirms a product-specific front-panel device, which PX-1 must not require. |

## Mechanical conclusions carried into PX-1 Rev.PS

1. Retain the external manual parallelogram lift; do not add a pressure-crossing full-width lift tube.
2. Retain one-handed fore/aft locking logic, but use a standard M8 adjustable clamping lever, Belleville stack, commercial 150 N gas spring and standard pins/circlips.
3. Retain field wheel removal through one central fastener. Replace the proprietary cam/index profile with a keyed removable hub, captive/retained M8 centre screw, wedge-lock washer and protective cap.
4. Retain removable side covers and individually serviceable axle seal carriers.
5. Retain the manual reel, mechanical brake, level wind and measuring wheel.
6. Retain one sealed tether connector and mechanical strain relief; do not create cartridge or cassette modules.

## Limits

The flash image does not provide manufacturing authority for PX-1 and does not close dimensions, materials, tolerances or load ratings. Video-derived geometry remains a functional reference. Final PX-1 dimensions come from its own CAD, measurements, calculations and prototype tests.

