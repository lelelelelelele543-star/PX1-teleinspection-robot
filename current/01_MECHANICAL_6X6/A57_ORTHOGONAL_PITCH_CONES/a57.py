import math,pathlib,json
P=pathlib.Path(__file__).resolve().parent
m,z1,z2,f=1.5,16,40,8.
R=m*math.hypot(z1,z2)/2
a=math.atan2(z1,z2);b=math.pi/2-a
assert f<R/3 and abs(a+b-math.pi/2)<1e-12
assert abs(R*math.sin(a)-m*z1/2)<1e-10
assert abs(R*math.sin(b)-m*z2/2)<1e-10
def section(t,ang,axis,s):
 return (-t*math.cos(ang),s*t*math.sin(ang)) if axis=='input' else (s*t*math.sin(ang),t*math.cos(ang))
def line(v,w,c,thick=2):
 x,y=v;u,z=w
 return f'<line x1="{450+8*x:.2f}" y1="{310-8*y:.2f}" x2="{450+8*u:.2f}" y2="{310-8*z:.2f}" stroke="{c}" stroke-width="{thick}"/>'
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="620">','<rect width="920" height="620" fill="#101827"/>','<text x="30" y="42" fill="white" font-size="24">PX1 A57 — orthogonal bevel pitch cones</text>','<text x="30" y="70" fill="#aebdd0">ASSUMED: m1.5, Z16/Z40, face 8 mm; NOT tooth CAD</text>',line((-45,0),(15,0),'#8899aa'),line((0,-20),(0,39),'#8899aa')]
for axis,ang,c in [('input',a,'#e8a65c'),('output',b,'#55c5d5')]:
 for s in [-1,1]:
  svg.append(line((0,0),section(R-f,ang,axis,s),c))
  svg.append(line(section(R-f,ang,axis,s),section(R,ang,axis,s),c,7))
svg += ['<circle cx="450" cy="310" r="5" fill="white"/>','<text x="75" y="285" fill="#e8a65c">Z16 INPUT</text>','<text x="470" y="110" fill="#55c5d5">Z40 OUTPUT</text>',f'<text x="30" y="510" fill="white">R={R:.3f} mm; pitch angles {math.degrees(a):.3f} / {math.degrees(b):.3f} degrees</text>','<text x="30" y="545" fill="#aebdd0">No teeth, hubs, bearings, motors or housing represented. No contact validation.</text>','</svg>']
(P/'a57_preview.svg').write_text('\n'.join(svg))
(P/'results.json').write_text(json.dumps({'R_mm':R,'angles_deg':[math.degrees(a),math.degrees(b)],'status':'PASS_ANALYTIC_ONLY'},indent=2))
print('PASS: orthogonal pitch cones; SKIPPED: FreeCAD, contact')
