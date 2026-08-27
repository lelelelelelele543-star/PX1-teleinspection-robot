# PX-1 Rev.CC — compact digital camera selection

Status: preferred prototype candidate selected; exact mechanical drawing and procurement availability still to be confirmed before RELEASE.

## Preferred camera candidate
SNM Technology SMX-1E67E32 class module.

Published characteristics:
- PCB: 32 x 32 mm;
- sensor: Sony IMX307, 1/2.8 inch STARVIS;
- effective video: 1920 x 1080 up to 30 fps;
- compression: H.265 / H.264 / MJPEG;
- network: 10/100BASE-T Ethernet;
- protocols include RTSP and ONVIF;
- supply: 12 V DC or PoE;
- published current: 210 mA;
- lens is not fixed by the module and can be selected for PX-1 field of view.

## Mechanical fit correction
A 32 x 32 mm square has a corner-to-corner diagonal of about 45.25 mm. With the current head target OD 52 mm and nominal wall 2.5 mm, nominal cylindrical ID is about 47 mm. Therefore a bare 32 x 32 PCB can fit geometrically inside the cylindrical envelope, but corner clearance is only about 0.87 mm radially at the diagonal.

This is too small to call production-safe without checking:
- PCB tolerance and components projecting beyond board outline;
- internal ribs / fasteners;
- electrical insulation;
- assembly insertion path;
- actual machined ID and anodizing/coating allowance.

Rev.CC therefore treats 32 mm as the largest acceptable square PCB candidate, not a released fit.

## Architecture
Rotating cartridge:
1. lens + IMX307 camera board;
2. local H.265 encoder on the camera module;
3. 100BASE-TX Ethernet;
4. compact Ethernet-rated slip ring;
5. separate power circuits through the same rotary unit where supported.

Fixed camera-head side:
- Ethernet leaves the ROLL joint;
- conversion to 10BASE-T1L occurs on the fixed side or crawler electronics bay;
- long tether uses single-pair Ethernet for video/data;
- no CVBS, PAL/NTSC or coaxial video conductor in the final architecture.

## Packaging decision
Do not enlarge the head yet. First attempt:
- use 32 x 32 board diagonally registered in a removable insulating carrier;
- reserve minimum 0.5 mm local assembly clearance at PCB corners;
- machine four shallow internal relief flats/pockets only if structural wall analysis allows it;
- keep electronics removable as a cartridge rather than potting the whole board.

If exact component heights or connectors violate the Ø52 envelope, next preference is a split sensor/encoder architecture rather than immediately increasing head diameter.

## Verification gates
- obtain exact PCB drawing including connector/component keep-outs;
- choose lens and verify optical window clearance/FOV;
- thermal test sealed at maximum lighting and encoder load;
- stream 1080p30 H.265 continuously through selected Ethernet rotary joint;
- 24 h stationary network test;
- rotating test at low/nominal/high ROLL speed;
- packet-loss and image-freeze logging;
- pressure/leak test after full assembly;
- rerun DN150 swept-clearance with final head solid.

## Source
SNM Technology SMX-1E67E32 product specification, accessed 2026-08-27: https://www.snmtechnology.com/smx-1e67e32
