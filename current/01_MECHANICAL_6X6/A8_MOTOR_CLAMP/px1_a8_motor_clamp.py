#!/usr/bin/env python3
"""PX1 A8: dimensioned transverse clamp clearance, mm. Pure Python 3."""
from pathlib import Path
from math import pi
MOTOR_D=24.0 # A7 ASSUMED, not vendor-confirmed
A7_BASE_W=26.0
A7_HOLE_Y=9.5
A7_HOLE_D=3.2
RADIAL_CLEARANCE=0.5 # design target
STRAP_T=3.0 # design target
NEW_BASE_W=44.0 # proposed, replaces A7 26 mm width
NEW_HOLE_Y=19.0 # proposed; fastener envelope within new base
CENTER_Z=17.0 # assumed motor centre in cross-section
R=MOTOR_D/2
R_IN=R+RADIAL_CLEARANCE
R_OUT=R_IN+STRAP_T
old_overlap=R+A7_HOLE_D/2-A7_HOLE_Y
new_edge_gap=NEW_HOLE_Y-A7_HOLE_D/2-R_OUT
assert old_overlap>0, "A7 bolt envelope unexpectedly clear"
assert new_edge_gap>0, "A8 strap and bolt envelopes intersect"
assert NEW_BASE_W/2 > NEW_HOLE_Y+A7_HOLE_D/2, "bolt breaks base edge"
assert R_IN>R
def pt(y,z):
    return f"{280+y*8:.2f},{305-z*8:.2f}"
def arc_path(radius):
    return f"M {pt(-radius,CENTER_Z)} A {radius*8} {radius*8} 0 0 1 {pt(radius,CENTER_Z)}"
svg=f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="580" viewBox="0 0 900 580">
<rect width="900" height="580" fill="#fff"/>
<text x="32" y="40" font-size="23" font-family="sans-serif">PX1 A8 — motor clamp, transverse section (mm)</text>
<text x="32" y="65" font-size="14" font-family="sans-serif">Parametric 2D, NOT validated 3D / NOT a manufacturing drawing</text>
<rect x="104" y="305" width="352" height="24" fill="#a8b4bf" stroke="#263746" stroke-width="2"/>
<circle cx="280" cy="169" r="96" fill="#dbe9f5" stroke="#145a82" stroke-width="3"/>
<path d="{arc_path(R_IN)}" transform="translate(0,0)" fill="none" stroke="#d04b31" stroke-width="3"/>
<path d="{arc_path(R_OUT)}" fill="none" stroke="#d04b31" stroke-width="3"/>
<line x1="180" y1="169" x2="128" y2="241" stroke="#d04b31" stroke-width="3"/>
<line x1="380" y1="169" x2="432" y2="241" stroke="#d04b31" stroke-width="3"/>
<circle cx="128" cy="305" r="12.8" fill="none" stroke="#444" stroke-width="2"/>
<circle cx="432" cy="305" r="12.8" fill="none" stroke="#444" stroke-width="2"/>
<line x1="280" y1="54" x2="280" y2="335" stroke="#777" stroke-dasharray="5,5"/>
<text x="495" y="130" font-size="17" font-family="sans-serif">Motor OD = 24 (ASSUMED A7)</text>
<text x="495" y="165" font-size="17" font-family="sans-serif">Strap ID = 25 (target)</text>
<text x="495" y="200" font-size="17" font-family="sans-serif">Strap OD = 31 (target)</text>
<text x="495" y="235" font-size="17" font-family="sans-serif">New base width = 44</text>
<text x="495" y="270" font-size="17" font-family="sans-serif">Bolt centres = +/-19</text>
<text x="495" y="305" font-size="17" font-family="sans-serif">Hole diameter = 3.2</text>
<text x="40" y="400" font-size="16" font-family="sans-serif">A7: hole-to-motor overlap = {old_overlap:.1f} mm (FAIL)</text>
<text x="40" y="432" font-size="16" font-family="sans-serif">A8: radial bolt-to-strap gap = {new_edge_gap:.1f} mm (2D PASS)</text>
<text x="40" y="470" font-size="14" font-family="sans-serif">A8 is a PROPOSED replacement of A7's 26 mm base, not a drop-in clamp.</text>
<text x="40" y="495" font-size="14" font-family="sans-serif">Feet/leg profiles schematic; no threads, ribs, actual motor mounting or tolerance stack modeled.</text>
<text x="40" y="525" font-size="14" font-family="sans-serif">Physical fit, strength, fastener access and 3D collision: NEEDS_PHYSICAL_CHECK / SKIPPED.</text>
</svg>"""
Path(__file__).with_name("px1_a8_motor_clamp_preview.svg").write_text(svg,encoding="utf-8")
print(f"PASS: A7 overlap={old_overlap:.2f} mm; A8 nominal bolt/strap gap={new_edge_gap:.2f} mm")
