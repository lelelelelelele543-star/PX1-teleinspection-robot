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
