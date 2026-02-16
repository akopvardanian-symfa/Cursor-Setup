# Prompt: generate Confluence scripts

You don’t have to copy Confluence attachment scripts from setup-pack — you can ask Cursor to generate them locally. Copy the text below and paste it in the Agent chat.

---

Create the **`Technical/`** folder in the project and write scripts for working with Confluence attachments via the REST API (so large data doesn’t go through MCP).

**Do this:**

1. Create **`Technical/.env.example`** with variables:
   - `CONFLUENCE_URL` (e.g. `https://company.atlassian.net/wiki`)
   - `CONFLUENCE_USERNAME`
   - `CONFLUENCE_API_TOKEN`  
   At the top of the file add: copy to `Technical/.env` and fill in; do not commit `.env`.

2. Create **`Technical/requirements.txt`** with one line: `requests>=2.28.0`.

3. Write Python scripts (read credentials from `Technical/.env` or env vars `CONFLUENCE_*`):
   - **`upload_confluence_attachment.py`** — upload a file as an attachment to a Confluence page. Usage: `python upload_confluence_attachment.py <page_id> <path_to_file>`. Use Confluence REST API (PUT /rest/api/content/{id}/child/attachment).
   - **`download_confluence_attachment.py`** — download an attachment by page_id and filename. Usage: `python download_confluence_attachment.py <page_id> <filename> [output_path]`.
   - **`delete_confluence_attachment.py`** — delete an attachment (only when the user explicitly asks). Usage: `python delete_confluence_attachment.py <page_id> <filename1> [filename2 ...]`.
   - **`confluence_upload_and_embed_image.py`** — upload an image as an attachment and embed it in the page body (storage HTML, macro `ac:image` with `ri:attachment`). Usage: `python confluence_upload_and_embed_image.py <page_id> <path_to_image> [--anchor "..." --alt "..." --width N]`.

Scripts should load `.env` from the same folder (Technical/) if the file exists. Print errors to stderr; put usage examples in each script’s docstring.

4. **Before installing dependencies** check for Python: run `python --version` or `py --version` in the terminal. If Python is installed — **run** `pip install -r Technical/requirements.txt`. If not — tell the user to install from [python.org](https://www.python.org/downloads/) or skip the scripts (attachments then only via Confluence web UI). Then briefly say what was created and what’s left (fill `Technical/.env`).

**Important:** on every machine where these scripts will run, Python must be installed and `pip install -r Technical/requirements.txt` must be run. Files can be copied between machines, but Python and dependencies must be installed on each.
