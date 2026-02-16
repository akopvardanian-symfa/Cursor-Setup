# MCP configuration examples

Short reference: what **`~/.cursor/mcp.json`** can look like when connecting several servers. Replace placeholders with your values.

---

## Single server: Atlassian only (Confluence + Jira)

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

## Atlassian + Google Drive (OAuth) — optional

*Google Drive is often connected via API scripts (e.g. `drive_api.py`) rather than MCP. Below is the MCP variant for use from Cursor chat.*

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

(Exact package name and variables: see [mcp-google-drive](https://github.com/Longtran2404/mcp-google-drive) or `Technical/MCP_GOOGLE_DRIVE_SETUP.md`.)

---

## Project-specific MCP (e.g. Canva)

You can create **`.cursor/mcp.json`** in the **project root**. Then that project will use the servers from this file (or they extend the global ones — depends on Cursor settings).

Example: Canva only (project-specific config):

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

## Where config lives

| Config        | Path                          | Scope           |
|---------------|-------------------------------|-----------------|
| Global MCP    | `~/.cursor/mcp.json`          | All projects    |
| Project MCP   | `<project root>/.cursor/mcp.json` | This project only |
| Script creds | `<project>/Technical/.env`    | Scripts in this project only (do not commit) |

After changing `mcp.json`, restart MCP: **Cursor Settings → Features → MCP → Restart Servers** or restart Cursor.
