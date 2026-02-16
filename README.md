# Cursor Setup Guide for Business Analysts

**Repository:** [github.com/akopvardanian-symfa/Cursor-Setup](https://github.com/akopvardanian-symfa/Cursor-Setup) — paste this link into the Agent chat and ask it to clone the repo and follow the docs inside; no need to download anything manually.

This guide explains how to install Cursor, set up integrations (Confluence, Jira, Google Drive, Canva, etc.), and organize folders and documentation. **Core idea:** you do as little manually as possible — all requests (integration setup, configs, scripts) are handled through Cursor in chat. To enable this, grant Cursor terminal and file access once during setup (see “Initial setup after install”).

---

## Table of contents

1. [Installing Cursor](#1-installing-cursor)
2. [Integrations and external connections (MCP and API)](#2-integrations-and-external-connections-mcp-and-api)
3. [Cursor rules (`.cursor/rules`)](#3-cursor-rules-cursorrules)
4. [Folder structure and documentation by project type](#4-folder-structure-and-documentation-by-project-type)
5. [Documentation guidelines](#5-documentation-guidelines)

---

## 1. Installing Cursor

### What is Cursor

**Cursor** is a VS Code–based IDE with built-in AI (chat, autocomplete, agent). For business analysts it’s useful because you can keep documentation in one place, edit it locally, and sync with Confluence/Jira via MCP or scripts when needed.

### Installation steps

1. **Download Cursor**  
   Official site: [cursor.com](https://cursor.com). Download the installer for your OS (macOS, Windows, Linux).

2. **Install**  
   Run the installer and follow the steps. Cursor installs as a separate app (not on top of VS Code).

3. **Sign in**  
   On first launch you’ll need to sign in (or create an account). Free or Pro subscription affects AI request limits and some features.

4. **Create and open a project folder**

   Cursor works in the context of a folder — your project (docs, scripts, configs). If you don’t have one yet, create it:

   *(Screenshot: cursor-welcome-open-clone.png — see [repo](https://github.com/akopvardanian-symfa/Cursor-Setup).)*  
   *On Cursor launch, click “Open project” to open a folder.*

   **a) Create a project folder:**
   - **Where:** somewhere you keep work projects, e.g.:
     - macOS/Linux: `~/Projects/` or `~/Documents/Work Projects/`
     - Windows: `C:\Users\YourName\Projects\` or `D:\Work\`
   - **Name:** project or client name for quick recognition. Examples:
     - `My Project` (single main project)
     - `Client A Documentation` (client-specific docs)
     - `Team Knowledge Base` (shared team knowledge)
   - **Create:** in Finder (macOS), File Explorer (Windows), or with `mkdir "Project name"` in the terminal.

   *(Screenshot: cursor-new-folder-dialog.png — see repo.)*  
   *New Folder dialog: enter the folder name and click Create.*

   **b) Open the folder in Cursor:**
   - In Cursor: **File → Open Folder** (or **Cmd+O** on macOS, **Ctrl+O** on Windows).
   - In the dialog, choose the folder (e.g. from your home directory or “Cursor Projects”) and click **Open**.

   *(Screenshot: cursor-open-folder-finder.png — see repo.)*  
   *Open dialog: go to the folder and click Open.*

   *(Screenshot: cursor-open-folder-empty.png — see repo.)*  
   *Select the folder and click Open.*

### Initial setup after install: full access for Cursor

So Cursor can do everything on its own (configs, installing uv, pip, writing to `~/.cursor/`), do the following **once** after first install:

1. **Allow running commands in the terminal**  
   Without this, Cursor can’t install uv, run `pip install`, or start MCP servers. Do either:

   **Option A — when first asked in chat:** when the Agent suggests running a command, a “Run” / “Allow” button or prompt will appear — click **Run** (or **Allow**) so the command runs. If offered “Add to allowlist”, you can add it so similar commands run without asking later.

   **Option B — enable once in settings:**
   - Open settings: **Cursor → Settings** (macOS) or **File → Preferences → Cursor Settings** (Windows/Linux), or press **Cmd+,** (macOS) / **Ctrl+,** (Windows/Linux) and select **Cursor Settings** (not “Preferences”) in the left panel.

   *(Screenshot: cursor-settings-menu.png — see repo.)*  
   *macOS: Cursor menu → Settings… → Cursor Settings.*

   - In the left menu go to **Agents** → **Auto-Run**.

   *(Screenshot: cursor-agents-autorun.png — see repo.)*  
   *Agents → Auto-Run: set Auto-Run Mode → Run Everything.*
   - Set **Auto-Run Mode** to **Run Everything** — the Agent will run all commands and actions without prompting.
   - Save (settings usually save automatically).

   After this, Cursor can run terminal commands by itself; little manual action is needed.

2. **Open a folder and paste the repo link and prompt in chat**  
   **File → Open Folder** — open any folder (e.g. an empty project folder). Then open **Agent**: **Cmd+I** (macOS) or **Ctrl+I** (Windows/Linux) and paste the **repository link** and **prompt** (copy in full):

   *(Screenshot: cursor-agent-chat.png — see repo.)*  
   *Paste the link and prompt in the input field.*

   **Repository link:**  
   `https://github.com/akopvardanian-symfa/Cursor-Setup`

   **Prompt:**  
   *Clone this repository into the current folder and follow the docs inside (run all steps from `setup-pack/00_START_HERE.md`).*

   The Agent will clone the repo (if the folder is empty) and run the setup steps. When it first suggests a terminal command, click **Run** / **Allow** (see step 1).

3. **Config access (macOS)**  
   MCP config lives in `~/.cursor/mcp.json`. If you get “permission denied” when writing to `~/.cursor/` or when running uv/npx — add Cursor in **System Settings → Privacy & Security → Full Disk Access**. Then Cursor can read and write configs and run commands without restriction. On Windows/Linux, default permissions are usually enough.

**Summary:** allow terminal commands (step 1) → open a folder in Cursor → paste the repo link and prompt in **Agent** (step 2). The Agent will clone the repo (if the folder is empty), open `setup-pack/00_START_HERE.md`, and walk you through integration setup with minimal manual steps.

---

## 2. Integrations and external connections (MCP and API)

Common connections:

| Tool           | Purpose                     | How it’s connected                    |
|----------------|-----------------------------|----------------------------------------|
| **Confluence** | Docs, pages                 | MCP (mcp-atlassian) + REST scripts    |
| **Jira**      | Issues, epics, boards       | MCP (mcp-atlassian)                   |
| **Google Drive** | Files, sheets, documents | API scripts (e.g. `drive_api.py`); optional MCP |
| **Canva**      | Presentations, design       | MCP (mcp-remote → Canva)              |

**What is MCP:** MCP (Model Context Protocol) is a standard for connecting external tools to AI in Cursor. In practice: via MCP, Cursor can read and update data in services (e.g. Confluence, Jira, Canva) from chat, without copying between apps by hand.

**Integration architecture:**

*(Diagram: cursor-integrations-slide.png — see [repo](https://github.com/akopvardanian-symfa/Cursor-Setup).)*

---

### Quick setup: setup-pack + one prompt

**Easiest path** — use the **setup-pack**: templates plus one prompt. Cursor will ask which integrations you want and configure them.

**How to use:** do the steps in **“Initial setup after install”** (steps 1 and 2): allow terminal → open folder → paste repo link and prompt in Agent.

**What happens next:** Cursor will ask which integrations you need (Confluence/Jira, Google Drive, Canva). For Confluence+Jira it will check [uv](https://docs.astral.sh/uv/) and install it if needed; if you see “uv: command not found” after install — restart Cursor and ask to continue setup. It will then create configs (`~/.cursor/mcp.json`, and `.env` if you have `Technical/`), optionally offer Confluence scripts (prompt in **`PROMPT_technical_scripts.md`**; scripts need Python and `pip install -r Technical/requirements.txt`) and rules from **`setup-pack/cursor-rules/`** into `.cursor/rules/`, and give you a checklist.

**If you chose Google Drive or Canva — Node.js check**  
   These integrations need **Node.js** (the `npx` command). The Agent may check this itself. If it didn’t ask about Node or you see something like `npx: command not found`, **paste this in the Agent chat at this step** (after choosing integrations, before or after Drive/Canva setup):

   **Prompt (copy and paste into chat):**  
   *Check if Node.js is installed (run `npx --version`). If not — tell me how to install it for my OS and run the install in the terminal. This is needed for MCP Google Drive and Canva.*

   After installing Node, restart Cursor if needed and ask the Agent to continue setup.

**Manual step: Atlassian API token and config values**  
   Cursor will have created configs with placeholders. You still need to create an API token in Atlassian and ask Cursor to fill in the config.

   **1. Create an API token in Atlassian**

   - In your browser open: **[Atlassian → Account settings → Security → API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)**  
     (or go to [id.atlassian.com](https://id.atlassian.com) → sign in → **Profile** → **Security** → **Create and manage API tokens**.)
   - If the create-token button is missing or access is restricted — your org may limit API tokens; ask your Atlassian admin or work without Confluence/Jira in Cursor.
   - Click **Create API token**.
   - In **Label** enter a name, e.g. `Cursor MCP` or `Confluence Jira`.
   - Click **Create**.
   - **Copy the token immediately** — it’s shown only once. Store it safely (password manager or temporary note). If you leave the page without copying, you’ll need to create a new token.

   **2. Fill configs via Cursor**

   - Have these three values ready:
     - **Atlassian site URL** — your Confluence or Jira base URL, e.g. `https://mycompany.atlassian.net` (Confluence often uses the same domain, e.g. `https://mycompany.atlassian.net/wiki` — for MCP use the base `https://mycompany.atlassian.net`).
     - **Email** — the same address you use to sign in to Atlassian.
     - **API token** — the one you just copied.
   - Open **Agent** in Cursor (Cmd+I / Ctrl+I) and write something like:

     > Update MCP and Technical configs: put these values into `~/.cursor/mcp.json` and, if there’s a Technical folder, into `Technical/.env`.  
     > URL: https://mycompany.atlassian.net  
     > Email: my.email@company.com  
     > API token: paste_your_token_here

     Use **your** URL, email, and token (don’t leave the example “paste_your_token_here”), and avoid leading/trailing spaces. Cursor will update `~/.cursor/mcp.json` (the `mcp-atlassian` block) and, if present, `Technical/.env`.  
   - After that, restart MCP: **Settings → Features → MCP → Restart Servers**. If you can’t find that section, restart Cursor entirely.  
   - If you get file access errors (“permission denied”) when creating or updating configs — see **“Initial setup after install”**, step “Config access”.

   **3. Verify**  
   In **Settings → MCP** servers should be green. In chat try: “Find open Jira issues” or “Show Confluence page [name]” — if you get a reply, the integration works.

**Done.** Integrations are set up.

---

---

**Reference — where to get MCP and API:** [mcp-atlassian (GitHub)](https://github.com/sooperset/mcp-atlassian) · [Confluence REST API](https://developer.atlassian.com/cloud/confluence/rest/v2/) · [Google Drive API v3](https://developers.google.com/drive/api/reference/rest/v3) · [Canva MCP](https://mcp.canva.com/mcp)

---

### 2.1. Confluence context in the project (space keys, page IDs)

So the AI and scripts know where to read and write, projects use a **context file**:

- In the `Technical/` folder, create **`CONFLUENCE_CONTEXT.md`** with base URL, space keys, page IDs of key pages, and links to Confluence. Update it when the instance or pages change.
- You can also record page IDs in rules or in `Technical/README.md`.

Recommendation: in any project that uses Confluence, have one such file (or a section in README) with base URL, spaces, and key page IDs.

---

## 3. Cursor rules (`.cursor/rules`)

Rules are files in **`.cursor/rules/`** with extension **`.mdc`**. They tell the AI how to behave in this project: which MCP to use, what not to edit, how to format docs.

### Rules from setup-pack

In **setup-pack**, the **`cursor-rules/`** folder contains one general rule — you can copy it into `.cursor/rules/` of your project:

| File in setup-pack     | Description |
|------------------------|-------------|
| **mcp-integrations.mdc** | MCP and integrations (Confluence, Jira): locally-first, Confluence as source of truth, when to use MCP vs scripts from `Technical/`, conflict checks (comments, changelog), attachments via scripts, project context (CONFLUENCE_CONTEXT.md). Not tied to specific spaces or projects. |

Copy files from `setup-pack/cursor-rules/` into **`.cursor/rules/`** of the folder you actually open in Cursor for day-to-day work (docs, content). If you only have the setup-pack open — create `.cursor/rules/` in your main project folder and copy there; otherwise the rules won’t apply when you open another folder.

**Asking Cursor to create or extend rules**

Instead of creating files by hand, you can ask **Agent**. Example prompts:

- **Rules for Confluence/Jira:**  
  *“Create the `.cursor/rules/` folder, copy into it the rule from `setup-pack/cursor-rules/mcp-integrations.mdc` (or create a rule for MCP and Confluence/Jira from that template).”*

- **Read-only folder:**  
  *“Add a rule: folder `Source Material/` (or `Source Materials/`) is read-only, do not edit. Final content lives in `Documentation/` (or specify yours). Save under `.cursor/rules/` with globs for that folder.”*

- **Presentation style:**  
  *“Add a rule in `.cursor/rules/`: presentation standard — fonts Object Sans / Inter, team colors and style, pre-final checklist. Describe in .mdc.”*

Cursor will create or update files in `.cursor/rules/`; adjust paths or names for your project if needed.

---

## 4. Folder structure and documentation by project type

Below are typical project structures. Use them as templates.

### 4.1. Project with documentation and Confluence

```
Project/
├── .cursor/
│   └── rules/                 # Cursor rules (MCP, Confluence, etc.)
├── Documentation/             # Docs: overviews, specs, reports
│   ├── Overview.md
│   └── ...
├── Source Materials/          # Read-only: transcripts, notes, incoming docs
│   └── ...
├── Resources/                 # Unchanging: templates, references
│   └── ...
├── Graphics/                  # Diagrams, images for docs
│   └── ...
└── Technical/                 # Scripts, Confluence, .env, README
    ├── README.md
    ├── .env
    ├── upload_confluence_attachment.py
    └── ...
```

- **Documentation** — working docs you edit and optionally publish to Confluence.  
- **Source Materials** — read-only (transcripts, notes, incoming material); final content goes in Documentation.  
- **Resources** — read-only (templates, references).  
- **Graphics** — images for docs and Confluence; upload scripts live in `Technical/`.  
- **Technical** — configs, scripts, and instructions for publishing with images.

---

### 4.2. Project with business overview and processes

```
BusinessDoc/
├── Business_Overview_and_Processes_Documentation.md   # Main artifact
├── Source Material/
│   ├── Transcript_*.txt
│   └── ...
└── .git
```

- One main artifact — a large Markdown doc. Sources in `Source Material/` are for reference only. You can add a source-material rule.

---

### 4.3. Project with MVP phases and source materials

```
MVPProject/
├── MVP phase 1/
│   ├── Feature_Requirements.md
│   ├── MVP_Overview.md
│   └── ...
├── MVP phase 2/
├── Source Materials MVP phase 1/
│   ├── Input docs/
│   └── ...
└── Source Materials MVP phase 2/
```

- Docs per phase in separate folders; source material (meetings, docs) in the matching “Source Materials” folders. Handy to have a root README and, if needed, rules marking “Source Materials” as read-only.

---

### 4.4. Utility project (scripts + data)

- Scripts (e.g. transcription, conversion), `requirements.txt`, folder for input files and results. Cursor rules are optional.  
- Reference material (docs, examples) — add a README and optional style/structure rule.

---

## 5. Documentation guidelines

### Documentation workflow

*(Diagram: business-process-documentation.png — see [repo](https://github.com/akopvardanian-symfa/Cursor-Setup).)*

**In short:** sources are read-only → edit locally → before publishing check Confluence → publish on request → keep Jira and Confluence in sync.

---

Summary of rules that repeat across projects:

### 5.1. Locally-first vs Confluence as source of truth

- **Locally-first:** drafts and edits live in the repo (in `.md` files). Confluence is updated only when you explicitly ask (“publish”, “sync”).
- **Source of truth for published content:** Confluence. Before updating a page in Confluence, always fetch current content once (MCP `confluence_get_page`) and comments if needed (`confluence_get_comments`), so you don’t overwrite manual edits.

### 5.2. Source Material — read-only

- Folders with transcripts, notes, incoming docs — **do not edit** or delete unless explicitly asked.  
- Final content lives in working folders (SI/, DI/, Documentation/, MVP phase 1/2, etc.) and, when relevant, in Confluence.

### 5.3. Conflicts: inform the user

- Before editing a Confluence page, check comments. If the same block is under discussion or there are alternative wordings — tell the user and don’t overwrite without confirmation.
- Same for Jira: when changing issue fields, check changelog/comments and report possible conflicts.

### 5.4. Confluence attachments

- Listing, uploading, embedding in body, deleting — prefer **scripts** from `Technical/` over MCP so you don’t pull large data into chat. Document commands in README or `Technical/README.md`.  
- **Important:** scripts require Python. On every machine that runs them you need [Python](https://www.python.org/downloads/) and: `pip install -r Technical/requirements.txt`. Without Python the scripts don’t run. If you skip Python — upload Confluence attachments manually in the web UI.

**Use case: images when reading and working with Confluence via MCP**  
When working with Confluence page content via MCP (search, read, update), **MCP cannot insert images or attachments onto a page**. So in `Technical/` there is a dedicated script (`confluence_upload_and_embed_image.py`) that Cursor runs automatically when the user asks to insert an image on a Confluence page or says they can’t see an image on the page. The user only needs to ask (“insert this image on page …”, “image doesn’t show on the page”); the agent fills in the right `page_id` and file path and runs the script from `Technical/`.

### 5.5. Syncing Jira and Confluence (when applicable)

- On initiative pages in Confluence there is a table of action items with a **Jira** column (links to issues). When creating a new Jira issue for an initiative, add a row to that table in Confluence with a link to the issue. Keep the Epic → Confluence page ID mapping in rules or in CONFLUENCE_CONTEXT.
