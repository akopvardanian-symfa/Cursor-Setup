# Скрипты для Confluence (примеры)

**Предпочтительно:** не копировать готовые скрипты, а попросить Cursor сгенерировать их у себя. Вставь в чат промпт из **`PROMPT_technical_scripts.md`** (в корне setup-pack) — Cursor создаст `Technical/` со скриптами в твоём проекте.

Если удобнее взять готовое — скопируй содержимое этой папки в **`Technical/`** своего проекта. Так Cursor и правила смогут вызывать скрипты по путям вида `Technical/upload_confluence_attachment.py`.

## Зависимости

```bash
pip install -r requirements.txt
```

Или: `pip install requests`

## Confluence

- Нужен файл **`Technical/.env`** с переменными:
  - `CONFLUENCE_URL` (например `https://your-company.atlassian.net/wiki`)
  - `CONFLUENCE_USERNAME`
  - `CONFLUENCE_API_TOKEN`

Шаблон `.env` лежит в корне setup-pack: **`env.example`** — скопируй его в `Technical/.env` и заполни.

## Скрипты

| Скрипт | Назначение |
|--------|------------|
| `upload_confluence_attachment.py` | Загрузить файл во вложения страницы Confluence |
| `download_confluence_attachment.py` | Скачать вложение со страницы |
| `delete_confluence_attachment.py` | Удалить вложение (только по явному запросу) |
| `confluence_upload_and_embed_image.py` | Загрузить картинку и встроить её в тело страницы |

Подробные примеры вызова — в docstring каждого скрипта.
