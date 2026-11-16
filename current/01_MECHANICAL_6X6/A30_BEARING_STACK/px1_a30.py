"""A30: axial bearing stack on X150; assumptions, not factory dimensions.
Run with Python 3 and cadquery. A29 is loaded as geometry source; it also executes its tests.
"""
from pathlib import Path
import runpy
import cadquery as cq
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
src=ROOT/"A29_Z50_MOTOR_BOOLEAN"/"px1_a29.py"
assert src.exists(), "A29 prerequisite absent"
a=runpy.run_path(str(src))
gear, shaft, motor=a["gear"],a["shaft"],a["motor"]
# ASSUMED candidate envelope, NOT a verified bearing SKU: 12x28x8 mm
def ring(z):
    return cq.Workplane("XY").workplane(offset=z).circle(14).circle(6).extrude(8).val()
front=ring(-8)
rear=ring(12)
for name,shape in [("front",front),("rear",rear)]:
    assert shape.isValid() and len(shape.Solids())==1
    assert shape.intersect(gear).Volume()<1e-6, name+" bearing collides with gear"
    assert shape.intersect(motor).Volume()<1e-6, name+" bearing collides with motor"
    assert shape.intersect(shaft).Volume()<1e-6, name+" bearing bore collides with shaft"
# Axial shoulders are NOT designed; bearing positioning is conceptual.
assert abs(front.BoundingBox().zmax-gear.BoundingBox().zmin)<1e-6
assert abs(rear.BoundingBox().zmin-gear.BoundingBox().zmax)<1e-6
assert shaft.BoundingBox().zmin <= front.BoundingBox().zmin
assert shaft.BoundingBox().zmax >= rear.BoundingBox().zmax
assembly=cq.Compound.makeCompound([gear,shaft,motor,front,rear])
cq.exporters.export(assembly,str(HERE/"px1_a30_bearing_stack.step"))
print("PASS: 2 ring solids; gear/bearing/motor/shaft clearance checks")
print("NEEDS_PHYSICAL_CHECK: bearing designation, fits, retaining shoulders, seal pressure")
