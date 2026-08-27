import FreeCAD as App, Part
# PX-1 Rev.BN TILT worm shaft/support packaging
# Worm pair dimensions follow selected compact m=0.5 / 20:1 class; exact purchased set governs manufacture.
doc=App.newDocument('PX1_Tilt_Worm_Support_RevBN')

SHAFT_D=3.0
SHAFT_L=34.0
WORM_OD=10.0
WORM_L=18.0
BEARING_ID=3.0
BEARING_OD=8.0
BEARING_W=4.0
COUPLING_OD=8.0
COUPLING_L=10.0

shaft=doc.addObject('Part::Feature','Worm_Shaft')
shaft.Shape=Part.makeCylinder(SHAFT_D/2,SHAFT_L)
shaft.addProperty('App::PropertyString','Material').Material='AISI 303/304 prototype, ground/polished journal preferred'
shaft.addProperty('App::PropertyString','Fit').Fit='Ø3 h6 candidate at bearings and worm'

worm=doc.addObject('Part::Feature','Worm_Envelope')
worm.Shape=Part.makeCylinder(WORM_OD/2,WORM_L,App.Vector(0,0,8))
worm.addProperty('App::PropertyString','Status').Status='PURCHASED MATCHED-SET ENVELOPE, m=0.5, 1-start, 20:1 target'

for i,z in enumerate((2.0,28.0),1):
    b=doc.addObject('Part::Feature',f'Bearing_3x8x4_{i}')
    b.Shape=Part.makeCylinder(BEARING_OD/2,BEARING_W,App.Vector(0,0,z)).cut(Part.makeCylinder(BEARING_ID/2,BEARING_W,App.Vector(0,0,z)))
    b.addProperty('App::PropertyString','Status').Status='3x8x4 bearing envelope; exact SKU HOLD'

coupling=doc.addObject('Part::Feature','Motor_Coupling')
coupling.Shape=Part.makeCylinder(COUPLING_OD/2,COUPLING_L,App.Vector(0,0,-COUPLING_L))
coupling.addProperty('App::PropertyString','Function').Function='N20 output to independent Ø3 worm shaft'
coupling.addProperty('App::PropertyString','Status').Status='Envelope only; bore sizes depend on exact N20 shaft'

rules=doc.addObject('App::FeaturePython','DesignRules')
rules.addProperty('App::PropertyString','Support').Support='Two bearings straddling worm load where possible; avoid cantilevered worm'
rules.addProperty('App::PropertyString','AxialRetention').AxialRetention='Use shaft shoulders + thin shims/circlips; avoid preloading miniature bearings'
rules.addProperty('App::PropertyString','Backdrive').Backdrive='Self-locking NOT assumed until physical test'
rules.addProperty('App::PropertyString','Release').Release='NO RELEASE until exact worm set, bearings and N20 shaft dimensions are verified'

doc.recompute()
doc.saveAs('PX1_Tilt_Worm_Support_RevBN.FCStd')
