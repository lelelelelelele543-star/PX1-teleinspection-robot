# PX-1 WB23E/WB23G pressure/camera service assembly — prototype BOM

Date: 2026-09-14
Status: **BOM CANDIDATE / PROCUREMENT HOLD**

This BOM is limited to the pressure-service cover and local camera/lift harness assembly.

| Qty | Item | Candidate article / material | Requirement | Installation | State |
|---:|---|---|---|---|---|
| 1 | Pressure/camera service cover | EN AW-6082-T6 machined plate | **86 x 44 x 6 mm** | top pressure roof, two M4 screws | WB23E screen PASS |
| 2 | Cover screws | A4 stainless M4, retained preferred | centres X226 / X296; length TBD from final boss engagement | blind threaded bosses | sample HOLD |
| 1 | Cover seal | 2.0 mm FKM cord or molded equivalent | provisional groove width 2.5 mm; final groove from real elastomer | continuous closed perimeter | groove HOLD |
| 1 | Cable gland | LAPP SKINTOP MS-M `53112000` | M12x1.5, 3.5–7 mm cable | horizontal forward-facing boss | candidate controlled |
| 1 | Pressure/fill valve | very low-profile service valve | preferred exposed envelope <=Ø12 x 5 mm; prototype hard screen <=Ø14 x 6 mm | service cover around X273/Y0 | article HOLD |
| 1 | Valve protection cap | compact/recessed preferred | cap included in pressure-port hard envelope | fill valve | HOLD |
| 1 | Dry receptacle housing | Molex Micro-Fit 3.0 `43025-0600` | 6 circuits | internal dry harness side | WB23G candidate |
| 1 | Dry plug housing | Molex Micro-Fit 3.0 `43020-0601` | 6 circuits, no panel ears | internal dry mating side | WB23G candidate |
| 6 | Female crimp contacts | Molex `43030-0007` candidate | 20/22/24 AWG class | `43025-0600` | sample HOLD |
| 6 | Male crimp contacts | Molex `43031` family | exact article after real conductor/insulation measurement | `43020-0601` | article HOLD |
| 1 | Local camera cable | **6 insulated cores + overall shield** | target 6 x 0.25 mm²; preferred OD 5.5–6.0 mm; hard max 6.5 mm | gland -> lift -> SP13 | article/flex HOLD |
| 1 | Size benchmark cable | LAPP UNITRONIC LiYCY `0034406` | 6 x 0.25 mm², shielded, nominal OD 6.0 mm | prototype/sample benchmark only | FLEX-LIFE HOLD |
| 1 | Camera cable plug | WEIPU `SP1310/S6I-N` | 6 sockets; cable range 4.0–6.5 mm | lift-harness end | WB15 candidate |
| 1 | Camera panel connector | WEIPU `SP1312/P6-C` | 6 male contacts | sealed camera rear panel | WB15 candidate |
| 1 | Lift-arm harness guard | 1 mm stainless/Al or printed fit prototype | conservative outside envelope ~10 mm; drain-open/removable | protects lower-arm straight run | WB23G screen PASS |
| 1 | Internal strain-relief clamp | P-clamp / machined clamp | fits real cable without jacket damage | before dry Micro-Fit connector | HOLD |

## Six-core allocation

1. +12V_HEAD
2. GND_HEAD
3. UART_TX
4. UART_RX
5. CVBS_SIGNAL
6. CVBS_RETURN

Overall braid/shield is EMC only and is not a DC return conductor.

## WB23E cover/opening control values

- cover centre X261 / Y0;
- cover 86 x 44 x 6 mm;
- service opening 48 x 22 mm;
- opening X237...285 / Y-11...+11;
- two M4 centres X226 / X296;
- provisional groove centre path offset 4.0 mm from opening edge;
- provisional groove width 2.5 mm;
- minimum M4 clearance-hole edge to provisional groove outer edge 3.5 mm;
- minimum M4 head edge to cover outer edge 4.0 mm;
- minimum provisional groove outer edge to cover Y edge 5.75 mm.

The groove depth/compression is not machining release until the real seal is selected.

## WB23G packaging correction

The previous ≤5 mm / 8-core local cable study is superseded. WB23G validates a six-core cable hard envelope up to Ø6.5 mm with a 10 mm conservative arm-guard envelope. LOW guard ideal-DN150 clearance remains about 27.78 mm with no collision against Z50 or the camera envelope.

## Material notes

- Cover: 6082-T6 first-machined prototype target; final surface treatment after corrosion/fit trials.
- Seal: FKM preferred initial wastewater/chemical candidate; NBR acceptable only for early dry bench work unless subsequently qualified.
- Fasteners: A4 stainless preferred externally; final torque depends on thread engagement, lubrication and gasket compression.

## Do not bulk-order yet

Do not bulk-order custom covers, cable, molded seals, fill valves or SP13/Micro-Fit quantities until first pressure/flex/electrical qualification passes. Buy only enough for prototype samples and destructive/backup tests.
