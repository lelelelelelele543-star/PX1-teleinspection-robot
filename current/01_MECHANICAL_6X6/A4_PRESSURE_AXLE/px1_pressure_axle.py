#!/usr/bin/env python3
"""PX1 A4: assumed axial seal-stack geometry and pressure-force check (NOT qualified)."""
from math import pi
from pathlib import Path
import argparse
import csv

SHAFT_D = 12.0
SEAL_W = 7.0
VENT_W = 4.0
BEARING_W = 7.0
END_W = 3.0
STACK = [("End", END_W, "#b0b9c3"), ("Seal A", SEAL_W, "#edaa63"),
         ("Vent", VENT_W, "#dcebf3"), ("Seal B", SEAL_W, "#edaa63"),
         ("Bearing", BEARING_W, "#94a8bd"), ("End", END_W, "#b0b9c3")]
PRESSURES_BAR = (0.4, 0.7)

def force_n(bar, diameter_mm):
    return bar * 0.1 * pi * diameter_mm ** 2 / 4

def check():
    assert sum(item[1] for item in STACK) == 31.0
    assert abs(force_n(0.7, 12) - 7.916813487) < 1e-6
    assert abs(force_n(0.4, 12) - 4.523893421) < 1e-6

def preview_svg():
    x, y, scale = 155.0, 120.0, 11.0
    pieces = []
    for label, width, color in STACK:
        w = width * scale
        pieces.append(f'<rect x="{x}" y="{y}" width="{w}" height="100" fill="{color}" stroke="#344054"/>')
        pieces.append(f'<text x="{x+w/2}" y="{y-12}" text-anchor="middle" font-size="12">{label}</text>')
        x += w
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="400" viewBox="0 0 900 400">
<rect width="900" height="400" fill="#fff"/>
<g font-family="sans-serif" fill="#202a33">
<text x="40" y="42" font-size="23" font-weight="bold">PX1 axle pressure boundary - DESIGN CONCEPT</text>
<text x="40" y="67" font-size="14">Axial envelope in mm, NOT a seal gland drawing or verified Proteus geometry</text>
{''.join(pieces)}
<rect x="140" y="137" width="371" height="66" fill="#68717c" fill-opacity="0.78" stroke="#202a33"/>
<text x="325" y="255" text-anchor="middle" font-size="14">31 mm axial stack / shaft diameter 12 mm (assumed)</text>
<text x="40" y="290" font-size="16">DRY BODY / pressure</text><text x="600" y="290" font-size="16">WET SIDE / external</text>
<text x="40" y="335" font-size="13">Vent cavity requires safe drainage / leak detection and pressure relief.</text>
<text x="40" y="360" font-size="13">Seal rating, gland tolerances, lip orientation and physical tests: NOT VERIFIED.</text>
</g></svg>'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=".")
    out = Path(parser.parse_args().out)
    out.mkdir(parents=True, exist_ok=True)
    check()
    (out / "px1_pressure_axle_preview.svg").write_text(preview_svg(), encoding="utf-8")
    with (out / "px1_pressure_axle_forces.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["pressure_bar_g", "shaft_d_mm", "shaft_area_mm2", "axial_force_N", "status"])
        for p in PRESSURES_BAR:
            writer.writerow([p, SHAFT_D, round(pi * SHAFT_D ** 2 / 4, 4), round(force_n(p, SHAFT_D), 4), "DESIGN_ESTIMATE"])
    print("PASS: parameter/force checks; SKIPPED: actual seal qualification")

if __name__ == "__main__":
    main()
