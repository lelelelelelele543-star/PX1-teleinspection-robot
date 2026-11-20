# PX1 gate — WARN

Сборка: `current/CAD/PX1_Current_Master.step.gz` (285 деталей), 2026-11-20 19:14. Это экран CAD-модели: не изготовление, не герметичность, не реальная тяга.

| Проверка | Итог | Коротко |
|---|---|---|
| Геометрия тел | PASS | невалидных 0, сверка с реестром: 285/285 имён, макс. расхождение объёма 0.000 % |
| Состав (колёса, Z50, Z16/Z40, моторы) | PASS | колёса 6/6, шестерни Z50 10/10, конические Z40 2/2, конические Z16 2/2, тяговые моторы 2/2 |
| Пересечения деталей | PASS | жёстких 0, ошибок 0, HOLD 0 (—); Boolean-пар 1252 |
| Зазор до стенки DN150 | WARN | минимум 3.22 мм — HOLD_QRW90_HUB_AL_-1_50.0_ESTIMATED; <3: 0, 3–5: 8 |
| Масса | WARN | 7.92 кг при цели 9.25 (-14.4 %) |
| Устойчивость в трубе | WARN | ЦТ ниже оси на 2.2 мм, вбок +0.1 мм, оси 49% / 33% / 17% |
| Мастер против чертежей Mini-Cam | PASS | PASS: 161 checks, PASS 161, FAIL 0, SKIP 0 |
| Лифт камеры и кабель | PASS | 21/21 проверок (радиусы изгиба кабеля ≥5×D/3×D, запас длины, газовая пружина, зазор при подъёме 2.29 мм) |
| Тесты расчёта питания по кабелю | PASS | PX1 A2 tether power tests: PASS |
| Бюджет мощности 24 В | INFO | wrote current/09_RELEASE/gate_20261120/power_budget.json |
| Тяга: 40 м сейчас, 100–150 м потом | WARN | 40 м: запас +20.7 Н (slime/grease); 100 м: запас +8.4 Н (slime/grease); осторожный кабель: slime/grease не тянет; 150 м: запас -1.9 Н (slime/grease); осторожный кабель: slime/grease, wet concrete/PVC не тянет |
| Интегральная проверка сборки | SKIP | нужна свежая сборка scripts/cloud/build_current.sh (~9 мин); STEP-проверки выше её дублируют |

PASS — требование выполнено; WARN — выполнено с малым запасом или не та цель; HOLD — контакт по замыслу, нужна отдельная проверка; FAIL — нарушение; INFO — расчёт без критерия; SKIP — не запускалось.

## Ближе всего к стенке трубы

| Деталь | Зазор, мм | Итог |
|---|---|---|
| HOLD_QRW90_HUB_AL_-1_50.0_ESTIMATED | 3.22 | WARN |
| HOLD_QRW90_HUB_AL_-1_150.0_ESTIMATED | 3.22 | WARN |
| HOLD_QRW90_HUB_AL_-1_250.0_ESTIMATED | 3.22 | WARN |
| HOLD_QRW90_HUB_AL_1_50.0_ESTIMATED | 3.22 | WARN |
| HOLD_QRW90_HUB_AL_1_150.0_ESTIMATED | 3.22 | WARN |
| HOLD_QRW90_HUB_AL_1_250.0_ESTIMATED | 3.22 | WARN |
| PX1_CAMERA_CABLE_BEND_GUIDE_R17_GLAND_ON_FITTING_HOLDER | 4.05 | WARN |
| HOLD_LAPP_0028679_CAMERA_HARNESS_6CORE_ROUTE | 4.50 | WARN |

## Самые тяжёлые детали

| Деталь | кг | плотность | правило |
|---|---|---|---|
| FSS002060_WEIGHT_PLATE_STAINLESS_M8_FIXING_HOLD | 1.154 | 7.9 | FSS-002-060 Waight Plate (DRW375) |
| HOLD_PRESSURE_BODY_CRP150_GRAPHIC278x68x64_CAVITY_UNRESOLVED | 0.589 | 2.7 | FAL-002-058 Crawler Housing |
| HOLD_CAM026_PAN_TILT_HEAD_ENVELOPE_120x74x74 | 0.545 | 1.727 | F18: CAM026 envelope density scaled to catalogue 0.864 kg (C |
| HOLD_CAM026_ROTATE_HOUSING_GRAPHIC_OD62p5 | 0.318 | 1.727 | F18: CAM026 envelope density scaled to catalogue 0.864 kg (C |
| HOLD_SIDE_COVER_-1_GRAPHIC262x60x7 | 0.253 | 2.7 | FAL-002-062 Side cover |
| HOLD_SIDE_COVER_1_GRAPHIC262x60x7 | 0.253 | 2.7 | FAL-002-062 Side cover |
| HOLD_BALLAST_1_STEEL | 0.209 | 7.85 | F17 ballast blocks, steel by default (override --ballast-den |
| HOLD_BALLAST_2_STEEL | 0.209 | 7.85 | F17 ballast blocks, steel by default (override --ballast-den |

Ограничения устойчивости: Сложенный лифт, номинальная поза, жёсткие шины. Поднятый лифт, натяжение кабеля и уклон не учтены.

Повторить: `python3 tools/gate/px1_gate.py` (≈5–10 мин). Требования: `tools/gate/px1_gate_spec.json`.
