import cadquery as cq, json, os

# PX1 Rev.PL — Rev.PK console with common-service modules fitted.
# Exact candidate envelopes: GF-AM071 monitor, TTL TO RS485 (C) isolated module,
# APEM 4000 generic closed-frame joystick envelope.
OUT=os.path.abspath('build_revpl'); os.makedirs(OUT,exist_ok=True)
W=380.; H=250.; PANEL_T=3.; DEPTH=125.; EDGE=15.
MON_W=180.; MON_H=121.; MON_D=74.; MON_CX=190.; MON_CY=178.

def box(x0,y0,z0,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(False,False,False)).translate((x0,y0,z0))
def cylz(x,y,z,r,h): return cq.Workplane('XY').center(x,y).circle(r).extrude(h).translate((0,0,z))

panel=box(0,0,0,W,H,PANEL_T)
# APEM exact cutout depends configured 4000 part; 45-mm circular pilot is NOT machining release.
controls=[('JOY_L',80,67,22.5),('JOY_R',300,67,22.5),('ESTOP',190,67,11),('POWER',135,25,9.5),('ENABLE',245,25,11),('HOME',52,25,9.5),('DIST_ZERO',92,25,9.5),('RECORD',288,25,9.5),('LIGHT_POT',330,25,4)]
for _,x,y,r in controls: panel=panel.cut(cylz(x,y,-.5,r,PANEL_T+1))
monitor=box(MON_CX-MON_W/2,MON_CY-MON_H/2,PANEL_T,MON_W,MON_H,MON_D)
shell_outer=box(0,0,-DEPTH,W,H,DEPTH); shell_inner=box(EDGE,EDGE,-DEPTH+EDGE,W-2*EDGE,H-2*EDGE,DEPTH)
enclosure=shell_outer.cut(shell_inner); inner=box(EDGE,EDGE,-DEPTH+EDGE,W-2*EDGE,H-2*EDGE,DEPTH-EDGE)
parts={
 'NUCLEO_F446RE':box(20,155,-28,82.5,70,20),
 'TTL_TO_RS485_C_42p8x15p2x4p75':box(20,120,-10,42.8,15.2,4.75),
 'MAX7456_OSD_ref':box(75,120,-22,45,25,14),
 'CVBS_receiver_ref':box(130,120,-26,55,30,20),
 '24to5_buck':box(195,120,-25,45,25,16),
 'K1_24V_40A_relay':box(250,120,-38,42,30,32),
 'Fuse_holder':box(305,120,-32,30,20,26),
 'TETHER_BOOST_200W_RESERVE':box(115,165,-90,175,60,50),
 'Terminal_block_reserve':box(305,165,-55,45,55,35),
 'APEM4000_LEFT_generic_envelope':box(50,37,-53,60,60,53),
 'APEM4000_RIGHT_generic_envelope':box(270,37,-53,60,60,53),
 'ESTOP_rear':cylz(190,67,-50,16,50)}
outside={n:round(p.val().cut(inner.val()).Volume(),6) for n,p in parts.items()}
inter={}; ks=list(parts)
for i,a in enumerate(ks):
    for b in ks[i+1:]:
        v=parts[a].val().intersect(parts[b].val()).Volume()
        if v>1e-5: inter[f'{a}__{b}']=round(v,6)
assy=cq.Assembly(name='PX1_ControlUnit_RevPL'); assy.add(enclosure,name='Enclosure'); assy.add(panel,name='FrontPanel'); assy.add(monitor,name='GF_AM071')
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_ControlUnit_RevPL.step'))
cq.exporters.export(panel,os.path.join(OUT,'PX1_ControlUnit_FrontPanel_RevPL.step'))
checks={'panel_mm':[W,H,PANEL_T],'depth_mm':DEPTH,'GF_AM071_mm':[MON_W,MON_H,MON_D],'joystick_candidate':'APEM 4000 two-axis; exact configured cutout HOLD','rs485_module':{'name':'TTL TO RS485 (C)','mm':[42.8,15.2,4.75]},'outside_mm3':outside,'intersections_mm3':inter,'PASS':all(v<1e-5 for v in outside.values()) and not inter}
with open(os.path.join(OUT,'REV_PL_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if not checks['PASS']: raise SystemExit(2)
