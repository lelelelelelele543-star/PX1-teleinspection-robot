# Session handoff — 2026-11-20

Ветка: feature/px1-integrated-cad-20261117 (claude/px1-audit-traction-20261119 на GitHub не существует).
Источник геометрии: current/CAD/PX1_Current_Master.py.

## Сделано
- F04 — зазор шин в DN150 ≥3 мм: current/09_RELEASE/f04_wheel_gap_20261119/README.md.
- F05 — торцевое уплотнение фланца по DRW-002-374: current/09_RELEASE/f05_flange_face_seal_20261119/README.md.
- F06 — коническая пара Z16/Z40 с зубьями: current/09_RELEASE/f06_bevel_teeth_20261119/README.md.
- F07 — резьба M5 колеса, сборка без пересечений и HOLD-контактов: current/09_RELEASE/f07_m5_cosmetic_thread_20261119/README.md.
- F08 — крепёж M3 крышек и фланцев: current/09_RELEASE/f08_m3_fasteners_20261119/README.md.
- F09 — бюджет тяги и скорости: current/07_TESTS/TRACTION_BUDGET_F09.md.
- F10 — уплотнение боковой крышки 190×1,5: current/09_RELEASE/f10_side_cover_seal_20261119/README.md.
- F11 — грузовая плита FSS-002-060, масса 6,1 кг: current/09_RELEASE/f11_weight_plate_20261119/README.md.
- F12 — подбор мотора класса Proteus: current/08_PROCUREMENT/MOTOR_F12_PROTEUS_CLASS_20261119.md.
- F16 — привод габарита Proteus вписан: current/09_RELEASE/f16_proteus_class_motor_20261119/README.md.
- F17 — балласт и ступицы, масса 7,1/8,0 кг: current/09_RELEASE/f17_ballast_hubs_20261119/README.md.
- F13 — замок колеса по ASS-002-103 (диск-кулачок, M6×14): current/09_RELEASE/f13_wheel_lock_20261119/README.md.
- F14 — крепление плиты 2×M8 по DRW-002-375: current/09_RELEASE/f14_plate_fixing_20261119/README.md.
- F18 — лифт камеры по DRW-002-744/752 (параллелограмм, зажим, газовая пружина, CAM026): current/09_RELEASE/f18_camera_lift_20261119/README.md.
- F19 — бюджет мощности: current/02_ELECTRICAL/POWER_BUDGET_F19_20261119.md.
- F20 — Cincon на крышке с термопрокладкой, конденсаторы/TVS/шунт шины 24 В: current/09_RELEASE/f20_cincon_thermal_20261120/README.md.
- F21 — крепление основания лифта 4×M4×12 и кабель камеры по лифту (петля, запас 14,4 мм): current/09_RELEASE/f21_lift_fixing_cable_20261120/README.md.
- F22 — крышка электроники по DRW-002-745: проём-пробка 143×53, радиальное 110×1,5, проходы ввода/клапана: current/09_RELEASE/f22_rear_cover_20261120/README.md.

Решения пользователя 2026-11-19: догрузить PX1 до ~9 кг; более сильный мотор искать сейчас; балласт — СТАЛЬ; работать с помощниками (агентами) параллельно, CAD-мастер правит один исполнитель за раз.

## Важно для следующей сессии
1. Прежние feature_list.json / progress.md / session-handoff.md на GitHub отсутствовали; список F05–F10 составлен заново.
1a. Доступ GitHub App для Claude установлен 2026-11-19, push работает.
2. tools/drawing_measure/check_master_vs_drawings.py в ветке нет — первую проверку из списка выполнить нельзя,
   пока скрипт не будет добавлен.
2a. Общий STEP хранится как current/CAD/PX1_Current_Master.step.gz (полный ~100 МБ > лимита GitHub). После сборки: gzip -9 -c _cloud_build/CAD/PX1_Current_Master.step > current/CAD/PX1_Current_Master.step.gz
2b. Сетку assembly_mesh.json.gz держать только в последнем F-выпуске (см. current/09_RELEASE/README.md).
3. Окружение: pip install --break-system-packages cadquery (2.8.0); сборка ~3–9 мин, интегральная проверка ~1 мин.

## Следующий шаг
F22 выполнен (ветка f22-rear-cover, без push). Следующий — первый пункт со статусом "next" в feature_list.json.
Открыто по F22: растяжение 110×1,5 ≈8 % (как у Proteus, H03); кольцо 16×1,5 у ввода — не деталь Proteus; ушки/4×M4
Proteus не перенесены (под ними полость PX1); внешнюю пару M4 лифта можно вернуть на |Y| 27,9 (торцевой канавки больше нет);
кабель внутри корпуса от прохода Ø8 не смоделирован. Разбор 745: current/01_MECHANICAL_6X6/REAR_COVER_DRW745_20261120.md.
Проём крышки теперь SERVICE_OPEN_X0..X1 = 88…231 (SERVICE_PLUG_L 143): электроника под крышкой должна быть внутри пробки
(|Y| ≤ 23,95, X 90,55…228,45), иначе пересечение с буртиком.
Открыто по F21: выход кабеля из SP13 — R3 (нужен угловой хвостовик или перенос разъёма в корпусе 752, H07);
форма кабеля в промежуточных положениях лифта не моделировалась (только длина, tools/lift/check_lift_kinematics.py);
внешняя пара M4 сдвинута |Y| 27,9 → 25,0 из-за канавки крышки; момент затяжки M4 в Al; крепление клипс к рычагу.
Трасса кабеля задаётся константой HARNESS_ROUTE (линии/дуги); при изменении лифта/ввода прогнать кинематику —
она же проверяет, что трасса приходит точно в ввод M12. Клипса 2 дальше X180 даёт петлю 150+ мм при подъёме.
Открыто по F20: код опции Cincon «-C» и число втулок (2/4); материал крышки L01 — только Al; разъёмы и петля
проводов Cincon ↔ корпус; мощность тормозного резистора и схема платы шунта (HOLD-P5); крепление 330 мкФ.
Метка ON_SERVICE_COVER в имени детали = снимается вместе с крышкой (учтено в проверке извлечения моторов).
Обязательные проверки: build, check_pipe_pose --active, check_integrated --roundtrip --require-pipe-service,
check_master_vs_drawings, tools/lift/check_lift_kinematics.py.
