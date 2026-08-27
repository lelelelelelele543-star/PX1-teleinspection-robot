import FreeCAD as App, Part

# PX-1 Rev.ET — first machining-oriented three-zone pressure body.
# Prototype geometry only. Dimensions remain engineering candidates.

doc = App.newDocument('PX1_PressureBody_RevET')

# -------- datums --------
L = 307.0
W = 92.0
Z0 = 8.0
Z1 = 90.0
H = Z1 - Z0

P0_X0 = 8.0
P0_X1 = 299.0
P0_Y = 31.0
P0_Z0 = 14.0

SIDE_X0 = 16.0
SIDE_X1 = 291.0
SIDE_Y_IN = 35.0
SIDE_Y_OUT = W/2.0
SIDE_Z0 = 12.0
SIDE_Z1 = 78.0

TOP_OPEN_X0 = 130.0
TOP_OPEN_X1 = 292.0
TOP_OPEN_Y = 29.0

# front camera pocket region: external recess only, P0 remains closed below it
NOSE_X0 = 40.0
NOSE_X1 = 125.0
NOSE_Y = 29.0
NOSE_Z0 = 58.0

# Locally lower front P0 roof to preserve a closed pressure wall below the folded camera.
FRONT_P0_X0 = 8.0
FRONT_P0_X1 = 128.0
FRONT_P0_Z1 = 53.0

# -------- outer billet --------
outer = Part.makeBox(L, W, H, App.Vector(0, -W/2.0, Z0))

# -------- P0 cavity --------
# Front P0 pocket with lowered roof.
p0_front = Part.makeBox(FRONT_P0_X1-FRONT_P0_X0,
                        2*P0_Y,
                        FRONT_P0_Z1-P0_Z0,
                        App.Vector(FRONT_P0_X0, -P0_Y, P0_Z0))

# Rear P0 volume runs upward to the service opening.
p0_rear = Part.makeBox(P0_X1-128.0,
                       2*P0_Y,
                       Z1-P0_Z0+2.0,
                       App.Vector(128.0, -P0_Y, P0_Z0))

shape = outer.cut(p0_front.fuse(p0_rear))

# -------- side pressure bays P1/P2 --------
side_len = SIDE_X1-SIDE_X0
side_h = SIDE_Z1-SIDE_Z0
for sign in (1, -1):
    if sign > 0:
        y0 = SIDE_Y_IN
    else:
        y0 = -SIDE_Y_OUT
    bay = Part.makeBox(side_len,
                       SIDE_Y_OUT-SIDE_Y_IN,
                       side_h,
                       App.Vector(SIDE_X0, y0, SIDE_Z0))
    shape = shape.cut(bay)

# -------- top service opening --------
# Only rear/central service opening; front remains a closed lowered roof.
top_open = Part.makeBox(TOP_OPEN_X1-TOP_OPEN_X0,
                        2*TOP_OPEN_Y,
                        Z1-P0_Z0+4.0,
                        App.Vector(TOP_OPEN_X0, -TOP_OPEN_Y, P0_Z0))
shape = shape.cut(top_open)

# -------- folded-camera external nose recess --------
# This cuts external upper material but stops at Z=58, leaving the front P0 roof at Z≈53.
nose = Part.makeBox(NOSE_X1-NOSE_X0,
                    2*NOSE_Y,
                    Z1-NOSE_Z0+2.0,
                    App.Vector(NOSE_X0, -NOSE_Y, NOSE_Z0))
shape = shape.cut(nose)

body = doc.addObject('Part::Feature', 'PressureBody_ThreeZone')
body.Shape = shape
body.addProperty('App::PropertyString','Material').Material = 'EN AW-6082-T6 candidate'
body.addProperty('App::PropertyString','P0').P0 = 'central cavity; front lowered roof + rear top service opening'
body.addProperty('App::PropertyString','P1P2').P1P2 = 'side bays X16..291, |Y|35..46, Z12..78; covered from outer faces'
body.addProperty('App::PropertyString','Bulkhead').Bulkhead = 'P0/side-bay nominal web Y31..35 = 4 mm before local bosses'
body.addProperty('App::PropertyString','Status').Status = 'PROTOTYPE MACHINING CANDIDATE; no released tolerances'

# -------- reference top cover --------
top_cover = doc.addObject('Part::Feature','TopCover_Reference')
top_cover.Shape = Part.makeBox(TOP_OPEN_X1-TOP_OPEN_X0+12.0,
                               2*TOP_OPEN_Y+12.0,
                               5.0,
                               App.Vector(TOP_OPEN_X0-6.0,-TOP_OPEN_Y-6.0,Z1))
top_cover.addProperty('App::PropertyString','Seal').Seal = 'closed-loop FKM O-ring; exact groove after real path is frozen'

# -------- side cover references --------
for side, sign in [('L',1),('R',-1)]:
    y0 = W/2.0 if sign > 0 else -W/2.0-5.0
    cover = doc.addObject('Part::Feature',f'SideCover_{side}_Reference')
    cover.Shape = Part.makeBox(281.0,5.0,76.0,
                               App.Vector(13.0,y0,7.0))
    cover.addProperty('App::PropertyString','Pressure').Pressure = f'closes P{1 if side=="L" else 2}'

# -------- key datums / rules --------
rules = doc.addObject('App::FeaturePython','RevET_Rules')
rules.addProperty('App::PropertyString','InputStation').InputStation = 'traction bevel/output station X=200 mm per Rev.ES'
rules.addProperty('App::PropertyString','FrontRoof').FrontRoof = 'P0 cavity top ~Z53 at X8..128; external camera recess starts Z58'
rules.addProperty('App::PropertyString','Service').Service = 'rear/central top opening X130..292; motors/electronics removable from top'
rules.addProperty('App::PropertyString','Pressure').Pressure = 'P0/P1/P2 physically separated by metal bulkheads'
rules.addProperty('App::PropertyString','Release').Release = 'body solid must pass full interference + pressure analysis before machining release'

doc.recompute()
doc.saveAs('PX1_PressureBody_RevET.FCStd')
