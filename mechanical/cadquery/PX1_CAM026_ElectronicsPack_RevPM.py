import cadquery as cq, json, os

# PX1 Rev.PM — first packing proof for ready electronics on rotating side of CAM026-like head.
OUT=os.path.abspath('build_revpm'); os.makedirs(OUT,exist_ok=True)

def box(x0,y0,z0,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(False,False,False)).translate((x0,y0,z0))
def cylx(x0,r,l): return cq.Workplane('YZ').circle(r).extrude(l).translate((x0,0,0))

# Reference internal cylindrical region from Rev.PC rear rotate body after wall allowance.
cavity=cylx(75,30,40)
mods={
 'RP2040_ZERO_REF':box(77,-9,-11.75,5,18,23.5),
 'DRV8871_PAN_REF':box(84,-13,-10,8,26,20),
 'BALANCED_VIDEO_TX_RESERVE':box(94,-15,-10,8,30,20),
 '12to5_BUCK_RESERVE':box(104,-10,-7.5,8,20,15),
}
outside={n:round(m.val().cut(cavity.val()).Volume(),6) for n,m in mods.items()}
inter={}; ks=list(mods)
for i,a in enumerate(ks):
    for b in ks[i+1:]:
        v=mods[a].val().intersect(mods[b].val()).Volume()
        if v>1e-5: inter[f'{a}__{b}']=round(v,6)
assy=cq.Assembly(name='PX1_CAM026_ElectronicsPack_RevPM')
assy.add(cavity,name='REFERENCE_INTERNAL_CAVITY')
for n,p in mods.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_CAM026_ElectronicsPack_RevPM.step'))
checks={'cavity':'Ø60 x 40 mm reference from Rev.PC','outside_mm3':outside,'intersections_mm3':inter,'PASS':all(v<1e-5 for v in outside.values()) and not inter,'note':'Packing screen only; connectors, wiring bends, LED driver and PAN sensor placement remain physical/detail gates.'}
with open(os.path.join(OUT,'REV_PM_CAMERA_PACKAGING.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
if not checks['PASS']: raise SystemExit(2)
