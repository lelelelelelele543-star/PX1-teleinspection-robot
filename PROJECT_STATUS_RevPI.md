# PX-1 Rev.PI — compact Proteus-style 150 m manual reel

Status: ACTIVE MASTER REEL DIRECTION.

## Why the full RMP300 is no longer the PX1 target
The uploaded RMP300 drawings are still the mechanical reference for the reel architecture, but the full production RMP300 is a 350 m class reel and is unnecessarily large/heavy for PX1.

PX1 retains the proven RMP functions:
- manual crank;
- mechanical brake;
- chain-driven layering spindle;
- measuring roller unit;
- replaceable slip ring;
- removable drip tray / open service layout.

The PX1 reel is narrowed for a 150 m inspection cable target.

## Source-controlled mechanical items retained
From uploaded MiniCam drawings:
- RMP200 layering spindle: 160 mm (ASS-002-545);
- crank handle: 160 mm (ASS-002-712);
- RMP300 chain: 670 mm with Z30 / Z16 sprockets (ASS-004-096);
- left support: 61904 2RS 20x37x9 + 16006 2RS 30x55x9 + shaft seal 30x42x7 (ASS-004-094);
- right support: 61804 2RS 20x32x7 + 6203 2RS 17x40x12 (ASS-004-095);
- meter counter bearings: 2x 618/8 8x16x4 and D29 guide roller (ASS-004-092 / ASS-002-696).

## PX1 capacity design
Design cable OD reference: 6.8 mm.
Target cable: 150 m.
Chosen PX1 drum geometry (design, not MiniCam source dimensions):
- core OD 140 mm;
- usable cable pack OD 300 mm;
- working width 145 mm;
- packing efficiency screen 0.78.

Calculated working width required for 150 m: about 126.3 mm.
Width reserve: about 18.7 mm.
Therefore the source 160 mm RMP200 layering traverse is sufficient for the PX1 150 m reel.

## Current PX1 reel envelope
Design target: approximately 530 x 240 x 520 mm.
This intentionally stays near the MiniCam manual-reel family form while being narrower than RMP200/300.

## Electronics simplification
- original meter counter PCB deleted;
- use simple magnetic angle encoder on the measuring wheel;
- original proprietary slip-ring PCB deleted;
- use standard 12-circuit slip ring, exact article remains BOM HOLD;
- no reel motor.

## CAD
Active source:
`mechanical/cadquery/PX1_PortableReel150_RevPI.py`

Local validation result:
- all solids valid;
- 150 m capacity screen PASS;
- exact side-plate contour, chain pitch and purchased slip-ring article remain HOLD.

## Lift status
DRW-002-744 confirms the source topology and service parts, but the available uploaded drawing does not provide manufacturing dimensions for FSS-002-068 / FSS-002-073 / ASS-002-723. Those dimensions remain HOLD rather than being invented. The existing Rev.PD topology file is therefore a functional placeholder only, not a machining source.
