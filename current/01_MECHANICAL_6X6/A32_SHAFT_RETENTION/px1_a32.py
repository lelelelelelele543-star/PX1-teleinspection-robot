"""PX1 A32: axial retention and bearing/gear stack; assumed design dimensions.
Run python3 px1_a32.py; creates preview.svg; stdlib only.
Coordinate x = axial millimeters; 12 mm shaft, 8 mm wide gear.
This is a dimensional schematic, NOT a validated CAD solid.
"""
from pathlib import Path
import csv
P=Path(__file__).resolve().parent
shaft=(-15,23)
gear=(0,8)
bearings=[(-10,-2),(10,18)]
spacers=[(-2,0),(8,10)]
# Circlip grooves and outer retaining elements, preliminary dimensions
clips=[(-11.0,-10.0),(18.0,19.0)]
# Two 0.5 mm spacers are NOT enough to bridge A31's 1 mm bearing/gear gaps.
# A32 closes the axial stack with 2 mm spacers and adds end clips.
def width(a):return a[1]-a[0]
def check():
    assert width(gear)==8
    assert all(width(a)==8 for a in bearings)
    assert all(width(a)==2 for a in spacers)
    assert bearings[0][1]==spacers[0][0]
    assert spacers[0][1]==gear[0]
    assert gear[1]==spacers[1][0]
    assert spacers[1][1]==bearings[1][0]
    assert clips[0][1]==bearings[0][0]
    assert clips[1][0]==bearings[1][1]
    assert shaft[0]<clips[0][0] and shaft[1]>clips[1][1]
    # Stack total from first clip's right face to last clip's left face:
    assert bearings[1][1]-bearings[0][0]==28
    return True
def render():
    scale=18
    X=lambda x: 90+(x+15)*scale
    rects=[]
    def rect(span,top,h,color,label):
        x=X(span[0]);w=width(span)*scale
        rects.append(f'<rect x="{x:.1f}" y="{top}" width="{w:.1f}" height="{h}" fill="{color}" stroke="#202b36" stroke-width="1.3"/>')
        rects.append(f'<text x="{x+w/2:.1f}" y="{top-7}" text-anchor="middle" font-size="11">{label}</text>')
    rect(shaft,170,24,"#b6c5d3","shaft Ø12")
    rect(gear,100,164,"#e3b45e","Z50 8")
    for i,a in enumerate(bearings):rect(a,125,115,"#6ba7ba","bearing 8")
    for i,a in enumerate(spacers):rect(a,152,61,"#9bc58b","spacer 2")
    for i,a in enumerate(clips):rect(a,144,77,"#dc857c","clip*")
    marks=[-11,-10,-2,0,8,10,18,19]
    for v in marks:
        rects.append(f'<line x1="{X(v)}" y1="270" x2="{X(v)}" y2="281" stroke="#333"/>')
        rects.append(f'<text x="{X(v)}" y="298" font-size="10" text-anchor="middle">{v}</text>')
    svg=f"""<svg xmlns="http://www.w3.org/2000/svg" width="940" height="375" viewBox="0 0 940 375">
<rect width="940" height="375" fill="#fafbfc"/>
<text x="32" y="35" font-size="21" font-family="Arial" font-weight="bold">PX1 A32 — X150 axial stack (assumed)</text>
<text x="32" y="58" font-size="13" font-family="Arial">Axial section schematic • all x in mm • not an actual STEP section</text>
<g font-family="Arial">{''.join(rects)}</g>
<line x1="{X(-12)}" y1="270" x2="{X(20)}" y2="270" stroke="#333"/>
<text x="32" y="328" font-size="12" font-family="Arial">* Clip envelope/groove dimensions are placeholders; verify DIN 471 groove, bearing inner race, fits.</text>
<text x="32" y="349" font-size="12" font-family="Arial">The 2 mm spacers close A31's 1 mm gaps; axial clearance and preload require tolerance analysis.</text>
</svg>"""
    (P/"px1_a32_preview.svg").write_text(svg,encoding="utf-8")
if __name__=="__main__":
    check();render()
    print("PASS: contiguous 28 mm bearing-spacer-gear-spacer-bearing axial stack")
    print("NEEDS_PHYSICAL_CHECK: clip groove, race contact, gear axial clearance, seal pressure")
