import FreeCAD as App, Part

# PX-1 Rev.AM purchased-part envelopes for assembly and collision checks.
# These are simplified envelopes, NOT vendor-certified manufacturing CAD.

doc = App.newDocument('PX1_Purchased_Parts_RevAM')

# 6000-2RS bearing: 10x26x8 mm
b = doc.addObject('Part::Feature','Bearing_6000_2RS')
b.Shape = Part.makeCylinder(13.0,8.0).cut(Part.makeCylinder(5.0,8.0))
b.addProperty('App::PropertyString','Spec').Spec='6000-2RS 10x26x8 mm'
b.addProperty('App::PropertyString','Status').Status='PURCHASED PART ENVELOPE'

# Radial shaft seal: 10x22x7 mm
s = doc.addObject('Part::Feature','Seal_10x22x7')
s.Shape = Part.makeCylinder(11.0,7.0).cut(Part.makeCylinder(5.0,7.0))
s.addProperty('App::PropertyString','Spec').Spec='10x22x7 FKM/NBR'
s.addProperty('App::PropertyString','Status').Status='PURCHASED PART ENVELOPE'

# AS5600 magnet envelope: Ø6x2.5 mm
m = doc.addObject('Part::Feature','AS5600_Magnet')
m.Shape = Part.makeCylinder(3.0,2.5)
m.addProperty('App::PropertyString','Spec').Spec='diametrically magnetized Ø6x2.5 mm'

# JGB37-class motor maximum permitted envelope.
# Actual motor is measured on incoming inspection and adapter PX1-551 is drilled after receipt.
motor = doc.addObject('Part::Feature','Traction_Motor_Max_Envelope')
motor.Shape = Part.makeBox(95,42,42)
motor.addProperty('App::PropertyString','Status').Status='MAXIMUM ALLOWED ENVELOPE - NOT MOTOR CAD'
motor.addProperty('App::PropertyString','Requirement').Requirement='24V, 40-60 rpm, metal gearbox, rated torque >=1.25 N*m'

doc.recompute()
doc.saveAs('PX1_Purchased_Parts_Envelopes_RevAM.FCStd')
