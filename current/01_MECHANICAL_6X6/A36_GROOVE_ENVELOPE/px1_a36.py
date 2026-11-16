"""PX1 A36 — preliminary shaft groove section, NOT DIN471-certified.
All dimensions assumed, mm. Run: python3 px1_a36.py
Outputs SVG and assertions; physical/catalog verification required.
"""
from pathlib import Path
D=12.0
groove_d=11.0 # ASSUMED, not DIN 471
groove_w=1.1 # ASSUMED, not DIN 471
left_x=-15.0
right_x=15.0
shaft_left=-21.0
shaft_right=21.0
bearing_inner_left=(-14.0,-6.0)
bearing_inner_right=(6.0,14.0)
gear=(-4.0,4.0)
spacer_left=(-6.0,-4.0)
spacer_right=(4.0,6.0)
def validate():
 assert groove_d<D and groove_w>0
 assert left_x+groove_w/2 < bearing_inner_left[0]
 assert right_x-groove_w/2 > bearing_inner_right[1]
 assert bearing_inner_left[1]==spacer_left[0] and spacer_left[1]==gear[0]
 assert gear[1]==spacer_right[0] and spacer_right[1]==bearing_inner_right[0]
 assert (D-groove_d)/2==0.5
 return "PASS preliminary geometric envelope; NEEDS_PHYSICAL_CHECK groove dimensions and retention"
def svg():
 scale=17
 X=lambda v: 470+v*scale
 Y=lambda d: 215-d*scale/2
 rect=lambda x0,x1,d,color: f'<rect x="{X(x0):.1f}" y="{Y(d):.1f}" width="{(x1-x0)*scale:.1f}" height="{d*scale:.1f}" fill="{color}" stroke="#203448" stroke-width="1.4"/>'
 s=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="455" viewBox="0 0 1000 455">','<rect width="1000" height="455" fill="#f7fafc"/>','<text x="32" y="43" font-family="sans-serif" font-size="23" font-weight="bold">PX1 A36 — X150 shaft / groove envelope</text>','<text x="32" y="70" font-family="sans-serif" font-size="14" fill="#9b2b2b">ASSUMED dimensions. Not a verified DIN 471 groove or manufacturing drawing.</text>']
 s.append(rect(shaft_left,shaft_right,D,'#8b9dad'))
 for x in [left_x,right_x]:
  s.append(rect(x-groove_w/2,x+groove_w/2,D,'#f7fafc'))
  s.append(rect(x-groove_w/2,x+groove_w/2,groove_d,'#8b9dad'))
 for a,b in [bearing_inner_left,bearing_inner_right]:s.append(rect(a,b,28,'#b5d7e9'))
 for a,b in [spacer_left,spacer_right]:s.append(rect(a,b,17,'#e9c57c'))
 s.append(rect(*gear,70,'#82c7a0'))
 s.append(f'<line x1="{X(-21)}" y1="215" x2="{X(21)}" y2="215" stroke="#c52e2e" stroke-dasharray="7 5"/>')
 for x,label in [(left_x,"groove L"),(right_x,"groove R")]:
  s.append(f'<line x1="{X(x)}" y1="315" x2="{X(x)}" y2="366" stroke="#1e344b"/><text x="{X(x)-43}" y="387" font-size="13" font-family="sans-serif">{label}</text>')
 s.append('<text x="32" y="413" font-size="14" font-family="sans-serif">Shaft Ø12; groove root Ø11; groove width 1.1; centres ±15 mm. Gear Z50 depicted as envelope only.</text>')
 s.append('<text x="32" y="438" font-size="13" font-family="sans-serif" fill="#a02b2b">Groove shoulder clearance to bearing = 0.45 mm (nominal). Ring shape, fit and load NOT validated.</text></svg>')
 return ''.join(s)
if __name__=="__main__":
 print(validate())
 Path(__file__).with_name("px1_a36_preview.svg").write_text(svg(),encoding="utf-8")
