#!/usr/bin/env python3
"""Parametric 2D projection of existing PX1 Current Master stations, NOT a CAD render.
Source: current/CAD/PX1_Current_Master.py as read 2026-11-22.
Only schematic envelopes; no assertion of gear-tooth mesh or physical fit.
"""
from pathlib import Path
import math
WHEEL_X=(50.,150.,250.)
GEAR_X=(50.,100.,150.,200.,250.)
BODY_X0=18.; BODY_L=278.; BODY_W=68.; BODY_Z0=11.; BODY_TOP=75.
WHEEL_Z=45.; WHEEL_D=90.; WHEEL_Y=54.5; WHEEL_AXIAL_HALF=12.
MOTOR_X=(91.6,189.5); MOTOR_Y=13.5; MOTOR_MAX_D=26.
assert len(WHEEL_X)*2==6 and len(GEAR_X)*2==10
assert 2*(WHEEL_Y+WHEEL_AXIAL_HALF)==133.
assert 2*MOTOR_Y>=MOTOR_MAX_D
S=3.
X=lambda x:80+x*S
Y=lambda y:220-y*S
p=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="720" viewBox="0 0 1100 720">',
'<rect width="1100" height="720" fill="white"/>',
'<style>text{font:16px sans-serif;fill:#193344}.h{font:bold 23px sans-serif}</style>',
'<text x="40" y="38" class="h">PX1 — current master / integrated 2D station projection</text>',
'<text x="40" y="67">SOURCE-RECONSTRUCTED + ESTIMATED; NOT a CAD render or manufacturing drawing</text>',
'<text x="40" y="100">TOP VIEW — body, wheel stations, Z50 pitch circles, motor envelopes</text>',
f'<rect x="{X(BODY_X0)}" y="{Y(BODY_W/2)}" width="{BODY_L*S}" height="{BODY_W*S}" fill="#e3eef8" stroke="#23628c" stroke-width="2"/>']
for sign in (-1,1):
 for x in WHEEL_X:
  y=sign*WHEEL_Y
  p.append(f'<rect x="{X(x)-WHEEL_D*S/2}" y="{Y(y+WHEEL_AXIAL_HALF)}" width="{WHEEL_D*S}" height="{2*WHEEL_AXIAL_HALF*S}" rx="8" fill="#3e5163" fill-opacity=".65" stroke="#243747"/>')
 for x in GEAR_X:
  p.append(f'<circle cx="{X(x)}" cy="{Y(sign*29)}" r="{25*S}" fill="none" stroke="#c47b21" stroke-width="2" stroke-dasharray="5 5"/>')
 y=sign*MOTOR_Y
 p.append(f'<rect x="{X(MOTOR_X[0])}" y="{Y(y+MOTOR_MAX_D/2)}" width="{(MOTOR_X[1]-MOTOR_X[0])*S}" height="{MOTOR_MAX_D*S}" rx="9" fill="#56a48d" fill-opacity=".5" stroke="#16715b" stroke-width="2"/>')
p.extend(['<text x="40" y="400">SIDE VIEW — Z and wheel diameter, schematic only</text>',
f'<rect x="{X(BODY_X0)}" y="{600-BODY_TOP*S}" width="{BODY_L*S}" height="{(BODY_TOP-BODY_Z0)*S}" fill="#e3eef8" stroke="#23628c" stroke-width="2"/>'])
for x in WHEEL_X:
 p.append(f'<circle cx="{X(x)}" cy="{600-WHEEL_Z*S}" r="{WHEEL_D*S/2}" fill="#3e5163" fill-opacity=".23" stroke="#243747" stroke-width="2"/>')
 p.append(f'<text x="{X(x)-16}" y="630">X{x:g}</text>')
p.extend(['<text x="40" y="660">PASS analytical: 6 wheels / 10 Z50 / 2 motors; width 133 mm. Assumed body X18..296.</text>',
'<text x="40" y="688">NOT_RUN: full 3D collisions, STEP, seal pressure, motor electrical compatibility.</text>','</svg>'])
out=Path(__file__).with_name('PX1_chassis_master_stations_2d.svg')
out.write_text('\n'.join(p),encoding='utf-8')
print(out)
