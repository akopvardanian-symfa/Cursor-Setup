# Промпт: сгенерировать скрипты Confluence

Скрипты для вложений Confluence не обязательно копировать из setup-pack — можно попросить Cursor сгенерировать их локально. Скопируй текст ниже и вставь в чат Composer или Agent.

---

Создай в проекте папку **`Technical/`** и напиши скрипты для работы с вложениями Confluence через REST API (чтобы не тянуть большие данные через MCP).

**Сделай:**

1. Создай **`Technical/.env.example`** с переменными:
   - `CONFLUENCE_URL` (например `https://company.atlassian.net/wiki`)
   - `CONFLUENCE_USERNAME`
   - `CONFLUENCE_API_TOKEN`  
   В начале файла напиши: скопировать в `Technical/.env` и заполнить; `.env` не коммитить.

2. Создай **`Technical/requirements.txt`** с одной строкой: `requests>=2.28.0`.

3. Напиши Python-скрипты (читают креды из `Technical/.env` или из переменных окружения `CONFLUENCE_*`):
   - **`upload_confluence_attachment.py`** — загрузка файла во вложения страницы Confluence. Вызов: `python upload_confluence_attachment.py <page_id> <path_to_file>`. Используй Confluence REST API (PUT /rest/api/content/{id}/child/attachment).
   - **`download_confluence_attachment.py`** — скачать вложение по page_id и имени файла. Вызов: `python download_confluence_attachment.py <page_id> <filename> [output_path]`.
   - **`delete_confluence_attachment.py`** — удалить вложение (только по явному запросу). Вызов: `python delete_confluence_attachment.py <page_id> <filename1> [filename2 ...]`.
   - **`confluence_upload_and_embed_image.py`** — загрузить картинку во вложения и встроить её в тело страницы (storage HTML, макрос `ac:image` с `ri:attachment`). Вызов: `python confluence_upload_and_embed_image.py <page_id> <path_to_image> [--anchor "..." --alt "..." --width N]`.

Скрипты должны загружать `.env` из той же папки (Technical/), если файл есть. Ошибки выводи в stderr, в docstring укажи примеры вызова.

4. **Перед установкой зависимостей** проверь наличие Python: выполни в терминале `python --version` или `py --version`. Если Python установлен — **выполни** `pip install -r Technical/requirements.txt`. Если Python нет — напиши пользователю: установить с [python.org](https://www.python.org/downloads/) или пропустить скрипты (вложения тогда только через веб-интерфейс Confluence). Затем напиши коротко: что создано и что осталось сделать (заполнить `Technical/.env`).

**Важно:** на каждом компьютере, где будут запускаться эти скрипты, нужны установленный Python и выполнение `pip install -r Technical/requirements.txt`. Без Python скрипты не работают. Файлы можно копировать между машинами, но Python и зависимости должны быть установлены на каждой.
