import FreeCAD as App, Part
# PX-1 Rev.EA — detailed side-drive prototype geometry.
# Models one middle wheel station, one outer wheel station, axle flange,
# side cover, stepped middle shaft and gear/bevel envelopes.
# Gear teeth are catalog envelopes only; this is NOT a machining release.

doc = App.newDocument('PX1_DriveDetail_RevEA')

# ---------------- master dimensions (mm) ----------------
SIDE = 1
WHEEL_Z = 45.0
COVER_Y0 = 46.0
COVER_T = 5.0
COVER_X0 = 15.5
COVER_L = 276.0
COVER_Z0 = 5.0
COVER_H = 81.0
FLANGE_OD = 48.0
FLANGE_T = 6.0
FLANGE_PILOT_OD = 36.0
BEARING_OD = 21.0
BEARING_ID = 12.0
BEARING_W = 5.0
SEAL_OD = 22.0
SEAL_ID = 12.0
SEAL_W = 7.0
SHAFT_D = 12.0
BEVEL_SEAT_D = 10.0
GEAR_OD = 52.0
GEAR_FACE = 8.0
BEVEL_LARGE_OD = 68.18
BEVEL_LARGE_LEN = 21.10

# ---------------- side cover blank ----------------
cover = doc.addObject('Part::Feature', 'SideCover_Blank')
cover.Shape = Part.makeBox(COVER_L, COVER_T, COVER_H,
                           App.Vector(COVER_X0, COVER_Y0, COVER_Z0))
cover.addProperty('App::PropertyString','Material').Material = 'Al 6082-T6, t=5 prototype'
cover.addProperty('App::PropertyString','Seal').Seal = 'closed-loop FKM 2.5mm section; groove dimensions provisional'

# Axle-through openings and flange counterbores at X50/150/250.
for x in (50.0, 150.0, 250.0):
    through = Part.makeCylinder(15.0, COVER_T + 2.0,
                                App.Vector(x, COVER_Y0-1.0, WHEEL_Z), App.Vector(0,1,0))
    cover.Shape = cover.Shape.cut(through)

# ---------------- generic removable axle flange ----------------
def add_flange(name, x):
    flange = doc.addObject('Part::Feature', name)
    outer = Part.makeCylinder(FLANGE_OD/2.0, FLANGE_T,
                              App.Vector(x, COVER_Y0+COVER_T, WHEEL_Z), App.Vector(0,1,0))
    bore = Part.makeCylinder(SEAL_OD/2.0 + 0.2, FLANGE_T+2.0,
                             App.Vector(x, COVER_Y0+COVER_T-1.0, WHEEL_Z), App.Vector(0,1,0))
    flange.Shape = outer.cut(bore)
    flange.addProperty('App::PropertyString','Pilot').Pilot = 'Ø36 h7 candidate into parent feature'
    flange.addProperty('App::PropertyString','Fasteners').Fasteners = '3x M4 on PCD40; pilot locates, screws clamp'
    flange.addProperty('App::PropertyString','StaticSeal').StaticSeal = 'FKM 30x1.5 face O-ring candidate'
    return flange

flg_outer = add_flange('AxleFlange_OuterStation', 50.0)
flg_mid = add_flange('AxleFlange_MiddleStation', 150.0)

# ---------------- outer station shaft stack ----------------
# Simplified shaft: inner bearing/gear section -> outer bearing -> seal -> wheel end.
shaft_outer = doc.addObject('Part::Feature', 'OuterWheelShaft_Ø12')
shaft_outer.Shape = Part.makeCylinder(SHAFT_D/2.0, 50.0,
                                      App.Vector(50.0, 20.0, WHEEL_Z), App.Vector(0,1,0))
shaft_outer.addProperty('App::PropertyString','Journal').Journal = 'Ø12 h6 bearing; Ø12 polished seal land; no keyway under lip'
shaft_outer.addProperty('App::PropertyString','WheelEnd').WheelEnd = 'positive drive + M6 internal axial retainer'

gear_outer = doc.addObject('Part::Feature','OuterWheel_Z50_Envelope')
gear_outer.Shape = Part.makeCylinder(GEAR_OD/2.0, GEAR_FACE,
                                     App.Vector(50.0, 35.0, WHEEL_Z), App.Vector(0,1,0))
gear_outer.addProperty('App::PropertyString','Catalog').Catalog = 'KHK SSG1-50 class; m1 Z50 OD52 face8 bore12'

bearing_outer = doc.addObject('Part::Feature','OuterStation_61801_Envelope')
bearing_outer.Shape = Part.makeCylinder(BEARING_OD/2.0, BEARING_W,
                                         App.Vector(50.0, 51.0, WHEEL_Z), App.Vector(0,1,0))

seal_outer = doc.addObject('Part::Feature','OuterStation_FKM_12x22x7_Envelope')
seal_outer.Shape = Part.makeCylinder(SEAL_OD/2.0, SEAL_W,
                                      App.Vector(50.0, 56.0, WHEEL_Z), App.Vector(0,1,0))

# ---------------- stepped middle input shaft ----------------
# Inner Ø10 seat for the large bevel, shoulder into Ø12 side-drive section.
shaft_mid = doc.addObject('Part::Feature','MiddleInputSteppedShaft')
seg10 = Part.makeCylinder(BEVEL_SEAT_D/2.0, 24.0,
                          App.Vector(150.0, 8.0, WHEEL_Z), App.Vector(0,1,0))
seg12 = Part.makeCylinder(SHAFT_D/2.0, 50.0,
                          App.Vector(150.0, 32.0, WHEEL_Z), App.Vector(0,1,0))
shaft_mid.Shape = seg10.fuse(seg12)
shaft_mid.addProperty('App::PropertyString','Material').Material = '40Cr13 / 1.4034 preferred final; AISI316 fit prototype optional'
shaft_mid.addProperty('App::PropertyString','BevelSeat').BevelSeat = 'Ø10 h6 keyed seat, shoulder retained; no adhesive-only torque path'
shaft_mid.addProperty('App::PropertyString','SideSection').SideSection = 'Ø12 h6 bearing/gear section; polished seal land outboard'

bevel_large = doc.addObject('Part::Feature','KHK_SB1_5_4518H_LargeBevel_Envelope')
bevel_large.Shape = Part.makeCone(BEVEL_LARGE_OD/2.0, 18.0, BEVEL_LARGE_LEN,
                                  App.Vector(150.0, 10.0, WHEEL_Z), App.Vector(0,1,0))
bevel_large.addProperty('App::PropertyString','Catalog').Catalog = 'SB1.5-4518H class, Z45, m1.5, 2.5 ratio mate'
bevel_large.addProperty('App::PropertyString','TorquePath').TorquePath = 'Ø10 keyed seat; exact key machining gate after purchased gear inspection'

gear_mid = doc.addObject('Part::Feature','MiddleWheel_Z50_Envelope')
gear_mid.Shape = Part.makeCylinder(GEAR_OD/2.0, GEAR_FACE,
                                   App.Vector(150.0, 39.0, WHEEL_Z), App.Vector(0,1,0))
gear_mid.addProperty('App::PropertyString','Catalog').Catalog = 'KHK SSG1-50 class, positive drive to Ø12 shaft'

bearing_mid_out = doc.addObject('Part::Feature','MiddleOuter_61801_Envelope')
bearing_mid_out.Shape = Part.makeCylinder(BEARING_OD/2.0, BEARING_W,
                                           App.Vector(150.0, 51.0, WHEEL_Z), App.Vector(0,1,0))
seal_mid_out = doc.addObject('Part::Feature','MiddleOuter_FKM_12x22x7_Envelope')
seal_mid_out.Shape = Part.makeCylinder(SEAL_OD/2.0, SEAL_W,
                                        App.Vector(150.0, 56.0, WHEEL_Z), App.Vector(0,1,0))

# ---------------- basic design rules ----------------
rules = doc.addObject('App::FeaturePython','RevEA_Rules')
rules.addProperty('App::PropertyString','PressureZones').PressureZones = 'P0 central body / P1 side drive isolated by secondary middle-shaft boundary'
rules.addProperty('App::PropertyString','Flange').Flange = 'Ø48 removable; 3xM4 PCD40; local FKM static seal; 61801 + 12x22x7 primary seal'
rules.addProperty('App::PropertyString','MiddleShaft').MiddleShaft = 'stepped Ø10 bevel seat -> Ø12 wheel/gear shaft family'
rules.addProperty('App::PropertyString','Release').Release = 'DETAIL MASTER ONLY; verify purchased gears/bearings/seals before machining drawings'

doc.recompute()
doc.saveAs('PX1_DriveDetail_RevEA.FCStd')
