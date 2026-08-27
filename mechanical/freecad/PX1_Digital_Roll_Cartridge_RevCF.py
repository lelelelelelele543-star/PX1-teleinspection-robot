import FreeCAD as App, Part
# PX-1 Rev.CF compact digital ROLL cartridge
# Target architecture: 32x32 IP camera + Ø6.5 miniature Ethernet slip ring + 2x6803 bearings.
# Purchased component bodies are keep-out envelopes until exact vendor drawings are frozen.
doc=App.newDocument('PX1_Digital_Roll_Cartridge_RevCF')

HEAD_OD=52.0
HEAD_WALL=2.5
HEAD_ID=HEAD_OD-2*HEAD_WALL
HEAD_L=72.0

# Fixed head shell inner envelope
inner=doc.addObject('Part::Feature','FixedHeadInnerEnvelope')
inner.Shape=Part.makeCylinder(HEAD_ID/2,HEAD_L)
inner.addProperty('App::PropertyString','Rule').Rule='All rotating parts and wiring must remain inside Ø47 mm nominal'

# 32x32 mm camera board envelope, centered and rotated 45° for worst-corner review
cam=doc.addObject('Part::Feature','CameraBoard_32x32')
cam.Shape=Part.makeBox(32,32,8,App.Vector(-16,-16,5))
cam.addProperty('App::PropertyString','Status').Status='Height/connectors HOLD until exact camera drawing'
cam.addProperty('App::PropertyString','RadialMargin').RadialMargin='Board diagonal 45.25 mm vs head ID 47 mm => ~0.87 mm radial corner margin nominal'

# Front 6803 support
for name,z in [('Front6803',27.0),('Rear6803',47.0)]:
    b=doc.addObject('Part::Feature',name)
    b.Shape=Part.makeCylinder(13,5,App.Vector(0,0,z)).cut(Part.makeCylinder(8.5,5,App.Vector(0,0,z)))
    b.addProperty('App::PropertyString','Envelope').Envelope='6803-2RS 17x26x5'

# Mini Ethernet slip ring keepout Ø6.5. Length remains HOLD pending exact drawing.
sr=doc.addObject('Part::Feature','MiniEthernetSlipRing')
sr.Shape=Part.makeCylinder(3.25,18,App.Vector(0,0,34))
sr.addProperty('App::PropertyString','Candidate').Candidate='JINPAT LPMS-12-0701-01E2 class'
sr.addProperty('App::PropertyString','Diameter').Diameter='Ø6.5 mm reported candidate'
sr.addProperty('App::PropertyString','Length').Length='18 mm temporary keep-out; replace with exact vendor dimension before release'

# Roll gear z51 envelope, m0.5
gear=doc.addObject('Part::Feature','RollGear_z51')
gear.Shape=Part.makeCylinder(13.25,3,App.Vector(0,0,54)).cut(Part.makeCylinder(8.5,3,App.Vector(0,0,54)))

# Camera lens/window reserve
lens=doc.addObject('Part::Feature','LensWindowReserve')
lens.Shape=Part.makeCylinder(10,10,App.Vector(0,0,0))

# Rear connector/service reserve
rear=doc.addObject('Part::Feature','RearServiceReserve')
rear.Shape=Part.makeCylinder(12,8,App.Vector(0,0,64))

rules=doc.addObject('App::FeaturePython','RevCF_Rules')
rules.addProperty('App::PropertyString','OD').OD='Head OD <=52 mm'
rules.addProperty('App::PropertyString','LengthTarget').LengthTarget='72 mm restored as target only; exact camera/slip-ring drawings may change it'
rules.addProperty('App::PropertyString','Bearings').Bearings='2x 6803-2RS retained'
rules.addProperty('App::PropertyString','Data').Data='100BASE-TX across ROLL; 10BASE-T1L only after fixed-side conversion'
rules.addProperty('App::PropertyString','Power').Power='Use dedicated slip-ring power circuits; LED ring stays fixed-side'
rules.addProperty('App::PropertyString','Release').Release='NO RELEASE until exact slip-ring length, camera height/connectors and thermal test are verified'

doc.recompute()
doc.saveAs('PX1_Digital_Roll_Cartridge_RevCF.FCStd')
