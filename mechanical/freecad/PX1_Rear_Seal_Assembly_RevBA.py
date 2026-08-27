import FreeCAD as App, Part
# PX-1 Rev.BA rear shaft sealing assembly verification model
# Purchased components are dimensional envelopes, not vendor CAD.
doc=App.newDocument('PX1_Rear_Seal_Assembly_RevBA')

# Carrier: Rev.AZ nominal envelope
carrier=doc.addObject('Part::Feature','Carrier')
carrier.Shape=Part.makeCylinder(30,28).cut(Part.makeCylinder(6,28))

# Shaft: Rev.AW nominal Ø10 with M8 end envelope
shaft=doc.addObject('Part::Feature','Shaft')
shaft.Shape=Part.makeCylinder(5,50).fuse(Part.makeCylinder(4,14,App.Vector(0,0,50)))

# 6000-2RS envelope 10x26x8
bearing=doc.addObject('Part::Feature','Bearing_6000_2RS')
bearing.Shape=Part.makeCylinder(13,8,App.Vector(0,0,4)).cut(Part.makeCylinder(5,8,App.Vector(0,0,4)))
bearing.addProperty('App::PropertyString','Status').Status='PURCHASED PART ENVELOPE 10x26x8'

# Radial shaft seal envelope 10x22x7
seal=doc.addObject('Part::Feature','Seal_10x22x7_FKM')
seal.Shape=Part.makeCylinder(11,7,App.Vector(0,0,15)).cut(Part.makeCylinder(5,7,App.Vector(0,0,15)))
seal.addProperty('App::PropertyString','Status').Status='PURCHASED PART ENVELOPE 10x22x7 FKM'

# Static face O-ring 40x2 represented as torus-like envelope
oring=doc.addObject('Part::Feature','ORing_40x2_FKM')
oring.Shape=Part.makeTorus(20,1,App.Vector(0,0,1.5))
oring.addProperty('App::PropertyString','Status').Status='PURCHASED PART ENVELOPE 40x2 FKM'

rules=doc.addObject('App::FeaturePython','Verification')
rules.addProperty('App::PropertyString','DynamicSeal').DynamicSeal='Seal lip must run only on Ø10 h6 Ra 0.2–0.4 um land'
rules.addProperty('App::PropertyString','StaticSeal').StaticSeal='40x2 FKM face O-ring; groove Rev.AY/AZ'
rules.addProperty('App::PropertyString','Assembly').Assembly='Lubricate seals; protect lip from keyway/thread during insertion'
rules.addProperty('App::PropertyString','Release').Release='NO RELEASE until physical pressure/leak test passes'

doc.recompute()
doc.saveAs('PX1_Rear_Seal_Assembly_RevBA.FCStd')
