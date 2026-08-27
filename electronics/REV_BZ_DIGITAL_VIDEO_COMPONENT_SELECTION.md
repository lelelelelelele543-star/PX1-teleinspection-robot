# PX-1 Rev.BZ — digital video component selection

Status: prototype selection; no CVBS/NTSC/PAL/coax in final architecture.

## Camera baseline
Prototype candidate: compact 38x38 mm H.265 IP camera module, Sony IMX307 + SigmaStar SSC335 class (example MC200J12).

Required functions:
- 1920x1080 up to 30 fps;
- H.265/H.264 hardware encoding;
- RTSP + ONVIF;
- 10/100 Ethernet electrical interface available on board header;
- 12 V supply;
- target power <=2 W;
- M12 interchangeable lens.

Reason: this gives a complete digital camera/encoder without designing a custom image-processing PCB.

## Long tether link
Prototype media conversion: Analog Devices EVAL-ADIN1100 / ADIN1101 family.
- standard 10BASE-T Ethernet <-> 10BASE-T1L;
- 10 Mbps over one twisted pair;
- vendor evaluation platform supports links up to 1.7 km;
- therefore 100-150 m PX-1 tether has large distance margin.

Evaluation boards are for bench validation only. They are too large to freeze into the Ø52 camera head. If the architecture passes testing, use a compact purchased module or later a dedicated small interface board; do not force the full evaluation PCB into the head.

## Recommended physical partition
ROTATING CAMERA CARTRIDGE:
IP camera module / sensor+encoder.

FIXED CAMERA-HEAD SECTION:
Ethernet-to-10BASE-T1L conversion where packaging permits.

TETHER:
one SPE twisted pair for Ethernet data. Power conductors may remain separate in prototype; SPoE is a later optimization, not required for first article.

CONSOLE:
10BASE-T1L-to-standard-Ethernet converter -> embedded computer/display.

## ROLL boundary warning
A normal low-cost capsule slip ring must NOT automatically be assumed suitable for 10BASE-T1L. The rotary interface must be demonstrated with link-quality/error testing through 360° rotation. Preferred paths, in order:
1. rated SPE/Ethernet rotary joint;
2. contactless Ethernet rotary coupler;
3. validated matched slip-ring pair only after BER/link-margin test.

Do not buy a generic slip ring and call it Ethernet-compatible without test evidence.

## Prototype acceptance
- 1080p30 H.265 RTSP stream for >=8 h;
- no visible frame corruption while ROLL rotates continuously;
- packet loss and link drops recorded;
- test at 40 m, 100 m and 150 m representative tether;
- simultaneous motors and lighting ON/OFF EMC test;
- latency measured end-to-end;
- camera recovers automatically after cable disconnect/reconnect and brownout.

## Sources checked 2026-08-27
- Analog Devices EVAL-ADIN1100: 10BASE-T1L / 10BASE-T media converter, 10 Mbps, vendor states up to 1.7 km.
- Analog Devices DEMO-ADIN1100D2Z / EVAL-10BT1L-MCS: current SPoE-capable reference platforms.
- MC200J12 class: SSC335 + Sony IMX307, H.265, 1080p30, RTSP/ONVIF, 38x38x15 mm.

## Next gate
Find or validate the rotary Ethernet/SPE transfer first. It is now the critical component that determines whether unlimited ROLL remains practical with the fully digital architecture.
