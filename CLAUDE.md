# VC Price Tracker

Учебный проект курса Vibe Coding / Хекслет. Цель — собрать трекер цен преимущественно через Claude Code и Claude Skills с минимальным ручным кодом.

## Правила работы

- Работать пошагово: один конкретный шаг → проверка → следующий шаг.
- Перед существенными действиями сверяться с `CLAUDE.md`.
- Не пересматривать уже принятые решения без явной команды пользователя.
- Не редактировать и не удалять `.github/workflows/hexlet-check.yml`.
- Не выполнять следующие крупные этапы заранее.

## Репозитории

- Основной: `man-and-code/vibecoding-claudecode-project-388`
- Данные прогонов: `man-and-code/tracker-data` — приватный репозиторий.

## Ниша и источник

Ниша: саке.

Источник: `https://decanter.ru/`

Цель — отслеживать обычные и акционные цены выбранных SKU саке.

## Контракт цены

Skill `extract-price` должен возвращать:

- `regular_price` — обычная цена;
- `sale_price` — текущая акционная цена;
- `has_credit` — наличие кредита/рассрочки.

Все три поля обязательны.

Если скидки нет, `sale_price = null`.

## Выбранные SKU

1. `04-259675` — Iku's Shiro 0,5 л — `https://decanter.ru/product/iku-s-shiro-id259675`
2. `09-127358` — Ozeki Josen Kinkan 0,72 л — `https://decanter.ru/product/ozeki-josen-kinkan-id127358`
3. `04-253906` — Akashi Tai Junmai Ginjo Sparkling 0,3 л — `https://decanter.ru/product/akashi-tai-junmai-ginjo-sparkling-id253906`
4. `04-258140` — Chiyomusubi Sorah Sparkling 0,36 л — `https://decanter.ru/product/chiyomusubi-sorah-sparkling-id258140`
5. `04-260714` — Yatagarasu Assemblage 0,72 л — `https://decanter.ru/product/yatagarasu-assemblage-id260714`
6. `04-259677` — Yatagarasu Junmai Bodaimoto 0,72 л — `https://decanter.ru/product/yatagarasu-junmai-bodaimoto-id259677`
7. `04-260703` — Inata Honten Kimoto Junmai GEN 0,72 л — `https://decanter.ru/product/inata-honten-kimoto-junmai-gen-id260703`
8. `04-259678` — Yatagarasu Nigori 0,72 л — `https://decanter.ru/product/yatagarasu-nigori-id259678`
9. `04-246837` — Akashi Tai Daiginjo Genshu 0,72 л — `https://decanter.ru/product/akashi-tai-daiginjo-genshu-id246837`
10. `04-246835` — Akashi Tai Junmai Daiginjo Genshu 0,72 л — `https://decanter.ru/product/akashi-tai-junmai-daiginjo-genshu-id246835`

Ассортимент выбран окончательно.

## Планируемая архитектура

- `.claude/skills/extract-price` — принимает один URL и извлекает данные цены.
- `.claude/skills/tracker` — обходит URL, вызывает `extract-price` и формирует данные прогона.
- Прогоны хранятся в `tracker-data` файлами: `YYYY-MM-DD.json`
- `KNOWLEDGE.md` — правила определения значимых изменений.
- `send.py` — отправка значимых изменений в Telegram; использовать только стандартную библиотеку Python.

Допустимо позже использовать Haiku sub-agent для подготовки Telegram-сводки.

## Текущее состояние

Уже выполнено:

- выбрана ниша саке;
- выбран Decanter;
- определён контракт `regular_price / sale_price / has_credit`;
- выбраны 10 SKU и прямые URL;
- создан приватный `tracker-data` с `README.md`;
- GitHub MCP имеет доступ к `tracker-data`;
- основной репозиторий доступен Claude Code на чтение и запись;
- проверка `/mcp` выполнена, GitHub MCP в статусе `Connected`;
- шаг 2 завершён;
- создан `SKILL.md` для `extract-price`.

Текущий этап:

- шаг 3 — скилл `extract-price`.
