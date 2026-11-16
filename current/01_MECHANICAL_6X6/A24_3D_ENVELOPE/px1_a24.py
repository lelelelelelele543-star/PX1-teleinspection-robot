#!/usr/bin/env python3
"""A24: assumed 3D motor/shaft envelope intersection, dependency-free.
All coordinates mm. NOT a Proteus measurement or validated assembled geometry.
x: crawler longitudinal; y: lateral; z: vertical.
"""
from math import hypot
from pathlib import Path

# Design targets, not sourced part dimensions. Boxes are closed solids.
# Motor is axis-aligned along X, cylinder with radius 12.5 mm.
MOTOR = dict(x0=101.0, x1=135.0, y=0.0, z=0.0, r=12.5)
# X150 transverse shaft runs along Y. x=150 station.
SHAFT = dict(x=150.0, z=0.0, y0=-32.0, y1=32.0, r=6.0)
# Z50 assumed centered at X150, outer envelope radius 37.5 in XZ,
# but gear position along Y is NOT fixed; no false clearance claim.
GEAR = dict(x=150.0, z=0.0, r=37.5, y0=24.0, y1=30.0)
AXIAL_TOL = 1.0  # total combined adverse X uncertainty, assumed

def interval_gap(a0,a1,b0,b1):
    return max(b0-a1,a0-b1,0.0)

def motor_shaft_clearance():
    # Exact for perpendicular cylinders when motor X end is before shaft X start;
    # conservative separating-plane clearance is sufficient, not necessary.
    return SHAFT['x']-SHAFT['r']-MOTOR['x1']

def motor_gear_overlap():
    # Bounding-envelope intersection test only, not tooth-level collision.
    gx0,gx1=GEAR['x']-GEAR['r'],GEAR['x']+GEAR['r']
    gy0,gy1=GEAR['y0'],GEAR['y1']
    mx0,mx1=MOTOR['x0'],MOTOR['x1']
    my0,my1=MOTOR['y']-MOTOR['r'],MOTOR['y']+MOTOR['r']
    return interval_gap(mx0,mx1,gx0,gx1)==0 and interval_gap(my0,my1,gy0,gy1)==0

def svg():
    # XZ projection: motor capsule drawn as rectangle with actual assumed bounds.
    s=4.0; ox=85; oy=140
    def X(x):return ox+(x-90)*s
    def Z(z):return oy-z*s
    shaft_x=SHAFT['x']; shaft_r=SHAFT['r']
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 330">
<rect width="750" height="330" fill="#fff"/>
<text x="24" y="29" font-family="sans-serif" font-size="17" font-weight="bold">PX1 A24 | XZ envelope screening | assumed mm</text>
<text x="24" y="49" font-family="sans-serif" font-size="12">Projection only: Y separation is checked in code. NOT CAD/Proteus measurements.</text>
<line x1="35" y1="{oy}" x2="720" y2="{oy}" stroke="#888" stroke-dasharray="5 5"/>
<rect x="{X(MOTOR['x0'])}" y="{Z(MOTOR['r'])}" width="{(MOTOR['x1']-MOTOR['x0'])*s}" height="{2*MOTOR['r']*s}" rx="8" fill="#90c3df" stroke="#205477" stroke-width="2"/>
<circle cx="{X(shaft_x)}" cy="{oy}" r="{shaft_r*s}" fill="#e3b474" stroke="#9b5418" stroke-width="2"/>
<circle cx="{X(GEAR['x'])}" cy="{oy}" r="{GEAR['r']*s}" fill="none" stroke="#b76b99" stroke-dasharray="8 5" stroke-width="2"/>
<text x="{X(105)}" y="{Z(18)}" font-family="sans-serif" font-size="13">motor Ø25</text>
<text x="{X(150)+29}" y="{Z(-8)}" font-family="sans-serif" font-size="13">shaft Ø12</text>
<text x="{X(150)+65}" y="{Z(32)}" font-family="sans-serif" font-size="12">Z50 bounding circle</text>
<line x1="{X(135)}" y1="237" x2="{X(144)}" y2="237" stroke="#222" stroke-width="2"/>
<path d="M{X(135)} 231 v12 M{X(144)} 231 v12" stroke="#222"/>
<text x="{X(135)-4}" y="259" font-family="sans-serif" font-size="13">9.0 mm X-plane gap</text>
<text x="24" y="298" font-family="sans-serif" font-size="12">Shaft: X=150, R=6. Motor: X=101..135. Gear Y=24..30; motor Y=-12.5..12.5.</text>
<text x="24" y="317" font-family="sans-serif" font-size="12">Gear's XZ projected overlap is NOT a collision: Y intervals are separated by 11.5 mm.</text>
</svg>'''

def main():
    gap=motor_shaft_clearance()
    gear_y_gap=interval_gap(MOTOR['y']-MOTOR['r'],MOTOR['y']+MOTOR['r'],GEAR['y0'],GEAR['y1'])
    assert abs(gap-9.0)<1e-9
    assert gap-AXIAL_TOL>0
    assert abs(gear_y_gap-11.5)<1e-9
    assert not motor_gear_overlap()
    # regression: moving gear inward makes its bounding box overlap
    old=GEAR['y0'],GEAR['y1']
    GEAR['y0'],GEAR['y1']=10.0,16.0
    assert motor_gear_overlap()
    GEAR['y0'],GEAR['y1']=old
    Path(__file__).with_name('px1_a24_preview.svg').write_text(svg(),encoding='utf-8')
    print(f'PASS: shaft X separating plane gap {gap:.2f} mm; after assumed X tolerance {gap-AXIAL_TOL:.2f} mm')
    print(f'PASS: motor/gear Y bounding separation {gear_y_gap:.2f} mm; regression overlap detected')
    print('SKIPPED: FreeCAD, exact gear teeth, bearing, housing and assembled 3D geometry')
    print('NEEDS_PHYSICAL_CHECK: purchased component dimensions and fits')

if __name__=='__main__': main()
