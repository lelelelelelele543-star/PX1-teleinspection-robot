# PX-1 Rev.CE — compact Ethernet slip-ring correction

Status: architecture correction; preferred candidate replaces Ø22 baseline.

## Key finding
JINPAT lists LPMS miniature Ethernet slip rings much smaller than the previously selected Ø22 LPC family.

Preferred candidate class:
- LPMS-12-0701-01E2
- outside diameter: approximately Ø6.5 mm
- Ethernet: 1x 100 Mbps
- auxiliary circuits: 7x 1 A
- customizable miniature series

This is a major packaging improvement. The Ø22 LPC-12-0602-01E2 remains a backup industrial option, not the preferred PX-1 baseline.

## Consequence for mechanics
Because the Ethernet rotary transfer no longer forces a >22 mm axial passage, the ROLL cartridge can return to the earlier compact bearing architecture. 6803-2RS (17x26x5 mm) can again be considered around the rotary-transfer axis, subject to the exact LPMS lead exit and body-length drawing.

Do NOT freeze the bearing seats until JINPAT provides the exact outline drawing and lead-wire bend envelope for LPMS-12-0701-01E2.

## Camera board
SMX-1E67E32 remains the current camera candidate:
- 32x32 mm PCB
- Sony IMX307
- H.265/H.264
- 10/100BASE-T
- 12 V nominal supply
- RTSP / ONVIF

The PCB diagonal is 45.25 mm. With a nominal Ø47 mm internal head cavity, theoretical corner clearance is only about 0.87 mm radially, therefore exact connector/component protrusions are still a release blocker.

## Preferred signal architecture
Rotating cartridge:
SMX-1E67E32 -> 100BASE-TX -> LPMS miniature Ethernet slip ring.

Fixed camera head:
100BASE-TX -> long-line digital interface (10BASE-T1L or another validated long-reach Ethernet bridge) -> tether.

No CVBS, PAL/NTSC, or coaxial video conductor is used.

## Release blockers
1. exact LPMS-12-0701-01E2 outline drawing and lead exit;
2. verified 100BASE-TX packet integrity while rotating under motor EMI;
3. exact SMX board Z-height and connector keep-outs;
4. power budget on auxiliary slip-ring circuits;
5. final ROLL bearing selection and axial stack;
6. thermal test inside sealed Ø52 head.
