# PX-1 Rev.AV — M8 rear-wheel retention freeze

Status: DRAWING-CANDIDATE.

## Locknut
Preferred purchasable specification from documentation indexed by ChipDip:
- RS stock no.: 2874056
- thread: M8 x 1.25
- type: nylon-insert self-locking hex nut
- standard: DIN 982 (tall P-type)
- material: A2 stainless steel
- across flats: 13 mm
- nominal height: 9.5 mm

This replaces the earlier generic M8 locknut placeholder.

## Flat washer
Geometry frozen for M8 flat washer:
- standard family: DIN 125 A / ISO 7089
- d1 = 8.4 mm
- d2 = 16 mm
- thickness = 1.6 mm

Material requirement for PX-1: stainless A2/A4. Exact ChipDip purchasable article remains procurement verification if the indexed item is a geometry-only catalogue reference.

## Shaft end
Rear output shaft external end:
- thread M8 x 1.25
- thread length: increase from 12 mm prototype target to 14 mm drawing target to accommodate DIN 982 nut height, washer and safe thread protrusion
- minimum fully engaged nut thread: 8 mm
- target protrusion after tightening: 1–2 full threads
- thread must remain completely outside the seal journal and bearing journal

## Tool envelope
- wrench/socket AF: 13 mm
- reserved socket OD envelope: >=20 mm
- straight axial approach required

## Environmental note
DIN 982 nylon-insert locking is acceptable for the first PX-1 prototype because normal robot temperature is far below typical nylon insert limits. If high-temperature operation or repeated aggressive chemical cleaning becomes a requirement, change to an all-metal prevailing-torque locknut.

## Release gate
Rear shaft and wheel hub can proceed to manufacturing drawing after FreeCAD is updated to the 14 mm threaded end and a physical 1:1 tool-access mock-up passes.
