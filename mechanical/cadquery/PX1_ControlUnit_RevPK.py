import cadquery as cq, json, os

# PX1 Rev.PK — compact Proteus-style serviceable control unit
# Operator logic follows Proteus: left joystick=crawler, right joystick=camera,
# physical ALL STOP, separate power/crawler enable. Electronics are PX1 replaceable modules.
OUT=os.path.abspath('build_revpk'); os.makedirs(OUT,exist_ok=True)

W=380.0; H=250.0; PANEL_T=3.0; DEPTH=125.0; EDGE=15.0
MON_W=180.0; MON_H=121.0; MON_D=74.0
MON_CX=190.0; MON_CY=178.0

def box(x0,y0,z0,dx,dy,dz):
    return cq.Workplane('XY').box(dx,dy,dz,centered=(False,False,False)).translate((x0,y0,z0))
def cylz(x,y,z,r,h):
    return cq.Workplane('XY').center(x,y).circle(r).extrude(h).translate((0,0,z))

panel=box(0,0,0,W,H,PANEL_T)
controls=[
 ('JOY_L',80,67,22.5),('JOY_R',300,67,22.5),('ESTOP',190,67,11.0),
 ('POWER',135,25,9.5),('ENABLE',245,25,11.0),('HOME',52,25,9.5),
 ('DIST_ZERO',92,25,9.5),('RECORD',288,25,9.5),('LIGHT_POT',330,25,4.0)]
for _,x,y,r in controls: panel=panel.cut(cylz(x,y,-0.5,r,PANEL_T+1.0))

monitor=box(MON_CX-MON_W/2,MON_CY-MON_H/2,PANEL_T,MON_W,MON_H,MON_D)
shell_outer=box(0,0,-DEPTH,W,H,DEPTH)
shell_inner=box(EDGE,EDGE,-DEPTH+EDGE,W-2*EDGE,H-2*EDGE,DEPTH)
enclosure=shell_outer.cut(shell_inner)
inner=box(EDGE,EDGE,-DEPTH+EDGE,W-2*EDGE,H-2*EDGE,DEPTH-EDGE)

parts={
 'NUCLEO_F446RE':box(20,155,-28,82.5,70,20),
 'RS485_isolated_ref':box(20,120,-24,45,20,16),
 'MAX7456_OSD_ref':box(75,120,-22,45,25,14),
 'CVBS_receiver_ref':box(130,120,-26,55,30,20),
 '24to5_buck':box(195,120,-25,45,25,16),
 'K1_24V_40A_relay':box(250,120,-38,42,30,32),
 'Fuse_holder':box(305,120,-32,30,20,26),
 'TETHER_BOOST_200W_RESERVE':box(115,165,-90,175,60,50),
 'Terminal_block_reserve':box(305,165,-55,45,55,35),
 'Joystick_L_rear':box(52,39,-48,56,56,48),
 'Joystick_R_rear':box(272,39,-48,56,56,48),
 'ESTOP_rear':cylz(190,67,-50,16,50),
}

outside={n:round(p.val().cut(inner.val()).Volume(),6) for n,p in parts.items()}
intersections={}
ks=list(parts)
for i,a in enumerate(ks):
    for b in ks[i+1:]:
        v=parts[a].val().intersect(parts[b].val()).Volume()
        if v>1e-5: intersections[f'{a}__{b}']=round(v,6)

assy=cq.Assembly(name='PX1_ControlUnit_RevPK')
assy.add(enclosure,name='ControlEnclosure')
assy.add(panel,name='FrontPanel')
assy.add(monitor,name='GF_AM071_180x121x74_Envelope')
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_ControlUnit_RevPK.step'))
cq.exporters.export(panel,os.path.join(OUT,'PX1_ControlUnit_FrontPanel_RevPK.step'))

checks={
 'panel_mm':[W,H,PANEL_T],
 'enclosure_depth_mm':DEPTH,
 'monitor_reference':{'article':'Giraffe GF-AM071','envelope_mm':[MON_W,MON_H,MON_D],'mounting_detail':'HOLD until physical monitor/bracket measured'},
 'controls':{n:[x,y,round(2*r,1)] for n,x,y,r in controls},
 'all_internal_parts_inside':all(v<1e-5 for v in outside.values()),
 'component_intersections_mm3':intersections,
 'packaging_PASS':all(v<1e-5 for v in outside.values()) and not intersections,
 'status':'PROTOTYPE PANEL/PACKAGING BASELINE; exact joystick articles, monitor bracket and tether boost article remain HOLD'
}
with open(os.path.join(OUT,'REV_PK_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if not checks['packaging_PASS']: raise SystemExit(2)
