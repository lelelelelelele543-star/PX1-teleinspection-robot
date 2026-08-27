import FreeCAD as App, Part
# PX-1 Rev.CD digital ROLL cartridge packaging
# 32x32 digital IP camera + Ø22 Ethernet slip ring.
# Exact vendor CAD/drawings still govern final release.
doc=App.newDocument('PX1_Digital_Roll_Cartridge_RevCD')

HEAD_OD=52.0
WALL=2.5
HEAD_ID=HEAD_OD-2*WALL  # 47 mm
CAM=32.0
CAM_THK=14.0           # packaging allowance until exact selected board drawing is frozen
SLIP_OD=22.0
SLIP_L=32.0            # provisional envelope; replace from exact supplier drawing

# Fixed head inner volume
inner=doc.addObject('Part::Feature','HeadInnerEnvelope')
inner.Shape=Part.makeCylinder(HEAD_ID/2,78)

# Rotating camera plate, centered and rotated 45° to maximize radial fit margin
cam=doc.addObject('Part::Feature','Camera32x32_Envelope')
cam.Shape=Part.makeBox(CAM,CAM,CAM_THK,App.Vector(-CAM/2,-CAM/2,4))
cam.Placement=App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),45))
cam.addProperty('App::PropertyString','FitCheck').FitCheck='32x32 board diagonal = 45.25 mm; head ID = 47 mm; ~0.87 mm radial corner margin before protruding components'

# Ethernet slip ring Ø22 on roll axis
slip=doc.addObject('Part::Feature','EthernetSlipRing_Envelope')
slip.Shape=Part.makeCylinder(SLIP_OD/2,SLIP_L,App.Vector(0,0,24))
slip.addProperty('App::PropertyString','Interface').Interface='100BASE-TX + separate power circuits candidate'
slip.addProperty('App::PropertyString','Status').Status='Exact length/lead exit HOLD until purchased SKU drawing is verified'

# Bearing concept revised for larger central component: use bearings outside slip-ring OD
# Candidate pair: 6805 (25x37x7) envelope only, final bearing selection not frozen.
for name,z in [('FrontBearingCandidate',20),('RearBearingCandidate',60)]:
    b=doc.addObject('Part::Feature',name)
    b.Shape=Part.makeCylinder(18.5,7,App.Vector(0,0,z)).cut(Part.makeCylinder(12.5,7,App.Vector(0,0,z)))
    b.addProperty('App::PropertyString','Status').Status='CANDIDATE 25x37x7 envelope; exact bearing selection HOLD'

# Roll gear moved outside camera PCB corner zone
gear=doc.addObject('Part::Feature','RollGearEnvelope')
gear.Shape=Part.makeCylinder(19.0,3,App.Vector(0,0,67)).cut(Part.makeCylinder(12.5,3,App.Vector(0,0,67)))
gear.addProperty('App::PropertyString','Note').Note='Tooth count/module to be re-optimized around revised bearing/slip-ring stack'

rules=doc.addObject('App::FeaturePython','RevCD_Rules')
rules.addProperty('App::PropertyString','Camera').Camera='32x32 digital H.265 IP board only; no analog video path'
rules.addProperty('App::PropertyString','RollData').RollData='100BASE-TX through Ethernet-rated slip ring'
rules.addProperty('App::PropertyString','LongLine').LongLine='10BASE-T1L conversion stays on fixed side after ROLL'
rules.addProperty('App::PropertyString','HeadOD').HeadOD='Ø52 mm remains target'
rules.addProperty('App::PropertyString','CriticalRisk').CriticalRisk='Camera PCB corner clearance is small; exact connector/component protrusions must be modeled'
rules.addProperty('App::PropertyString','Release').Release='NO RELEASE until exact camera + slip-ring drawings and bearing stack are frozen'

doc.recompute()
doc.saveAs('PX1_Digital_Roll_Cartridge_RevCD.FCStd')
