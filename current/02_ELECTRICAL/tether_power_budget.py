"""PX1 integrated 40 m power budget: design assumptions, not qualification.
Run: python current/02_ELECTRICAL/tether_power_budget.py
Outputs SVG in same directory. No third-party packages.
"""
from pathlib import Path
from html import escape

LENGTH_M = 40.0
RHO20 = 0.0175  # assumed ohm*mm2/m
ALPHA = 0.00393  # assumed 1/K copper
SOURCE_V = 24.0
# All currents are ASSUMED input at 24 V, not measured motor or lamp data.
LOADS_A = {"traction_left": 0.65, "traction_right": 0.65,
           "camera_video": 0.18, "illumination": 0.32,
           "controller_rs485": 0.12, "reserve": 0.08}
POWER_CORE_MM2 = (0.75, 1.0, 1.5, 2.5)
TEMPERATURE_C = (20.0, 60.0)
MIN_INPUT_V = 21.0  # design target; actual DC/DC and motor UVLO NOT verified
def analyze(area, temperature, loads=LOADS_A):
    if area <= 0 or not -40 <= temperature <= 120:
        raise ValueError("invalid area or temperature")
    if any(v < 0 for v in loads.values()):
        raise ValueError("negative current")
    current = sum(loads.values())
    rho = RHO20 * (1 + ALPHA * (temperature - 20))
    loop_r = 2 * LENGTH_M * rho / area
    drop = current * loop_r
    return dict(area=area, temperature=temperature, current=current,
                resistance=loop_r, drop=drop, at_robot=SOURCE_V-drop,
                cable_heat=current*drop, pass_voltage=SOURCE_V-drop >= MIN_INPUT_V)
def svg(rows):
    out=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 650">',
         '<rect width="1080" height="650" fill="#f8fafc"/>',
         '<text x="35" y="45" font-family="sans-serif" font-size="25" font-weight="bold">PX1 / 40 m / integrated 24 V power screening</text>',
         '<text x="35" y="72" font-family="sans-serif" font-size="14">ALL loads, copper sizes, 21 V limit and temperatures are DESIGN ASSUMPTIONS, not validated hardware</text>',
         '<rect x="32" y="98" width="480" height="184" rx="12" fill="#e2e8f0"/>',
         '<text x="52" y="128" font-family="sans-serif" font-size="18" font-weight="bold">Load allocation at 24 V (assumed)</text>']
    for j,(name,current) in enumerate(LOADS_A.items()):
        y=156+j*21
        out.append(f'<text x="54" y="{y}" font-family="monospace" font-size="14">{escape(name):24s} {current:.2f} A</text>')
    out += ['<text x="560" y="125" font-family="sans-serif" font-size="18" font-weight="bold">Architecture: six independent copper cores</text>',
            '<text x="560" y="159" font-family="sans-serif" font-size="15">1: +24 V      2: power return</text>',
            '<text x="560" y="190" font-family="sans-serif" font-size="15">3: RS485 A     4: RS485 B</text>',
            '<text x="560" y="221" font-family="sans-serif" font-size="15">5: CVBS signal 6: CVBS return</text>',
            '<text x="560" y="253" font-family="sans-serif" font-size="14">No coax / twisted pair / fiber assumed</text>',
            '<text x="35" y="324" font-family="sans-serif" font-size="18" font-weight="bold">Round-trip copper loss over 40 m, two power conductors</text>',
            '<text x="40" y="356" font-family="monospace" font-size="14">Core area  Temp  Current  Loop R  Drop    Robot V  Heat   Voltage target</text>']
    for j,row in enumerate(rows):
        y=386+j*28
        fill="#dcfce7" if row["pass_voltage"] else "#fee2e2"
        out.append(f'<rect x="35" y="{y-18}" width="990" height="25" rx="3" fill="{fill}"/>')
        s=f'{row["area"]:>5.2f} mm2   {row["temperature"]:>2.0f} C   {row["current"]:>4.2f} A   {row["resistance"]:>4.2f} R   {row["drop"]:>4.2f} V   {row["at_robot"]:>5.2f} V   {row["cable_heat"]:>5.2f} W   {"PASS" if row["pass_voltage"] else "FAIL"}'
        out.append(f'<text x="49" y="{y}" font-family="monospace" font-size="14">{escape(s)}</text>')
    out += ['<text x="35" y="617" font-family="sans-serif" font-size="14">NOT_RUN: motor start/stall transients, DC/DC UVLO, CVBS attenuation, RS485 BER, cable heating</text>',
            '<text x="35" y="640" font-family="sans-serif" font-size="14">PHYSICAL_CHECK: connector pinout, Kevlar cable construction, pressure gland, bend radius</text>','</svg>']
    return "\n".join(out)+"\n"
def main():
    rows=[analyze(area,temp) for temp in TEMPERATURE_C for area in POWER_CORE_MM2]
    assert len(LOADS_A)==6 and abs(sum(LOADS_A.values())-2.0)<1e-9
    assert abs(analyze(1.0,20)["drop"]-2.8)<1e-9
    assert analyze(1.0,60)["drop"]>analyze(1.0,20)["drop"]
    assert not analyze(1.0,60)["pass_voltage"]
    assert analyze(1.5,60)["pass_voltage"]
    assert all(analyze(a,20)["drop"]>0 for a in POWER_CORE_MM2)
    target=Path(__file__).with_name("tether_power_budget.svg")
    target.write_text(svg(rows),encoding="utf-8")
    for row in rows:
        print(f'{row["area"]:g} mm2 / {row["temperature"]:g} C: {row["at_robot"]:.2f} V, {row["cable_heat"]:.2f} W, {"PASS" if row["pass_voltage"] else "FAIL"}')
    print("PASS: arithmetic, hot-copper sensitivity, SVG generated",target)
if __name__=="__main__":
    main()
