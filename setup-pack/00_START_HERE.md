# Cursor integration setup — start here

**If you don’t have the repo yet:** in Cursor open any folder, open Agent (Cmd+I), paste the repository link and the prompt from the main guide’s “Initial setup after install”, step 2 — the Agent will clone the repo and run the instructions in this file.

Copy the text below in full and paste it into the **Agent** chat in Cursor (Cmd+I or the panel button; when the repo is already open in Cursor).

---

You are helping set up Cursor according to the “Cursor Setup Guide for Business Analysts”.

**Context:** this folder (or the `setup-pack` subfolder) contains:
- `mcp.json.template` — MCP config template
- `env.example` — template for Technical/.env (Confluence)
- `technical/` — reference only (README, requirements.txt). No scripts are shipped; if the user needs attachment scripts, ask them to paste the prompt from `PROMPT_technical_scripts.md` and you will generate the scripts in their project under `Technical/`.
- `cursor-rules/` — general Cursor rules for MCP and integrations (not tied to specific projects). Can be copied into the project’s `.cursor/rules/`.

**My goal:** set up Cursor integrations with external tools.

**Do the following:**

1. **Ask me which integrations I need:**
   - Confluence + Jira (docs, issues) — main combo
   - Google Drive (files, documents) — optional
   - Canva (presentations, design) — optional

2. **For each chosen integration, run the setup:**

   **Confluence + Jira:**
   - **Install uv (for mcp-atlassian):** check if uv is installed (`uv --version`). If not — install in the terminal:
     - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh` or `brew install uv`
     - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` (see https://docs.astral.sh/uv/)
     After install you may need to restart the terminal or Cursor. If `uv` is not found (uv: command not found) — ask the user to restart Cursor and rerun setup (or do the mcp.json step manually).
   - Read `mcp.json.template`.
   - Create or update `~/.cursor/mcp.json`, adding the `mcp-atlassian` block. Leave placeholders (YOUR-COMPANY, your.email@company.com, YOUR_ATLASSIAN_API_TOKEN) — the user will fill them later.
   - If the user needs Confluence attachment scripts (upload, embed images): suggest pasting the prompt from `PROMPT_technical_scripts.md` in chat — you will generate the scripts in the project’s `Technical/` (upload_confluence_attachment.py, download, delete, confluence_upload_and_embed_image.py, .env.example, requirements.txt). That way each user gets their own scripts without copying from setup-pack. If the project already has `Technical/`, create `.env` there from `env.example`.
   - Suggest copying the general rules from `setup-pack/cursor-rules/` into **`.cursor/rules/`** of the **user’s working folder** (the one they open for day-to-day work). If only setup-pack is open — clarify: copy rules into `.cursor/rules/` of their main project folder, not into setup-pack. See cursor-rules/README.md.
   - Give a Confluence+Jira checklist:
     1. **Create API token in Atlassian:** open [id.atlassian.com → Security → API tokens](https://id.atlassian.com/manage-profile/security/api-tokens) → Create API token → Label (e.g. “Cursor MCP”) → Create → copy the token right away (shown once).
     2. **Fill configs via chat:** the user writes in Cursor Agent chat, e.g.: “Update MCP and Technical configs: put these values in ~/.cursor/mcp.json and Technical/.env” and pastes their site URL (e.g. https://company.atlassian.net), email, and API token. You update `~/.cursor/mcp.json` (mcp-atlassian block) and, if Technical/ exists, `Technical/.env`.
     3. When generating scripts in Technical/ — first check for Python (`python --version` or `py --version`). If Python is installed — **run in terminal** `pip install -r Technical/requirements.txt`. If not — tell the user to install from python.org or skip scripts (Confluence attachments then only via web UI).
     4. Restart MCP: Settings → Features → MCP → Restart Servers.

   **Google Drive:**
   - **Node.js (npx):** if the user chose Google Drive or Canva, first check `npx --version`. If not installed — suggest installing (nodejs.org, or macOS: `brew install node`) and run the install in the terminal; or suggest pasting the prompt from the main guide README (section “If you chose Google Drive or Canva — Node.js check”).
   - Check if the project has `Technical/drive_api.py` and `get_gdrive_refresh_token.py`. If not — say these scripts are needed (mcp-google-drive: https://github.com/Longtran2404/mcp-google-drive).
   - Explain: they need an OAuth client (Google Cloud), file `gdrive-oauth-client.json`, and a refresh token (obtained with `get_gdrive_refresh_token.py`).
   - If they want Drive MCP from chat — add the `google-drive` block to `~/.cursor/mcp.json` with `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` (see mcp-google-drive repo).
   - Give a checklist: create OAuth client in Google Cloud, enable Drive API, run refresh token script, restart Cursor.

   **Canva:**
   - Canva also needs Node.js (npx). If you haven’t checked yet — run `npx --version`; if Node is missing — same as in the Google Drive block above.
   - Add to `~/.cursor/mcp.json`:
     ```json
     "Canva": {
       "command": "npx",
       "args": ["-y", "mcp-remote@latest", "https://mcp.canva.com/mcp"]
     }
     ```
   - Give a checklist: restart Cursor; on first use of Canva — authorize in the browser.

3. **After all integrations:**
   - Summary: what was created (mcp.json, .env), what to fill manually, how to verify (Cursor Settings → MCP; servers should be green; in chat you can ask “Find open Jira issues” to test).
   - Remind: after filling in values — restart MCP (Restart Servers) or Cursor; if the user pasted token/URL with extra spaces or forgot to replace a placeholder — suggest checking configs and pasting again.

**Links:** [Atlassian API token](https://id.atlassian.com/manage-profile/security/api-tokens), [uv](https://docs.astral.sh/uv/), [mcp-atlassian](https://github.com/sooperset/mcp-atlassian), [Canva MCP](https://mcp.canva.com/mcp).

Work through the steps in order. Ask if anything is unclear or needs clarification.
