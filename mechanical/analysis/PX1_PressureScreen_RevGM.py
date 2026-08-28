import math, json, os
from scipy import constants

# PX-1 Rev.GM — independent plate/tube structural screening
# NOT an FEA release. Navier simply-supported plate series is used as a reproducible screening model.
# Dimensions mm, loads N, stresses MPa (=N/mm2).

OUT='build_revgm'
os.makedirs(OUT,exist_ok=True)
E=69000.0
NU=0.33
DP_WORST=0.060
DP_NOMINAL=0.050

def plate_ss(a,b,t,q,N=101):
    D=E*t**3/(12*(1-NU**2))
    w=dxx=dyy=0.0
    for m in range(1,N+1,2):
        sm=math.sin(m*math.pi/2)
        for n in range(1,N+1,2):
            sn=math.sin(n*math.pi/2)
            lam=(m/a)**2+(n/b)**2
            W=16*q/(m*n*math.pi**6*D*lam**2)
            w += W*sm*sn
            dxx -= (m*math.pi/a)**2*W*sm*sn
            dyy -= (n*math.pi/b)**2*W*sm*sn
    Mx=-D*(dxx+NU*dyy)
    My=-D*(dyy+NU*dxx)
    sx=6*Mx/t**2
    sy=6*My/t**2
    vm=math.sqrt(sx*sx-sx*sy+sy*sy)
    return {
        'a_mm':a,'b_mm':b,'t_mm':t,'q_MPa':q,
        'center_deflection_mm':w,
        'center_sigma_x_MPa':sx,'center_sigma_y_MPa':sy,'center_von_mises_MPa':vm,
        '3x_screen_stress_MPa':3*vm,
        '3x_screen_deflection_mm':3*w,
    }

cases={
 'P0_top_cover_clear_span': plate_ss(144.0,60.0,5.0,DP_WORST),
 'P0_P1_side_membrane_full_bay': plate_ss(286.0,80.0,4.0,DP_WORST),
 'P0_main_floor_clear_span': plate_ss(291.0,68.0,6.0,DP_WORST),
 'P0_main_sidewall_screen': plate_ss(291.0,71.0,4.0,DP_WORST),
 'P1_sidecover_between_fastener_regions': plate_ss(54.0,70.0,5.0,DP_WORST),
 'rear_pressure_extension_wall': plate_ss(68.0,33.0,4.0,DP_WORST),
}

pressure_forces={
 'top_clear_span_N':DP_WORST*144.0*60.0,
 'one_side_bay_full_projected_N':DP_WORST*286.0*80.0,
 'rear_extension_end_68x36_N':DP_WORST*68.0*36.0,
}

b=76.0; h=44.0; bi=68.0; hi=36.0
A=b*h-bi*hi
Iy=(b*h**3-bi*hi**3)/12.0
Zy=Iy/(h/2.0)
def rear_load(F_N,e_mm):
    axial=F_N/A
    bending=F_N*e_mm/Zy
    return {'proof_load_N':F_N,'eccentricity_mm':e_mm,'axial_MPa':axial,'bending_MPa':bending,'combined_MPa':axial+bending}
rear={
 'section_area_mm2':A,'Iy_mm4':Iy,'section_modulus_mm3':Zy,
 '2kN_centered':rear_load(2000.0,0.0),
 '2kN_at_30mm_offset':rear_load(2000.0,30.0),
 '2kN_at_50mm_offset':rear_load(2000.0,50.0),
 '5kN_at_30mm_abuse_screen':rear_load(5000.0,30.0),
}

plate_screen_limit_MPa=80.0
plate_deflection_limit_mm=0.50
rear_screen_limit_MPa=80.0
passes={
 'plate_stress': all(c['3x_screen_stress_MPa'] <= plate_screen_limit_MPa for c in cases.values()),
 'plate_deflection': all(c['3x_screen_deflection_mm'] <= plate_deflection_limit_mm for c in cases.values()),
 'rear_tether': rear['5kN_at_30mm_abuse_screen']['combined_MPa'] <= rear_screen_limit_MPa,
}
result={
 'method':'Navier simply-supported plate series + rectangular-tube axial/bending screen; NOT FEA release',
 'material_screen':{'E_MPa':E,'nu':NU,'exact_alloy':'HOLD'},
 'pressure_cases':{
   'worst_differential_MPa':DP_WORST,
   'worst_differential_bar':DP_WORST*10.0,
   'nominal_screen_MPa':DP_NOMINAL,
   'interpretation':'0.6 bar reverse-differential screen covers ~10 m external water vs ~0.4 bar internal positive pressure and failed-zone differential cases'
 },
 'plate_cases':cases,
 'pressure_resultants':pressure_forces,
 'rear_tether_section':rear,
 'screen_limits':{'3x_plate_stress_MPa':plate_screen_limit_MPa,'3x_plate_deflection_mm':plate_deflection_limit_mm,'rear_combined_MPa':rear_screen_limit_MPa},
 'passes':passes,
 'status':'PASS_SCREEN' if all(passes.values()) else 'FAIL_SCREEN',
 'release_gates':['FreeCAD/CalculiX 3D FEA on filleted perforated body','exact alloy and temper','bolt preload/contact','X200 cartridge-seat local stress','rear transition fillet stress','physical hydrostatic/pressure and tether proof tests']
}
with open(os.path.join(OUT,'REV_GM_PRESSURE_SCREEN.json'),'w') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
if result['status']!='PASS_SCREEN': raise SystemExit(2)
