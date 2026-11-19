"""M1 lid pressure-boundary 2D packing regression; Python 3 stdlib only.
All sizes design assumptions, mm. This is NOT pressure qualification.
"""
from pathlib import Path
import ast
src=Path(__file__).with_name("PX1_Integrated_6x6_M1_interface_repair.py").read_text()
ast.parse(src)
expected=[
 "lid_bolts=[(x,y) for x in (-90.,0.,90.) for y in (-35.5,35.5)]",
 "gasket=Part.makeBox(176,66,1,V(-88,-33,35)).cut(Part.makeBox(170,60,1,V(-85,-30,35)))",
 "lid_opening=Part.makeBox(170,60,12,V(-85,-30,29))",
]
for item in expected:
    assert item in src, "FAIL: source geometry changed; review "+item
opening=(170,60); ring_inner=(170,60); ring_outer=(176,66)
bolt=(90,35.5); clearance_radius=1.7; head_radius=2.8
lid_half=(95,39)
assert ring_inner==opening, "FAIL gasket unsupported over aperture"
assert ring_outer[0]/2<=lid_half[0] and ring_outer[1]/2<=lid_half[1]
hole_to_ring_x=bolt[0]-clearance_radius-ring_outer[0]/2
hole_to_ring_y=bolt[1]-clearance_radius-ring_outer[1]/2
head_to_edge_x=lid_half[0]-bolt[0]-head_radius
head_to_edge_y=lid_half[1]-bolt[1]-head_radius
assert min(hole_to_ring_x,hole_to_ring_y,head_to_edge_x,head_to_edge_y)>=0
assert 8==len([(x,y) for x in (-90.,0.,90.) for y in (-35.5,35.5)]+[(-90.,0.),(90.,0.)])
print("PASS source AST and gasket support; ring 3 mm land on all 4 edges")
print("PASS nominal M3 hole-to-ring clearances X/Y:",hole_to_ring_x,hole_to_ring_y,"mm")
print("PASS screw head-to-lid-edge clearances X/Y:",head_to_edge_x,head_to_edge_y,"mm")
print("NOT_RUN FreeCAD solids, screw preload, lid deflection, extrusion and leakage")
print("PHYSICAL_CHECK 0.4-0.7 bar pressure boundary and gasket material")
