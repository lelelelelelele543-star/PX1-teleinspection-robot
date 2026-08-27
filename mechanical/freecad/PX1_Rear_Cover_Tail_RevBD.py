import FreeCAD as App, Part
# PX-1 Rev.BD rear pressure cover + LEMO/towing/strain-relief candidate
# LEMO body represented by manufacturer dimensional envelope; no proprietary internal geometry.

doc=App.newDocument('PX1_Rear_Cover_Tail_RevBD')

W=94.0; H=76.0; T=10.0
PILOT_W=82.0; PILOT_H=64.0; PILOT_D=3.0

# Cover plate
plate=Part.makeBox(T,W,H)
# Pilot step on body side
pilot=Part.makeBox(PILOT_D,PILOT_W,PILOT_H,App.Vector(0,(W-PILOT_W)/2,(H-PILOT_H)/2))
shape=plate.fuse(pilot)

# LEMO EGG.5K.870.CLL5 panel thread M45x1.5: model nominal Ø45 passage only.
# Position high/central to retain lower room for tow/strain relief.
conn_y=W/2
conn_z=50.0
hole=Part.makeCylinder(22.5,T+PILOT_D,App.Vector(0,conn_y,conn_z),App.Vector(1,0,0))
shape=shape.cut(hole)

# Eight M5 cover clearance holes around perimeter, outside intended sealing line.
for y,z in ((10,10),(W/2,10),(W-10,10),(10,H/2),(W-10,H/2),(10,H-10),(W/2,H-10),(W-10,H-10)):
    h=Part.makeCylinder(2.75,T,App.Vector(0,y,z),App.Vector(1,0,0))
    shape=shape.cut(h)

cover=doc.addObject('Part::Feature','Rear_Cover')
cover.Shape=shape
cover.addProperty('App::PropertyString','Material').Material='EN AW-6082 T6'
cover.addProperty('App::PropertyString','Connector').Connector='LEMO EGG.5K.870.CLL5; M45x1.5 panel thread; 55 mm outer A envelope'
cover.addProperty('App::PropertyString','ConnectorCutout').ConnectorCutout='Ø45 nominal model only; manufacture to LEMO M45x1.5 mounting requirements'
cover.addProperty('App::PropertyString','Fasteners').Fasteners='8x M5 candidate; final body thread engagement and O-ring line HOLD'
cover.addProperty('App::PropertyString','Status').Status='DRAWING-CANDIDATE — exact cover O-ring groove/tow proof load pending'

# LEMO external envelope: A=55, L=47.5 from manufacturer data
lemo=doc.addObject('Part::Feature','LEMO_EGG5K870_Envelope')
lemo.Shape=Part.makeCylinder(27.5,47.5,App.Vector(T,conn_y,conn_z),App.Vector(1,0,0))
lemo.addProperty('App::PropertyString','SourceDims').SourceDims='LEMO: A=55 mm, L=47.5 mm, panel thread M45x1.5'

# Mechanical tow clevis block: load path separate from connector
clevis=doc.addObject('Part::Feature','Tow_Clevis_Block')
block=Part.makeBox(18,30,18,App.Vector(T,32,6))
# transverse pin hole Ø8
pin_hole=Part.makeCylinder(4,30,App.Vector(T+9,32,15),App.Vector(0,1,0))
clevis.Shape=block.cut(pin_hole)
clevis.addProperty('App::PropertyString','Function').Function='Towing/lowering load path; never load LEMO shell/contact system'
clevis.addProperty('App::PropertyString','Pin').Pin='Ø8 prototype pin/shackle interface; proof load HOLD'

# Cable bending/strain-relief keepout behind straight plug
strain=doc.addObject('Part::Feature','Cable_StrainRelief_Keepout')
strain.Shape=Part.makeCylinder(24,120,App.Vector(T+47.5,conn_y,conn_z),App.Vector(1,0,0))
strain.addProperty('App::PropertyString','Requirement').Requirement='No rigid tow member may intersect connector release sleeve or first 120 mm cable bend zone'

doc.recompute()
doc.saveAs('PX1_Rear_Cover_Tail_RevBD.FCStd')
