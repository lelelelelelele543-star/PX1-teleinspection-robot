import FreeCAD as App, Part
# PX-1 Rev.AQ removable side drivetrain cover
# Flat 3 mm prototype cover with M4 perimeter screws and tool clearance.
doc=App.newDocument('PX1_Side_Cover_RevAQ')
L=214.0
H=66.0
T=3.0
R=5.0
cover=doc.addObject('Part::Feature','Side_Drivetrain_Cover')
shape=Part.makeBox(L,T,H)
# wheel/shaft service openings at x=25 and 185 in local coordinates
for x in (25.0,185.0):
    opening=Part.makeCylinder(18.0,T,App.Vector(x,0,33.0),App.Vector(0,1,0))
    shape=shape.cut(opening)
# six M4 clearance holes; locations kept away from gear-center line
for x,z in ((10,8),(107,8),(204,8),(10,58),(107,58),(204,58)):
    hole=Part.makeCylinder(2.25,T,App.Vector(x,0,z),App.Vector(0,1,0))
    shape=shape.cut(hole)
cover.Shape=shape
cover.addProperty('App::PropertyString','Material').Material='Al 2-3 mm or impact-resistant polymer prototype'
cover.addProperty('App::PropertyString','Fasteners').Fasteners='6x M4 captive-preferred'
cover.addProperty('App::PropertyString','Removal').Removal='Remove without wheel removal target'
cover.addProperty('App::PropertyString','Status').Status='PROTOTYPE - collision/tool-access verification required'
doc.recompute()
doc.saveAs('PX1_Side_Cover_RevAQ.FCStd')
