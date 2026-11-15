"""PX1 A18: independent analytic check of A17 assumed cylindrical relief."""
import math
R=13.0; axis_y=13.5; plate_inner=22.5; plate_outer=28.5; cut_length=32.0
web=plate_outer-axis_y-R
half_height=math.sqrt(R**2-(plate_inner-axis_y)**2)
area=2*((axis_y-plate_inner)*half_height+0.5*(half_height*math.sqrt(R**2-half_height**2)+R**2*math.asin(half_height/R)))
volume=area*cut_length
assert abs(web-2.0)<1e-10
assert abs(half_height-9.3808315196)<1e-8
assert abs(volume-1657.7859)<0.01
print("PASS nominal web",web,"mm; cut half-height",half_height,"mm; volume",volume,"mm3/plate")
print("SKIPPED FreeCAD; NEEDS_PHYSICAL_CHECK material strength, tolerances, true motor size")
