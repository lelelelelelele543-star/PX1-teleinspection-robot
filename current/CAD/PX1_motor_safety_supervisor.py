#!/usr/bin/env python3
"""PX1 integrated motor undervoltage supervisor: simulation only, NOT firmware.
All thresholds, cable dimensions and current loads are DESIGN ASSUMPTIONS.
Run: python current/CAD/PX1_motor_safety_supervisor.py
"""
from dataclasses import dataclass
from pathlib import Path
import json
L=40.0; A=1.5; RHO=0.0175; ALPHA=0.00393
SOURCE=24.0; MIN_V=20.0; UV_TRIP=19.5; UV_CLEAR=21.0
def loop_r(temp):
    return 2*L*RHO/A*(1+ALPHA*(temp-20))
@dataclass
class Supervisor:
    fault: str = ""
    uv_samples: int = 0
    clear_samples: int = 0
    def step(self,left,right,aux,temp,bus,hardware_trip=False,reset=False):
        if min(left,right,aux)<0: raise ValueError("negative current request")
        if hardware_trip: self.fault="HARDWARE_TRIP"
        self.uv_samples=self.uv_samples+1 if bus<UV_TRIP else 0
        if self.uv_samples>=3 and not self.fault: self.fault="UNDERVOLTAGE"
        self.clear_samples=self.clear_samples+1 if bus>=UV_CLEAR and not hardware_trip else 0
        if reset and self.clear_samples>=3 and not hardware_trip:
            self.fault=""; self.uv_samples=0
        budget=(SOURCE-MIN_V)/loop_r(temp)
        if aux>budget: self.fault="AUX_OVER_BUDGET"
        l=min(left,4.0); r=min(right,4.0) # assumed command cap, NOT rated motor limit
        factor=min(1,max(0,budget-aux)/(l+r)) if l+r else 1
        if self.fault: factor=0
        return {"fault":self.fault or "NONE","left_A":round(l*factor,4),
                "right_A":round(r*factor,4),
                "predicted_bus_V":round(SOURCE-(aux+(l+r)*factor)*loop_r(temp),4),
                "measured_bus_V":bus,"release":False}
def test():
    s=Supervisor()
    a=s.step(2,2,.8,60,22)
    assert a["fault"]=="NONE" and 0<a["left_A"]<2
    assert a["predicted_bus_V"]>=MIN_V-.001
    for _ in range(3): b=s.step(2,2,.8,60,19)
    assert b["fault"]=="UNDERVOLTAGE" and b["left_A"]==0
    for _ in range(3): c=s.step(2,2,.8,60,22)
    assert c["fault"]=="UNDERVOLTAGE"
    d=s.step(2,2,.8,60,22,reset=True)
    assert d["fault"]=="NONE" and d["left_A"]>0
    e=s.step(2,2,.8,60,22,hardware_trip=True)
    assert e["fault"]=="HARDWARE_TRIP" and e["left_A"]==0
    f=Supervisor().step(2,2,5,60,22)
    assert f["fault"]=="AUX_OVER_BUDGET" and f["left_A"]==0
    return {"limited_60C":a,"uv_latched":b,"reset":d,"hardware_trip":e,
            "aux_fault":f,"software_simulation":"PASS",
            "stm32":"NOT_RUN","hardware_protection":"NOT_RUN",
            "physical_checks":"PHYSICAL_CHECK"}
def preview(path):
    labels=["24 V supply","40 m copper tether","Bus voltage sensor","STM32 supervisor","2 motor drivers"]
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="330" viewBox="0 0 1100 330">',
         '<rect width="1100" height="330" fill="#f6f8fa"/>',
         '<text x="25" y="35" font-size="22" font-family="sans-serif">PX1 motor safety — calculated system diagram (ASSUMED)</text>']
    for i,label in enumerate(labels):
        x=20+i*215
        out.extend([f'<rect x="{x}" y="90" width="185" height="72" rx="8" fill="#dbe9f3" stroke="#3a5872"/>',
                    f'<text x="{x+92}" y="131" text-anchor="middle" font-size="13" font-family="sans-serif">{label}</text>'])
        if i<4: out.append(f'<path d="M{x+185} 125 h30" stroke="#285a82" stroke-width="3"/>')
    out.extend(['<rect x="450" y="205" width="390" height="65" rx="8" fill="#fff0dc" stroke="#a36b25"/>',
                '<text x="645" y="232" text-anchor="middle" font-size="14" font-family="sans-serif">Independent hardware overcurrent trip REQUIRED</text>',
                '<text x="645" y="251" text-anchor="middle" font-size="12" font-family="sans-serif">NOT implemented / NOT tested</text>',
                '<path d="M645 205 V162" stroke="#a36b25" stroke-dasharray="5 4"/>',
                '<text x="25" y="310" font-size="12" font-family="sans-serif">Power path only. RS485 and balanced CVBS use remaining four conductors. No CAD / STEP claim.</text>','</svg>'])
    path.write_text("\n".join(out)+"\n",encoding="utf-8")
if __name__=="__main__":
    p=Path(__file__).resolve().parent
    result=test()
    preview(p/"previews"/"PX1_motor_safety_supervisor.svg")
    (p/"previews"/"PX1_motor_safety_supervisor_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
