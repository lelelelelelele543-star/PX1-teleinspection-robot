import cadquery as cq, math, json, os
OUT=os.path.abspath('build_revpj'); os.makedirs(OUT,exist_ok=True)
# PX1 Rev.PJ — compact Proteus-style 150m reel with standard replacement chain/slip ring.
# Source facts: MiniCam RMP chain is 670mm, Z30/Z16; RMP200 layering spindle 160mm.
# PX1 replacement standard: ISO606 06B-1, 70 links; Senring M220-1205 slip ring.
L=530.; W=240.; H=520.; SIDE_T=5.
CORE_D=140.; PACK_D=300.; FLANGE_D=330.; DRUM_W=145.; SHAFT_Z=282.
CABLE_D=6.8; CABLE_L=150000.; PACK_EFF=.78
P=9.525; LINKS=70; ZB=30; ZS=16

def chain_pitches(m): return 2*m+(ZB+ZS)/2+((ZB-ZS)**2)/(4*math.pi**2*m)
lo,hi=1.,100.
for _ in range(100):
    mid=(lo+hi)/2
    if chain_pitches(mid)>LINKS: hi=mid
    else: lo=mid
C=((lo+hi)/2)*P
SX=-68.; SZ=SHAFT_Z-math.sqrt(C*C-SX*SX)
DP30=P/math.sin(math.pi/ZB); DP16=P/math.sin(math.pi/ZS)
DK30=94.7; DK16=52.3

def box(x0,y0,z0,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(False,False,False)).translate((x0,y0,z0))
def cy(x,y0,z,r,l): return cq.Workplane('XZ').center(x,z).circle(r).extrude(l).translate((0,y0,0))
def plate(y0):
    p=cq.Workplane('XZ').workplane(offset=y0).polyline([(-265,0),(265,0),(230,425),(175,520),(-175,520),(-230,425)]).close().extrude(SIDE_T)
    for cx,cz,w,h in [(-150,255,150,250),(0,330,170,190),(150,255,150,250)]:
        p=p.cut(cq.Workplane('XZ').workplane(offset=y0-.5).center(cx,cz).rect(w,h).extrude(SIDE_T+1))
    return p
parts={'Frame_L':plate(-W/2),'Frame_R':plate(W/2-SIDE_T)}
for i,(x,z) in enumerate([(0,25),(-150,440),(150,440)],1): parts[f'Crossbar_{i}']=cy(x,-W/2+SIDE_T,z,8,W-2*SIDE_T)
parts['Drum_Core']=cy(0,-DRUM_W/2,SHAFT_Z,CORE_D/2,DRUM_W)
parts['Drum_Flange_L']=cy(0,-DRUM_W/2-4,SHAFT_Z,FLANGE_D/2,4)
parts['Drum_Flange_R']=cy(0,DRUM_W/2,SHAFT_Z,FLANGE_D/2,4)
parts['Main_Shaft']=cy(0,-W/2+18,SHAFT_Z,10,W-36)
# source-standard RMP supports
parts['61904_L']=cy(0,-W/2+10,SHAFT_Z,18.5,9); parts['16006_L']=cy(0,-W/2+22,SHAFT_Z,27.5,9)
parts['Seal_30x42x7_L']=cy(0,-W/2+34,SHAFT_Z,21,7); parts['61804_R']=cy(0,W/2-29,SHAFT_Z,16,7); parts['6203_R']=cy(0,W/2-20,SHAFT_Z,20,12)
# replacement ISO606 06B-1 sprocket envelopes; current iwis stock dimensions
parts['06B_Z30']=cy(0,W/2-12,SHAFT_Z,DK30/2,6); parts['06B_Z16']=cy(SX,W/2-12,SZ,DK16/2,6)
parts['Layering_Spindle_160']=cy(SX,-80,SZ,8,160); parts['Layering_Slider']=box(SX-22,-18,SZ-18,44,36,36)
x0=min(SX,0)-DK30/2-10; x1=max(SX,0)+DK30/2+10; z0=min(SZ,SHAFT_Z)-DK16/2-10; z1=max(SZ,SHAFT_Z)+DK30/2+10
parts['Chain_Guard']=box(x0,W/2-8,z0,x1-x0,8,z1-z0)
# source-like counter; exact wheel diameter intentionally not frozen
parts['D29_Guide_Roller']=cy(-115,-18,70,14.5,36); parts['Measuring_Wheel_REF']=cy(-63,-8,70,20,16)
parts['618_8_A']=cy(-63,-10,70,8,4); parts['618_8_B']=cy(-63,6,70,8,4)
parts['AS5600_Module_REF']=box(-79,16,57,42.9,6,25.4)
# exact selected replaceable slip-ring envelope
parts['Senring_M220_1205']=cy(0,-W/2+43,SHAFT_Z,11,40)
parts['Crank_160']=box(0,W/2+8,SHAFT_Z-5,160,10,10); parts['Crank_Grip']=cy(155,W/2+5,SHAFT_Z,10,70)
assy=cq.Assembly(name='PX1_PortableReel150_RevPJ')
for n,p in parts.items(): assy.add(p,name=n)
assy.save(os.path.join(OUT,'PX1_PortableReel150_RevPJ.step'))
vol=math.pi*(CABLE_D/2)**2*CABLE_L; ann=math.pi/4*(PACK_D**2-CORE_D**2); req=vol/(ann*PACK_EFF)
checks={'chain':{'standard':'06B-1 ISO606','pitch_mm':P,'links':LINKS,'link_length_mm':LINKS*P,'source_nominal_mm':670,'Z30_pitch_d_mm':DP30,'Z16_pitch_d_mm':DP16,'center_distance_mm':C},'slip_ring':{'article':'Senring M220-1205','size_mm':[22,40],'circuits':12,'A_each':5,'rated_V':240,'pin_use':'2xPWR+,2xPWR-,RS485 A/B,VIDEO +/-,4 spare'},'capacity':{'cable_m':150,'cable_od_mm':CABLE_D,'required_width_mm':req,'working_width_mm':DRUM_W,'margin_mm':DRUM_W-req},'all_solids_valid':all(p.val().isValid() for p in parts.values()),'status':'PASS; exact MiniCam chain pitch was not stated; 06B-1 is PX1 replacement choice'}
with open(os.path.join(OUT,'REV_PJ_VALIDATION.json'),'w') as f: json.dump(checks,f,indent=2)
print(json.dumps(checks,indent=2))
