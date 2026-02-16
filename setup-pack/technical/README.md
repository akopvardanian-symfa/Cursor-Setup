# Confluence scripts (reference)

Scripts are **not** shipped here — generate them in your project via Cursor. Paste the prompt from **`PROMPT_technical_scripts.md`** (in the setup-pack root) in the Agent chat; Cursor will create `Technical/` with the scripts.

## Dependencies

```bash
pip install -r requirements.txt
```

Or: `pip install requests`

## Confluence

You need **`Technical/.env`** with:

- `CONFLUENCE_URL` (e.g. `https://your-company.atlassian.net/wiki`)
- `CONFLUENCE_USERNAME`
- `CONFLUENCE_API_TOKEN`

The `.env` template is in the setup-pack root: **`env.example`** — copy it to `Technical/.env` and fill in.

## Scripts the prompt creates

| Script                              | Purpose |
|-------------------------------------|---------|
| `upload_confluence_attachment.py`   | Upload a file as an attachment to a Confluence page |
| `download_confluence_attachment.py`| Download an attachment from a page |
| `delete_confluence_attachment.py`  | Delete an attachment (only when explicitly asked) |
| `confluence_upload_and_embed_image.py` | Upload an image and embed it in the page body |

Usage examples are in each script’s docstring after generation.
