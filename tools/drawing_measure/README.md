# drawing_measure — сверка мастера с чертежами Mini-Cam

`check_master_vs_drawings.py` сравнивает константы `current/CAD/PX1_Current_Master.py` с таблицей
размеров, восстановленных по чертежам Mini-Cam CRP150 (DRW-/ASS-), каталогам покупных деталей и
задокументированным расчётам. Проект требует держать эту проверку в PASS после любого изменения.

## Запуск
```
python3 tools/drawing_measure/check_master_vs_drawings.py            # отчёт в _cloud_build/drawing_check.json
python3 tools/drawing_measure/check_master_vs_drawings.py --quiet    # только FAIL/SKIP
python3 tools/drawing_measure/check_master_vs_drawings.py --master <файл> --out <json>
```
Код выхода 0 — нет ни одного FAIL. CadQuery не нужен: мастер не импортируется и не исполняется,
верхнеуровневые присваивания разбираются через `ast` и вычисляются ограниченным вычислителем
(литералы, арифметика, уже вычисленные имена, `math.*`).

## Таблица `drawing_reference.json`
- `checks`: `{id, master_constant (имя или выражение над константами), expected, tol_mm, tag, source}`
  (или `min` вместо `expected` для односторонней проверки).
- `derived_checks`: расчётные проверки — длина дорожки бокового кольца 190×1,5 (та же конструкция дуг,
  что в `lobed_seal_face`, растяжение 0…+3 %), сжатие/заполнение канавок, зазор шины в DN150
  (вершинная оценка из `scripts/cloud/check_pipe_pose.py`), ширина по колёсам 133, зад мотора ≥ сервисного окна.

Метки: **CONFIRMED** — выноска чертежа, спецификация, каталог, требование проекта; **DERIVED** — снято
с масштабного вида или вычислено; **ESTIMATED** — инженерное решение. Нет константы: CONFIRMED → FAIL,
остальные → SKIP. Допуск CONFIRMED-значения нельзя расширять, чтобы проверка прошла: расхождение
исправляется в мастере или явно объясняется в отчёте.

В `source` указывается документ репозитория (README в `current/09_RELEASE/f*`, `SOURCE_REGISTER.md`,
`PX1_Current_BOM.csv`, `08_PROCUREMENT`, `07_TESTS`), где значение уже записано.

## Чертежи
Сами чертежи Mini-Cam (PDF DRW-/ASS-) лежат у владельца на Google Диске и читаются оттуда.
Репозиторий публичный — **никогда не копировать чертежи, их фрагменты или сканы в репозиторий**;
сюда попадают только числа с меткой и ссылкой на номер чертежа.
