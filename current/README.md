# PX1 Current

## Текущее состояние (2026-11-20, F25 + крепление GP26)

Актуальная геометрия — `CAD/PX1_Current_Master.py` (CadQuery). Комплект проверки:
[GP26 mounting](09_RELEASE/gp26_mount_20261120/README.md), база `980c82a`, отдельная ветка `feature/px1-gp26-mount-integration-20261120`.
Сборка содержит 295 компонентов, пересечений нет. Проверки CAD/STEP 20/20, чертежей 161/161, лифта 21/21. Крепление моторов интегрировано с корпусом через внутренние бобышки; дно не просверлено насквозь.
Статус: **инженерный прототип, HOLD, не выпуск к изготовлению**.

- Ходовая: колёса QRW90 с зазором ≥3 мм в DN150 (F04), уплотнения фланца/крышки (F05, F10), коническая пара Z16/Z40 (F06),
  замок колеса M6×14 ISO 7380 по ASS-002-103 (F13), плита 2×M8 (F14), металлическая ступица (F15), балласт до ~8 кг (F17).
- Мотор: кандидат класса Proteus — ZHAOWEI ZWSMD026026 i=62 + MP2238 24 В-обмотка (F12/F16). Длительно 0,83 Н·м /
  82 об/мин при КПД 0,81 ESTIMATED; тяга 69,5 Н, 9,3 м/мин (расчёт, см. 07_TESTS/TRACTION_BUDGET_F09.md, поправка 20.11).
  GA24Y-370 и JGA25-370B — прежние примерочные кандидаты, заменены. Не куплен — H05.
- Питание: Cincon CQB150W-110S24 основанием на Al крышку L01 (F20), бюджет и тепловой режим — 02_ELECTRICAL/POWER_BUDGET_F19_20261119.md:
  длительно ток мотора ≤ 0,60 А RMS; 120/150 Вт и лимит 1,8 А — только кратковременно.
- Верх: крышка электроники по DRW-002-745 — сверху, задней крышки нет (F22); лифт камеры по DRW-002-744/752 (F18),
  крепление 4×M4×12 (F21), выход кабеля камеры из SP13 в литом хвостовике (F23). HOLD H07 (tether, разъёмы) открыт.

Прежние отчёты ([GA24 19.11](09_RELEASE/ga24_integration_20261119/README.md), [DN150 18.11](09_RELEASE/pipe_service_20261118/README.md))
— история, текущую конфигурацию не описывают. Старые PDF/изображения вне актуального комплекта не пересозданы.

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
- CAD/PX1_Current_Master.step.gz — экспорт после успешной сборки, сжат gzip (полный STEP ~100 МБ превышает лимит GitHub); распаковать `gunzip -k`.
- PX1_Current_BOM.csv — единая BOM.
- PX1_Current_Validation.json — проверка конкретного экспорта; старые результаты не переносить.
- PX1_Change_Log.md — единый журнал изменений.
- SOURCE_REGISTER.md — источники размеров и границы достоверности.
- ELECTRICAL_Current.md — схемные соединения и логические распиновки.
- ASSEMBLY_AND_TESTS_Current.md — герметизация, давление, сборка, обслуживание, испытания.
- PX1_Drawings_Current.pdf / PX1_Documentation_Current.pdf — текущие документы.

Frozen crawler architecture: six wheels; stations X50/X150/X250; ten Z50 total; two traction motors; Z16→Z40→rear X250 axle→Z50 train. Manual lift, separately sealed camera, reinforced six-core main tether without coax, no custom main PCB required for the first prototype.

`Metal_HOLD` and unresolved CAD remain prototype-only. A successful CAD export is not an engineering PASS. Historical WB/Rev files are retained as history and cannot override `current/`.
