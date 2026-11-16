"""A25: actual CadQuery solid Boolean test, all dimensions assumed in mm.
X longitudinal, Y lateral, Z vertical. Z50 is cylindrical envelope, not teeth.
"""
import cadquery as cq
from pathlib import Path
O=Path(__file__).resolve().parent
motor=cq.Solid.makeCylinder(12.5,34,cq.Vector(101,0,0),cq.Vector(1,0,0))
shaft=cq.Solid.makeCylinder(6,64,cq.Vector(150,-32,0),cq.Vector(0,1,0))
gear=cq.Solid.makeCylinder(37.5,6,cq.Vector(150,24,0),cq.Vector(0,1,0))
def vol(a,b): return a.intersect(b).Volume()
assert all(x.isValid() for x in (motor,shaft,gear))
assert vol(motor,shaft)<1e-7 and vol(motor,gear)<1e-7
assert vol(shaft,gear)>0 # intentional gear-to-shaft mating volume
assert vol(motor.translate((0,26,0)),gear)>1 # negative regression
cq.exporters.export(cq.Compound.makeCompound([motor,shaft,gear]),str(O/'px1_a25_envelopes.step'))
# Preview is deterministic from the same geometry's solid bounding boxes.
bm,bg=motor.BoundingBox(),gear.BoundingBox()
s=3; X=lambda x:85+(x-90)*s; Z=lambda z:170-z*s
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 480">
<rect width="820" height="480" fill="white"/>
<g font-family="sans-serif" fill="#172b42"><text x="25" y="30" font-size="20" font-weight="bold">PX1 A25 — CAD solid envelope, XZ / Y intervals</text>
<text x="25" y="52" font-size="13">CadQuery solid bounds; assumed mm. Z50 shown as a cylinder, NOT teeth.</text></g>
<line x1="35" y1="170" x2="790" y2="170" stroke="#888" stroke-dasharray="6 5"/>
<rect x="{X(bm.xmin)}" y="{Z(bm.zmax)}" width="{(bm.xmax-bm.xmin)*s}" height="{(bm.zmax-bm.zmin)*s}" fill="#91c5de" stroke="#245778" stroke-width="2"/>
<circle cx="{X(150)}" cy="170" r="18" fill="#f0c68a" stroke="#945a20" stroke-width="2"/>
<circle cx="{X(150)}" cy="170" r="112.5" fill="none" stroke="#a54686" stroke-width="2" stroke-dasharray="8 5"/>
<g font-family="sans-serif" font-size="14" fill="#172b42"><text x="124" y="113">Motor Ø25</text><text x="290" y="175">Shaft Ø12</text><text x="310" y="77">Z50 envelope Ø75</text><text x="25" y="330">Y intervals (mm):</text></g>
<line x1="120" y1="375" x2="700" y2="375" stroke="#777"/>
<rect x="{120+(bm.ymin+40)*6}" y="350" width="{(bm.ymax-bm.ymin)*6}" height="22" fill="#91c5de" stroke="#245778"/>
<rect x="{120+(bg.ymin+40)*6}" y="390" width="{(bg.ymax-bg.ymin)*6}" height="22" fill="#e4b3d1" stroke="#a54686"/>
<g font-family="sans-serif" font-size="13"><text x="25" y="367">Motor</text><text x="25" y="406">Gear</text><text x="25" y="449">Motor–gear Y gap: 11.5 mm. Motor–shaft X separating gap: 9.0 mm.</text><text x="25" y="469">CAD boolean: motor/shaft = 0; motor/gear = 0; gear/shaft overlap intentional.</text></g></svg>'''
(O/'px1_a25_preview.svg').write_text(svg,encoding='utf8')
print('PASS: valid solids, motor/shaft=0, motor/gear=0, negative regression detected')
print('SKIPPED: true gear teeth, bearings, housing, full assembly and physical verification')
