Cursor setup pack (integrations in one go)
==========================================
Repository: https://github.com/akopvardanian-symfa/Cursor-Setup
Paste the repo link in the Agent chat — it will clone and run the steps from 00_START_HERE; no need to download manually.

Contents:
  00_START_HERE.md    — MAIN PROMPT: start here
  mcp.json.template   — template for ~/.cursor/mcp.json
  env.example         — template for Technical/.env (Confluence scripts)
  technical/          — reference only (README, requirements); scripts generated via prompt
  PROMPT_technical_scripts.md — prompt: “generate Confluence scripts in Technical/” (paste in chat)
  cursor-rules/       — general Cursor rules for MCP (copy to .cursor/rules/)

Quick start:
  Option A (recommended): In Cursor open any folder. Open Agent (Cmd+I). Paste in chat the link (https://github.com/akopvardanian-symfa/Cursor-Setup) and the prompt from the main guide README, section “Initial setup after install”, step 2 — the Agent will clone the repo and run all steps from 00_START_HERE.
  Option B (repo already open in Cursor):
  1. In Cursor open the repo folder (if not already).
  2. Ensure Cursor has terminal access (allow when first prompted).
  3. Open 00_START_HERE.md, copy the prompt and paste it in Agent.
  4. Cursor will ask which integrations you need — choose (Confluence+Jira, Drive, Canva).
  5. Cursor will create configs (for Confluence+Jira it will install uv if needed) and give a checklist.
  6. Create an API token in Atlassian (id.atlassian.com → Security → API tokens → Create → copy token). In Cursor chat write: “Update configs: put these values in” and paste site URL, email, and API token — Cursor will update mcp.json and Technical/.env. Restart MCP (Settings → MCP → Restart Servers). Full details are in the main README, section “Manual step: Atlassian API token and config values”.
