# Отчёт по практической работе

## Окружение

- ОС: macOS (darwin, Apple Silicon)
- Python: 3.12.14 (установлен через Homebrew)
- Poetry: 2.5.1
- Менеджер пакетов Python: pip

## Пути к интерпретаторам

- pip_project: `/Users/vadim/Desktop/pip_project/.venv/bin/python`
- poetry_project: `/Users/vadim/Desktop/poetry_project/.venv/bin/python`

## Прямые зависимости и их назначение

| Пакет | Назначение |
|---|---|
| requests | HTTP-запрос к Open-Meteo |
| pandas | Построение DataFrame, работа с CSV |
| matplotlib | Построение и сохранение графика |
| pytest (test) | Запуск тестов |
| ruff (dev) | Линтер и форматтер |

Модуль `numpy` не является прямой зависимостью: скрипт его не импортирует,
он устанавливается автоматически как транзитивная зависимость `pandas` и
`matplotlib`.

## Примеры транзитивных зависимостей

- `pandas` → `numpy`, `python-dateutil`, `tzdata`
- `matplotlib` → `contourpy`, `kiwisolver`, `fonttools`
- `requests` → `urllib3`, `certifi`, `idna`

## Результат восстановления pip_project

После удаления `.venv` и создания нового пустого окружения выполнена команда
`python -m pip install -r requirements.txt`. Все 17 пакетов установлены,
скрипт `python plt_temp.py` завершился без ошибок, `temperature_24h.csv`
содержит 24 строки и столбцы `time`, `temperature_c`.

## Проверка групп Poetry

- `poetry sync --only main` — основные зависимости на месте (`requests`,
  `pandas`, `matplotlib` импортируются, скрипт работает), `pytest` и `ruff`
  удалены из окружения.
- `poetry sync --only test` — установлен только `pytest` с зависимостями;
  `requests` отсутствует, основной скрипт падает с `ModuleNotFoundError`.
- `poetry sync` (по умолчанию) — установлены все три группы, тесты проходят,
  скрипт создаёт CSV и PNG.

## Обновление зависимости

Команда `poetry show --outdated` не вывела ничего: все прямые зависимости
уже находятся в последних версиях, разрешённых диапазонами в
`pyproject.toml`. Обновление `requests` (`poetry update requests`) также не
изменило версий — установлена последняя совместимая (`2.34.2`). Это
ожидаемый результат: диапазон `^2.34.2` допускает только минорные и
патчевые обновления в пределах `2.x`, а более новых совместимых версий
на момент выполнения не было.

## Чистое восстановление Poetry

После удаления `poetry_project/.venv` выполнена команда `poetry install`.
Poetry автоматически выбрал Python 3.12.14, создал новый `.venv` в папке
проекта и установил 22 пакета строго по `poetry.lock`. Тесты (`poetry run
pytest`) — 3 passed. Скрипт (`poetry run python plt_temp.py`) создал
`temperature_24h.csv` (24 строки, 2 столбца) и `temperature_24h.png`.

## Сравнение venv + pip и Poetry

| Критерий | venv + pip | Poetry |
|---|---|---|
| Изоляция | `python3.12 -m venv .venv` | создаёт `.venv` автоматически |
| Описание прямых зависимостей | вручную, отсутствует | `pyproject.toml` |
| Точные версии | `requirements.txt` (`pip freeze`) | `poetry.lock` |
| Группы зависимостей | нет | `main` / `test` / `dev` |
| Разрешение версий | при установке, вручную | отдельный resolver |
| Воспроизводимость | снимок текущего окружения; прямые и транзитивные зависимости не разделены | разделены: намерения в `pyproject.toml`, точное решение в `poetry.lock` |

В подходе `venv + pip` воспроизводимость обеспечивается только файлом
`requirements.txt`, который фиксирует все пакеты без разделения на прямые
и транзитивные. В Poetry воспроизводимость обеспечивается парой
`pyproject.toml` (что нужно проекту) и `poetry.lock` (какие именно версии
были подобраны), плюс явное разделение групп.