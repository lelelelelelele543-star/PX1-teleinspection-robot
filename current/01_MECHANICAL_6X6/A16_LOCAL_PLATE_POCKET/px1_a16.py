#!/usr/bin/env python3
"""PX1 A16: design-only local plate pocket clearance, from A15 documented geometry."""
from pathlib import Path
import math
p=Path(__file__).resolve().parent
diameter=25.; center=13.5; plate_center=25.5; thickness=6.; clearance=.5
face=plate_center-thickness/2
overlap=center+diameter/2-face
pocket=overlap+clearance
web=thickness-pocket
assert abs(overlap-3.5)<1e-9 and abs(pocket-4.)<1e-9
assert abs(web-2.)<1e-9
# 2D section; dimensions mm. Pockets only on inner plate, NOT pressure housing.
S=6; O=300
def X(y):return O+S*y
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 420">
<rect width="760" height="420" fill="#f8fafc"/>
<text x="28" y="38" font-size="22" font-family="sans-serif">PX1 A16 — proposed local plate pocket</text>
<text x="28" y="60" font-size="13" font-family="sans-serif">Dimensioned Y-Z section, ASSUMED 0.5 mm assembly clearance, NOT a 3D solid</text>
<rect x="{X(-plate_center-thickness/2)}" y="100" width="{S*thickness}" height="205" fill="#94a3b8"/>
<rect x="{X(face)}" y="100" width="{S*thickness}" height="205" fill="#94a3b8"/>
<rect x="{X(face)}" y="145" width="{S*pocket}" height="115" fill="#f8fafc" stroke="#ea580c" stroke-width="2"/>
<rect x="{X(-face-pocket)}" y="145" width="{S*pocket}" height="115" fill="#f8fafc" stroke="#ea580c" stroke-width="2"/>
<circle cx="{X(-center)}" cy="200" r="{S*diameter/2}" fill="#93c5fd" stroke="#1d4ed8" stroke-width="2"/>
<circle cx="{X(center)}" cy="200" r="{S*diameter/2}" fill="#93c5fd" stroke="#1d4ed8" stroke-width="2"/>
<g font-family="sans-serif" fill="#0f172a" font-size="15">
<text x="28" y="337">Motor diameter 25 mm | center Y = +/-13.5 mm | plate inner face = +/-22.5 mm</text>
<text x="28" y="361">Pocket depth = {pocket:.1f} mm | remaining web = {web:.1f} mm | nominal gap = {clearance:.1f} mm</text>
<text x="28" y="388" font-size="13">LOCAL pocket candidate only; length along X, bearings, strength and seals NOT verified</text>
</g></svg>'''
(p/'px1_a16_preview.svg').write_text(svg,encoding='utf-8')
print(f'PASS arithmetic: overlap={overlap}, pocket={pocket}, web={web}, gap={clearance}')
print('NEEDS_PHYSICAL_CHECK strength; SKIPPED 3D boolean, actual motor envelope')
