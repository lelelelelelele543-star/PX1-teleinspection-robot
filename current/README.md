# PX1 Current

Единственный текущий комплект. Механический эталон Proteus CRP-150; собственная электроника на готовых платах.

## Rev.A fast-track

**Rev.A обязательно шестиколёсный. 4-колёсный вариант не является допустимым упрощением.**

Активный порядок разработки описан в [REV_A_FAST_TRACK.md](REV_A_FAST_TRACK.md).

Рабочие пакеты:
- [00_PROJECT_CONTROL](00_PROJECT_CONTROL/README.md)
- [01_MECHANICAL_6X6](01_MECHANICAL_6X6/README.md)
- [02_ELECTRICAL](02_ELECTRICAL/README.md)
- [03_FIRMWARE](03_FIRMWARE/README.md)
- [04_CAMERA_HEAD](04_CAMERA_HEAD/README.md)
- [05_TETHER_REEL](05_TETHER_REEL/README.md)
- [06_CONSOLE](06_CONSOLE/README.md)
- [07_TESTS](07_TESTS/README.md)
- [08_PROCUREMENT](08_PROCUREMENT/README.md)
- [09_RELEASE](09_RELEASE/README.md)

## Current engineering baseline

- CAD/PX1_Current_Master.py — единственный исходник текущей сборки.
- CAD/PX1_Current_Master.step — экспорт после успешной сборки.
- PX1_Current_BOM.csv — единая BOM.
- PX1_Current_Validation.json — проверка конкретного экспорта; старые результаты не переносить.
- PX1_Change_Log.md — единый журнал изменений.
- SOURCE_REGISTER.md — источники размеров и границы достоверности.
- ELECTRICAL_Current.md — схемные соединения и логические распиновки.
- ASSEMBLY_AND_TESTS_Current.md — герметизация, давление, сборка, обслуживание, испытания.
- PX1_Drawings_Current.pdf / PX1_Documentation_Current.pdf — текущие документы.

Frozen crawler architecture: six wheels; stations X50/X150/X250; ten Z50 total; two traction motors; Z16→Z40→rear X250 axle→Z50 train. Manual lift, separately sealed camera, reinforced six-core main tether without coax, no custom main PCB required for the first prototype.

`Metal_HOLD` and unresolved CAD remain prototype-only. A successful CAD export is not an engineering PASS. Historical WB/Rev files are retained as history and cannot override `current/`.
