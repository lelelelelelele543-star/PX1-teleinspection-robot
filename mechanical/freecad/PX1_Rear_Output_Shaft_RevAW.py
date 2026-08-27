import FreeCAD as App, Part
# PX-1 Rev.AW rear output shaft — drawing-candidate geometry
# IMPORTANT: M8 thread is represented by nominal cylinder in CAD; thread callout governs manufacture.

doc=App.newDocument('PX1_Rear_Output_Shaft_RevAW')

# Axial stations from inner end, mm
L_TOTAL=64.0
L_INNER=6.0
L_BEARING=8.0
L_SEAL=12.0
L_EXTERNAL=24.0
L_THREAD=14.0
D_SHAFT=10.0
D_THREAD=8.0

# Main Ø10 body to thread start
shape=Part.makeCylinder(D_SHAFT/2, L_TOTAL-L_THREAD)
# M8 nominal thread envelope
shape=shape.fuse(Part.makeCylinder(D_THREAD/2, L_THREAD, App.Vector(0,0,L_TOTAL-L_THREAD)))

shaft=doc.addObject('Part::Feature','Rear_Output_Shaft')
shaft.Shape=shape
shaft.addProperty('App::PropertyString','Material').Material='AISI 316L prototype; 40X13 alternate after corrosion/hardness review'
shaft.addProperty('App::PropertyLength','OverallLength').OverallLength=L_TOTAL
shaft.addProperty('App::PropertyString','BearingJournal').BearingJournal='Ø10 h6, L=8 mm; 6000-2RS'
shaft.addProperty('App::PropertyString','SealJournal').SealJournal='Ø10 h6; Ra 0.2–0.4 µm; no thread/keyway; polish circumferentially'
shaft.addProperty('App::PropertyString','ExternalDrive').ExternalDrive='Ø10; 3x3 keyway only outside seal journal'
shaft.addProperty('App::PropertyString','Thread').Thread='M8x1.25-6g, L=14 mm'
shaft.addProperty('App::PropertyString','EdgeBreak').EdgeBreak='0.2–0.5 x45° unless otherwise specified'
shaft.addProperty('App::PropertyString','Runout').Runout='seal journal to bearing journal <=0.02 mm TIR target'
shaft.addProperty('App::PropertyString','GeneralTolerance').GeneralTolerance='ISO 2768-mK candidate; critical fits override'
shaft.addProperty('App::PropertyString','Status').Status='DRAWING-CANDIDATE — prototype inspection required before RELEASE'

doc.recompute()
doc.saveAs('PX1_Rear_Output_Shaft_RevAW.FCStd')
