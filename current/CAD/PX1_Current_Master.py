import cadquery as cq
from cadquery import exporters
import math, json, csv, os, hashlib, textwrap
from pathlib import Path

ROOT=Path(os.environ.get('PX1_OUT', str(Path(__file__).resolve().parents[1])))
CAD=ROOT/'CAD'; METAL=CAD/'Metal_HOLD'; PRINT=CAD/'Print_STL'; IMG=ROOT/'images'
for d in (ROOT,CAD,METAL,PRINT,IMG): d.mkdir(parents=True, exist_ok=True)

# -------------------------------
# PX1 CURRENT MASTER — Proteus CRP-150 derived
# Coordinates: X longitudinal front->rear, Y left/right, Z up.
# Exact source/purchased dimensions are used where available.
# Any reconstruction lacking a controlled source dimension is named HOLD/ТРЕБУЕТСЯ_ЗАМЕР.
# -------------------------------

# Source-confirmed / source-reconstructed drivetrain datums
WHEEL_X=(50.0,150.0,250.0)
GEAR_X=(50.0,100.0,150.0,200.0,250.0)
WHEEL_Z=45.0
Z50_TEETH=50; Z50_MOD=1.0; Z50_PD=50.0; Z50_OD=52.0; Z50_FACE=4.0
Z16_TEETH=16; Z40_TEETH=40; BEVEL_MOD=1.0
Z16_OD=17.86; Z40_OD=40.74
B61801=(12.0,21.0,5.0)
B61903=(17.0,30.0,7.0)
B61800=(10.0,19.0,5.0)
XRING=(18.72,2.62)
SEAL_18_30_7=(18.0,30.0,7.0)
SIDE_ORING=(190.0,1.5)
SIDE_COVER_L=262.0; SIDE_COVER_H=60.0; SIDE_COVER_T=7.0   # DRW-002-374 side cover ~262x60x7, DERIVED
# F17 ballast blocks in free cavity space (bbox search, 0.5 mm shrink, motor-extraction keep-out). Material: STEEL (user decision 2026-11-19).
# F14: block 5 split around the rear plate-screw boss (was 266..287 x Z25..54): 5 = X270..287 Z25..55.75 (MPRLS-0.5),
#      6 = X266..270 above the boss Z39..55.75. Net volume -289 mm3 (-2.3 g steel).
BALLAST_BOXES=[(25.0,-21.5,25.0,90.0,-11.5,66.0),(25.0,11.5,25.0,90.0,21.5,66.0),(117.0,-25.5,25.0,188.0,25.5,30.0),(266.0,10.5,25.0,287.0,25.5,68.0),(270.0,-25.5,25.0,287.0,-10.5,55.75),(266.0,-25.5,39.0,270.0,-10.5,55.75)]
QRW_HUB_R=22.0   # F17 aluminium hub radius inside D90 tyre, ESTIMATED from Mini-Cam ASS-004-496 view (hub ~0.5 D)
# F11 FSS-002-060 weight plate (DRW-002-375 A-A, 1:1): stainless, in external bottom recess, flush.
WEIGHT_PLATE_W=50.3; WEIGHT_PLATE_H=12.0     # DERIVED from 1:1 section (±0.1)
WEIGHT_PLATE_X0=24.5; WEIGHT_PLATE_X1=272.0  # ESTIMATED: front ~5 mm from housing end per side view; rear not visible
CAVITY_FLOOR_Z=24.0                           # was 23; leaves 1.0 Al over plate (Proteus ~1.4 under Z40), ESTIMATED
# F14 plate fixing: DRW-002-375 pos.15 FIX-002-764 M8x16 DIN 7984 x2, pos.16 FIX-002-741 M8 spring washer x2.
# Side view 1:1 measured at 600 dpi (housing 278.07 over 278 -> scale 1.000). Drawing right end = PX1 front (X18).
PLATE_SCREW_XY=((46.0,0.0),(263.0,-15.5))   # #1: 28.0 from front end, DERIVED (±0.2); Y0 ESTIMATED (centre-plane section)
                                            # #2: not visible on DRW-002-375; PX1 position clear of Z40 pair, ESTIMATED
DIN7984_M8=(6.5,5.0,5.0)      # head dk/2, k, socket s — DIN 7984 M8, CONFIRMED standard (drawing k 5.1)
PLATE_SCREW_L=16.0            # FIX-002-764 M8 X 16, CONFIRMED (part list)
SPRING_WASHER_M8=(4.05,7.4,2.0)  # DIN 127 B M8 d1/2, d2/2, s, CONFIRMED standard
PLATE_CBORE_R=7.5             # Ø15.0 counterbore in plate, DERIVED (15.0)
PLATE_CBORE_LIG=4.0           # plate ligament under counterbore floor, DERIVED (4.0)
PLATE_SCREW_HOLE_R=4.2        # Ø8.4 through hole (ISO 273 fine; drawing ~8.1), ESTIMATED
M8_COSMETIC_THREAD_R=4.0      # tapped hole drawn at major Ø8 (cosmetic thread), ISO 262 M8, CONFIRMED standard
PLATE_TAP_TOP_Z=37.0          # thread Z23..37 = 14 mm (allows M8x20 option), ESTIMATED
PLATE_BOSS_R=6.5; PLATE_BOSS_TOP_Z=38.5   # Ø13 Al boss from cavity floor, 1.5 mm closed cap (pressure housing), ESTIMATED
# F10 side-cover seal SEA-002-102 190x1.5, lobed track around Z50 gears (DRW-002-374 top view):
SIDE_SEAL_R=28.0        # lobe radius about each Z50 centre, DERIVED from drawing (~27.5-28)
SIDE_SEAL_CUSP=19.0     # track distance from axis between gears, DERIVED from drawing (~18.4-19)
SIDE_SEAL_W=2.0; SIDE_SEAL_D=1.15   # groove in cover inner face, ESTIMATED (23% squeeze)
FLANGE_ORING=(32.0,1.5)
M6_COSMETIC_THREAD_R=3.0         # F13: shaft-end tapped hole shown at major Ø6 (cosmetic thread), ISO 262 M6 — CONFIRMED standard
# F13 Mini-Cam ASS-002-103 "Crawler Wheel Bolt - ASSY" (section A-A 2:1 + top view 2:1, measured at 600 dpi,
# scale checked on M6 thread 6.01 mm and button head dk 10.50 mm). Local axis from disk flange back face.
WD_FLANGE_T=6.0          # FSS-002-065 flange thickness, DERIVED (6.01)
WD_FLANGE_R=8.27         # cam profile circle radius, DERIVED (section r8.25 at 90°, top view r8.78 lobe)
WD_FLANGE_E=0.51         # cam profile eccentricity toward lobe, DERIVED (top view r8.78 / r7.11)
WD_FLAT=7.11             # flat on the side opposite the lobe, distance from axis, DERIVED (top view)
WD_FACE_R=6.54           # outer face radius before 45° chamfer, DERIVED
WD_SPIGOT_R=5.2          # spigot Ø10.4, DERIVED (10.37)
WD_SPIGOT_FLAT=3.9       # spigot D-flat (lobe side), DERIVED (top view)
WD_SPIGOT_L=2.6          # spigot length, DERIVED (2.60)
WD_LIP_R=5.5; WD_LIP_D=1.04         # Ø11.0 entry lip retaining the O-ring, DERIVED
WD_GROOVE_R=6.5; WD_GROOVE_D=3.32   # Ø13.0 O-ring groove from face 1.04..3.32, DERIVED
WD_SEAT_R=5.5; WD_SEAT_D=4.5        # Ø11.0 washer seat 3.32..4.50, DERIVED
WD_HOLE_R=3.2                        # Ø6.4 clearance for M6, ESTIMATED (ISO 273 medium)
ISO7380_M6=(5.25,3.3,4.0)            # dk/2, k, hex s — ISO 7380 M6, CONFIRMED standard
WD_HEAD_BEAR_D=3.42                  # head bearing face below disk outer face, DERIVED
WHEEL_SCREW_L=14.0                   # FIX-002-105 M6x14, CONFIRMED (part list)
SCHNORR_M6=(3.2,5.0,1.06)            # FIX-002-104 spring washer ri/ro/installed h, DERIVED (Ø6.4 std, Ø10 measured)
WD_ORING=(5.6,0.88,2.2)              # SEA-002-106 10x1.8 installed: torus major r / tube r / centre below face, DERIVED
SHAFT_SPIGOT_BORE_R=5.3; SHAFT_SPIGOT_BORE_D=2.7   # shaft-end counterbore for disk spigot, ESTIMATED
# F25: disk outer face was |Y|66.95 > tyre face 66.5 (width 133.9 > catalogue 133). Shaft end and disk recessed 0.5 into
# the hub pocket (whole ASS-002-103 stack moves with it: spigot bore, M6 tap, engagement unchanged). Outer face 66.45, DERIVED.
WHEEL_DISK_RECESS=0.5                # ESTIMATED (>=0.45 needed)
SHAFT_END_Y=60.9-WHEEL_DISK_RECESS   # 60.4 wheel-shaft end face |Y|, DERIVED
WD_BACK_Y=SHAFT_END_Y+0.05           # disk flange back |Y|, 0.05 above shaft end, ESTIMATED
WHEEL_KEY_Y0=48.9                    # 4x4 key inner end |Y| (key now ends at the shaft end), ESTIMATED
# F05 axle-flange face seal, DRW-002-374 section A-A (layout DERIVED, sizes ESTIMATED):
COVER_BEARING_BORE_R=15.0      # 61903 OD30 seat in side cover, CONFIRMED bearing OD
COVER_BEARING_SHOULDER_R=13.5  # Ø27 <= SKF Da max 28 for 61903, ESTIMATED
FLANGE_GROOVE_RI=16.0          # = O-ring ID32/2, zero stretch, ESTIMATED
FLANGE_GROOVE_RO=18.1          # width 2.1, ESTIMATED
FLANGE_GROOVE_DEPTH=1.15       # 23% squeeze of CS1.5, ESTIMATED
FLANGE_COLLAR_T=2.6            # was 2.0; 1.45 above groove, M3x6 engages 3.4 in cover, ESTIMATED
# F08 fasteners per DRW-002-374 (pos.15 FIX-000-359 M3x8, pos.16 FIX-002-738 M3x6, Torx button head):
COVER_SCREW_DX=(-125.0,-75.0,-25.0,25.0,75.0,125.0)  # about X150, DERIVED from DRW374 view (±0.2)
COVER_SCREW_DZ=(-24.0,24.0)                           # about Z45, DERIVED
COVER_SCREW_CBORE=(3.25,3.0)                          # Ø6.5 x 3 head recess, ESTIMATED (8-long screw in 7 cover)
FLANGE_SCREW_R=20.9                                   # 4x at 45°, DERIVED from DRW374 view
ISO7380_M3=(2.85,1.65)                                # head r, height — ISO 7380 M3, CONFIRMED standard
FLANGE_ORING_INST_RO=FLANGE_GROOVE_RI+math.pi*.75**2/FLANGE_GROOVE_DEPTH  # area-equal installed section

# Current reconstructed global CRP150/PX1 screen from recovered CAD audits.
# These are NOT released manufacturing dimensions unless separately called out.
BODY_L_SOURCE_SCREEN=278.0
BODY_HALF_W_SCREEN=34.0
BODY_Z0=11.0
BODY_TOP=75.0
PIPE_R=75.0
WHEEL_CENTRE_Y=54.5
WHEEL_CROWN_R=45.0
# DERIVED: paired lower-wall crown contacts, not an arbitrary fit translation.
PIPE_CENTER_Z=WHEEL_Z-WHEEL_CROWN_R+math.sqrt(PIPE_R**2-WHEEL_CENTRE_Y**2)
# ESTIMATED asymmetric outer shoulder; retains D90 and total width133.
# F04 (2026-11-19): outer shoulder r34.5->r28.5 @y8, edge r27.5->r20.5 @y12.
# DERIVED limit for >=3 mm radial gap in nominal ID150 at contact pose:
#   r <= sqrt((PIPE_R-3)^2-(WHEEL_CENTRE_Y+y)^2)-(PIPE_CENTER_Z-WHEEL_Z) -> 29.22@y8, 21.08@y12.
# Crown r45@y0 (contact) and inner side unchanged; values themselves ESTIMATED, not OEM QRW90.
WHEEL_PROFILE=[(26,-12),(32,-12),(42,-8),(45,0),(28.5,8),(20.5,12),(8,12),(8,-2),(26,-2)]
WHEEL_MIN_NONCONTACT_GAP=3.0

# F16 Proteus-class drive envelope (DRW-002-386 1:1: gearhead D26.0x44.6, motor D22.2x51.7 — DERIVED).
# Candidate ZHAOWEI ZWSMD026026 3-stage (44.9) + D22 motor, NOT seller-verified (see F12 report).
# Motor length 53.0 >= Proteus 51.7, so the envelope also covers the original-class motor.
MOTOR_OD=22.2; MOTOR_LEN=53.0; GEARHEAD_OD=26.0; GEARHEAD_LEN=44.9  # 53.0 DERIVED (ZHAOWEI total 97.9 - gearhead 44.9); rear X91.6
MOTOR_SHAFT_D=4.0; MOTOR_SHAFT_L=17.5
MOTOR_FACE=189.5; MOTOR_Y=13.5
MOTOR_PILOT_D=6.4; MOTOR_PILOT_L=2.0
COUPLING_OD=20.0; COUPLING_L=24.0; COUPLING_BORE=6.0 # NBK MLR-20C-6-6

# Purchased exact / published component dims
LAPP_OD=17.6; LAPP_CMAX=26.5; LAPP_THREAD_L=6.5; LAPP_SW=16.0
ACE_BODY_OD=12.0; ACE_ROD_OD=4.0; ACE_STROKE=60.0; ACE_EXTENDED=152.0   # F25: ACE GS-12-60-V4A (catalogue L ext 152, stroke 60), CONFIRMED
# F25: ACE catalogue L is the bare spring (fittings ordered separately, GS-12-xx-AA; nb-parts convention GL = L + L1 + L2), DERIVED.
# End fittings A3,5-V4A eye (M3.5x0.6) both ends: face-to-eye-centre 8.0, eye OD 8, bore 4.1 - ESTIMATED from the ACE GS-8/10/12
# accessory drawing numbers (12 / 8 / 4.1); confirm on the ACE CAD file before ordering.
ACE_EYE_L=8.0; ACE_EYE_OD=8.0; ACE_EYE_BORE=4.1; ACE_EYE_W=4.0
ACE_BODY_L=84.0                     # body tube length from the body-end face, ESTIMATED (compressed 92 - rod stub)
ACE_MARGIN=3.0                      # required margin of the bare length to both ends of the stroke, ESTIMATED
SP13_PLUG_OD=18.0; SP13_PLUG_L=48.0 # retailer/manufacturer class dimensions, exact connector still sample-gated
SP17_PLUG_OD=24.6; SP17_PLUG_L=56.5; SP17_PANEL_OD=25.0; SP17_PANEL_THREAD=17.0; SP17_PANEL_L=19.7
NUCLEO=(82.5,70.0,12.0)
CINCON=(57.9,36.8,12.7)
# F20 (2026-11-20) Cincon thermal mount, HOLD-P3: baseplate UP, bonded to the underside of the removable Al service
# cover L01 (7 mm, outer face = housing top) via 0.5 mm pad; 4x DIN 912 M3x18 from the pin side into blind taps in the cover.
CINCON_XC=155.0; CINCON_YC=0.0                 # unchanged X/Y over the motor pair, ESTIMATED
CINCON_HOLE_PITCH=(47.2,26.15)                 # CQB150W drawing 1.86" x 1.030", DERIVED (4 inserts ESTIMATED)
CINCON_HOLE_R=1.6                              # option "-C" clear insert D3.2, DERIVED (datasheet)
CINCON_PIN_ROW_DX=50.8                         # pin-row pitch 2.000", DERIVED
CINCON_PIN_L=4.1                               # 0.16" min, DERIVED
CINCON_PIN_Y_IN=(-7.62,0.0,7.62)               # 3 input pins @0.300" (rear row, toward SP17), DERIVED pitch / ESTIMATED order
CINCON_PIN_Y_OUT=(-7.62,-3.81,0.0,3.81,7.62)   # 5 output pins @0.150" (front row, toward 470 uF), DERIVED pitch / ESTIMATED order
CINCON_PIN_R=0.75                              # D1.5 envelope for all pins, ESTIMATED
THERMAL_PAD_T=0.5                              # silicone pad ~3 W/mK, ESTIMATED
ISO4762_M3=(2.75,3.0)                          # DIN 912 / ISO 4762 M3 head dk/2, k, CONFIRMED standard
CINCON_SCREW_L=18.0                            # 12.7 module + 0.5 pad + 4.8 thread (1.6d) in cover, DERIVED
COVER_TAP_DEPTH=5.3                            # blind M3 in 7 mm cover, 1.7 mm skin left, no through hole, ESTIMATED
# F20 24 V bus protection per POWER_BUDGET_F19 (envelopes, ESTIMATED unless noted).
BUS_CAP_330=(5.0,16.0)       # 330 uF/50 V low-ESR radial D10x16 (UHE1H331MPD class), ESTIMATED
BUS_CAP_470=(5.0,20.0)       # 470 uF/50 V low-ESR radial D10x20 (UHE1H471MPD class), ESTIMATED
SMB_DO214AA=(5.6,3.9,2.6)    # SMBJ26A DO-214AA max L(incl. leads) x W x H, CONFIRMED JEDEC outline
SHUNT_R_ENV=(30.0,16.0,9.0)  # 10 Ohm 10 W Al-housed (Arcol HS10 / Vishay RH010 class) L x W x H incl. tabs, ESTIMATED
SHUNT_R_TAB=(6.0,3.0)        # mounting tab length / thickness, holes at tab centres, ESTIMATED
SHUNT_BOARD=(30.0,14.0,1.6)  # comparator 27.0/26.0 V + MOSFET board, PCB, ESTIMATED
MPRLS=(17.8,16.7,7.5)
NICHICON_D=18.0; NICHICON_L=25.0
BTS_SCREEN=(50.0,50.0,43.0) # board-dependent HOLD
POLOLU_5577=(25.4,25.4,9.0)
POLOLU_5571=(25.4,25.4,9.0)
WAVESHARE_27479=(42.8,15.2,4.75)
VIDEO_SCREEN=(43.0,16.0,15.0)  # Delta TR-1D*P2 packaging screen

# F25 (2026-11-20) electronics cover L01 reshaped to the Proteus principle (DRW-002-745 + 375 + 744): the plug is flush with the
# housing top (Z75) and the lift base FAL-002-067 sits on the housing top over the cover rear end (as the Proteus cover U-slot end
# under the lift). Only a central pad stays raised 7 mm over the Cincon (F20 heat sink); it is narrower than the side links.
SERVICE_Z=75.0                                 # housing top = plug / lid top, DERIVED (BODY_TOP)
SERVICE_T=7.0                                  # raised pad thickness over the plug (Cincon / shunt heat sink, F20), ESTIMATED
SERVICE_PAD_X=(74.0,184.0)                     # pad X: front tongue over the housing top .. 0.07 behind the Cincon end X183.93, ESTIMATED
SERVICE_PAD_HW=25.0                            # pad half width: inside the side links (|Y| 25.9), ESTIMATED
SERVICE_L=SERVICE_PAD_X[1]-SERVICE_PAD_X[0]; SERVICE_W=2*SERVICE_PAD_HW; SERVICE_CX=(SERVICE_PAD_X[0]+SERVICE_PAD_X[1])/2  # 110 x 50, PX1 ESTIMATED
SERVICE_LID_T=2.4                              # flush lid behind the pad (Z72.6..75, over the STM32 top Z72.1), ESTIMATED
SERVICE_PAD_GROOVE=(165.0,7.5,5.0)             # gas-spring groove in the pad top: X start, half width, depth (floor Z77), ESTIMATED
TAP_LEAD=2.5                                   # blind-tap allowance beyond the thread: >= 3P plug-tap chamfer (M4: 2.1), ESTIMATED
TAP_SKIN=1.5                                   # material left below a blind tap, ESTIMATED
ISO7380_M4=(3.8,2.2)                           # ISO 7380 M4 head dk/2, k, CONFIRMED standard
COVER_FIX_XY=(80.0,19.0)                       # 2x M4 cover screws at the front (Proteus FIX-002-518 front pair |Y|19, DERIVED); X ESTIMATED
COVER_FIX_L=12.0                               # PX1 ISO 7380 M4x12 (Proteus M4x8 in a 2.5 ear; PX1 pad 7.0), ESTIMATED
COVER_FIX_ENGAGE=COVER_FIX_L-SERVICE_T         # 5.0 mm in the housing-top boss, DERIVED
COVER_FIX_TAP_DEPTH=COVER_FIX_ENGAGE+TAP_LEAD  # 7.5, DERIVED
COVER_FIX_BOSS_R=3.5                           # internal boss under the housing top wall, ESTIMATED
# F25: camera-cable fitting holder (Proteus FAL-002-086 role: M12 gland + valve + sealed feed-through) moved off the cover onto the
# housing top behind the lift base; PX1 plate form 32 x 68 x 7 keeps the F22 passages (Ø8 / Ø4) and the F21/F23 gland exit Z102.
HOLDER_X=(258.0,290.0); HOLDER_T=7.0           # ESTIMATED
HOLDER_SCREW_XY=(284.0,30.5)                   # 2x M3x12 ISO 7380 into the former cover pilot holes (solid side rails), ESTIMATED
SERVICE_TOOL_POINTS=((COVER_FIX_XY[0],COVER_FIX_XY[1]),(COVER_FIX_XY[0],-COVER_FIX_XY[1]),
                     (HOLDER_SCREW_XY[0],HOLDER_SCREW_XY[1]),(HOLDER_SCREW_XY[0],-HOLDER_SCREW_XY[1]))
# F22 (2026-11-20) DRW-002-745 "Crawler Cover Parts": FAL-002-059 "Cover Electronic" is the TOP electronics cover of the
# CRP150 housing (not a rear cover). Read from the 1:1 views (scale checked on the M4 thread 4.0-4.3 and the M12 gland hex):
PROTEUS_COVER_L=157.5; PROTEUS_COVER_W=53.0; PROTEUS_COVER_T=7.1  # outline incl. screw ears, DERIVED (+-0.3)
PROTEUS_COVER_EAR_T=2.5                       # screw ears at both ends, outer-face level, DERIVED
PROTEUS_COVER_M4=(149.5,38.0,40.0)            # 4x FIX-002-518 M4x8 button: X pitch, |Y| pitch front / rear, DERIVED (+-0.5)
PROTEUS_HOLDER=(38.8,20.3,16.3)               # FAL-002-086 cable-fitting holder L x W x H on the cover, DERIVED
PROTEUS_VALVE_FROM_FRONT=(30.8,17.4)          # valve FSS-001-843/844 axis: from cover front end / from centreline, DERIVED
PROTEUS_GLAND_AXIS=(15.4,9.6)                 # M12 CAB-002-461 axis (parallel to cover, toward the U-slot end): |Y| / above cover, DERIVED
PROTEUS_FEED_BORE_D=8.0                       # vertical cable bore holder->cover, sealed by SEA-001-861 10x1.5, DERIVED
# Sealing principle per 745 C-C: the cover is a PLUG in the housing-top opening with the 110x1.5 O-ring (SEA-002-721,
# CONFIRMED part list) in a groove round its periphery = RADIAL seal against the opening wall (not a face seal).
SERVICE_ORING_OEM_REFERENCE=(110.0,1.5)       # SEA-002-721, CONFIRMED part list; historical OEM reference ONLY
# PX1 DESIGN ASSUMPTION (2026-11-22): candidate 115x1.5 on the SAME existing
# service-plug groove; original 110x1.5 yields ~8% perimeter stretch.
# 115x1.5 reduces calculated stretch to ~3.37%; NOT supplier-verified,
# NOT pressure-qualified. Side-cover lobed 190x1.5 seal is unchanged.
# Recheck groove squeeze, fill, extrusion clearance and 0.7 bar in CAD/bench.
SERVICE_ORING=(115.0,1.5)                     # PX1 ASSUMED candidate, NOT SEA-002-721 OEM
PASSAGE_ORING=(10.0,1.5)                      # SEA-001-861 (745 pos.15), CONFIRMED part list
GLAND_PASSAGE_ORING=(16.0,1.5)                # PX1: around the M12 bore (Proteus has 10x1.5 round an 8 mm bore), ESTIMATED
SERVICE_PLUG_L=143.0; SERVICE_OPEN_W=53.0; SERVICE_PLUG_R=6.6   # plug body = housing opening, DERIVED from 745 (+-0.5)
SERVICE_OPEN_X0=88.0; SERVICE_OPEN_X1=SERVICE_OPEN_X0+SERVICE_PLUG_L   # X88..231: motors X91.6..207.1 + cover electronics, ESTIMATED
SERVICE_PLUG_CLR=0.05                         # radial clearance spigot/opening, ESTIMATED (H8/f7 class)
SERVICE_SPIGOT_H=4.0; SERVICE_SPIGOT_WALL=2.5 # spigot rim under the PX1 plate = housing top wall Z71..75; hollow so the
                                              # Cincon/shunt keep the Z75 cover underside as heat sink, ESTIMATED
SERVICE_RGROOVE_Z=73.0; SERVICE_RGROOVE_W=2.0; SERVICE_RGROOVE_D=1.10  # groove in the spigot periphery, ESTIMATED
SERVICE_RGLAND_D=SERVICE_RGROOVE_D+SERVICE_PLUG_CLR                    # 1.15 radial gland -> 23.3 % nominal squeeze, DERIVED
PASSAGE_GROOVE_D=1.15; PASSAGE_GROOVE_W=2.0   # face grooves (cover underside) round the valve / gland passages, ESTIMATED
VALVE_SEAT_Z0=77.0                            # valve body counterbore from the cover top, Ø4 vent below, ESTIMATED
SERVICE_RGROOVE_ROOT_P=(2*((SERVICE_PLUG_L-2*SERVICE_PLUG_CLR-2*SERVICE_RGROOVE_D)+(SERVICE_OPEN_W-2*SERVICE_PLUG_CLR-2*SERVICE_RGROOVE_D))
                        -(8-2*math.pi)*(SERVICE_PLUG_R-SERVICE_PLUG_CLR-SERVICE_RGROOVE_D))   # 373.4 groove-root perimeter, DERIVED
SERVICE_ORING_STRETCH=SERVICE_RGROOVE_ROOT_P/(math.pi*SERVICE_ORING[0])-1                     # candidate ~3.37 % ID stretch, ANALYTIC (verify)
SERVICE_ORING_CS_INST=SERVICE_ORING[1]/math.sqrt(1+SERVICE_ORING_STRETCH)                     # candidate stretched section, ANALYTIC
# Guard against silent reintroduction of the OEM-labelled 110 mm ring into the 115 mm design candidate.
# Engineering screening only; pressure qualification and supplier confirmation remain outstanding.
assert 0 <= SERVICE_ORING_STRETCH <= 0.05, 'service ring stretch exceeds preliminary 5% limit'
assert 0.15 <= (SERVICE_ORING_CS_INST-SERVICE_RGLAND_D)/SERVICE_ORING_CS_INST <= 0.35, 'radial seal squeeze outside 15-35% screen'


# F18 camera lift per DRW-002-744 (Crawler Lift Parts) + DRW-002-752 (Lift Housing), folded state theta=0.
# Origin A = clamp axle FSS-002-089 (M10, 3x DIN2093) = pivot of central lever ASS-002-723.
# In PX1 coordinates "toward camera" = -X. Tags: CONFIRMED / DERIVED / ESTIMATED.
# F25 (2026-11-20): Proteus lift geometry restored. The base stands on the housing top Z75 (over the flush cover rear end, as the
# Proteus cover U-slot end under the lift), not on a 7 mm plate; the PX1 yoke of F24 is removed and C / D are the 752 pivots.
LIFT_BASE_L=55.0; LIFT_BASE_W=68.7            # FAL-002-067 54.8..55.5 x 68.7, DERIVED (744 top/side 1:1.5)
LIFT_A_ABOVE_BASE=22.9                         # A above base seating face, DERIVED (744 side view)
LIFT_BASE_BEHIND_A=10.2                        # base rear end behind A, DERIVED (744 side view)
LIFT_A_Z=BODY_TOP+LIFT_A_ABOVE_BASE            # 97.9: base on the housing top (Proteus), DERIVED
LIFT_AB=(38.2,-12.5)                           # side-link base pivot FSS-002-075 rel. A, DERIVED (|AB|=40.2)
LINK_L=200.1                                   # AC = BD (central lever / side links FSS-002-068), DERIVED (200.1/200.0)
LIFT_THETA_MAX=69.0                            # stop, ESTIMATED (F18 value kept; raised axis 259.7 with the 752 axis 72.9)
LIFT_CAT_RANGE=(70.0,257.0)                    # CRP150 catalogue manual lift, camera axis above floor, CONFIRMED
LIFT_GAS_E=(7.0,-16.8)                         # gas spring lower eye rel. A; Proteus (7.0,-24.8) DERIVED sits in a base boss in the housing-top
                                               # pocket (375 A-A 20.7x9.9); PX1 has the STM32 under that spot, no boss: +8 up, ESTIMATED
LIFT_GAS_G=(125.0,1.0)                         # upper eye on lever rel. A, DERIVED (744, +-2)
LIFT_SIDE_Y=27.9; LIFT_SIDE_T=4.0; LIFT_SIDE_H=15.0  # F25: side links back on 744 top view |Y|27.9, t4 h15, DERIVED
LIFT_SHIM_D=0.4; LIFT_SHIM_B=0.25              # brass shims FBR-002-750 (0.4, D pin, housing side) / FBR-002-751 (0.25, B axle, base lug), CONFIRMED part list (744)
LIFT_SHIM_R=(4.05,6.5)                         # shim bore / outer radius, ESTIMATED
LIFT_LEVER_PLATE_W=54.4                        # FSS-002-073 lever sheet plate width, DERIVED
LIFT_CHEEK_Y=(6.6,9.6)                         # central-lever cheeks (fork 24 wide at C, DERIVED) around gas spring, ESTIMATED
CAM026_ENVELOPE=(120.0,74.0,74.0)              # GAP catalogue sy1083 L x W x H, CONFIRMED (0.864 kg)
CAM026_MASS_KG=0.864                           # CONFIRMED catalogue
CRP150_CATALOGUE_LWH=(307.0,133.0,110.0)       # GAP sy1083 CRP150 L x W x H, CONFIRMED (what H includes is not stated)
# F25 interpretation of H110 (DERIVED): overall height wheels-on-floor to the top of the folded lift with the camera fitted. The Proteus
# reconstruction (base on the housing top, 752 literal) gives camera top 109.9 / lever plate 106.9 / 752 housing 107.9 / light window
# FAL-002-080 111.9: the catalogue 110 is reproduced within the 744 reading tolerance (A height 22.9 read at 1:1.5, +-2).
FOLDED_H_LIMIT=CRP150_CATALOGUE_LWH[2]+2.0     # 112.0 limit for the copied structure, DERIVED
# F24 (2026-11-20) lift housing per DRW-002-752 "LIFT HOUSING" (all views 1:1; vector geometry of the PDF; scale checked on
# FIX-000-637 M4 button head dk 7.43 (ISO 7380 7.6) + hex 2.73, FIX-002-517 M3 CSK Torx T10 2.86 (2.74) / head 5.65..6.03).
# Frame: axial = behind the lock-ring front face (+X in PX1), up = above the camera axis, Y about the housing centre.
LH752_LOCK=(48.64,35.81,22.99)                 # FSS-001-889 lock ring: front OD / rear OD / length, DERIVED
LH752_LOCK_BORE=34.16                          # lock-ring front bore (camera seat), DERIVED (A-A)
LH752_SPIGOT=(3.65,34.0)                       # FAL-002-071 front spigot under the ring: front face axial / OD, DERIVED (A-A 3.65, 35.1-0.9 ESTIMATED)
LH752_NECK_OD=35.1                             # visible neck lock ring -> body, DERIVED (A-A 35.1, side view 35.2)
LH752_BODY_X=(26.92,53.91,55.63)               # body front / body rear face / lift cover FAL-002-081 outer face, axial, DERIVED
LH752_W=(46.04,41.97)                          # body width upper / lower part, DERIVED (C-C, rear view 46.04 / 41.8..41.97)
LH752_Z=(-23.0,35.0,39.0)                      # body bottom / body top / light cover FAL-002-080 top, DERIVED (A-A, side, C-C)
LH752_C=(72.42,24.99)                          # pivot C = axle FSS-002-076 "Axle Lever top" in the rear fork, DERIVED (A-A)
LH752_D=(34.39,12.03)                          # pivot D = side-link taps both sides, DERIVED (side view hole + C-C taps)
LH752_C_AXLE_D=7.05                            # FSS-002-076 Ø (A-A 7.05, rear view 6.98), DERIVED
LH752_FORK=(12.22,23.02,79.37)                 # C fork lugs |Y| inner / outer, lug end axial, DERIVED (gap 24.45)
LH752_D_TAP=(5.21,8.0)                         # D blind taps: drawn D1 5.21 / depth 8.0 (C-C), DERIVED; thread M6 class ESTIMATED
LH752_COVER=(45.02,40.9,1.72)                  # lift cover FAL-002-081 W x H x t (Z axis-23..+17.9), DERIVED
LH752_COVER_SCREWS=((19.69,14.51),(17.53,-19.47))  # 4x FIX-002-517 M3x8 CSK: (|Y|, up) upper / lower pair, DERIVED
LH752_GLAND=(-5.25,7.85)                       # CAB-002-461 M12x1.5 cable fitting on the rear face (Y, up), DERIVED +-1 (not used in PX1)
LH752_LIGHT=(44.9,18.2,27.6)                   # light cover FAL-002-080 on top: centre axial / length / width, DERIVED
LIFT_HOUSING_W=LH752_W[0]; LIFT_HOUSING_L=LH752_BODY_X[2]-LH752_BODY_X[0]   # 46.04 x 28.71 body + lift cover, DERIVED
CAM_Z=LIFT_A_Z-LH752_C[1]                      # 72.91 camera axis folded = A level - 752 C height (752 literal), DERIVED; catalogue 70 +-5
LH_REAR_X=14.0                                 # lift-cover outer face in PX1: 4.0 to the crawler front X18, ESTIMATED
LH_X0=LH_REAR_X-LH752_BODY_X[2]                # -41.63 lock-ring front face, DERIVED
LIFT_A_X=LH_X0+LH752_C[0]+LINK_L               # 230.89: C on the 752 pattern, AC = 200.1, DERIVED (from LH_REAR_X ESTIMATED).
                                               # Proteus check: A <= ~231 or the 752 body hits the crawler nose (X18, top Z75); the
                                               # gas spring E (A-7) then lies in the cover-rear U-slot zone (745: U 21 x 20), DERIVED.
CAM_REAR_X=LH_X0-0.5                           # camera rear face = lock-ring front -0.5, ESTIMATED (was -40.5)
LH_LUG_Z0=CAM_Z+18.0                           # C fork lug bottom = 752 lug bottom (axis+18), above lift-cover top +17.9, DERIVED
LH_SPINE_Y=6.4                                 # central cable spine between the fork lugs (F21 C-arm), ESTIMATED
LIFT_C_RING=(3.25,5.2,0.8,1.0)                 # DIN 471 7x0.8 on FSS-002-076 in Ø11.0x1.0 lug recesses: groove r / ring r / t / recess, ESTIMATED
LIFT_D_PIN=(2.95,3.95,LIFT_SIDE_Y+LIFT_SIDE_T/2-LH752_W[0]/2+0.1)  # FSS-002-079 stepped pin: M6 thread r / Ø8 journal r / journal length
                                               # (shim + link + 0.1), ESTIMATED / DERIVED
LIFT_D_RING=(3.75,5.9,0.8)                     # DIN 471 8x0.8 (744 list 8x0.8 x4): groove r / ring r / t, ESTIMATED
CAM_DROP=LIFT_A_Z-CAM_Z                        # C/A level to camera axis = 752 C height 24.99, DERIVED
CAM026_MEASURED_BASE_OD=62.5; CAM_R=CAM026_MEASURED_BASE_OD/2; CAM_LEN=132.0  # ASM000 boom variant (head 132), DERIVED reference only
CAM_GLAND_XY=(272.0,0.0); VALVE_XY=(272.0,18.0) # camera cable M12 gland + pressure valve in the fitting holder (F25), ESTIMATED
# F21 (2026-11-20) lift base fixing: DRW-002-744 pos.14 FIX-000-598 "M4 X 12 SKT CAPHEAD A2" x4 (CONFIRMED part list) = ISO 4762 M4x12 A2.
# Pattern from 744 vector geometry (top view + A-A, 1:1.5; scale re-checked on the M4 thread stub 4.00 and socket s3 2.95).
LIFT_M4_DRW_PATTERN=((-1.0,27.9),(20.0,25.0))  # (dx toward camera from A, |Y|): outer pair at A (-1.0 = 1.0 behind A), inner pair
                                               # 20.0 toward camera; DERIVED (+-0.3). Inner pair seen protruding 4.95 below base in A-A.
LIFT_M4_Y_PX1=(27.9,21.0)                      # F25: outer pair |Y|27.9 = 744 (DERIVED), into the housing top (internal boss).
                                               # Inner pair lands on the flush cover lid: |Y|25 would cut the 110x1.5 groove of the
                                               # plug spigot -> |Y|21 (inside the spigot inner wall 23.95), ESTIMATED deviation -4.0
LIFT_M4_X=(LIFT_A_X-LIFT_M4_DRW_PATTERN[0][0],LIFT_A_X-LIFT_M4_DRW_PATTERN[1][0])  # X231.89 / X210.89, DERIVED
ISO4762_M4=(3.5,4.0,3.0)                       # head dk/2, k, socket s - ISO 4762 M4, CONFIRMED standard
LIFT_M4_SCREW_L=12.0                           # FIX-000-598 M4x12, CONFIRMED (part list)
LIFT_M4_PROTEUS_PROTRUSION=4.95                # thread below base in 744 A-A, DERIVED -> Proteus clamp length 7.05
LIFT_M4_CLAMP=7.0                              # head bearing 7.0 above base seat (8 mm plate, 1.0 Ø8 counterbore), DERIVED from 7.05 / ESTIMATED cbore
LIFT_M4_ENGAGE=LIFT_M4_SCREW_L-LIFT_M4_CLAMP   # 5.0 mm (1.25d), DERIVED
LIFT_M4_TAP_DEPTH=LIFT_M4_ENGAGE+TAP_LEAD      # 7.5 blind tap (standard plug tap, no thread milling needed), DERIVED
LIFT_M4_BOSS_R=4.0                             # bosses under the housing top (outer pair) / under the cover lid (inner pair), ESTIMATED
LIFT_M4_BOSS_Z0=SERVICE_Z-LIFT_M4_TAP_DEPTH-TAP_SKIN   # 66.0 boss bottom, DERIVED
LIFT_M4_HOLE_R=2.25; LIFT_M4_CBORE=(4.0,1.0)   # Ø4.5 clearance (ISO 273 medium) CONFIRMED standard; Ø8 x 1.0 counterbore ESTIMATED
# F21 camera harness on the lift: LAPP 0028679 OD 5.4 (CONFIRMED catalogue); min bend 5xD flexing / 3xD fixed (CONFIRMED LAPP).
HARNESS_OD=5.4
HARNESS_R_FLEX=5*HARNESS_OD                    # 27.0, dynamic spans (CONFIRMED rule)
HARNESS_R_FIXED_MIN=3*HARNESS_OD               # 16.2, fixed installation (CONFIRMED rule)
HARNESS_R_FIXED=17.0                           # static bends: riser top in the C-arm and gland exit, ESTIMATED (>=16.2)
# F23 (2026-11-20) camera cable exit at the SP13 (HOLD H07 closed): option (b) chosen - LAPP kept, straight SP13 without its
# rear clamp nut inside a potted bend tail. Option (a) right-angle M12-A 8p moulded (binder 77-3434 family) evaluated in
# tools/lift/check_lift_kinematics.py: elbow collides with the housing front, binder PVC Ø6.0 needs R60 moving -> rejected.
SP13_PLUG_KEEP=30.0                            # SP13 plug kept X-36..-6: coupling nut + insert + solder cups, clamp nut removed, ESTIMATED
HARNESS_TAIL_X0=-6.0                           # cable leaves the potted solder-cup end, = HARNESS_START X, ESTIMATED
HARNESS_TAIL_XE=-1.0                           # start of the fixed R17 bend: tail shell 2.4 clear of the body corner X18/Z75, ESTIMATED
HARNESS_TAIL_PHI=70.0                          # fixed S-riser: R17 up 70 deg -> straight -> R17 back to +X at P (X39.8), ESTIMATED;
                                               # P must stay <= X41 or the R27 span P->clip 1 needs a loop at theta>=60 (F23 check)
HARNESS_TAIL_WALL=1.5                          # potted tail shell around the cable (PA12 print + PU potting), ESTIMATED
HARNESS_TAIL_LINE=8.0                          # tail covers the first 8 mm of the riser line, then the C-arm channel takes over, ESTIMATED
HARNESS_TAIL_SLEEVE=(10.5,6.0,2.0)             # sleeve over the SP13 body (r9): outer r / overlap / end-cap length, ESTIMATED
HARNESS_GUIDE_X=(90.0,190.0)                   # 2 open clips on lever plate FSS-002-073 (cable slides through), ESTIMATED;
                                               # F25 (A X230.9, P 5.4 behind C): clip 1 >= X88 keeps P->clip 1 loop-free, clip 2 <= X192
HARNESS_LOOP_Y=-22.0                           # lateral S-loop on the lever plate (plate +-27.2), ESTIMATED
HARNESS_LOOP_A=math.degrees(math.acos(1-abs(HARNESS_LOOP_Y)/(2*HARNESS_R_FLEX)))  # 53.7 deg per arc, DERIVED
HARNESS_LOOP_CX=140.0                          # loop centre X between the clips (loop X96.5..183.5), ESTIMATED
HARNESS_FIX_TURN=75.0                          # fixed bend-guide arc at the gland exit (heading -15 -> -90), ESTIMATED; 75 keeps the
                                               # span-2 crest at Z119.3 (harness bbox inside DN150)
GLAND_EXIT_Z=SERVICE_Z+.5+LAPP_CMAX            # 102.0 top of Skintop M12 (cable exits vertically), DERIVED

# Integrated packaging datums: ESTIMATED engineering dimensions, mm.
# Same six-wheel topology; no change to gear or motor axes.
MIDDLE_INNER_Y=26.8
MIDDLE_BUSH_W=3.0
IDLER_PIN_INNER_Y=27.0
SUPPORT_BOSS_INNER_Y=26.5
LIFT_PLATE_TOP_Z=LIFT_A_Z+9.0          # 106.9 lever plate FSS-002-073 top (A+7.5 +-1.5), ESTIMATED
HARNESS_TOP_Z=LIFT_PLATE_TOP_Z+HARNESS_OD/2+.2   # 109.8: F21 cable rests on the lever plate +0.2, DERIVED
# F21 route (folded, theta=0): start in SP13 backshell, heading +X. ('S',len) straight; ('A',R,deg,axis) arc about axis.
# Span-2 S-bend to the fixed gland bend guide: solved so the route ends exactly at the gland exit (checked at build).
_HK=math.radians(90-HARNESS_FIX_TURN)          # dynamic heading at fixed point K (15 deg below +X)
_KX=CAM_GLAND_XY[0]-HARNESS_R_FIXED+HARNESS_R_FIXED*math.cos(math.radians(HARNESS_FIX_TURN))
_KZ=GLAND_EXIT_Z+HARNESS_R_FIXED*math.sin(math.radians(HARNESS_FIX_TURN))
HARNESS_SB=math.degrees(math.acos((HARNESS_TOP_Z+HARNESS_R_FLEX+HARNESS_R_FLEX*math.cos(_HK)-_KZ)/(2*HARNESS_R_FLEX)))  # S-bend up angle, DERIVED
_SB=math.radians(HARNESS_SB)
_XS=_KX-HARNESS_R_FLEX*math.sin(_SB)-HARNESS_R_FLEX*(math.sin(_SB)+math.sin(_HK))
_LA=math.radians(HARNESS_LOOP_A); _LX0=HARNESS_LOOP_CX-2*HARNESS_R_FLEX*math.sin(_LA)
_TPH=math.radians(HARNESS_TAIL_PHI)
HARNESS_TAIL_LD=(HARNESS_TOP_Z-CAM_Z-2*HARNESS_R_FIXED*(1-math.cos(_TPH)))/math.sin(_TPH)   # riser line length, DERIVED
HARNESS_P_X=HARNESS_TAIL_XE+2*HARNESS_R_FIXED*math.sin(_TPH)+HARNESS_TAIL_LD*math.cos(_TPH)  # clamp P X (was 32.0), DERIVED
HARNESS_ROUTE=(('S',HARNESS_TAIL_XE-HARNESS_TAIL_X0),('A',HARNESS_R_FIXED,HARNESS_TAIL_PHI,(0,-1,0)),('S',HARNESS_TAIL_LD),
    ('A',HARNESS_R_FIXED,HARNESS_TAIL_PHI,(0,1,0)),                       # -> P: clamped in lift-housing C-arm slot (fixed)
    ('S',_LX0-HARNESS_P_X),                                  # through clip 1 (X74)
    ('A',HARNESS_R_FLEX,HARNESS_LOOP_A,(0,0,-1)),('A',HARNESS_R_FLEX,HARNESS_LOOP_A,(0,0,1)),
    ('A',HARNESS_R_FLEX,HARNESS_LOOP_A,(0,0,1)),('A',HARNESS_R_FLEX,HARNESS_LOOP_A,(0,0,-1)),   # S-loop on the lever plate
    ('S',_XS-(HARNESS_LOOP_CX+2*HARNESS_R_FLEX*math.sin(_LA))),          # through clip 2 (X176)
    ('A',HARNESS_R_FLEX,HARNESS_SB,(0,-1,0)),('A',HARNESS_R_FLEX,HARNESS_SB+90-HARNESS_FIX_TURN,(0,1,0)),  # -> K (fixed)
    ('A',HARNESS_R_FIXED,HARNESS_FIX_TURN,(0,1,0)),                       # printed bend guide on the gland (fixed)
    ('S',6.0))                                                            # into the Skintop bore
HARNESS_START=(HARNESS_TAIL_X0,0.0,CAM_Z)      # F23: at the potted SP13 solder-cup end, = CAM_Z
HARNESS_SEG_P=4; HARNESS_SEG_K=12              # route index after which the point is P (housing clamp) / K (gland guide)
# F23 option (a) data for the evaluation in tools/lift/check_lift_kinematics.py (not modelled as the chosen option):
CAMEXIT_A_ELBOW=(14.5,27.0)                    # binder 77-3434 M12-A 8p right-angle moulded: nut Ø x length along the mating axis, ESTIMATED
CAMEXIT_A_CABLE_OD=6.0; CAMEXIT_A_R_FLEX=60.0  # binder PVC cable Ø6.0 / moving bend >= 60 (CONFIRMED binder, procurement 20.11)
# F23 internal camera cable (fixed, >= 3xD): Skintop bore -> Ø8 housing passage -> R16.5 to -X in the Y0 slot between the Z40
# bevels, over the 61800 -> jacket end + potted breakout boot -> 6-core bundle -> 6-pole wire-to-wire service connector beside the
# STM32 board (under the plug opening, outside the motor extraction envelope). PX1-side wires to RS485 / 12 V / balun: HOLD.
INNER_R=16.5                                   # LAPP bend below the passage, >= 3xOD 16.2; limited by the 61800 top Z54.5, ESTIMATED
INNER_START=(CAM_GLAND_XY[0],CAM_GLAND_XY[1],GLAND_EXIT_Z-6.0)   # = end of HARNESS_ROUTE inside the Skintop (Z96), DERIVED
INNER_BEND_Z0=SERVICE_Z+.5                     # bend starts at the Skintop thread bottom Z75.5 (cable offset 0.63 at Z71 in the Ø8), ESTIMATED
INNER_ROUTE=(('S',INNER_START[2]-INNER_BEND_Z0),('A',INNER_R,90.0,(0,1,0)),('S',0.3))   # jacket end X255.2 Z59 (F25: 2.0->0.3 for the Ø3.3 bundle R10), DERIVED
INNER_BOOT=(3.4,8.0,6.0)                       # breakout boot (heat-shrink + potting) r / length / over the cores, ESTIMATED
BUNDLE_CORE_OD=1.1                             # 0.25 mm2 single core incl. insulation (UL1007/1061 class 1.0..1.2), ESTIMATED
BUNDLE_OD=3*BUNDLE_CORE_OD                     # 3.3: 6 cores laid round (6-around-1 packing), d_bundle = 3 d_core, DERIVED
BUNDLE_R=10.0                                  # >= 3 x BUNDLE_OD 9.9, ESTIMATED
BUNDLE_Z=64.0                                  # bundle level for the -Y crossing over the Z40 bevel (top <= Z61.4 at X<=238), ESTIMATED
BUNDLE_RISE=math.degrees(math.acos(1-(BUNDLE_Z-(INNER_BEND_Z0-INNER_R))/(2*BUNDLE_R)))   # S-rise angle 43.8 deg, DERIVED
BUNDLE_ROUTE=(('S',.5),('A',BUNDLE_R,BUNDLE_RISE,(0,1,0)),('A',BUNDLE_R,BUNDLE_RISE,(0,-1,0)),
    ('A',BUNDLE_R,90.0,(0,0,1)),('S',1.5),('A',BUNDLE_R,90.0,(0,0,-1)),('S',.5))   # -> Y-21.5 heading -X into the connector
SVC_CONN=(16.5,7.0,10.0)                       # 6-pole 2.0 mm wire-to-wire, mated envelope L x W x H (JST PH/PHD class), ESTIMATED
SVC_CONN_ZC=60.5                               # F25: 65 -> 60.5 under the lid M4 boss (Z66); coupling top Z53.9 at |Y|18, ESTIMATED

# ------------------------------- helpers

def wp(s): return cq.Workplane('XY').newObject([s])
def boxc(x,y,z,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(True,True,True)).translate((x,y,z))
def box0(x0,y0,z0,dx,dy,dz): return cq.Workplane('XY').box(dx,dy,dz,centered=(False,False,False)).translate((x0,y0,z0))
def cyl_x(x,y,z,r,l,dir=1):
    base=cq.Vector(x,y,z)
    return wp(cq.Solid.makeCylinder(r,l,base,cq.Vector(dir,0,0)))
def cyl_y(x,y,z,r,l,dir=1):
    base=cq.Vector(x,y,z)
    return wp(cq.Solid.makeCylinder(r,l,base,cq.Vector(0,dir,0)))
def cyl_z(x,y,z,r,l): return wp(cq.Solid.makeCylinder(r,l,cq.Vector(x,y,z),cq.Vector(0,0,1)))
def ring_y(x,y,z,ro,ri,w):
    o=cyl_y(x,y-w/2,z,ro,w); i=cyl_y(x,y-w/2-0.2,z,ri,w+0.4)
    return wp(o.val().cut(i.val()))
def fuse_all(parts):
    s=parts[0].val()
    for p in parts[1:]: s=s.fuse(p.val())
    return wp(s)
def cut(a,b): return wp(a.val().cut(b.val()))
def intervol(a,b):
    return a.val().intersect(b.val()).Volume() # errors must propagate, never become zero

def between(p1,p2,r):
    a=cq.Vector(*p1); b=cq.Vector(*p2); v=b-a
    return wp(cq.Solid.makeCylinder(r,v.Length,a,v.normalized()))

def plate_between(p1,p2,y,t=4,h=14):
    x1,z1=p1; x2,z2=p2; dx=x2-x1; dz=z2-z1
    L=math.hypot(dx,dz); ang=math.degrees(math.atan2(dz,dx))
    p=boxc(0,y,0,L,t,h).rotate((0,0,0),(0,1,0),-ang)
    return p.translate(((x1+x2)/2,0,(z1+z2)/2))

def make_spur_gear(teeth=50,module=1.0,face=4.0,bore=12.0,axis='Y'):
    # Analytical involute reference at 20 degrees. Source pressure angle is unknown.
    # This is explicitly HOLD; never export as a manufacturing tooth definition.
    rp=module*teeth/2; ra=rp+module; rf=rp-1.25*module
    alpha=math.radians(20); rb=rp*math.cos(alpha)
    invol=lambda r: math.sqrt(max(0,(r/rb)**2-1))-math.acos(min(1,rb/r)) if r>=rb else 0
    half=math.pi/(2*teeth)+math.tan(alpha)-alpha
    pts=[]
    for i in range(teeth):
        a=i*2*math.pi/teeth
        for r in [rf]+[max(rf,rb)+(ra-max(rf,rb))*j/7 for j in range(8)]:
            t=a-half+invol(r); pts.append((r*math.cos(t),r*math.sin(t)))
        for r in list(reversed([max(rf,rb)+(ra-max(rf,rb))*j/7 for j in range(8)]))+[rf]:
            t=a+half-invol(r); pts.append((r*math.cos(t),r*math.sin(t)))
    clean=[]
    for pt in pts:
        if not clean or math.dist(pt,clean[-1])>1e-9: clean.append(pt)
    g=cq.Workplane('XY').polyline(clean).close().extrude(face/2,both=True)
    g=g.cut(cq.Workplane('XY').circle(bore/2).extrude(face,both=True))
    if axis=='Y': g=g.rotate((0,0,0),(1,0,0),90)
    elif axis=='X': g=g.rotate((0,0,0),(0,1,0),90)
    return g

def make_bearing(id_,od,w,axis='Y'):
    # Manufacturer boundary envelope: correct full width, not internal rolling geometry.
    p=cq.Workplane('XY').circle(od/2).circle(id_/2).extrude(w/2,both=True)
    if axis=='Y': p=p.rotate((0,0,0),(1,0,0),90)
    elif axis=='X': p=p.rotate((0,0,0),(0,1,0),90)
    return p

def make_seal(id_,od,w,axis='Y'):
    p=cq.Workplane('XY').circle(od/2).circle(id_/2).extrude(w/2,both=True)
    if axis=='Y': p=p.rotate((0,0,0),(1,0,0),90)
    elif axis=='X': p=p.rotate((0,0,0),(0,1,0),90)
    return p

def make_button_screw(x,y,z,length,axis_dir):
    """ISO 7380 M3 button head; head on +axis_dir side, shank goes -axis_dir from bearing face y."""
    hr,hh=ISO7380_M3
    head=cyl_y(x,y,z,hr,hh,dir=axis_dir)
    shank=cyl_y(x,y,z,1.5,length,dir=-axis_dir)
    return fuse_all([head,shank])
def _wd_local_to_world(shape,x,side):
    """Local build: axis +Z from disk back face, lobe toward local -Y. Maps local Z->|Y|, local -Y->+Z (key side)."""
    sh=shape.rotate((0,0,0),(1,0,0),-90).translate((0,WD_BACK_Y,0))
    if side<0: sh=sh.mirror('XZ')
    return sh.translate((x,0,45))
def make_wheel_bolt_assy(x,side):
    """Mini-Cam ASS-002-103 wheel bolt assembly, shown in the 'aligned' state: lobe and spigot D-flat toward the
    key (spigot flat clears the 4x4 key, DERIVED). Turning CW swings the lobe over the hub pocket floor."""
    T=WD_FLANGE_T
    prof=(cq.Workplane('XY').center(0,-WD_FLANGE_E).circle(WD_FLANGE_R).extrude(T)
          .cut(cq.Workplane('XY').box(40,20,T+2,centered=(True,False,False)).translate((0,WD_FLAT,-1))))
    cone=cq.Workplane('XY').add(cq.Solid.makeCone(WD_FACE_R+T,WD_FACE_R,T,cq.Vector(0,0,0),cq.Vector(0,0,1)))
    disk=prof.intersect(cone)
    spig=(cq.Workplane('XY').circle(WD_SPIGOT_R).extrude(-WD_SPIGOT_L)
          .cut(cq.Workplane('XY').box(20,10,WD_SPIGOT_L+2,centered=(True,False,False)).translate((0,-WD_SPIGOT_FLAT-10,-WD_SPIGOT_L-1))))
    disk=disk.union(spig)
    for r,d0,d1 in ((WD_LIP_R,0,WD_LIP_D),(WD_GROOVE_R,WD_LIP_D,WD_GROOVE_D),(WD_SEAT_R,WD_GROOVE_D,WD_SEAT_D)):
        disk=disk.cut(cq.Workplane('XY').circle(r).extrude(d1-d0+.001).translate((0,0,T-d1)))
    disk=disk.cut(cq.Workplane('XY').circle(WD_HOLE_R).extrude(T+WD_SPIGOT_L+2).translate((0,0,-WD_SPIGOT_L-1)))
    hr,hk,hs=ISO7380_M6; zb=T-WD_HEAD_BEAR_D; Rs=(hr*hr+hk*hk)/(2*hk)
    head=cq.Workplane('XY').add(cq.Solid.makeSphere(Rs,cq.Vector(0,0,zb+hk-Rs),angleDegrees1=-90,angleDegrees2=90))
    head=head.intersect(cq.Workplane('XY').circle(hr).extrude(hk).translate((0,0,zb)))
    head=head.cut(cq.Workplane('XY').polygon(6,hs/math.cos(math.pi/6)).extrude(2.0).translate((0,0,zb+hk-2.0)))
    shank=cq.Workplane('XY').circle(M6_COSMETIC_THREAD_R).extrude(-WHEEL_SCREW_L).translate((0,0,zb))
    screw=head.union(shank)
    wri,wro,wh=SCHNORR_M6
    washer=cq.Workplane('XY').circle(wro).circle(wri).extrude(wh).translate((0,0,T-WD_SEAT_D+.005))
    R0,rt,dc=WD_ORING
    oring=cq.Workplane('XY').add(cq.Solid.makeTorus(R0,rt,cq.Vector(0,0,T-dc),cq.Vector(0,0,1)))
    return [('FSS002065_WHEEL_DISK_CAM_ASS002103',_wd_local_to_world(disk,x,side),'metal'),
            ('FIX002105_M6x14_ISO7380_WHEEL_BOLT',_wd_local_to_world(screw,x,side),'shaft'),
            ('FIX002104_M6_SPRING_WASHER_SCHNORR',_wd_local_to_world(washer,x,side),'metal'),
            ('SEA002106_ORING_10x1p8_WHEEL_DISK',_wd_local_to_world(oring,x,side),'seal')]
def lobed_seal_face(o):
    """Closed lobed track (offset o from centreline) in local XY: x=X, y=Z-45. DERIVED, see F10."""
    R=SIDE_SEAL_R; c=SIDE_SEAL_CUSP; half=25.0
    rf=((c*c+half*half)-R*R)/(2*(R-c)); zc=c+rf
    cx=[g for g in GEAR_X]; Rg=R+o; Rf=rf-o
    def P(cxx,cy,r,a): return (cxx+r*math.cos(a),cy+r*math.sin(a))
    phi=math.atan2(zc,half)
    w=cq.Workplane('XY').moveTo(*P(cx[0],0,Rg,math.pi))
    for sgn in (1,-1):
        seq=cx if sgn>0 else cx[::-1]
        for k,g in enumerate(seq):
            first,last=k==0,k==len(seq)-1
            if sgn>0:
                a0=math.pi if first else math.pi-phi; a1=0.0 if last else phi
            else:
                a0=0.0 if first else -phi; a1=-math.pi if last else -(math.pi-phi)
            if sgn>0: am=(a0+a1)/2
            else: am=(a0+a1)/2
            w=w.threePointArc(P(g,0,Rg,am),P(g,0,Rg,a1))
            if not last:
                nx=g+sgn*50; fx=(g+nx)/2; fy=sgn*zc
                b0=math.atan2(-sgn*zc,(g-fx)); b1=math.atan2(-sgn*zc,(nx-fx))
                w=w.threePointArc(P(fx,fy,Rf,-sgn*math.pi/2),P(fx,fy,Rf,b1))
    return w.close()
def lobed_band(o_in,o_out,depth,side,y_face):
    outer=lobed_seal_face(o_out).extrude(depth); inner=lobed_seal_face(o_in).extrude(depth)
    band=wp(outer.val().cut(inner.val()))
    band=band.rotate((0,0,0),(1,0,0),90)          # local y->Z, extrusion -> -Y
    if side>0: return band.translate((0,y_face+depth,45))
    return band.translate((0,-y_face,45))
def make_coupling():
    p=cyl_x(0,0,0,COUPLING_OD/2,COUPLING_L)
    bore=cyl_x(-0.5,0,0,COUPLING_BORE/2,COUPLING_L+1)
    p=cut(p,bore)
    # clamp slot + screw heads (visual)
    p=cut(p,boxc(COUPLING_L/2,0,8.0,2,COUPLING_OD+2,4))
    return p

def make_sp13_plug():
    # F23: rear clamp nut / straight backshell removed (SP13_PLUG_KEEP); cable exit potted in the bend tail.
    body=cyl_x(0,0,0,SP13_PLUG_OD/2,SP13_PLUG_KEEP)
    collar=cyl_x(8,0,0,SP13_PLUG_OD/2+2,12)
    return fuse_all([body,collar])

def make_sp17_panel():
    body=cyl_x(0,0,0,SP17_PANEL_OD/2,SP17_PANEL_L)
    thread=cyl_x(-4,0,0,SP17_PANEL_THREAD/2,8)
    flange=boxc(2,0,0,4,32,32)
    return fuse_all([body,thread,flange])

def make_gland():
    # LAPP M12 brass gland, simplified exact envelope with hex wrench section
    thread=cyl_x(0,0,0,6.0,LAPP_THREAD_L)
    hexp=cq.Workplane('YZ').polygon(6,LAPP_SW/math.cos(math.pi/6)).extrude(8).translate((LAPP_THREAD_L,0,0))
    tail=cyl_x(LAPP_THREAD_L+8,0,0,LAPP_OD/2,max(0.1,LAPP_CMAX-LAPP_THREAD_L-8))
    return cut(fuse_all([thread,hexp,tail]),cyl_x(-.1,0,0,3.5,LAPP_CMAX+.2))


# SOURCE-DRIVEN RECONSTRUCTION. GRAPHIC_APPROX dimensions are not manufacturing tolerances.
components=[]; side_covers=[]
def add(n,p,c): components.append((n,p,c)); return p
profile=[(18,17),(24,11),(278,11),(296,29),(296,73),(294,75),(20,75),(18,73)]
body=cq.Workplane('XZ',origin=(0,34,0)).polyline(profile).close().extrude(68)
body=cut(body,box0(24,-26.5,CAVITY_FLOOR_Z,264,53,75.1-CAVITY_FLOOR_Z))
body=cut(body,box0(WEIGHT_PLATE_X0,-WEIGHT_PLATE_W/2,BODY_Z0-.1,WEIGHT_PLATE_X1-WEIGHT_PLATE_X0,WEIGHT_PLATE_W,WEIGHT_PLATE_H+.1))  # plate recess
body=wp(body.val().fuse(box0(24,-26.5,71,264,53,4).val()))
# F14: threaded bosses for FIX-002-764 (blind, closed top), part of the housing solid.
for _px,_py in PLATE_SCREW_XY:
    body=wp(body.val().fuse(cyl_z(_px,_py,CAVITY_FLOOR_Z-.5,PLATE_BOSS_R,PLATE_BOSS_TOP_Z-CAVITY_FLOOR_Z+.5).val()))
    body=cut(body,cyl_z(_px,_py,BODY_Z0+WEIGHT_PLATE_H-.05,M8_COSMETIC_THREAD_R,PLATE_TAP_TOP_Z-BODY_Z0-WEIGHT_PLATE_H+.05))
# F22: Proteus FAL-002-059 plug opening 143x53 R6.6 (DRW-002-745) in the 4 mm top wall, replaces the 188x53 window.
body=cut(body,boxc((SERVICE_OPEN_X0+SERVICE_OPEN_X1)/2,0,73.0,SERVICE_PLUG_L,SERVICE_OPEN_W,4.2).edges('|Z').fillet(SERVICE_PLUG_R))
# F22: sealed feed-throughs under the cover-rear valve / camera gland (Proteus: Ø8 holder->cover bore, 745 C-C).
body=cut(body,cyl_z(CAM_GLAND_XY[0],CAM_GLAND_XY[1],70.9,PROTEUS_FEED_BORE_D/2,4.2))
body=cut(body,cyl_z(VALVE_XY[0],VALVE_XY[1],70.9,2.0,4.2))
# F25: two M3 pilot holes in the solid side rails for the fitting holder (former cover rear screws). Threads unmodelled.
for sy in (-1,1): body=cut(body,cyl_z(HOLDER_SCREW_XY[0],sy*HOLDER_SCREW_XY[1],67,1.25,8.1))
# F25: blind M4 taps (cosmetic major Ø4) from the housing top with internal bosses (no break-through into the dry cavity):
# cover front pair (M4x10, 3.0 engaged) and the lift-base outer pair per DRW-002-744 (M4x12, 5.0 engaged, Proteus: base on housing).
for (_bx,_by),_br,_tap in (((COVER_FIX_XY[0],COVER_FIX_XY[1]),COVER_FIX_BOSS_R,COVER_FIX_TAP_DEPTH),
                           ((LIFT_A_X-LIFT_M4_DRW_PATTERN[0][0],LIFT_M4_Y_PX1[0]),LIFT_M4_BOSS_R,LIFT_M4_ENGAGE+TAP_LEAD)):
    for sy in (-1,1):
        _z0=SERVICE_Z-_tap-TAP_SKIN
        body=wp(body.val().fuse(cyl_z(_bx,sy*_by,_z0,_br,71.0-_z0+.01).val()))
        body=cut(body,cyl_z(_bx,sy*_by,SERVICE_Z-_tap,2.0,_tap+.1))
for side in (-1,1):
    pockets=fuse_all([cyl_y(x,side*27.6,45,26.5,6.5,dir=side) for x in GEAR_X])
    body=cut(body,pockets)
    # Extend supported middle/idler seats into the pocket, rather than leaving
    # shortened shafts floating. Boss faces stop at the gear face Y29.8.
    for bx,br in [(150,8.5),(100,7.0),(200,7.0)]:
        body=wp(body.val().fuse(cyl_y(bx,side*SUPPORT_BOSS_INNER_Y,45,br,
                     29.8-SUPPORT_BOSS_INNER_Y,dir=side).val()))
    for x,r,y,w in [(50,10.5,24,5),(150,7,26.4,3.5),(250,15,22,12)]:
        body=cut(body,cyl_y(x,side*y,45,r,w+.1,dir=side))
    for x in (100,200): body=cut(body,cyl_y(x,side*24,45,5,10.2,dir=side))
    cv=boxc(150,side*(34.0+SIDE_COVER_T/2),45,SIDE_COVER_L,SIDE_COVER_T,SIDE_COVER_H).edges('|Y').chamfer(1)
    # F05 per DRW-002-374 A-A: 61903 straddles cover/flange joint, no flange spigot.
    for x in WHEEL_X:
        cv=cut(cv,cyl_y(x,side*33.9,45,COVER_BEARING_SHOULDER_R,5.2,dir=side)) # outer-race shoulder
        cv=cut(cv,cyl_y(x,side*38.9,45,COVER_BEARING_BORE_R,2.2,dir=side))     # 61903 OD30 seat
    for dx in COVER_SCREW_DX:
        for dz in COVER_SCREW_DZ:
            sx,sz=150+dx,45+dz
            cv=cut(cv,cyl_y(sx,side*33.9,45+dz,1.7,7.2,dir=side))                 # clearance Ø3.4
            cv=cut(cv,cyl_y(sx,side*(41-COVER_SCREW_CBORE[1]),sz,COVER_SCREW_CBORE[0],COVER_SCREW_CBORE[1]+.1,dir=side))
            body=cut(body,cyl_y(sx,side*34.1,sz,1.5,5.1,dir=-side))                # M3 cosmetic thread, depth 5
    for x in WHEEL_X:
        for a in (45,135,225,315):  # M3 cosmetic taps for flange screws, depth 4
            fx=x+FLANGE_SCREW_R*math.cos(math.radians(a)); fz=45+FLANGE_SCREW_R*math.sin(math.radians(a))
            cv=cut(cv,cyl_y(fx,side*41.1,fz,1.5,4.1,dir=-side))
    cv=cut(cv,lobed_band(-SIDE_SEAL_W/2,SIDE_SEAL_W/2,SIDE_SEAL_D,side,34.0))   # F10 groove
    side_covers.append((f'HOLD_SIDE_COVER_{side}_GRAPHIC262x60x7',cv));add(side_covers[-1][0],cv,'metal')
    _hw=math.pi*.75**2/SIDE_SEAL_D/2   # area-equal installed section half-width
    add(f'HOLD_SIDE_ORING_190x1p5_{side}_LOBED_GLAND_INSTALLED',lobed_band(-_hw,_hw,SIDE_SEAL_D,side,34.0),'seal')
    for dx in COVER_SCREW_DX:
        for dz in COVER_SCREW_DZ:
            add(f'FIX000359_M3x8_ISO7380_COVER_{side}_{int(150+dx)}_{int(45+dz)}',
                make_button_screw(150+dx,side*(41-COVER_SCREW_CBORE[1]),45+dz,8,side),'shaft')
    for j,x in enumerate(GEAR_X):
        gear=make_spur_gear(50,1,4,12,'Y')
        if j%2:gear=gear.rotate((0,0,0),(0,1,0),3.6)
        add(f'HOLD_Z50_{side}_{int(x)}_PROFILE_UNCONFIRMED',gear.translate((x,side*31.8,45)),'gear')
        if j%2:
            add(f'IDLE_BUSH_10_12_4_{side}_{x}',ring_y(x,side*31.8,45,6,5,4),'bearing')
            add(f'HOLD_IDLE_PIN_{side}_{x}',cyl_y(x,side*IDLER_PIN_INNER_Y,45,5,34-IDLER_PIN_INNER_Y,dir=side),'shaft')
    add(f'61801_SIDE_{side}_50_SOURCE_ONE_PER_SIDE',make_bearing(12,21,5).translate((50,side*26.5,45)),'bearing')
    add(f'MIDDLE_BUSH_12_14_3_{side}',ring_y(150,side*(MIDDLE_INNER_Y+MIDDLE_BUSH_W/2),45,7,6,MIDDLE_BUSH_W),'bearing')
    for x in WHEEL_X:
        inner_y=MIDDLE_INNER_Y if x==150 else 23.0
        shaft=fuse_all([cyl_y(x,side*inner_y,45,6,39-inner_y,dir=side),cyl_y(x,side*39,45,8.5,7,dir=side),
          cyl_y(x,side*46,45,9,2.8,dir=side),cyl_y(x,side*48.8,45,8,SHAFT_END_Y-48.8,dir=side)])   # F25: end at SHAFT_END_Y
        key=boxc(x,side*(WHEEL_KEY_Y0+SHAFT_END_Y)/2,52,4,SHAFT_END_Y-WHEEL_KEY_Y0,4);shaft=cut(shaft,key)
        # F13: shaft end per ASS-002-103 — counterbore for the FSS-002-065 spigot + M6 tapped hole drawn at
        # major Ø6 (cosmetic thread). Screw tip at |Y|49.53, hole bottom 48.9 -> tip gap 0.63 mm, DERIVED.
        shaft=cut(shaft,cyl_y(x,side*(SHAFT_END_Y-SHAFT_SPIGOT_BORE_D),45,SHAFT_SPIGOT_BORE_R,SHAFT_SPIGOT_BORE_D+.1,dir=side))
        _tap0=SHAFT_END_Y-SHAFT_SPIGOT_BORE_D+.05; _tapbot=WD_BACK_Y+WD_FLANGE_T-WD_HEAD_BEAR_D-WHEEL_SCREW_L-0.63
        shaft=cut(shaft,cyl_y(x,side*_tap0,45,M6_COSMETIC_THREAD_R,_tap0-_tapbot,dir=-side))
        add(f'HOLD_WHEEL_SHAFT_{side}_{x}_GRAPHIC_AXIAL_PACKAGE',shaft,'shaft')
        add(f'KEY_4x4x12_{side}_{x}',key,'shaft')
        add(f'61903_SIDE_{side}_{x}',make_bearing(17,30,7).translate((x,side*42.5,45)),'bearing')
        flange=fuse_all([cyl_y(x,side*41,45,17,7.8,dir=side),cyl_y(x,side*41,45,25,FLANGE_COLLAR_T,dir=side)])
        flange=cut(flange,cyl_y(x,side*40.9,45,9.08,8.2,dir=side))
        flange=cut(flange,cyl_y(x,side*40.9,45,15,5.1,dir=side))
        # Face-seal groove in flange underside (DRW374 pos.11 location; dims ESTIMATED).
        flange=cut(flange,ring_y(x,side*(41+FLANGE_GROOVE_DEPTH/2-.05),45,FLANGE_GROOVE_RO,FLANGE_GROOVE_RI,FLANGE_GROOVE_DEPTH+.1))
        flange=cut(flange,cyl_y(x,side*46,45,11.4,2.8,dir=side))
        fscrews=[]
        for a in (45,135,225,315):
            fx=x+FLANGE_SCREW_R*math.cos(math.radians(a)); fz=45+FLANGE_SCREW_R*math.sin(math.radians(a))
            flange=cut(flange,cyl_y(fx,side*40.9,fz,1.7,FLANGE_COLLAR_T+.2,dir=side))
            fscrews.append((a,fx,fz))
        add(f'HOLD_AXLE_FLANGE_{side}_{x}_GRAPHIC_CONTOUR',flange,'metal')
        for a,fx,fz in fscrews:
            add(f'FIX002738_M3x6_ISO7380_FLANGE_{side}_{int(x)}_{a}',
                make_button_screw(fx,side*(41+FLANGE_COLLAR_T),fz,6,side),'shaft')
        add(f'HOLD_XRING_INSTALLED_{side}_{x}_FREE18p72x2p62',ring_y(x,side*47.4,45,11.4,9,2.8),'seal')
        add(f'HOLD_FLANGE_ORING_32x1p5_{side}_{x}_FACE_GLAND_INSTALLED',
            ring_y(x,side*(41+FLANGE_GROOVE_DEPTH/2),45,FLANGE_ORING_INST_RO,FLANGE_GROOVE_RI,FLANGE_GROOVE_DEPTH),'seal')
        pts=list(WHEEL_PROFILE)
        if side<0:pts=[(r,-yy) for r,yy in pts]
        tyre=cq.Workplane('XY').polyline(pts).close().revolve(360,(0,0),(0,1)).translate((x,side*WHEEL_CENTRE_Y,WHEEL_Z))
        tyre=cut(tyre,key)
        # F13: pocket in the Al hub for the FSS-002-065 cam disk (Ø20.4 vs disk max r8.78), ESTIMATED.
        tyre=cut(tyre,cyl_y(x,side*SHAFT_END_Y,45,10.2,WHEEL_CENTRE_Y+12.1-SHAFT_END_Y,dir=side))   # F25: open to the face (6.2 deep)
        hubcyl=cyl_y(x,side*30,45,QRW_HUB_R,40,dir=side)
        hub=wp(tyre.val().intersect(hubcyl.val())); tyre=cut(tyre,hubcyl)
        add(f'HOLD_QRW90SR150_WHEEL_{side}_{x}_ENGINEERED_OUTER_SHOULDER',tyre,'wheel')
        add(f'HOLD_QRW90_HUB_AL_{side}_{x}_ESTIMATED',hub,'metal')
        for nm,part,cat in make_wheel_bolt_assy(x,side):
            add(f'{nm}_{side}_{int(x)}',part,cat)
def candidate_motor_pack(y):
    # Provisional conservative family envelope; leads and exact 138:1 outline unresolved.
    return fuse_all([
        cyl_x(MOTOR_FACE-GEARHEAD_LEN-MOTOR_LEN,y,45,MOTOR_OD/2,MOTOR_LEN),
        cyl_x(MOTOR_FACE-GEARHEAD_LEN,y,45,GEARHEAD_OD/2,GEARHEAD_LEN),
        cyl_x(MOTOR_FACE,y,45,MOTOR_PILOT_D/2,MOTOR_PILOT_L),
        cyl_x(MOTOR_FACE,y,45,MOTOR_SHAFT_D/2,MOTOR_SHAFT_L)])
# F06 bevel pair, built once. Layout DERIVED: apex (250,±MOTOR_Y,45); Z16 pitch circle X230,
# Z40 pitch circle |Y|5.5. m1, 20°, face 6, backlash .05, tip clearance .1 — ESTIMATED (H04).
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor_py'))
import cq_gears
BEVEL_FACE_W=6.0; BEVEL_BACKLASH=0.05; BEVEL_CLEARANCE=0.1
_bp=cq_gears.BevelGearPair(module=BEVEL_MOD,gear_teeth=Z40_TEETH,pinion_teeth=Z16_TEETH,face_width=BEVEL_FACE_W,
                           backlash=BEVEL_BACKLASH,clearance=BEVEL_CLEARANCE)
_ba=_bp.assemble(build_gear=True,build_pinion=True,transform_pinion=True)
def _child(asm,key):
    c=[ch for ch in asm.children if key(ch.name)][0]
    o=c.obj.val() if hasattr(c.obj,'val') else c.obj
    return o.moved(c.loc)
BEVEL_GEAR_SOLID=_child(_ba,lambda n:'gear' in n and 'pinion' not in n)
BEVEL_PINION_SOLID=_child(_ba,lambda n:'pinion' in n)
BEVEL_CONE_H=float(_bp.gear.cone_h)    # apex height above Z40 back face in library frame
BEVEL_APEX_Y=MOTOR_Y
motor_holder=boxc(MOTOR_FACE+1.5,0,45,3,52.8,30)
pinion_holder=boxc(227,0,45,5,52.8,26)
for side in (-1,1):
    y=side*MOTOR_Y
    # F06: straight bevel teeth (cq_gears), common apex at Z40 axis x Z16 axis.
    def place(sh):
        sh=sh.rotate(cq.Vector(0,0,0),cq.Vector(1,0,0),-90*side)
        return wp(sh.translate(cq.Vector(250,side*(BEVEL_APEX_Y-BEVEL_CONE_H),45)))
    z40=place(BEVEL_GEAR_SOLID)
    z40=cut(z40,cyl_y(250,side*(BEVEL_APEX_Y-BEVEL_CONE_H-.1),45,9.7,5.5-(BEVEL_APEX_Y-BEVEL_CONE_H)+.15,dir=side)) # 61800 clearance counterbore, ESTIMATED
    z40=cut(z40,cyl_y(250,side*.4,45,5,15,dir=side))   # bore on Z40 output shaft r5
    z16=place(BEVEL_PINION_SOLID)
    z16=cut(z16,cyl_x(228,y,45,3,12))                  # bore on Z16 shaft r3
    add(f'HOLD_Z40_BEVEL_{side}_STRAIGHT_M1_TEETH',z40,'bevel');add(f'HOLD_Z16_BEVEL_{side}_STRAIGHT_M1_TEETH',z16,'bevel')
    axle=fuse_all([cyl_y(250,side*.5,45,5,19.5,dir=side),cyl_y(250,side*20,45,9,9.8,dir=side)])
    axle=cut(axle,cyl_y(250,side*23,45,6,6.9,dir=side))
    add(f'HOLD_Z40_OUTPUT_SHAFT_{side}_SOCKET_TORQUE_TRANSFER_HOLD',axle,'shaft')
    add(f'61800_Z40_{side}',make_bearing(10,19,5).translate((250,side*3,45)),'bearing')
    add(f'SHAFT_SEAL_Z40_{side}_18x30x7',make_seal(18,30,7).translate((250,side*25.5,45)),'seal')
    pin=fuse_all([cyl_x(209,y,45,3,15.5),cyl_x(224.5,y,45,6,5),cyl_x(229.5,y,45,3,7.5)])
    add(f'HOLD_Z16_SHAFT_{side}',pin,'shaft')
    add(f'61801_Z16_SUPPORT_{side}',make_bearing(12,21,5,'X').translate((227,y,45)),'bearing')
    pinion_holder=cut(pinion_holder,cyl_x(224.4,y,45,10.5,5.2))
    add(f'HOLD_NBK_MLR20C_6_6_COUPLING_{side}_EXTERNAL_DETAIL',make_coupling().translate((199.5,y,45)),'purchased')
    adapter=cut(cyl_x(199.5,y,45,3,8),cyl_x(199.4,y,45,2,8.2))
    adapter=cut(adapter,boxc(203.5,y+2.75,45,8.2,1.5,.5))
    add(f'HOLD_MOTOR_SPLIT_ADAPTER_6_TO_4_{side}',adapter,'shaft')
    add(f'TRACTION_MOTOR_{side}_PROTEUS_CLASS_GP26_D22_ESTIMATED_HOLD',candidate_motor_pack(y),'purchased')
    motor_holder=cut(motor_holder,cyl_x(MOTOR_FACE-.1,y,45,3.3,3.2))
    # ESTIMATED 4-hole pattern; exact supplied variant and body attachment HOLD.
    for angle in (45,135,225,315):
        a=math.radians(angle)
        motor_holder=cut(motor_holder,cyl_x(MOTOR_FACE-.1,y+9.5*math.cos(a),45+9.5*math.sin(a),1.35,3.2))
add('HOLD_PAIRED_MOTOR_HOLDER_GP26_ESTIMATED',motor_holder,'metal')
add('HOLD_PAIRED_PINION_BEARING_HOLDER',pinion_holder,'metal')
# F26 pressure-retention revision: move front M4 X84->80, extend 7mm raised pad front X80->74 (head edge >=2mm, boss to opening >=4mm), M4x10->M4x12 (5mm engagement); all PX1 ESTIMATED, recheck 3D and pressure.
# F25 cover L01 = Proteus-type flush plug (hollow spigot rim Z71..75 with the radial 110x1.5, DRW-002-745 C-C) + flush lid behind
# the pad (top Z75 = housing top, the lift base stands on it) + raised central pad 104 x 50 x 7 over the Cincon / shunt (F20).
_SPX=(SERVICE_OPEN_X0+SERVICE_OPEN_X1)/2; _SPL=SERVICE_PLUG_L-2*SERVICE_PLUG_CLR; _SPW=SERVICE_OPEN_W-2*SERVICE_PLUG_CLR
_SPR=SERVICE_PLUG_R-SERVICE_PLUG_CLR
def rrect(cx,z0,L,W,r,h): return box0(cx-L/2,-W/2,z0,L,W,h).edges('|Z').fillet(r)
def rframe(cx,z0,L,W,r,t,h): return cut(rrect(cx,z0,L,W,r,h),rrect(cx,z0-.1,L-2*t,W-2*t,r-t,h+.2))
cover=box0(SERVICE_PAD_X[0],-SERVICE_PAD_HW,SERVICE_Z,SERVICE_L,SERVICE_W,SERVICE_T)
_gx0,_ghw,_gd=SERVICE_PAD_GROOVE                     # gas-spring groove (spring body passes over the pad rear end)
cover=cut(cover,box0(_gx0,-_ghw,SERVICE_Z+SERVICE_T-_gd,SERVICE_PAD_X[1]-_gx0+.1,2*_ghw,_gd+.1))
spigot=rframe(_SPX,SERVICE_Z-SERVICE_SPIGOT_H,_SPL,_SPW,_SPR,SERVICE_SPIGOT_WALL,SERVICE_SPIGOT_H)
spigot=cut(spigot,rframe(_SPX,SERVICE_RGROOVE_Z-SERVICE_RGROOVE_W/2,_SPL+.2,_SPW+.2,_SPR+.1,
                         SERVICE_RGROOVE_D+.1,SERVICE_RGROOVE_W))
_lw=SERVICE_SPIGOT_WALL-.1                            # lid fills the inside of the spigot rim (0.1 into the wall), clear of the O-ring groove
_lid=wp(rrect(_SPX,SERVICE_Z-SERVICE_LID_T,_SPL-2*_lw,_SPW-2*_lw,_SPR-_lw,SERVICE_LID_T).val().intersect(
        box0(SERVICE_PAD_X[1],-30,SERVICE_Z-SERVICE_LID_T-.1,SERVICE_OPEN_X1-SERVICE_PAD_X[1]+5,60,SERVICE_LID_T+.2).val()))
LIFT_M4_POINTS=[(x,sy*y) for x,y in zip(LIFT_M4_X,LIFT_M4_Y_PX1) for sy in (-1,1)]
for sy in (-1,1):                                    # F25: lid bosses for the lift-base inner M4 pair (744 pos.14)
    _lid=wp(_lid.val().fuse(cyl_z(LIFT_M4_X[1],sy*LIFT_M4_Y_PX1[1],LIFT_M4_BOSS_Z0,LIFT_M4_BOSS_R,SERVICE_Z-LIFT_M4_BOSS_Z0).val()))
cover=wp(cover.val().fuse(spigot.val()).fuse(_lid.val()).clean())
for sy in (-1,1):
    cover=cut(cover,cyl_z(LIFT_M4_X[1],sy*LIFT_M4_Y_PX1[1],SERVICE_Z-LIFT_M4_TAP_DEPTH,2.0,LIFT_M4_TAP_DEPTH+.1))  # blind M4, skin 1.5
    cover=cut(cover,cyl_z(COVER_FIX_XY[0],sy*COVER_FIX_XY[1],SERVICE_Z-.1,2.25,SERVICE_T+.2))                        # M4 clearance Ø4.5
def face_groove_od(o): return o[0]/2+o[1]           # groove OD radius = ring OD/2
# F20: blind taps in the cover underside (no penetration of the 7 mm pressure wall).
F20_CINCON_HOLES=[(CINCON_XC+sx*CINCON_HOLE_PITCH[0]/2,CINCON_YC+sy*CINCON_HOLE_PITCH[1]/2) for sx in (-1,1) for sy in (-1,1)]
F20_SHUNT_XY=(109.0,15.2)                                   # resistor centre under cover, ESTIMATED (F22: Y17.5->15.2 inside the spigot rim)
F20_SHUNT_HOLES=[(F20_SHUNT_XY[0]+sx*(SHUNT_R_ENV[0]-SHUNT_R_TAB[0])/2,F20_SHUNT_XY[1]) for sx in (-1,1)]
F20_BOARD_XY=(109.0,0.0)
F20_STANDOFFS=[(97.0,0.0),(121.0,0.0)]
for _hx,_hy in F20_CINCON_HOLES+F20_SHUNT_HOLES:
    cover=cut(cover,cyl_z(_hx,_hy,SERVICE_Z-.1,1.5,COVER_TAP_DEPTH+.1))   # M3 cosmetic thread (major D3)
for _hx,_hy in F20_STANDOFFS:
    cover=cut(cover,cyl_z(_hx,_hy,SERVICE_Z-.1,1.5,4.1))
add('HOLD_PRESSURE_ELECTRONICS_COVER_FLUSH_PLUG_PAD110x50x7',cover,'metal')
for _i,sy in enumerate((-1,1),1):                    # PX1: 2x ISO 7380 M4x12 into housing-top bosses (5.0 engaged)
    _hr,_hk=ISO7380_M4; _zt=SERVICE_Z+SERVICE_T
    add(f'FIX_ISO7380_M4x12_ELECTRONICS_COVER_FRONT_ON_SERVICE_COVER_{_i}',
        fuse_all([cyl_z(COVER_FIX_XY[0],sy*COVER_FIX_XY[1],_zt,_hr,_hk),cyl_z(COVER_FIX_XY[0],sy*COVER_FIX_XY[1],_zt-COVER_FIX_L,2.0,COVER_FIX_L)]),'shaft')
# F22 seals. Installed sections: area-equal bands, stretched cross-section d'=d/sqrt(1+stretch) (volume constant).
_bh=math.pi*SERVICE_ORING_CS_INST**2/4/SERVICE_RGLAND_D
# band from groove root +0.01 to opening wall -0.01 (no modelled contact; squeeze is checked numerically)
add(f'PX1_ASSUMED_SERVICE_ORING_ID{SERVICE_ORING[0]:g}_CS{SERVICE_ORING[1]:g}_RADIAL_NOT_OEM',
    rframe(_SPX,SERVICE_RGROOVE_Z-_bh/2,SERVICE_PLUG_L-.02,SERVICE_OPEN_W-.02,SERVICE_PLUG_R-.01,SERVICE_RGLAND_D-.02,_bh),'seal')
# F25: camera-cable fitting holder (Proteus FAL-002-086 role) on the housing top behind the lift base: M12 gland, valve, sealed
# feed-throughs Ø8 / Ø4 with SEA-001-861 10x1.5 (valve, as 745 pos.15) and 16x1.5 (gland) face rings on its underside.
holder=box0(HOLDER_X[0],-BODY_HALF_W_SCREEN,SERVICE_Z,HOLDER_X[1]-HOLDER_X[0],2*BODY_HALF_W_SCREEN,HOLDER_T)
_hz1=SERVICE_Z+HOLDER_T
for sy in (-1,1): holder=cut(holder,cyl_z(HOLDER_SCREW_XY[0],sy*HOLDER_SCREW_XY[1],SERVICE_Z-.1,1.7,HOLDER_T+.2))
holder=cut(holder,cyl_z(VALVE_XY[0],VALVE_XY[1],VALVE_SEAT_Z0,5.05,_hz1+.1-VALVE_SEAT_Z0))  # F22: valve seat (blind) ...
holder=cut(holder,cyl_z(VALVE_XY[0],VALVE_XY[1],SERVICE_Z-.1,2.0,VALVE_SEAT_Z0-SERVICE_Z+.2))  # ... + Ø4 vent to the housing passage
holder=cut(holder,cyl_z(CAM_GLAND_XY[0],CAM_GLAND_XY[1],SERVICE_Z-.1,6.05,HOLDER_T+.2))     # M12 camera-cable gland thread, ESTIMATED
for (_px,_py),_o in ((VALVE_XY,PASSAGE_ORING),(CAM_GLAND_XY,GLAND_PASSAGE_ORING)):
    _ro=face_groove_od(_o)
    holder=cut(holder,cut(cyl_z(_px,_py,SERVICE_Z-.1,_ro,PASSAGE_GROOVE_D+.1),cyl_z(_px,_py,SERVICE_Z-.2,_ro-PASSAGE_GROOVE_W,PASSAGE_GROOVE_D+.3)))
add('PX1_CAMERA_FITTING_HOLDER_FAL002086_ROLE_ON_HOUSING_TOP',holder,'metal')
for _i,sy in enumerate((-1,1),1):
    add(f'FIX_ISO7380_M3x12_FITTING_HOLDER_{_i}',fuse_all([cyl_z(HOLDER_SCREW_XY[0],sy*HOLDER_SCREW_XY[1],_hz1,ISO7380_M3[0],ISO7380_M3[1]),
        cyl_z(HOLDER_SCREW_XY[0],sy*HOLDER_SCREW_XY[1],_hz1-12.0,1.2,12.0)]),'shaft')
for (_px,_py),_o,_nm in ((VALVE_XY,PASSAGE_ORING,'SEA001861_ORING_10x1p5_VALVE_PASSAGE_UNDER_FITTING_HOLDER'),
                         (CAM_GLAND_XY,GLAND_PASSAGE_ORING,'HOLD_ORING_16x1p5_GLAND_PASSAGE_UNDER_FITTING_HOLDER')):
    _ro=face_groove_od(_o)-.01; _w=math.pi*_o[1]**2/4/PASSAGE_GROOVE_D
    add(_nm,cut(cyl_z(_px,_py,SERVICE_Z+.01,_ro,PASSAGE_GROOVE_D-.02),cyl_z(_px,_py,SERVICE_Z,_ro-_w,PASSAGE_GROOVE_D)),'seal')
VX,VY=VALVE_XY
valve_body=cut(cyl_z(VX,VY,78,5,14),cyl_z(VX,VY,77.9,2.1,14.2))
add('HOLD_PRESSURE_VALVE_BODY_SOURCE_FAMILY',valve_body,'valve')
add('HOLD_PRESSURE_VALVE_CAP',cyl_z(VX,VY,92,6,1.5),'valve')
add('HOLD_PRESSURE_VALVE_4MM_BALL',cq.Workplane('XY').sphere(2).translate((VX,VY,88)),'valve')
# Camera cable enters the holder through a vertical M12 gland behind the lift base (Proteus: M12 entry on FAL-002-086, DRW-002-745).
lapp=make_gland().rotate((0,0,0),(0,1,0),-90).translate((CAM_GLAND_XY[0],CAM_GLAND_XY[1],SERVICE_Z+.5))
add('HOLD_LAPP_SKINTOP_53112000_M12x1p5_CAMERA_CABLE_IN_FITTING_HOLDER',lapp,'purchased')

# ---------------- F18 camera lift DRW-002-744 / DRW-002-752 (folded, theta=0) ----------------
AX,AZ=LIFT_A_X,LIFT_A_Z
def lift_rel(d): return (AX-d[0],AZ+d[1])        # toward camera = -X
LB=lift_rel(LIFT_AB)                             # side-link base pivot B
LC=(AX-LINK_L,AZ)                                # central lever top pivot C (on lift housing)
LD=(LB[0]-LINK_L,LB[1])                          # side-link top pivot D: exact parallelogram, CD=AB
LE=lift_rel(LIFT_GAS_E); LG=lift_rel(LIFT_GAS_G) # gas spring eyes
BASE_X0=AX-(LIFT_BASE_L-LIFT_BASE_BEHIND_A); BASE_X1=AX+LIFT_BASE_BEHIND_A; BASE_Z0=BODY_TOP   # F25: on the housing top
SW_IN=LIFT_SIDE_Y-LIFT_SIDE_T/2; SW_OUT=LIFT_SIDE_Y+LIFT_SIDE_T/2
# Base FAL-002-067: 8 mm plate (ESTIMATED) on the housing top / flush cover lid, A-cheeks, B-lugs, gas-spring slot and side-link reliefs.
lbase=box0(BASE_X0,-LIFT_BASE_W/2,BASE_Z0,LIFT_BASE_L,LIFT_BASE_W,8)
for sy in (-1,1):
    lbase=lbase.union(box0(AX-10,sy*12.2-2,BASE_Z0+8,20,4,AZ+10-BASE_Z0-8))                      # A cheeks Y+-10.2..14.2
    _lug_in=SW_OUT+LIFT_SHIM_B+.2                                                                  # F25: room for the 0.25 brass shim
    lbase=lbase.union(box0(LB[0]-6.5,_lug_in if sy>0 else -LIFT_BASE_W/2,BASE_Z0+8,14,
                           LIFT_BASE_W/2-_lug_in,LB[1]+8-BASE_Z0-8))                               # B lugs outside links
    lbase=cut(lbase,box0(BASE_X0-.1,(SW_IN-.3) if sy>0 else -(SW_OUT+LIFT_SHIM_B+.2),BASE_Z0-.1,LB[0]+8-BASE_X0,SW_OUT-SW_IN+LIFT_SHIM_B+.5,8.2))
lbase=cut(lbase,box0(BASE_X0-.1,-6.5,BASE_Z0-.1,LE[0]+6.5-BASE_X0+.1,13,8.2))                     # gas-spring slot
lbase=cut(lbase,cyl_y(AX,-15,AZ,5.1,30)); lbase=cut(lbase,cyl_y(LB[0],-35,LB[1],4.05,70))
lbase=cut(lbase,cyl_y(LE[0],-12.1,LE[1],ACE_EYE_BORE/2,24.2))   # F25: Ø4 pin for the ACE A3,5 eye
_m4_bear=BASE_Z0+LIFT_M4_CLAMP                                                                     # head bearing Z82.0
for _hx,_hy in LIFT_M4_POINTS:                                                                     # F21: 4x Ø4.5 + Ø8x1 cbore
    lbase=cut(lbase,cyl_z(_hx,_hy,BASE_Z0-.1,LIFT_M4_HOLE_R,8.2))
    lbase=cut(lbase,cyl_z(_hx,_hy,_m4_bear,LIFT_M4_CBORE[0],BASE_Z0+8-_m4_bear+.1))
add('HOLD_LIFT_BASE_FAL002067_ON_HOUSING_TOP',lbase,'lift')
for _i,(_hx,_hy) in enumerate(LIFT_M4_POINTS,1):                                                   # FIX-000-598 ISO 4762 M4x12 A2
    _hr,_hk,_hs=ISO4762_M4
    _head=cut(cyl_z(_hx,_hy,_m4_bear,_hr,_hk),cq.Workplane('XY').polygon(6,_hs/math.cos(math.pi/6)).extrude(2.0).translate((_hx,_hy,_m4_bear+_hk-2.0+.01)))
    add(f'FIX000598_M4x12_ISO4762_A2_LIFT_BASE_ON_HOUSING_TOP_{_i}',fuse_all([_head,cyl_z(_hx,_hy,_m4_bear-LIFT_M4_SCREW_L,2.0,LIFT_M4_SCREW_L)]),'shaft')
# Clamp axle FSS-002-089 (M10, M8 end), washer FSS-002-077, 3x DIN2093 20x10.2x1.1, 2x ISO4035 M10, clamp lever FIX-002-527 M8.
caxle=fuse_all([cyl_y(AX,-20.35,AZ,4.95,44.55),cyl_y(AX,-28.35,AZ,4.0,8.0)])
add('HOLD_LIFT_CLAMP_AXLE_FSS002089_M10',caxle,'lift')
add('HOLD_LIFT_CLAMP_WASHER_FSS002077',ring_y(AX,-14.95,AZ,10,5.1,1.5),'lift')
for i,yc in enumerate((-16.475,-18.025,-19.575),1):
    add(f'HOLD_LIFT_DISC_SPRING_DIN2093_20x10p2x1p1_{i}',ring_y(AX,yc,AZ,10,5.1,1.55),'lift')
def hex_nut_y(y0,w):
    n=cq.Workplane('XZ').polygon(6,17/math.cos(math.pi/6)).extrude(-w).translate((AX,y0,AZ))
    return cut(n,cyl_y(AX,y0-.1,AZ,5.0,w+.2))
for i,y0 in enumerate((14.2,19.2),1):add(f'HOLD_LIFT_NUT_ISO4035_M10_{i}',hex_nut_y(y0,5),'lift')
clamp=fuse_all([cyl_y(AX,-28.35,AZ,8,8),between((AX,-24.35,AZ),(AX-70,-24.35,AZ),3.5)])
clamp=cut(clamp,cyl_y(AX,-28.45,AZ,4.05,8.2))
add('HOLD_LIFT_CLAMP_LEVER_M8_FIX002527',clamp,'lift')
# Central lever ASS-002-723 + lever sheet plate FSS-002-073 (AC = LINK_L).
lever=[cyl_y(AX,-10,AZ,9,20),boxc((LC[0]+14+AX-11)/2,0,AZ+7.5,AX-11-LC[0]-14,LIFT_LEVER_PLATE_W,3)]
for sy in (-1,1):
    yc=sy*sum(LIFT_CHEEK_Y)/2; tc=LIFT_CHEEK_Y[1]-LIFT_CHEEK_Y[0]
    lever.append(plate_between((AX,AZ+.25),(LC[0],AZ+.25),yc,tc,11.5))
    lever.append(cyl_y(LC[0],yc-tc/2,LC[1],7,tc))
lever=fuse_all(lever)
lever=cut(lever,cyl_y(AX,-10.1,AZ,5.1,20.2)); lever=cut(lever,cyl_y(LC[0],-10,LC[1],LH752_C_AXLE_D/2+.05,20))   # F24: Ø7 axle FSS-002-076
lever=cut(lever,cyl_y(LG[0],-10,LG[1],ACE_EYE_BORE/2,20))
add('HOLD_LIFT_CENTRAL_LEVER_ASS002723_FSS002073',lever,'lift')
# Side links FSS-002-068 (BD = LINK_L) with axles FSS-002-075 (base) and FSS-002-079 (lift housing).
for sy in (-1,1):
    yc=sy*LIFT_SIDE_Y
    link=fuse_all([plate_between(LB,LD,yc,LIFT_SIDE_T,LIFT_SIDE_H),
                   cyl_y(LB[0],yc-LIFT_SIDE_T/2,LB[1],7.5,LIFT_SIDE_T),cyl_y(LD[0],yc-LIFT_SIDE_T/2,LD[1],7.5,LIFT_SIDE_T)])
    for px,pz in (LB,LD):link=cut(link,cyl_y(px,yc-LIFT_SIDE_T/2-.1,pz,4.05,LIFT_SIDE_T+.2))
    add(f'HOLD_LIFT_SIDE_LINK_FSS002068_{sy}',link,'lift')
    add(f'HOLD_LIFT_SIDE_AXLE_FSS002075_{sy}',fuse_all([cyl_y(LB[0],sy*SW_IN,LB[1],3.95,(LIFT_BASE_W/2-SW_IN),dir=sy),
        cyl_y(LB[0],sy*LIFT_BASE_W/2,LB[1],6,1.5,dir=sy)]),'lift')
    # F24: D per DRW-002-752 C-C = blind taps 8 deep in both housing sides (no through axle): stepped pin FSS-002-079 (M6 thread
    # in the yoke, Ø8 journal through the link) + DIN 471 8x0.8 outside the link (744 list: rings 8x0.8 x4).
    _tr,_jr,_jl=LIFT_D_PIN; _gr,_rr,_rt=LIFT_D_RING; _hw=LIFT_HOUSING_W/2
    _pin=fuse_all([cyl_y(LD[0],sy*(_hw-LH752_D_TAP[1]+.1),LD[1],_tr,LH752_D_TAP[1]-.1,dir=sy),
                   cyl_y(LD[0],sy*_hw,LD[1],_jr,_jl,dir=sy),cyl_y(LD[0],sy*(_hw+_jl),LD[1],_gr,_rt+.1,dir=sy),
                   cyl_y(LD[0],sy*(_hw+_jl+_rt+.1),LD[1],_jr,.4,dir=sy)])
    add(f'HOLD_LIFT_TOP_AXLE_FSS002079_{sy}',_pin,'lift')
    add(f'HOLD_LIFT_D_PIN_RING_DIN471_8x0p8_{sy}',ring_y(LD[0],sy*(_hw+_jl+.05+_rt/2),LD[1],_rr,_gr+.02,_rt),'lift')
    # F25: brass shims per 744 list: FBR-002-750 0.4 on the D pin (housing side), FBR-002-751 0.25 on the B axle (base-lug side).
    add(f'FBR002750_BRASS_SHIM_0p4_LIFT_D_{sy}',ring_y(LD[0],sy*(_hw+LIFT_SHIM_D/2),LD[1],LIFT_SHIM_R[1],LIFT_SHIM_R[0],LIFT_SHIM_D),'lift')
    add(f'FBR002751_BRASS_SHIM_0p25_LIFT_B_{sy}',ring_y(LB[0],sy*(SW_OUT+LIFT_SHIM_B/2),LB[1],LIFT_SHIM_R[1],LIFT_SHIM_R[0],LIFT_SHIM_B),'lift')
# Gas spring SPR-002-524 150 N -> F25: ACE GS-12-60-V4A (bare 92..152) + 2x A3,5-V4A eyes (8.0 each), Ø4 pins (eye bore 4.1).
E3=cq.Vector(LE[0],0,LE[1]); G3=cq.Vector(LG[0],0,LG[1]); gu=(G3-E3).normalized()
gas_length=(G3-E3).Length; body_pt=E3.toTuple(); moving=G3.toTuple()
gas_bare=gas_length-2*ACE_EYE_L                                   # folded bare length (catalogue L datum), DERIVED
_eo,_eb,_ew=ACE_EYE_OD/2,ACE_EYE_BORE/2,ACE_EYE_W
gbody=fuse_all([ring_y(LE[0],0,LE[1],_eo,_eb,_ew),between((E3+gu*(_eo-.2)).toTuple(),(E3+gu*ACE_EYE_L).toTuple(),2.5),
                between((E3+gu*ACE_EYE_L).toTuple(),(E3+gu*(ACE_EYE_L+ACE_BODY_L)).toTuple(),ACE_BODY_OD/2)])
add('HOLD_ACE_GS12_60_V4A_150N_BODY_A3p5_EYE',gbody,'purchased')
grod=fuse_all([between((E3+gu*(ACE_EYE_L+ACE_BODY_L)).toTuple(),(G3-gu*ACE_EYE_L).toTuple(),ACE_ROD_OD/2),
               between((G3-gu*ACE_EYE_L).toTuple(),(G3-gu*(_eo-.2)).toTuple(),2.5),ring_y(LG[0],0,LG[1],_eo,_eb,_ew)])
add('HOLD_ACE_GS12_60_ROD_A3p5_EYE',grod,'purchased')
add('HOLD_LIFT_GAS_SPRING_PIN_D4x18_ACE_A3p5_LOWER',cyl_y(LE[0],-9,LE[1],_eb-.1,18),'lift')
add('HOLD_LIFT_GAS_SPRING_PIN_D4_ACE_A3p5_UPPER',cyl_y(LG[0],-LIFT_CHEEK_Y[1],LG[1],_eb-.1,2*LIFT_CHEEK_Y[1]),'lift')
# F21 camera harness: SP13 (in lift housing) -> fixed riser R17 in the housing C-arm -> clamp P -> guide 1 -> S-loop on the
# lever plate -> guide 2 -> S-bend -> fixed point K on the printed bend guide -> R17 -> vertical into the M12 gland.
def route_walk(start,heading,route):
    """Pure-geometry walk of HARNESS_ROUTE: list of (kind, points, tangents); arcs give start/mid/end."""
    V=cq.Vector; p=V(*start); t=V(*heading).normalized(); segs=[]
    for sg in route:
        if sg[0]=='S':
            q=p+t*sg[1]; segs.append(('S',[p,q],[t,t])); p=q
        else:
            R,deg,k=sg[1],sg[2],V(*sg[3]); n=k.cross(t); c=p+n*R; pts=[]; tans=[]
            for a in (0.0,math.radians(deg)/2,math.radians(deg)):
                pts.append(c+n*(-R*math.cos(a))+t*(R*math.sin(a))); tans.append(t*math.cos(a)+n*math.sin(a))
            segs.append(('A',pts,tans)); p=pts[-1]; t=tans[-1].normalized()
    return segs
def _route_frame(t):
    y=cq.Vector(0,1,0); e1=y-t*y.dot(t)
    if e1.Length<1e-9: e1=cq.Vector(1,0,0)-t*t.x                 # F23: tangent along Y (internal bundle)
    e1=e1.normalized(); return e1,t.cross(e1)
def route_tube(segs,r,a=0.0,b=0.0):
    """Sweep a circle along the route offset by (a,b) in the (Y-like, normal) frame: lines stay lines, arcs stay arcs."""
    edges=[]
    for kind,pts,tans in segs:
        q=[]
        for pp,tt in zip(pts,tans):
            e1,e2=_route_frame(tt.normalized()); q.append(pp+e1*a+e2*b)
        if (q[-1]-q[0]).Length<1e-6: continue
        edges.append(cq.Edge.makeLine(q[0],q[1]) if kind=='S' else cq.Edge.makeThreePointArc(q[0],q[1],q[2]))
    t0=segs[0][2][0].normalized(); e1,e2=_route_frame(t0)
    prof=cq.Wire.makeCircle(r,segs[0][1][0]+e1*a+e2*b,t0)
    return wp(cq.Solid.sweep(prof,[],cq.Wire.assembleEdges(edges),True,False,None,'right'))
harness_segs=route_walk(HARNESS_START,(1,0,0),HARNESS_ROUTE)
_hend=harness_segs[-1][1][-1]
assert abs(_hend.x-CAM_GLAND_XY[0])<1e-6 and abs(_hend.y-CAM_GLAND_XY[1])<1e-6 and abs(_hend.z-(GLAND_EXIT_Z-6.0))<1e-6, _hend
HARNESS_P=harness_segs[HARNESS_SEG_P-1][1][-1]; HARNESS_K=harness_segs[HARNESS_SEG_K-1][1][-1]
# F24 lift housing per DRW-002-752 (camera end of the parallelogram). X(a)=LH_X0+a (axial), Z=CAM_Z+up.
def lhx(a): return LH_X0+a
_bf,_br,_bc=(lhx(v) for v in LH752_BODY_X); _wu,_wl=LH752_W; _zb,_zt,_zl=(CAM_Z+v for v in LH752_Z)
_lug_x0=_br-.5                                                    # F25: 752 fork lugs / spine grow out of the body rear (X11.78)
_cav=(lhx(31.88),12.0,CAM_Z-17.5,CAM_Z+16.5)    # PCB cavity (Mini-Cam electronics; PX1: SP13 rear + cable riser), DERIVED/ESTIMATED
lh=fuse_all([box0(_bf,-_wu/2,CAM_Z,_br-_bf,_wu,_zt-CAM_Z),                                        # upper body 46.04
             box0(_bf,-_wl/2,_zb,_br-_bf,_wl,CAM_Z-_zb+.5).edges('|X and <Z').fillet(5.0),          # lower body 41.97
             cyl_x(lhx(LH752_LOCK[2]),0,CAM_Z,LH752_NECK_OD/2,LH752_BODY_X[0]-LH752_LOCK[2]+.2),     # neck Ø35.1
             cyl_x(lhx(LH752_SPIGOT[0]),0,CAM_Z,LH752_SPIGOT[1]/2,LH752_LOCK[2]-LH752_SPIGOT[0]+.1),  # spigot under the lock ring
             ]
            # F25: no PX1 yoke - C fork lugs per 752 (|Y| 12.22..23.02, lug end axial 79.37 = C + r6.95) and D taps in the body sides.
            +[box0(_lug_x0,sy*LH752_FORK[0] if sy>0 else -LH752_FORK[1],LH_LUG_Z0,LC[0]-_lug_x0,LH752_FORK[1]-LH752_FORK[0],
                   LC[1]+7-LH_LUG_Z0) for sy in (-1,1)]
            +[cyl_y(LC[0],sy*LH752_FORK[0],LC[1],lhx(LH752_FORK[2])-LC[0],LH752_FORK[1]-LH752_FORK[0],dir=sy) for sy in (-1,1)]
            +[box0(_lug_x0,-LH_SPINE_Y,LH_LUG_Z0,LC[0]+7.1-_lug_x0,2*LH_SPINE_Y,LIFT_A_Z+7.1-LH_LUG_Z0)])   # PX1 cable spine (F21 C-arm)
lh=cut(lh,box0(_cav[0],-_cav[1],_cav[2],_br-_cav[0]+.01,2*_cav[1],_cav[3]-_cav[2]))
lh=cut(lh,cyl_x(lhx(LH752_SPIGOT[0])-.1,0,CAM_Z,11.5,_cav[0]-lhx(LH752_SPIGOT[0])+.2))           # SP13 bore (r11 collar)
_lr_a=11.0                                                                                         # lock-ring screws axial, DERIVED (side view)
lh=cut(lh,cut(cyl_x(lhx(_lr_a)-1.85,0,CAM_Z,LH752_SPIGOT[1]/2+.2,3.7),cyl_x(lhx(_lr_a)-1.9,0,CAM_Z,15.3,3.8)))  # dog-point groove
lh=cut(lh,cyl_y(LC[0],-LH752_FORK[1]-.1,LC[1],LH752_C_AXLE_D/2+.025,2*LH752_FORK[1]+.2))         # C bore Ø7.05 (fork + spine)
for sy in (-1,1):
    lh=cut(lh,cyl_y(LC[0],sy*(LH752_FORK[1]-LIFT_C_RING[3]),LC[1],5.5,LIFT_C_RING[3]+.1,dir=sy))   # ring recess Ø11 x 1.0
    lh=cut(lh,cyl_y(LD[0],sy*(_wu/2-LH752_D_TAP[1]),LD[1],LIFT_D_PIN[0]+.05,LH752_D_TAP[1]+.1,dir=sy))  # D blind tap 8 deep
for (ly,lu) in LH752_COVER_SCREWS:
    for sy in (-1,1): lh=cut(lh,cyl_x(_br-6.3,sy*ly,CAM_Z+lu,1.5,6.4))                          # M3 taps for FAL-002-081
_chan=route_tube(harness_segs[:HARNESS_SEG_P+1],HARNESS_OD/2+.3)                               # fixed riser channel -> clamp P
lh=cut(lh,_chan)
# F23 potted bend tail on the SP13 rear (option b): sleeve over the plug body + shell r(OD/2+1.5) along the fixed R17 bend.
_tsegs=route_walk(HARNESS_START,(1,0,0),HARNESS_ROUTE[:2]+(('S',HARNESS_TAIL_LINE),))
_sr,_sov,_scap=HARNESS_TAIL_SLEEVE; _sp13_end=-36.0+SP13_PLUG_KEEP
tail_env=fuse_all([cyl_x(_sp13_end-_sov,0,CAM_Z,_sr,_sov+_scap),route_tube(_tsegs,HARNESS_OD/2+HARNESS_TAIL_WALL)])
_tail_cut=fuse_all([cyl_x(_sp13_end-_sov-.2,0,CAM_Z,_sr+.2,_sov+_scap+.4),route_tube(_tsegs,HARNESS_OD/2+HARNESS_TAIL_WALL+.2)])
lh=cut(lh,_tail_cut)
add('HOLD_LIFT_HOUSING_FAL002071_DRW752',lh,'lift')
# Lift cover FAL-002-081 (rear plate, 4x M3x8 CSK FIX-002-517); cable passes through it in the potted tail (752 gland position).
_cw,_ch,_ct=LH752_COVER
lcov=box0(_br,-_cw/2,_zb,_ct,_cw,_ch)
for (ly,lu) in LH752_COVER_SCREWS:
    for sy in (-1,1): lcov=cut(lcov,cyl_x(_br-.1,sy*ly,CAM_Z+lu,2.85,_ct+.2))
lcov=cut(cut(lcov,_chan),_tail_cut)
add('HOLD_LIFT_COVER_FAL002081_DRW752',lcov,'lift')
for _i,(ly,lu,sy) in enumerate([(a,b,c) for a,b in LH752_COVER_SCREWS for c in (-1,1)],1):
    add(f'FIX002517_M3x8_CSK_TORX_LIFT_COVER_{_i}',fuse_all([cyl_x(_br,sy*ly,CAM_Z+lu,2.8,_ct),cyl_x(_br-6.28,sy*ly,CAM_Z+lu,1.45,6.3)]),'shaft')
# Light cover FAL-002-080 on top (Mini-Cam LED window, O-ring 21x1.5); PX1 use of the window HOLD.
_la,_ll,_lw=LH752_LIGHT
add('HOLD_LIFT_LIGHT_COVER_FAL002080_DRW752',box0(lhx(_la-_ll/2),-_lw/2,_zt,_ll,_lw,_zl-_zt).edges('|Z').fillet(4.0),'lift')
# Lock ring FSS-001-889 (cone 48.64 -> 35.81 x 22.99, bore 34.16) + lock-ring screw FSS-001-891 and M5x6 dog point FIX-001-892
# radial at axial 11 into a groove of the spigot (ring captive, turns to pull the camera onto the connector), ESTIMATED.
lring=wp(cq.Solid.makeCone(LH752_LOCK[0]/2,LH752_LOCK[1]/2,LH752_LOCK[2],cq.Vector(LH_X0,0,CAM_Z),cq.Vector(1,0,0)))
lring=cut(lring,cyl_x(LH_X0-.1,0,CAM_Z,LH752_LOCK_BORE/2,LH752_LOCK[2]+.2))
_lr_dirs=((1,28.5),(-1,0.0))                                                                     # (+Y 28.5 deg up: FSS-001-891, -Y: FIX-001-892)
for sy,ang in _lr_dirs:
    v=cq.Vector(0,sy*math.cos(math.radians(ang)),math.sin(math.radians(ang)))
    lring=cut(lring,wp(cq.Solid.makeCylinder(2.55,9.0,cq.Vector(lhx(_lr_a),0,CAM_Z)+v*16.9,v)))
add('HOLD_LOCK_RING_FSS001889_DRW752',lring,'lift')
for (sy,ang),nm in zip(_lr_dirs,('HOLD_LOCK_RING_SCREW_FSS001891','FIX001892_M5x6_DOG_POINT_SET_SCREW_LOCK_RING')):
    v=cq.Vector(0,sy*math.cos(math.radians(ang)),math.sin(math.radians(ang))); o=cq.Vector(lhx(_lr_a),0,CAM_Z)
    add(nm,fuse_all([wp(cq.Solid.makeCylinder(1.75,1.7,o+v*15.4,v)),wp(cq.Solid.makeCylinder(2.5,3.9,o+v*17.1,v))]),'shaft')
# Axle FSS-002-076 Ø7 through fork lugs, lever cheeks and spine; DIN 471 7x0.8 in the lug recesses (inside |Y| 23.02).
_g0=LH752_FORK[1]-LIFT_C_RING[3]
caxle76=cyl_y(LC[0],-(LH752_FORK[1]-.02),LC[1],LH752_C_AXLE_D/2-.025,2*(LH752_FORK[1]-.02))
for sy in (-1,1):
    caxle76=cut(caxle76,cut(cyl_y(LC[0],sy*_g0,LC[1],4.0,.9,dir=sy),cyl_y(LC[0],sy*(_g0-.1),LC[1],LIFT_C_RING[0],1.1,dir=sy)))
    add(f'HOLD_LIFT_C_AXLE_RING_DIN471_7x0p8_{sy}',ring_y(LC[0],sy*(_g0+.05+LIFT_C_RING[2]/2),LC[1],LIFT_C_RING[1],LIFT_C_RING[0]+.02,LIFT_C_RING[2]),'lift')
add('HOLD_LIFT_TOP_LEVER_AXLE_FSS002076',caxle76,'lift')
# CAM026 catalogue envelope 120x74x74 (rear rotate housing + pan/tilt head + window).
cam_rear=CAM_REAR_X; cam_front=cam_rear-CAM026_ENVELOPE[0]
add('HOLD_CAM026_ROTATE_HOUSING_GRAPHIC_OD62p5',cyl_x(cam_rear-60,0,CAM_Z,CAM_R,60),'camera')
head=boxc(cam_front+1+29.5,0,CAM_Z,59,CAM026_ENVELOPE[1],CAM026_ENVELOPE[2]).edges('|X').fillet(12)
add('HOLD_CAM026_PAN_TILT_HEAD_ENVELOPE_120x74x74',head,'camera')
add('HOLD_CAM026_FRONT_WINDOW_DIAMETER_UNKNOWN',cyl_x(cam_front,0,CAM_Z,12,1),'camera')
sp13=make_sp13_plug().translate((-36,0,CAM_Z));add('HOLD_WEIPU_SP1310_S6I_N_AND_PANEL_INTERFACE',sp13,'connector')
tail=cut(cut(tail_env,sp13),route_tube(harness_segs[:3],HARNESS_OD/2+.15))
add('PX1_SP13_POTTED_BEND_TAIL_R17_LAPP_CAMERA_EXIT',tail,'print')
jacket=route_tube(harness_segs,HARNESS_OD/2)
_core_ab=[(a,b) for b in (-.6,.6) for a in (-1.0,0.0,1.0)]   # 6 cores, 2x3 grid in the jacket section, ESTIMATED
for i,name in enumerate(['12V','GND','TX','RX','CVBS_SIGNAL','CVBS_RETURN']):
    core=route_tube(harness_segs,.22,*_core_ab[i])
    jacket=cut(jacket,core);add(f'CAMERA_HARNESS_CORE_{i+1}_{name}_ROUTE_HOLD',core,'wire')
add('HOLD_LAPP_0028679_CAMERA_HARNESS_6CORE_ROUTE',jacket,'cable')
# Open snap clips on the lever plate (cable slides through, 4.0 mouth < OD 5.4), bonded/screwed to the plate top Z106.9.
def harness_clip(hx):
    c=cut(between((hx-6,0,HARNESS_TOP_Z),(hx+6,0,HARNESS_TOP_Z),4.5),between((hx-6.1,0,HARNESS_TOP_Z),(hx+6.1,0,HARNESS_TOP_Z),HARNESS_OD/2+.15))
    c=cut(c,box0(hx-6.2,-5,AZ,12.4,10,LIFT_PLATE_TOP_Z+.05-AZ))
    return cut(c,boxc(hx,0,HARNESS_TOP_Z+4,14,4,5))
hguard=harness_clip(HARNESS_GUIDE_X[0])
add('PX1_LIFT_HARNESS_CLIP_ON_LEVER_OPEN_PROFILE_1',hguard,'print')
add('PX1_LIFT_HARNESS_CLIP_ON_LEVER_OPEN_PROFILE_2',harness_clip(HARNESS_GUIDE_X[1]),'print')
# Printed bend guide (fixed, R17 >= 3xOD) on the Skintop top face: tube K -> gland exit + seat disc on the gland.
_gsegs=harness_segs[HARNESS_SEG_K:HARNESS_SEG_K+1]
bguide=cut(route_tube(_gsegs,HARNESS_OD/2+1.5),route_tube(_gsegs,HARNESS_OD/2+.15))
bguide=fuse_all([bguide,cut(cyl_z(CAM_GLAND_XY[0],CAM_GLAND_XY[1],GLAND_EXIT_Z,LAPP_OD/2,1.6),
                             cyl_z(CAM_GLAND_XY[0],CAM_GLAND_XY[1],GLAND_EXIT_Z-.1,HARNESS_OD/2+.15,1.8))])
bguide=cut(bguide,route_tube(_gsegs,HARNESS_OD/2+.15))
add('PX1_CAMERA_CABLE_BEND_GUIDE_R17_GLAND_ON_FITTING_HOLDER',bguide,'print')
# F23 internal camera cable (fixed). Service disconnect: SVC connector beside the STM32 board, under the plug opening.
inner_segs=route_walk(INNER_START,(0,0,-1),INNER_ROUTE)
_je=inner_segs[-1][1][-1]                                            # jacket end (X255.2, Y0, Z59)
add('HOLD_LAPP_0028679_CAMERA_CABLE_INTERNAL_PASSAGE_TO_BREAKOUT',route_tube(inner_segs,HARNESS_OD/2),'cable')
bundle_segs=route_walk(_je.toTuple(),(-1,0,0),BUNDLE_ROUTE)
bundle=route_tube(bundle_segs,BUNDLE_OD/2)
_bb_r,_bb_l,_bb_c=INNER_BOOT
boot=cut(cut(cyl_x(_je.x-_bb_c,0,_je.z,_bb_r,_bb_l),route_tube(inner_segs,HARNESS_OD/2)),bundle)
add('HOLD_CAMERA_CABLE_BREAKOUT_BOOT_POTTED',boot,'cable')
add('HOLD_CAMERA_CORE_BUNDLE_6x0p25_TO_SERVICE_CONNECTOR',bundle,'wire')
_ce=bundle_segs[-1][1][-1]
SVC_CONN_X1=_ce.x
add('HOLD_CAMERA_SERVICE_CONNECTOR_6P_W2W_MATED',box0(SVC_CONN_X1-SVC_CONN[0],_ce.y-SVC_CONN[1]/2,SVC_CONN_ZC-SVC_CONN[2]/2,*SVC_CONN),'connector')
controller=cq.importers.importStep(str(CAD/'vendor'/'WeAct_F4_64Pin_V11_Manufacturer.step'))
controller=wp(cq.Compound.makeCompound(controller.vals()))
b=controller.val().BoundingBox();controller=controller.translate((-(b.xmin+b.xmax)/2,-(b.ymin+b.ymax)/2,-b.zmin))
controller=controller.rotate((0,0,0),(0,0,1),90).translate((208,0,60.1))
add('WEACT_STM32F446RET6_V11_MANUFACTURER_STEP',controller,'electronics')
g2=cq.importers.importStep(str(CAD/'vendor'/'Pololu_G2_24v13_Manufacturer.step')).translate((-16.51,-10.16,0))
for i,(x,z) in enumerate(((47,59),(99,24.5)),1):add(f'POLOLU_2992_G2_24v13_{i}_MANUFACTURER_STEP',g2.translate((x,0,z)),'electronics')  # F16: #2 lowered under motors; F14: #1 raised Z26->59 above the balun (clears M8 plate-screw boss)
# ---------------- F20 Cincon on the cover underside + 24 V bus protection ----------------
_pad_z0=SERVICE_Z-THERMAL_PAD_T; _mod_z0=_pad_z0-CINCON[2]          # pad Z74.5..75, module Z61.8..74.5
cinc=boxc(CINCON_XC,CINCON_YC,_mod_z0+CINCON[2]/2,*CINCON)
for _hx,_hy in F20_CINCON_HOLES: cinc=cut(cinc,cyl_z(_hx,_hy,_mod_z0-.1,CINCON_HOLE_R,CINCON[2]+.2))
_pins=[cyl_z(CINCON_XC+CINCON_PIN_ROW_DX/2,CINCON_YC+y,_mod_z0-CINCON_PIN_L,CINCON_PIN_R,CINCON_PIN_L+.01) for y in CINCON_PIN_Y_IN]
_pins+=[cyl_z(CINCON_XC-CINCON_PIN_ROW_DX/2,CINCON_YC+y,_mod_z0-CINCON_PIN_L,CINCON_PIN_R,CINCON_PIN_L+.01) for y in CINCON_PIN_Y_OUT]
cinc=fuse_all([cinc]+_pins)
add('HOLD_CINCON_CQB150W110S24C_BASEPLATE_UP_ON_SERVICE_COVER',cinc,'electronics')
pad=boxc(CINCON_XC,CINCON_YC,_pad_z0+THERMAL_PAD_T/2,CINCON[0],CINCON[1],THERMAL_PAD_T)
for _hx,_hy in F20_CINCON_HOLES: pad=cut(pad,cyl_z(_hx,_hy,_pad_z0-.1,1.7,THERMAL_PAD_T+.2))
add('HOLD_THERMAL_PAD_0p5_3WmK_DCDC_ON_SERVICE_COVER',pad,'electronics_hold')
def socket_screw_up(x,y,z_bear,length):
    hr,hk=ISO4762_M3
    head=cut(cyl_z(x,y,z_bear-hk,hr,hk),cq.Workplane('XY').polygon(6,2.5/math.cos(math.pi/6)).extrude(2.0).translate((x,y,z_bear-hk-.01)))
    return fuse_all([head,cyl_z(x,y,z_bear,1.5,length)])
for _i,(_hx,_hy) in enumerate(F20_CINCON_HOLES,1):
    add(f'FIX_DIN912_M3x18_DCDC_ON_SERVICE_COVER_{_i}',socket_screw_up(_hx,_hy,_mod_z0,CINCON_SCREW_L),'shaft')
# Brake shunt 10 Ohm Al-housed resistor, bonded (pad) to the cover, 2x M3x8 through its tabs.
_sx,_sy=F20_SHUNT_XY; _L,_W,_H=SHUNT_R_ENV; _tl,_tt=SHUNT_R_TAB; _rz0=_pad_z0
shunt=fuse_all([boxc(_sx,_sy,_rz0-_tt/2,_L,_W,_tt),boxc(_sx,_sy,_rz0-_H/2,_L-2*_tl,_W,_H)])
for _hx,_hy in F20_SHUNT_HOLES: shunt=cut(shunt,cyl_z(_hx,_hy,_rz0-_tt-.1,1.6,_tt+.2))
add('HOLD_BRAKE_SHUNT_10R_10W_ALU_HOUSED_ON_SERVICE_COVER',shunt,'electronics_hold')
spad=boxc(_sx,_sy,_pad_z0+THERMAL_PAD_T/2,_L,_W,THERMAL_PAD_T)
for _hx,_hy in F20_SHUNT_HOLES: spad=cut(spad,cyl_z(_hx,_hy,_pad_z0-.1,1.7,THERMAL_PAD_T+.2))
add('HOLD_THERMAL_PAD_0p5_BRAKE_SHUNT_ON_SERVICE_COVER',spad,'electronics_hold')
for _i,(_hx,_hy) in enumerate(F20_SHUNT_HOLES,1):
    add(f'FIX_DIN912_M3x8_BRAKE_SHUNT_ON_SERVICE_COVER_{_i}',socket_screw_up(_hx,_hy,_rz0-_tt,8.0),'shaft')
# Shunt control board (comparator 27.0 on / 26.0 off + MOSFET) on 2x M3 hex standoffs; TVS SMBJ26A on its underside.
_bx,_by=F20_BOARD_XY; _bL,_bW,_bT=SHUNT_BOARD; _so=2.5; _pcb_z1=SERVICE_Z-_so
board=fuse_all([boxc(_bx,_by,_pcb_z1-_bT/2,_bL,_bW,_bT),box0(_bx-_bL/2+1,_by-_bW/2+1,_pcb_z1-_bT-4.5,18,_bW-2,4.5)])
add('HOLD_BRAKE_SHUNT_CTRL_BOARD_CMP27V_MOSFET_ON_SERVICE_COVER',board,'electronics_hold')
for _i,(_hx,_hy) in enumerate(F20_STANDOFFS,1):
    add(f'FIX_M3_HEX_STANDOFF_2p5_BOARD_ON_SERVICE_COVER_{_i}',fuse_all([cyl_z(_hx,_hy,_pcb_z1,2.75,_so),cyl_z(_hx,_hy,SERVICE_Z,1.5,4.0)]),'shaft')
_tL,_tW,_tH=SMB_DO214AA
add('HOLD_TVS_SMBJ26A_DO214AA_ON_SERVICE_COVER',boxc(_bx+_bL/2-5,_by,_pcb_z1-_bT-_tH/2,_tL,_tW,_tH),'electronics_hold')
# 470 uF/50 V at the Cincon output row (front, X129.6), lying along X under the cover.
add('HOLD_BUS_CAP_470uF_50V_CINCON_OUT_ON_SERVICE_COVER',cyl_x(100.0,-15.5,69.0,*BUS_CAP_470),'electronics_hold')
# 2x 330 uF/50 V next to each G2 (power terminals end), housing-mounted (clip/adhesive HOLD).
add('HOLD_BUS_CAP_330uF_50V_G2_1',cyl_x(64.5,0.0,64.0,*BUS_CAP_330),'electronics_hold')
add('HOLD_BUS_CAP_330uF_50V_G2_2',cyl_z(77.0,0.0,CAVITY_FLOOR_Z+.5,*BUS_CAP_330),'electronics_hold')
add('NICHICON_UCS2D221MHD1TN_BODY18x25',cyl_z(278,0,30,9,25),'electronics')
add('ADAFRUIT_MPRLS_3965_ENVELOPE',boxc(277.5,-17.5,60,*MPRLS),'electronics')
add('HOLD_POLOLU_5577_D42V55F12_ENVELOPE',boxc(211.5,-13.5,29,*POLOLU_5577),'electronics')
add('HOLD_POLOLU_5571_D42V55F5_ENVELOPE',boxc(211.5,13.5,29,*POLOLU_5571),'electronics')
add('HOLD_WAVESHARE_27479_ISOLATED_RS485_C_ENVELOPE',boxc(264,-15.0,68,*WAVESHARE_27479),'electronics')  # F22: Y0->-15, clears the gland feed-through below X272
add('HOLD_DELTA_TR1D_P2_VIDEO_BALUN',boxc(52,0,50,*VIDEO_SCREEN),'electronics_hold')  # F16: moved forward of motors
body=cut(body,cyl_x(287.9,0,45,8.6,8.2))
add('HOLD_WEIPU_SP1712_7PIN_REAR_PANEL_6_USED',make_sp17_panel().translate((296,0,45)),'connector')
strain=cut(cyl_x(316,0,45,12,32),cyl_x(315.9,0,45,10,32.2))
cone=cq.Workplane('YZ').circle(10).workplane(offset=30).circle(6).loft(combine=True).translate((316,0,45))
cone=cut(cone,cyl_x(315.9,0,45,4.5,32.2))
add('HOLD_REAR_TETHER_STRAIN_SLEEVE',strain,'metal');add('HOLD_REAR_TETHER_ARAMID_CONE',cone,'metal')
add('HOLD_MAIN_TETHER_6CORE_REINFORCED_ARTICLE_UNKNOWN',cyl_x(348,0,45,4.5,80),'cable')
plate=box0(WEIGHT_PLATE_X0,-WEIGHT_PLATE_W/2,BODY_Z0,WEIGHT_PLATE_X1-WEIGHT_PLATE_X0,WEIGHT_PLATE_W,WEIGHT_PLATE_H)
_cb_floor=BODY_Z0+WEIGHT_PLATE_H-PLATE_CBORE_LIG          # Z19.0
_wri,_wro,_ws=SPRING_WASHER_M8; _hr,_hk,_hs=DIN7984_M8
_bear=_cb_floor-_ws                                         # head bearing face Z17.0; head bottom Z12.0 (1.0 recessed)
for _i,(_px,_py) in enumerate(PLATE_SCREW_XY,1):
    plate=cut(plate,cyl_z(_px,_py,BODY_Z0-.1,PLATE_CBORE_R,_cb_floor-BODY_Z0+.1))
    plate=cut(plate,cyl_z(_px,_py,_cb_floor-.1,PLATE_SCREW_HOLE_R,PLATE_CBORE_LIG+.2))
    head=cut(cyl_z(_px,_py,_bear-_hk,_hr,_hk),
             cq.Workplane('XY').polygon(6,_hs/math.cos(math.pi/6)).extrude(3.0).translate((_px,_py,_bear-_hk-.01)))
    screw=fuse_all([head,cyl_z(_px,_py,_bear,M8_COSMETIC_THREAD_R,PLATE_SCREW_L)])   # tip Z33.0, engagement 10.0
    add(f'FIX002764_M8x16_DIN7984_PLATE_{_i}',screw,'shaft')
    add(f'FIX002741_M8_SPRING_WASHER_{_i}',cut(cyl_z(_px,_py,_bear,_wro,_ws),cyl_z(_px,_py,_bear-.1,_wri,_ws+.2)),'shaft')
add('FSS002060_WEIGHT_PLATE_STAINLESS_M8_FIXING_HOLD',plate,'metal')
for i,b in enumerate(BALLAST_BOXES,1):
    add(f'HOLD_BALLAST_{i}_STEEL',box0(b[0],b[1],b[2],b[3]-b[0],b[4]-b[1],b[5]-b[2]),'metal')
components.insert(0,('HOLD_PRESSURE_BODY_CRP150_GRAPHIC278x68x64_CAVITY_UNRESOLVED',body,'body'))
from release_tools import finish_build
finish_build(globals())
