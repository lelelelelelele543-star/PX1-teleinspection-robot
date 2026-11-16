"""A35 shaft pressure thrust screening. Assumptions, NOT physical validation."""
from math import pi
from pathlib import Path
import xml.etree.ElementTree as ET
D=12.0
AREA=pi*D**2/4
F_LOW=0.4*0.1*AREA
F_HIGH=0.7*0.1*AREA
assert abs(F_HIGH-7.916813487)<1e-6
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="390" viewBox="0 0 900 390"><rect width="900" height="390" fill="white"/><g font-family="Arial" fill="#172b3e"><text x="30" y="35" font-size="24">PX1 A35 | X150 shaft pressure thrust</text><text x="30" y="62" font-size="14">Parametric 2D cross-section; all geometry ASSUMED, not CAD solid</text><rect x="90" y="125" width="300" height="160" fill="#d5e8f7" stroke="#496b83"/><rect x="390" y="125" width="90" height="160" fill="#efdfc8" stroke="#876d4a"/><rect x="480" y="125" width="300" height="160" fill="#f2f3f5" stroke="#69727d"/><rect x="90" y="179" width="690" height="52" fill="#aab4bd" stroke="#344858"/><line x1="390" y1="110" x2="390" y2="300" stroke="#b44" stroke-width="3" stroke-dasharray="8 5"/><path d="M235 155 L360 155 L348 148 M360 155 L348 162" stroke="#126ba3" stroke-width="4" fill="none"/><text x="110" y="110" font-size="16">0.4–0.7 bar inside</text><text x="530" y="110" font-size="16">Ambient</text><text x="405" y="157" font-size="14">Seal</text><text x="570" y="250" font-size="14">Shaft Ø12</text><text x="30" y="326" font-size="16">Area = π × 12² / 4 = {AREA:.2f} mm²</text><text x="30" y="350" font-size="16">Thrust = {F_LOW:.2f}–{F_HIGH:.2f} N; 2× screening = {2*F_HIGH:.2f} N</text><text x="30" y="377" font-size="12">Not a seal rating, bearing rating or pressure test.</text></g></svg>'''
ET.fromstring(svg)
(Path(__file__).parent/'px1_a35_preview.svg').write_text(svg,encoding='utf-8')
print('PASS:',round(AREA,3),'mm2;',round(F_LOW,3),round(F_HIGH,3),'N')
