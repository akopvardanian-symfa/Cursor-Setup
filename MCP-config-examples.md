# Примеры конфигурации MCP

Краткая шпаргалка: как может выглядеть **`~/.cursor/mcp.json`** при подключении нескольких серверов. Замените плейсхолдеры на свои значения.

---

## Один сервер: только Atlassian (Confluence + Jira)

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_USERNAME": "you@company.com",
        "JIRA_API_TOKEN": "ATATT3x...",
        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "you@company.com",
        "CONFLUENCE_API_TOKEN": "ATATT3x..."
      }
    }
  }
}
```

---

## Atlassian + Google Drive (OAuth) — опционально

*Обычно Google Drive подключают скриптами по API (например `drive_api.py`), а не MCP. Ниже — вариант с MCP для работы из чата Cursor.*

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_USERNAME": "you@company.com",
        "JIRA_API_TOKEN": "ATATT3x...",
        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "you@company.com",
        "CONFLUENCE_API_TOKEN": "ATATT3x..."
      }
    },
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-drive"],
      "env": {
        "GOOGLE_CLIENT_ID": "....apps.googleusercontent.com",
        "GOOGLE_CLIENT_SECRET": "...",
        "GOOGLE_REFRESH_TOKEN": "1//..."
      }
    }
  }
}
```

(Точное имя пакета и переменные см. в [mcp-google-drive](https://github.com/Longtran2404/mcp-google-drive) или в `Technical/MCP_GOOGLE_DRIVE_SETUP.md`.)

---

## Проект-специфичный MCP (например, Canva)

В **корне проекта** можно создать **`.cursor/mcp.json`**. Тогда в этом проекте будут использоваться серверы из этого файла (или они дополнят глобальные — зависит от настроек Cursor).

Пример только Canva (проект-специфичный конфиг):

```json
{
  "mcpServers": {
    "Canva": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://mcp.canva.com/mcp"]
    }
  }
}
```

---

## Где лежит конфиг

| Конфиг | Путь | Область |
|--------|------|--------|
| Глобальный MCP | `~/.cursor/mcp.json` | Все проекты |
| Проектный MCP | `<корень проекта>/.cursor/mcp.json` | Только этот проект |
| Креды для скриптов | `<проект>/Technical/.env` | Только скрипты в этом проекте (не коммитить) |

После изменений в `mcp.json` перезапустите MCP: **Cursor Settings → Features → MCP → Restart Servers** или перезапустите Cursor.
