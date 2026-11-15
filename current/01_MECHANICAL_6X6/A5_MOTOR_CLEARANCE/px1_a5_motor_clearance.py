#!/usr/bin/env python3
"""A5 preliminary XY motor/axle envelope, millimetres; no FreeCAD required."""
from dataclasses import dataclass
from pathlib import Path
import csv

@dataclass(frozen=True)
class Design:
    body_length: float = 278.0
    body_width: float = 68.0
    wall: float = 4.0
    motor_diameter: float = 25.0
    motor_length: float = 54.0
    motor_x_front: float = 170.0
    motor_y_offset: float = 15.5
    axle_x: tuple = (50.0, 150.0, 250.0)
    axle_diameter: float = 17.0
    target_min_clearance: float = 2.0

def evaluate(d=Design()):
    x_end = d.motor_x_front + d.motor_length
    axle_r = d.axle_diameter / 2
    motor_r = d.motor_diameter / 2
    x150_gap = d.motor_x_front - (d.axle_x[1] + axle_r)
    x250_gap = (d.axle_x[2] - axle_r) - x_end
    side_gap = d.body_width / 2 - d.wall - (d.motor_y_offset + motor_r)
    pair_gap = 2 * d.motor_y_offset - d.motor_diameter
    return dict(x150_gap_mm=x150_gap, x250_gap_mm=x250_gap,
                inner_wall_to_motor_mm=side_gap, motor_pair_gap_mm=pair_gap,
                pass_envelope=all(v >= d.target_min_clearance for v in
                                  (x150_gap, x250_gap, side_gap, pair_gap)))

def svg(d=Design()):
    r = evaluate(d)
    scale=3
    def xx(v): return 40+scale*v
    def yy(v): return 170-scale*v
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 400">',
         '<rect width="950" height="400" fill="#f8fafc"/>',
         '<text x="40" y="28" font-size="18" font-family="sans-serif">PX1 A5 — motor / X150 clearance (XY envelope, assumed)</text>',
         f'<rect x="{xx(0)}" y="{yy(d.body_width/2)}" width="{scale*d.body_length}" height="{scale*d.body_width}" rx="8" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>',
         f'<rect x="{xx(0)}" y="{yy(d.body_width/2-d.wall)}" width="{scale*d.body_length}" height="{scale*(d.body_width-2*d.wall)}" fill="#fff" stroke="#64748b" stroke-dasharray="5 4"/>']
    for x in d.axle_x:
        out.append(f'<rect x="{xx(x-d.axle_diameter/2)}" y="{yy(d.body_width/2)}" width="{scale*d.axle_diameter}" height="{scale*d.body_width}" fill="#94a3b8" fill-opacity=".55" stroke="#64748b"/>')
        out.append(f'<text x="{xx(x)-14}" y="290" font-size="14" font-family="sans-serif">X{x:g}</text>')
    for y in (-d.motor_y_offset,d.motor_y_offset):
        out.append(f'<rect x="{xx(d.motor_x_front)}" y="{yy(y+d.motor_diameter/2)}" width="{scale*d.motor_length}" height="{scale*d.motor_diameter}" rx="8" fill="#38bdf8" fill-opacity=".75" stroke="#0369a1" stroke-width="2"/>')
    out.append(f'<text x="545" y="184" font-size="13" font-family="sans-serif">2 x Ø25 × 54 motor envelopes</text>')
    out.append(f'<text x="40" y="320" font-size="14" font-family="monospace">X150 gap: {r["x150_gap_mm"]:.1f} mm | X250 gap: {r["x250_gap_mm"]:.1f} mm | wall gap: {r["inner_wall_to_motor_mm"]:.1f} mm | motor gap: {r["motor_pair_gap_mm"]:.1f} mm</text>')
    out.append('<text x="40" y="346" font-size="13" font-family="sans-serif">Axles shown as projected full-width keep-out zones. Gearbox, Z16/Z40, bearing seats and wiring NOT modeled.</text>')
    out.append('<text x="40" y="369" font-size="13" font-family="sans-serif">Not a CRP150 measurement, no manufacturing release; all envelope checks are 2D only.</text></svg>')
    return '\n'.join(out)

if __name__ == "__main__":
    d=Design()
    r=evaluate(d)
    print(r)
    assert r["pass_envelope"], "Envelope collision or insufficient clearance"
    Path(__file__).with_name("px1_a5_motor_clearance_preview.svg").write_text(svg(d),encoding="utf-8")
