# CLAUDE.md — как Claude работает в PX1

Инженерная постановка общая с ChatGPT/Codex — она здесь:
@AGENTS.md

Ниже — только то, что касается Claude.

## Ветка
- Claude работает **только в ветке `claude/px1`**. В `main` и `feature/*` не пушить: это ветки ChatGPT/Codex.
- Начало сессии: `git fetch`, затем
  `git for-each-ref --sort=-committerdate refs/remotes --format='%(committerdate:short) %(refname:short) %(subject)' | head`.
  Если в ветках ChatGPT появилось нужное — влить merge-ом в `claude/px1` и записать это в progress.md.
- Конец сессии: коммит и `git push origin claude/px1`. Если push не прошёл — сразу сказать пользователю,
  сделать `git format-patch` и отправить файл, чтобы работа не потерялась.

## Порядок работы (WIP = 1)
1. Прочитать `session-handoff.md` и `feature_list.json`.
2. Делать задачу пользователя; если её нет («продолжай») — первую со статусом `next`.
3. Проверить (ниже), обновить `progress.md`, `feature_list.json`, `session-handoff.md`, закоммитить, запушить.
4. Если следующий шаг очевиден и время есть — продолжать, не спрашивая разрешения.

## Проверки модели
```bash
pip install --break-system-packages -q cadquery   # ~2 мин
bash scripts/cloud/build_current.sh                # ~9 мин, пишет в _cloud_build/
python3 scripts/cloud/check_pipe_pose.py --active
python3 scripts/cloud/check_integrated.py --roundtrip --require-pipe-service
```
Источник геометрии — `current/CAD/PX1_Current_Master.py`. HOLD не превращать в PASS.

## Отчёт пользователю (он работает с телефона)
- По-русски. 5–8 строк: что сделано, что не получилось, что дальше.
- Если менялась геометрия — отправить картинку (PNG рендер или схему) файлом.
- Не грузить процессом (ветки, handoff, списки задач) — только результат и трудности.
- Размеры помечать CONFIRMED / DERIVED / ESTIMATED; оценку не выдавать за заводской размер.
- Не просить мерить CRP150, если размер можно восстановить по чертежам, фото и расчёту.
- Чертежи Proteus (DRW-002-xxx) лежат у пользователя на Google Диске.
