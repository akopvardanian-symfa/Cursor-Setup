# Установка интеграций Cursor — начни здесь

Скопируй текст ниже целиком и вставь в чат **Composer** (Cmd+I) или **Agent** в Cursor.

---

Ты помогаешь настроить Cursor по гайду «Гайд по настройке Cursor для бизнес-системного аналитика».

**Контекст:** в этой папке (или в подпапке `setup-pack`) лежат файлы:
- `mcp.json.template` — шаблон конфига MCP
- `env.example` — шаблон для Technical/.env (Confluence)
- `technical/` — примеры скриптов Confluence (опционально). Лучше не раздавать готовые скрипты: если нужны скрипты для вложений — попроси пользователя вставить промпт из `PROMPT_technical_scripts.md`, и ты сгенерируешь скрипты в его проекте в папке `Technical/`. Папку `technical/` в setup-pack можно использовать как референс, если пользователь предпочитает скопировать готовое.
- `cursor-rules/` — универсальные правила Cursor для MCP и интеграций (без привязки к конкретным проектам). Можно скопировать в `.cursor/rules/` проекта.

**Моя задача:** настроить интеграции Cursor с внешними инструментами.

**Сделай так:**

1. **Спроси меня, какие интеграции нужны:**
   - Confluence + Jira (документация, задачи) — основная связка
   - Google Drive (файлы, документы) — опционально
   - Canva (презентации, дизайн) — опционально

2. **Для каждой выбранной интеграции выполни настройку:**

   **Confluence + Jira:**
   - **Установка uv (для mcp-atlassian):** проверь, установлен ли uv (`uv --version`). Если нет — выполни установку в терминале:
     - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh` или `brew install uv`
     - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (см. https://docs.astral.sh/uv/)
     После установки может понадобиться перезапустить терминал или Cursor. Если затем команда `uv` не находится (uv: command not found) — попроси пользователя перезапустить Cursor и повторить настройку (или выполнить шаг с mcp.json вручную).
   - Прочитай `mcp.json.template`.
   - Создай или обнови `~/.cursor/mcp.json`, добавив блок `mcp-atlassian`. Оставь плейсхолдеры (YOUR-COMPANY, your.email@company.com, YOUR_ATLASSIAN_API_TOKEN) — я подставлю позже.
   - Если пользователю нужны скрипты для вложений Confluence (загрузка, встраивание картинок): предложи вставить промпт из `PROMPT_technical_scripts.md` в чат — ты сгенерируешь скрипты в папке `Technical/` проекта (upload_confluence_attachment.py, download, delete, confluence_upload_and_embed_image.py, .env.example, requirements.txt). Так скрипты будут у каждого свои, без копирования из setup-pack. Если в проекте уже есть `Technical/`, создай там `.env` на основе `env.example`.
   - Предложи скопировать универсальные правила из `setup-pack/cursor-rules/` в `.cursor/rules/` **рабочей папки пользователя** (той, которую он будет открывать для повседневной работы). Если сейчас открыт только setup-pack — уточни: правила копировать в `.cursor/rules/` его основной папки проекта, а не в setup-pack. См. cursor-rules/README.md.
   - Дай чек-лист для Confluence+Jira:
     1. **Создать API-ключ в Atlassian:** открыть [id.atlassian.com → Security → API tokens](https://id.atlassian.com/manage-profile/security/api-tokens) → Create API token → Label (например «Cursor MCP») → Create → сразу скопировать токен (показывается один раз).
     2. **Подставить данные в конфиги через чат:** пользователь в чате Cursor (Composer/Agent) пишет, например: «Обнови конфиги MCP и Technical: подставь эти данные в ~/.cursor/mcp.json и в Technical/.env» и вставляет свои URL компании (например https://company.atlassian.net), email и API-токен. Ты обновляешь `~/.cursor/mcp.json` (блок mcp-atlassian) и при наличии Technical/ — `Technical/.env`.
     3. Когда генерируешь скрипты в Technical/ — сначала проверь наличие Python (`python --version` или `py --version`). Если Python установлен — **выполни в терминале** `pip install -r Technical/requirements.txt`. Если Python нет — сообщи пользователю: установить с python.org или пропустить скрипты (вложения в Confluence тогда только через веб-интерфейс).
     4. Перезапустить MCP: Settings → Features → MCP → Restart Servers.

   **Google Drive:**
   - Проверь, есть ли в проекте `Technical/drive_api.py` и `get_gdrive_refresh_token.py`. Если нет — скажи, что нужны эти скрипты (mcp-google-drive: https://github.com/Longtran2404/mcp-google-drive).
   - Объясни: нужен OAuth client (Google Cloud), файл `gdrive-oauth-client.json` и refresh token (получить скриптом `get_gdrive_refresh_token.py`).
   - Если я хочу MCP для Drive из чата — добавь в `~/.cursor/mcp.json` блок `google-drive` с `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (инструкция в репозитории mcp-google-drive).
   - Дай чек-лист: создать OAuth client в Google Cloud, включить Drive API, запустить скрипт refresh token, перезапустить Cursor.

   **Canva:**
   - Добавь в `~/.cursor/mcp.json` блок:
     ```json
     "Canva": {
       "command": "npx",
       "args": ["-y", "mcp-remote@latest", "https://mcp.canva.com/mcp"]
     }
     ```
   - Дай чек-лист: перезапустить Cursor, при первом обращении к Canva — авторизация в браузере.

3. **После всех интеграций:**
   - Сводка: что создано (mcp.json, .env), что нужно заполнить вручную, как проверить (Cursor Settings → MCP; серверы должны быть зелёными; в чате можно спросить «Найди в Jira открытые задачи» для проверки).
   - Напомни: после подстановки данных — перезапустить MCP (Restart Servers) или Cursor целиком; если пользователь вставил токен/URL с лишними пробелами или забыл заменить плейсхолдер — предложи проверить конфиги и вставить данные ещё раз.

**Ссылки:** [API-токен Atlassian](https://id.atlassian.com/manage-profile/security/api-tokens), [uv](https://docs.astral.sh/uv/), [mcp-atlassian](https://github.com/sooperset/mcp-atlassian), [Canva MCP](https://mcp.canva.com/mcp).

Выполняй по очереди. Спрашивай, если что-то непонятно или нужны уточнения.
