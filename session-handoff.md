# Session handoff — 2026-11-19 (вечер)

Ветка Claude: **claude/px1** (создана от feature/px1-integrated-cad-20261117 @ 0aeb551). Правила — CLAUDE.md.
Источник геометрии: current/CAD/PX1_Current_Master.py.

## Сделано
- F04 — зазор шин в DN150 ≥3 мм: current/09_RELEASE/f04_wheel_gap_20261119/README.md.
- F05 — торцевое уплотнение фланца по DRW-002-374: current/09_RELEASE/f05_flange_face_seal_20261119/README.md.
  (F04/F05 закоммичены прямо в ветку ChatGPT feature/px1-integrated-cad-20261117 — дальше так не делать.)
- Заведена постоянная ветка claude/px1 и CLAUDE.md, чтобы пользователь мог гонять Claude с телефона.

## Важно для следующей сессии
1. Первая ревизия Claude (ветка claude/px1-audit-traction-20261119: tools/drawing_measure, calc/traction_requirement.py)
   на GitHub так и не попала (push 403) — утеряна. Восстановление — F11; расчёт тяги — F09.
2. ChatGPT параллельно ведёт feature/px1-m1-integrated-interface-repair-20261118 (другая линия модели, FreeCAD-генератор M1).
   Перед работой смотреть свежие коммиты в его ветках.
3. Окружение: pip install --break-system-packages cadquery (2.8.0); сборка ~9 мин, интегральная проверка ~1 мин.

## Следующий шаг
F06 — коническая пара Z16/Z40 (status "next" в feature_list.json).
