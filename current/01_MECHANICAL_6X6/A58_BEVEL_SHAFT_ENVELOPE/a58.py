#!/usr/bin/env python3
"""A58: orthogonal shaft-end envelope study. Coordinates are assumed, mm.
Only pitch cones/shaft cross-sections; no gear tooth contact claim."""
import math, json, pathlib
O=pathlib.Path(__file__).resolve().parent
m,z1,z2,face=1.5,16,40,8.0
R=m*math.hypot(z1,z2)/2
a=math.atan2(z1,z2); b=math.pi/2-a
# Local axes intersect at the theoretical cone apex (0,0), NOT at shaft ends.
# Input shaft ends at x=-10, output shaft starts at y=+10.
shaft_radius=4.0
input_end=-10.0
output_start=10.0
# For perpendicular semi-infinite shaft cylinders, minimum clearance between
# their axial segments occurs at the closest endpoints (-10,0) and (0,10).
axis_gap=math.hypot(-input_end,output_start)
surface_clearance=axis_gap-2*shaft_radius
assert surface_clearance>0
assert abs(R*math.sin(a)-12)<1e-10
assert abs(R*math.sin(b)-30)<1e-10
assert abs(a+b-math.pi/2)<1e-12
# 2D shaft rectangles in axial section (not full 3D collision check).
def xy(x,y): return (460+7*x,365-7*y)
def line(x1,y1,x2,y2,color,width=2,dash=''):
 X,Y=xy(x1,y1);U,V=xy(x2,y2)
 return f'<line x1="{X:.2f}" y1="{Y:.2f}" x2="{U:.2f}" y2="{V:.2f}" stroke="{color}" stroke-width="{width}" {dash}/>'
def rect(x1,y1,x2,y2,color,opacity):
 X,Y=xy(x1,y2);W=7*(x2-x1);H=7*(y2-y1)
 return f'<rect x="{X:.2f}" y="{Y:.2f}" width="{W:.2f}" height="{H:.2f}" fill="{color}" fill-opacity="{opacity}" stroke="{color}"/>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="680" viewBox="0 0 1000 680">',
'<rect width="1000" height="680" fill="#101827"/>',
'<text x="28" y="40" fill="white" font-size="24">PX1 A58 — bevel shaft-end section (ASSUMED)</text>',
'<text x="28" y="68" fill="#b8c7d9" font-size="16">Orthogonal shafts Ø8; Z16/Z40 pitch cones only; NOT teeth / 3D collision test</text>',
line(-70,0,18,0,'#75869c',1,'stroke-dasharray="6 5"'),line(0,-20,0,58,'#75869c',1,'stroke-dasharray="6 5"'),
rect(-48,-4,input_end,4,'#e8a65c',0.36),rect(-4,output_start,4,48,'#55c5d5',0.36)]
for t in (R-face,R):
 # shared pitch generator in quadrant upper-left
 x=-t*math.cos(a); y=t*math.sin(a)
 s.append(line(0,0,x,y,'#e8a65c',3))
 s.append(line(0,0,-t*math.sin(b),t*math.cos(b),'#55c5d5',1))
# face segment along pitch generator
s.append(line(-R*math.cos(a),R*math.sin(a),-(R-face)*math.cos(a),(R-face)*math.sin(a),'#ffda79',8))
s += ['<circle cx="460" cy="365" r="4" fill="white"/>',
'<text x="35" y="330" fill="#e8a65c" font-size="18">Input shaft Ø8; ends 10 mm before apex</text>',
'<text x="510" y="145" fill="#55c5d5" font-size="18">Output shaft Ø8; starts 10 mm after apex</text>',
f'<text x="28" y="570" fill="white" font-size="18">Axis endpoint separation = {axis_gap:.3f} mm; conservative end-sphere clearance = {surface_clearance:.3f} mm</text>',
'<text x="28" y="600" fill="#b8c7d9" font-size="16">Shaft-end clearance is a conservative proxy, not a bearing/hub/gear collision result.</text>',
'<text x="28" y="626" fill="#b8c7d9" font-size="16">Gear tooth surfaces, hubs, bearings and actual mount positions are NOT modeled.</text>','</svg>']
(O/'a58_preview.svg').write_text('\n'.join(s),encoding='utf-8')
(O/'results.json').write_text(json.dumps({'assumed':{'shaft_diameter_mm':8,'input_end_x_mm':input_end,'output_start_y_mm':output_start,'face_width_mm':face},'derived':{'pitch_cone_distance_mm':R,'axis_endpoint_distance_mm':axis_gap,'conservative_clearance_mm':surface_clearance},'tests':{'analytic':'PASS','freecad':'SKIPPED','physical':'NEEDS_PHYSICAL_CHECK'}},indent=2),encoding='utf-8')
print('PASS analytic; conservative clearance',round(surface_clearance,3),'mm')
