"""PX1 engineering datum layout from existing current/CAD/PX1_Current_Master.py.
2D only; NOT a CAD export. Run: python current/CAD/px1_datum_preview.py
"""
import ast
from pathlib import Path

MASTER=Path(__file__).with_name("PX1_Current_Master.py")
OUT=Path(__file__).with_name("px1_datum_preview.svg")
def load():
    values={}
    for n in ast.parse(MASTER.read_text(encoding="utf-8")).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try: values[n.targets[0].id]=ast.literal_eval(n.value)
            except (ValueError,TypeError): pass
    return values
def draw(c):
    wx=c["WHEEL_X"]; gx=c["GEAR_X"]; z=c["WHEEL_Z"]; r=c["WHEEL_CROWN_R"]
    assert len(wx)==3 and len(gx)==5 and all(x in gx for x in wx)
    assert all(b-a==50 for a,b in zip(gx,gx[1:]))
    assert c["BODY_Z0"]<z<c["BODY_TOP"] and max(wx)<c["BODY_L_SOURCE_SCREEN"]
    X=lambda x:100+2.5*x
    Y=lambda h:330-2.5*h
    p=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 510" width="1000" height="510">','<rect width="1000" height="510" fill="#f8fafc"/>','<text x="45" y="40" font-size="23" font-family="sans-serif">PX1 — master datum side projection (mm)</text>','<text x="45" y="65" font-size="15" fill="#a04c20">2D only / not a CAD render / estimated geometry not certified</text>']
    p.append(f'<rect x="{X(0)}" y="{Y(c["BODY_TOP"])}" width="{2.5*c["BODY_L_SOURCE_SCREEN"]}" height="{2.5*(c["BODY_TOP"]-c["BODY_Z0"])}" fill="#c9d7e5" fill-opacity=".6" stroke="#30465f"/>')
    for x in gx:
        p.append(f'<circle cx="{X(x)}" cy="{Y(z)}" r="65" fill="none" stroke="#ad612d" stroke-dasharray="5 5"/>')
    for x in wx:
        p.append(f'<circle cx="{X(x)}" cy="{Y(z)}" r="{2.5*r}" fill="#6588a8" fill-opacity=".23" stroke="#254461" stroke-width="3"/>')
        p.append(f'<circle cx="{X(x)}" cy="{Y(z)}" r="15" fill="white" stroke="#254461"/>')
        p.append(f'<text x="{X(x)-14}" y="{Y(z)+5}" font-size="13">{x}</text>')
    p.extend(['<text x="95" y="407" font-size="16">6 wheels, 2 sides × (3 wheels + 5 Z50 gear stations)</text>','<text x="95" y="433" font-size="15" fill="#9b4b1e">Motors, bearings, covers, seals and input gears: NOT SHOWN / NOT VALIDATED</text>','<text x="95" y="459" font-size="15">Only datums extracted from the existing CAD master. No new chassis geometry.</text>','</svg>'])
    return "\n".join(p)
if __name__=="__main__":
    OUT.write_text(draw(load()),encoding="utf-8")
    print("PASS: wheel/gear stations and side projection; NOT_RUN: FreeCAD and physical tests")
