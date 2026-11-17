#!/usr/bin/env python3
"""PX1 A41: simply-supported X150 gear load, design assumptions ONLY."""
import math
from pathlib import Path
T_NM=10.0; MODULE_MM=1.5; Z=50; PRESSURE_ANGLE_DEG=20.0
SPAN_MM=24.0; LOAD_X_MM=12.0
assert 0 < LOAD_X_MM < SPAN_MM
pitch_radius_m=MODULE_MM*Z/2000
ft=T_NM/pitch_radius_m
fr=ft*math.tan(math.radians(PRESSURE_ANGLE_DEG))
ra_t=ft*(SPAN_MM-LOAD_X_MM)/SPAN_MM
rb_t=ft*LOAD_X_MM/SPAN_MM
ra_r=fr*(SPAN_MM-LOAD_X_MM)/SPAN_MM
rb_r=fr*LOAD_X_MM/SPAN_MM
reaction_a=math.hypot(ra_t,ra_r); reaction_b=math.hypot(rb_t,rb_r)
m_t=ra_t*LOAD_X_MM/1000; m_r=ra_r*LOAD_X_MM/1000
m_equiv=math.hypot(m_t,m_r)
assert abs(ra_t+rb_t-ft)<1e-9
assert abs(ra_r+rb_r-fr)<1e-9
assert abs(ra_t*SPAN_MM-ft*(SPAN_MM-LOAD_X_MM))<1e-8
assert abs(rb_t*SPAN_MM-ft*LOAD_X_MM)<1e-8
assert abs(reaction_a-reaction_b)<1e-9
print(f"PASS Ft={ft:.3f}N Fr={fr:.3f}N RA=RB={reaction_a:.3f}N Mmax={m_equiv:.4f}Nm")
# SVG geometry derives from the same engineering parameters.
scale=17; left=130; y=175
xa=left; xb=left+SPAN_MM*scale; xp=left+LOAD_X_MM*scale
svg=f"""<svg xmlns="http://www.w3.org/2000/svg" width="850" height="440" viewBox="0 0 850 440">
<rect width="850" height="440" fill="white"/>
<text x="36" y="42" font-family="Arial" font-size="24">PX1 A41 — X150 gear radial reactions</text>
<text x="36" y="70" font-family="Arial" font-size="14">ASSUMED design model: simple supports, central Z50, no axial/helical load</text>
<line x1="{xa}" y1="{y}" x2="{xb}" y2="{y}" stroke="#243746" stroke-width="13"/>
<circle cx="{xp}" cy="{y}" r="35" fill="none" stroke="#4477aa" stroke-width="5"/>
<path d="M{xa-22} {y+27} L{xa+22} {y+27} L{xa} {y+3} Z M{xb-22} {y+27} L{xb+22} {y+27} L{xb} {y+3} Z" fill="#aac3d7" stroke="#243746"/>
<path d="M{xp} {y-105} V{y-45}" stroke="#c04c37" stroke-width="4"/>
<path d="M{xp-9} {y-55} L{xp} {y-43} L{xp+9} {y-55}" fill="none" stroke="#c04c37" stroke-width="4"/>
<text x="{xp+18}" y="{y-90}" font-family="Arial" font-size="15">Ft={ft:.1f} N; Fr={fr:.1f} N (orthogonal)</text>
<path d="M{xa} {y+100} V{y+35} M{xb} {y+100} V{y+35}" stroke="#16805d" stroke-width="4"/>
<text x="{xa-75}" y="{y+125}" font-family="Arial" font-size="15">RA={reaction_a:.1f} N</text>
<text x="{xb-10}" y="{y+125}" font-family="Arial" font-size="15">RB={reaction_b:.1f} N</text>
<path d="M{xa} 335 V355 H{xb} V335" stroke="#333" fill="none"/>
<text x="{xp-85}" y="378" font-family="Arial" font-size="16">bearing span {SPAN_MM:.0f} mm</text>
<text x="36" y="415" font-family="Arial" font-size="14">T={T_NM:.1f} Nm; m={MODULE_MM:.1f}; Z={Z}; alpha={PRESSURE_ANGLE_DEG:.0f} deg; Mmax={m_equiv:.3f} Nm</text>
</svg>"""
Path(__file__).with_name("a41_preview.svg").write_text(svg,encoding="utf-8")
