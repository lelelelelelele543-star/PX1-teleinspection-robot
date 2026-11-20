# PX1 gate — независимая проверка всей сборки

Одна команда, один итог: PASS / WARN / HOLD / FAIL по всей сборке.

```bash
pip install --break-system-packages -q cadquery==2.8.0
python3 tools/gate/selftest_px1_gate.py     # проверка самой проверки, ~10 с
python3 tools/gate/px1_gate.py              # мастер current/CAD/PX1_Current_Master.step.gz, ~2 мин
```

Результат пишется в `_gate/`: `gate_report.md` (таблица), `gate_report.json`, `gate_views.png`
(сечение в трубе и вид сбоку с ЦТ и нагрузками на оси). Код выхода 1 — есть FAIL.

## Что проверяется

| Раздел | Что | Порог |
|---|---|---|
| geometry | тела валидны, объём > 0, объёмы совпадают с `current/component_registry.json` | любое невалидное тело — FAIL |
| census | 6 колёс, 10×Z50, 2×Z40, 2×Z16, 2 тяговых мотора | по AGENTS.md |
| interference | все пары деталей: AABB → Boolean | >1e-4 мм³ — FAIL, кроме классов HOLD из `release_tools.py` |
| pipe_dn150 | краулер ставится на колёса в трубу Ø150, зазор каждой детали до стенки | <3 мм FAIL, 3–5 мм WARN (REV_FQ) |
| mass_cog | масса и центр тяжести; плотности из `tools/traction/px1_traction_budget.py` | цель 9,25 кг ±10 % (WARN) |
| stability | ЦТ ниже оси трубы (сам выравнивается при крене), боковое смещение ЦТ, доли нагрузки на оси | ≤0 мм FAIL, <5 мм WARN; доля оси <20 % WARN (ESTIMATED) |
| domain | чертежи Mini-Cam, лифт и радиусы изгиба кабеля, питание по кабелю, мощность, тяга 40/100/150 м | как в самих скриптах; тяга 40 м обязательна, 100–150 м — WARN |

Пороги и их источники — `px1_gate_spec.json`. Менять порог только с записью причины в `progress.md`.

Гейт **не** заменяет `scripts/cloud/build_current.sh` + `check_integrated.py` (сборка из исходника, повторяемость,
обход шестерён) и не является квалификацией изготовления, герметичности или реальной тяги.

## Проверка чужой сборки (FreeCAD M1 и любая другая)

Гейт читает только STEP, поэтому проверяет сборку из любого генератора, если выполнен контракт:

1. Один STEP на всю сборку, мм; **X — вперёд/назад вдоль трубы, Y — вбок, Z — вверх**.
2. У каждой детали своё имя (PRODUCT в STEP; во FreeCAD — Label детали).
3. В именах есть метки: колёса `WHEEL_-1_…` / `WHEEL_1_…`, `Z50_`, `Z40_BEVEL`, `Z16_BEVEL`, `TRACTION_MOTOR`.
4. Для массы: имена как в `NAME_DENSITY` трактового расчёта или реестр с категориями (`--registry`);
   детали без правила считаются с плотностью 2,7 и перечисляются в отчёте.

```bash
python3 tools/gate/px1_gate.py --step path/to/assembly.step --registry none --skip-domain --out _gate_m1
```

`--skip-domain` — расчёты проекта относятся к CadQuery-мастеру; для чужой сборки остаются только STEP-проверки.
