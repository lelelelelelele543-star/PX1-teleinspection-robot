# Mini-Cam Proteus: verified public service-source leads (2026-11-05)

This index records publicly accessible technical material and distinguishes component catalogs from circuit schematics.

## Newly confirmed engineering facts
- Official Minicam page: all Proteus crawlers feature **CAN bus** between attached modules; speed, pressure, inclination, temperature telemetry. This is public evidence of use of CAN on system modules, **not a connector pinout, CAN bitrate, frame ID list or proof of CAN signal transport over the entire tether**. Source: https://www.minicam.co.uk/systems/crawlers/
- Older Mini-Cam Proteus manufacturer brochure also explicitly mentions CAN bus technology. Source: https://ndtshop.dk/upload_dir/shop/Minicam/proteus-en.pdf
- Parts supplier indexes **CAM026TESTRIG-EXZ1**, a standard/ExZ1 CAM026 test rig, and **ASS-007-917**, a crawler-to-CCU test lead. They are service-related hardware part numbers; the catalog does **not** provide their circuit diagrams, software or usage instructions. Source: https://heartandindustry.com/brands/b-minicam-ltd
- Supplier indexes **PCB-003-463**, the CCU rear-panel video/serial connector PCB, **PCB-002-203** USB hub PCB, **PCB-002-215** CCU joystick PCB, and **PCB-002-681** CCU HV PSU PCB. These give additional subsystem board identities, not schematics. Source: https://heartandindustry.com/brands/b-minicam-ltd
- The parts supplier specifically says **no photograph yet** for **PCB-002-238**, CRP150 top-housing main PCB. Source: same catalog.
- Minicam confirms component-level troubleshooting requires understanding schematics and technical drawings in its service-technician role descriptions. This shows professional servicing is supported, **not** that service schematic documents are publicly released. Source: https://www.minicam.co.uk/company/careers/
- Minicam service pages state full camera/crawler teardown and rebuild, PCB replacements and fault-finding are available through service centres. Source: https://www.minicam.co.uk/servicing/minicam-servicing/
- Manufacturing of CRP150 ceased in 2018 and official support ended 2026-04-01; a limited spare-parts inventory remains. Source: https://www.minicam.co.uk/support/

## Available owner-held drawings
Already verified in private Drive: CRP150 DRW-002-374, DRW-002-375, DRW-002-386, DRW-002-744, DRW-002-745; CAM026 ASM001, ASM002, ASM004, ASM005, ASM011. These show assembly position and part identities, **not electronic circuit/netlist data**. Do not re-upload restricted manufacturer PDFs to the public repository.

## Negative findings and required next evidence
Web searches for the exact strings PCB-001-982, PCB-002-238 and PCB-002-053.S in combination with schematic, PDF, board photo, repair and eBay returned catalog references, but no verified publicly accessible electrical netlists or clear two-sided board photographs. Search results are not proof of nonexistence. Never mislabel unrelated 'minCam' or 'MoniCam' photos as Mini-Cam Proteus.

For independently designed PX1: investigate CAN protocol using passive measurements on **owner-authorized hardware only** (physical connector, isolated CAN transceiver, controlled bench), document pinout only after measurement and verify signal voltage and bus topology before attempting connection.

## Second search pass: public manuals / further direct documents

1. **Legacy Proteus CRP150 user manual, 56 pages**: https://www.manualslib.com/manual/1529286/Mini-Cam-Proteus-Crp150.html . It has CRP150 specific chapters on maintenance (pp. 31-33), camera (pp. 34-36), CCU208 (pp. 46-54), wiring connection diagrams (pp. 21-25). **It is not a component-level service manual** and does not include PCB schematics.
2. **Older Proteus Lite Version C, 2019 hosted copy, 111+ pages**: https://ehle-hd.com/wp-content/uploads/2019/04/Proteus_Lite_Manual_EN_VerC.pdf . Contents include pages 48-54 on CCU208 Wi-Fi setup, PC file sharing and WinCan Web, pages 67-69 CAM026 pressure/testing. Its safety section explicitly restricts electronics repairs to trained technicians/service center (not a service schematic).
3. **Older Proteus manual in German Version D** with troubleshooting for older crawler/reel arrangements: https://www.manualslib.de/manual/204524/Minicam-Proteus.html ; troubleshooting near page 82. Readable documentation, **not a PCB-level manual**.
4. **VCU500/ VKU500 Version B public manual**: https://device.report/m/648f476c3f7fe841b25fcfe45bb276a7518498e64111cf8219a5eeb42468ef46 . States VCU500 is a 1U rack variant developed from CCU208, with HDMI/VGA and two BNC composite outputs. Functional similarity is established, **not identical PCB design**.
5. **Original Proteus Lite technical brochure**: https://minicaminc.com/wp-content/uploads/2024/10/Proteus-Lite.pdf . Specifies CCU208 + RMPL250 + CPL150S + CAM026, PAL 512x582 CCD camera, 6-LED lighting, manual elevator, 6.8 mm Kevlar-reinforced cable for the Lite reel (250m, 5.5kg/100m, stated 500kg breaking strength). These are specifications for *Lite*, not necessarily CRP150 original tether. Do not confuse external power adapter input (12/24V vehicle) with internal module voltages.
6. **Minicam HD 6-core copper cable**: https://www.minicam.co.uk/systems/crawlers/hd-mainline-system/ . Current generation Proteus HD claims 500m Full HD over lightweight repairable **6-core copper cable**, and reuses this cable type. This confirms the manufacturer's cable choice at system level; **not** the conductor pin assignment, electrical modulation or proof every revision is identical.
7. **Original Proteus ATEX Zone 1 user manual**: https://www.manualslib.com/manual/1855972/Proteus-Atex-Zone-1.html . Has operational troubleshooting on page 66 (power supply and failed pressurisation), **not schematic**.
8. **CAM026 one-page official specification**: https://www.minicam.co.uk/wp-content/uploads/2022/04/CAM026-1.pdf and https://www.minicam.co.uk/products/cameras/pan-rotate/ . Useful for envelope, FOV, and mechanical reference, **not PCB**.

## Search quality / negative results

Image search with "Minicam" repeatedly returns unrelated A9 spy-camera PCB tear-downs and incorrectly tagged consumer electronics. **Do not cite or reproduce those images as Mini-Cam Ltd Proteus circuit boards**. No verified publicly indexed double-sided board images, CAD netlists, test-rig manuals, or official component-level repair manuals for PCB-001-982, PCB-002-238, PCB-002-053.S or CAM026TESTRIG-EXZ1 were found in this pass. Search result absence does not establish nonexistence.

## Technical decision from evidence

- Prefer a **separate self-developed control architecture** for PX1 rather than trying to duplicate undocumented proprietary PCB netlists.
- For passive characterization on an owner-owned robot, log mechanical/connector geometry, take macro photographs and use manufacturer-accessible operating manuals to identify safe pressure and power limits.
- CAN is confirmed in the Proteus modular crawler family, but whether CAN runs directly through the **entire 6-core long tether** is **not** proven by documentation; do not assume direct CAN signalling at 500m.
