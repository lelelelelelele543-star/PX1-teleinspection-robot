import FreeCAD as App
import Part

# Run PX1_Master_Parameters.py first in the same FreeCAD document.
doc = App.ActiveDocument
if doc is None:
    raise RuntimeError('Open/create a FreeCAD document and run PX1_Master_Parameters.py first')
p = doc.getObject('PX1_Parameters')
if p is None:
    raise RuntimeError('PX1_Parameters object not found')

L=float(p.BodyLength.Value); W=float(p.BodyWidth.Value); H=float(p.BodyHeight.Value)
ws=float(p.WallSide.Value); wf=float(p.WallFrontRear.Value); wh=float(p.WallFloorRoof.Value)
rear_x=float(p.RearAxleX.Value); axle_z=float(p.AxleZ.Value)
carrier_bore=float(p.RearCarrierBore.Value)

# Main shell envelope
outer = Part.makeBox(L,W,H)
inner = Part.makeBox(L-2*wf, W-2*ws, H-2*wh, App.Vector(wf,ws,wh))
shape = outer.cut(inner)

# Only two rotating body penetrations: rear left and rear right
axis = App.Vector(0,1,0)
for y in (-1.0, W+1.0):
    cyl = Part.makeCylinder(carrier_bore/2, 12.0, App.Vector(rear_x,y,axle_z), axis if y < 0 else App.Vector(0,-1,0))
    shape = shape.cut(cyl)

# Rear connector pilot: kept as a nominal interface only.
# Final manufacturing thread geometry follows the controlled LEMO drawing.
tail_r = float(p.TailThreadMajor.Value)/2.0
rear_center = App.Vector(L-14.0,W/2.0,H/2.0)
tail = Part.makeCylinder(tail_r, 20.0, rear_center, App.Vector(1,0,0))
shape = shape.cut(tail)

obj = doc.getObject('PX1_Body_Master') or doc.addObject('PartDesign::Feature','PX1_Body_Master')
obj.Label='PX-1 Main Sealed Body - Master'
obj.Shape=shape
obj.addProperty('App::PropertyString','Revision','Control') if not hasattr(obj,'Revision') else None
obj.Revision='Rev.AK'
obj.addProperty('App::PropertyString','Status','Control') if not hasattr(obj,'Status') else None
obj.Status='PROTOTYPE CAD - CHECK PURCHASED INTERFACES BEFORE MACHINING'

# Reference axle center objects
for name,x in [('FrontAxleRef',float(p.FrontAxleX.Value)),('RearAxleRef',rear_x)]:
    ref=doc.getObject(name) or doc.addObject('PartDesign::Feature',name)
    ref.Label=name
    ref.Shape=Part.makeCylinder(1.0,W+20,App.Vector(x,-10,axle_z),App.Vector(0,1,0))
    ref.ViewObject.LineColor=(0.8,0.2,0.2)
    ref.ViewObject.ShapeColor=(0.8,0.2,0.2)

obj.ViewObject.ShapeColor=(0.72,0.74,0.76)
doc.recompute()
