#!/usr/bin/env python3
"""PX1 A6 twin motor saddles, XY design-target. Generate exact parameter SVG."""
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class P:
    inner_half_width:float=30
    motor_y:float=15.5
    motor_d:float=25
    motor_x:float=170
    motor_length:float=54
    saddle_x:float=175
    saddle_length:float=44
    saddle_width:float=26
    saddle_thickness:float=3
    hole_d:float=3.2
    hole_y:float=10
    hole_x:float=6

def check(p=P()):
    wall=p.inner_half_width-(p.motor_y+p.saddle_width/2)
    pair=2*p.motor_y-p.saddle_width
    front=p.saddle_x-(150+8.5)
    rear=(250-8.5)-(p.saddle_x+p.saddle_length)
    margin=p.saddle_width/2-(p.hole_y+p.hole_d/2)
    assert p.saddle_width>=p.motor_d
    assert p.saddle_x>=p.motor_x and p.saddle_x+p.saddle_length<=p.motor_x+p.motor_length
    assert wall>=1 and pair>=1 and front>0 and rear>0 and margin>=1
    return dict(wall=wall,pair=pair,front=front,rear=rear,hole_edge=margin)

def drawing(p=P()):
    r=check(p); X=lambda x:55+3*x; Y=lambda y:190-3*y
    a=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 455">',
       '<rect width="1000" height="455" fill="white"/>',
       '<text x="55" y="30" font-size="20" font-family="sans-serif">PX1 A6 - twin motor saddles (XY design target, mm)</text>',
       f'<rect x="{X(0)}" y="{Y(30)}" width="834" height="180" fill="#f1f5f9" stroke="#475569" stroke-width="2"/>']
    for ax in (50,150,250):
        a.append(f'<rect x="{X(ax-8.5)}" y="{Y(30)}" width="51" height="180" fill="#cbd5e1" opacity=".65"/>')
        a.append(f'<text x="{X(ax)-14}" y="300" font-size="14">X{ax}</text>')
    for sign in (-1,1):
        y=sign*p.motor_y
        a.append(f'<rect x="{X(p.saddle_x)}" y="{Y(y+p.saddle_width/2)}" width="{3*p.saddle_length}" height="{3*p.saddle_width}" fill="#94a3b8" stroke="#334155"/>')
        a.append(f'<rect x="{X(p.motor_x)}" y="{Y(y+p.motor_d/2)}" width="{3*p.motor_length}" height="{3*p.motor_d}" rx="7" fill="#38bdf8" fill-opacity=".6" stroke="#0369a1"/>')
        for x in (p.saddle_x+p.hole_x,p.saddle_x+p.saddle_length-p.hole_x):
            for yy in (y-p.hole_y,y+p.hole_y):
                a.append(f'<circle cx="{X(x)}" cy="{Y(yy)}" r="{1.5*p.hole_d}" fill="white" stroke="#dc2626" stroke-width="2"/>')
    a.extend([f'<text x="55" y="334" font-size="14" font-family="monospace">Saddles {p.saddle_length} x {p.saddle_width} x {p.saddle_thickness} mm; 8 x D{p.hole_d} holes (underside screws)</text>',
      f'<text x="55" y="358" font-size="14" font-family="monospace">Wall {r["wall"]} | pair {r["pair"]} | X150 {r["front"]} | X250 {r["rear"]} | hole edge {r["hole_edge"]} mm</text>',
      '<text x="55" y="387" font-size="14" font-family="sans-serif">Screw heads, clamp, Z-height, motor shaft, gear stage and cable routes NOT MODELLED.</text>',
      '<text x="55" y="414" font-size="14" font-family="sans-serif">Conceptual 2D design, NOT a Proteus measurement or manufacturing-ready CAD.</text></svg>'])
    return '\n'.join(a)

if __name__=='__main__':
    p=P();print(check(p))
    Path(__file__).with_name('px1_a6_motor_saddles_preview.svg').write_text(drawing(p),encoding='utf-8')
