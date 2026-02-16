Набор для настройки Cursor (интеграции за один раз)
==================================================

Содержимое:
  00_START_HERE.md    — ГЛАВНЫЙ ПРОМПТ: начни с него
  mcp.json.template  — шаблон для ~/.cursor/mcp.json
  env.example        — шаблон для Technical/.env (скрипты Confluence)
  technical/         — примеры скриптов Confluence (опционально; лучше генерировать по промпту)
  PROMPT_technical_scripts.md — промпт: «сгенерируй скрипты Confluence в Technical/» (вставь в чат)
  cursor-rules/      — универсальные правила Cursor для MCP (копировать в .cursor/rules/)

Быстрый старт:
  1. Распакуй setup-pack в свой проект (MyProject/setup-pack/) или открой как отдельную папку.
  2. Открой папку проекта в Cursor (File → Open Folder).
  3. Открой 00_START_HERE.md, скопируй промпт и вставь в Composer/Agent.
  4. Cursor спросит, какие интеграции нужны — выбери (Confluence+Jira, Drive, Canva).
  5. Cursor создаст конфиги (для Confluence+Jira при необходимости установит uv) и даст чек-лист.
  6. Создай API-ключ в Atlassian (id.atlassian.com → Безопасность → API-токены → Создать → скопировать токен). В чате Cursor напиши: «Обнови конфиги: подставь эти данные» и вставь URL компании, email и API-токен — Cursor обновит mcp.json и Technical/.env. Перезапусти MCP (Settings → MCP → Restart Servers). Подробный гайд — в основном README гайда, раздел «Доделай вручную».
