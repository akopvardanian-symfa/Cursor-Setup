#!/usr/bin/env python3
"""
Upload an image to a Confluence page AND embed it into the page body.

Why:
  - MCP doesn't provide attachment upload
  - Doing this via REST avoids pulling huge page bodies into LLM context

Requirements:
  - requests (pip install requests)
  - Confluence creds in env or Technical/.env:
      CONFLUENCE_URL=https://example.atlassian.net/wiki
      CONFLUENCE_USERNAME=...
      CONFLUENCE_API_TOKEN=...

Usage:
  python3 confluence_upload_and_embed_image.py <page_id> <path_to_image> \
    --anchor "Process diagram" --alt "Process Flow" --width 900

Idempotent:
  - If the attachment exists, Confluence updates it.
  - If the image is already embedded, page update is skipped.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
import re
from typing import Optional, Tuple

try:
    import requests
except ImportError:
    print("Install requests: pip install requests", file=sys.stderr)
    sys.exit(1)


def load_env_from_technical_dir() -> None:
    """Load optional Technical/.env (CONFLUENCE_* only)."""
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        if key.startswith("CONFLUENCE_") and key not in os.environ:
            os.environ[key] = value


def confluence_auth() -> Tuple[str, str, str]:
    base_url = os.environ.get("CONFLUENCE_URL", "").rstrip("/")
    username = os.environ.get("CONFLUENCE_USERNAME", "")
    api_token = os.environ.get("CONFLUENCE_API_TOKEN", "")
    if not base_url or not username or not api_token:
        raise RuntimeError(
            "Set CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN "
            "(env or Technical/.env)."
        )
    return base_url, username, api_token


def guess_mime(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }.get(suffix, "application/octet-stream")


def upload_attachment(
    *,
    base_url: str,
    username: str,
    api_token: str,
    page_id: str,
    file_path: Path,
    comment: str = "",
    minor_edit: bool = True,
) -> dict:
    """
    PUT /rest/api/content/{id}/child/attachment
    """
    url = f"{base_url.rstrip('/')}/rest/api/content/{page_id}/child/attachment"
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    mime = guess_mime(file_path)

    with open(file_path, "rb") as f:
        files = {"file": (file_path.name, f, mime)}
        data = {"minorEdit": "true" if minor_edit else "false"}
        if comment:
            data["comment"] = comment

        headers = {"X-Atlassian-Token": "nocheck"}
        resp = requests.put(
            url,
            auth=(username, api_token),
            headers=headers,
            files=files,
            data=data,
            timeout=60,
        )

    resp.raise_for_status()
    return resp.json()


def get_page_storage(
    *,
    base_url: str,
    username: str,
    api_token: str,
    page_id: str,
) -> Tuple[str, int, str]:
    """
    Returns (title, version_number, storage_html)
    """
    url = f"{base_url.rstrip('/')}/rest/api/content/{page_id}"
    params = {"expand": "body.storage,version,title"}
    resp = requests.get(url, auth=(username, api_token), params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    title = data.get("title") or ""
    version_number = int((data.get("version") or {}).get("number") or 0)
    storage = ((data.get("body") or {}).get("storage") or {}).get("value") or ""
    if not title or version_number <= 0 or not isinstance(storage, str):
        raise RuntimeError("Unexpected Confluence response while fetching page.")
    return title, version_number, storage


def update_page_storage(
    *,
    base_url: str,
    username: str,
    api_token: str,
    page_id: str,
    title: str,
    new_version_number: int,
    storage_html: str,
    version_message: str,
    minor_edit: bool = True,
) -> dict:
    url = f"{base_url.rstrip('/')}/rest/api/content/{page_id}"
    payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "version": {
            "number": new_version_number,
            "minorEdit": bool(minor_edit),
            "message": version_message,
        },
        "body": {
            "storage": {
                "value": storage_html,
                "representation": "storage",
            }
        },
    }
    resp = requests.put(
        url,
        auth=(username, api_token),
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def build_image_macro(filename: str, alt: str = "", width: Optional[int] = None) -> str:
    """
    Build a Confluence storage-format image macro that references an attachment.
    """
    alt_attr = f' ac:alt="{alt}"' if alt else ""
    width_attr = f' ac:width="{int(width)}"' if width else ""
    return (
        f"<ac:image{alt_attr}{width_attr}>"
        f'<ri:attachment ri:filename="{filename}" />'
        f"</ac:image>"
    )


def _has_image_macro(storage_html: str, filename: str) -> bool:
    return (
        f'ri:attachment ri:filename="{filename}"' in storage_html
        or f'ri:filename="{filename}"' in storage_html
        or f"ri:attachment ri:filename='{filename}'" in storage_html
        or f"ri:filename='{filename}'" in storage_html
    )


def _replace_image_macro(storage_html: str, filename: str, new_macro: str) -> Tuple[str, bool]:
    escaped = re.escape(filename)
    pat = re.compile(
        rf"<ac:image\b[^>]*>\s*<ri:attachment\b[^>]*\bri:filename=(['\"])({escaped})\1[^>]*/>\s*</ac:image>",
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not pat.search(storage_html):
        return storage_html, False
    return pat.sub(new_macro, storage_html, count=1), True


def _find_img_tag_pattern(filename: str) -> re.Pattern:
    escaped = re.escape(filename)
    return re.compile(
        rf"(?:<p>\s*)?<img\b[^>]*\bsrc=(['\"])({escaped})\1[^>]*\/?>\s*(?:<\/p>)?",
        flags=re.IGNORECASE,
    )


def insert_image(
    *,
    storage_html: str,
    filename: str,
    alt: str,
    anchor: Optional[str],
    width: Optional[int],
) -> Tuple[str, bool]:
    """
    Returns (new_storage_html, changed?)
    """
    macro = build_image_macro(filename=filename, alt=alt, width=width)

    if _has_image_macro(storage_html, filename):
        if alt or width:
            return _replace_image_macro(storage_html, filename, macro)
        return storage_html, False

    img_pat = _find_img_tag_pattern(filename)
    if img_pat.search(storage_html):
        new_storage = img_pat.sub(macro, storage_html, count=1)
        return new_storage, True

    if anchor:
        idx = storage_html.find(anchor)
        if idx != -1:
            insert_at = idx + len(anchor)
            return storage_html[:insert_at] + "\n" + macro + "\n" + storage_html[insert_at:], True

    needle = "<strong>Process diagram</strong>"
    idx = storage_html.find(needle)
    if idx != -1:
        p_close = storage_html.find("</p>", idx)
        if p_close != -1:
            insert_at = p_close + len("</p>")
            return storage_html[:insert_at] + "\n" + macro + "\n" + storage_html[insert_at:], True

    prefix = f"<p><strong>Process diagram</strong></p>\n{macro}\n"
    return prefix + storage_html, True


def main() -> int:
    load_env_from_technical_dir()

    parser = argparse.ArgumentParser(
        description="Upload an image to Confluence and embed it in the page body."
    )
    parser.add_argument("page_id", help="Confluence page ID")
    parser.add_argument("image_path", type=Path, help="Path to image (png/jpg/...)")
    parser.add_argument("--alt", default="", help="Alt text for the image macro (optional).")
    parser.add_argument(
        "--width",
        type=int,
        default=0,
        help="Optional image width in pixels (e.g. 900).",
    )
    parser.add_argument(
        "--anchor",
        default="",
        help="Optional anchor substring in storage HTML. If found, image macro is inserted right after it.",
    )
    parser.add_argument("--comment", default="", help="Optional attachment comment.")
    parser.add_argument("--message", default="Embed image attachment", help="Confluence page version message.")
    parser.add_argument("--no-minor-edit", action="store_true", help="Record as a full version (default: minor edit).")
    parser.add_argument("--dry-run", action="store_true", help="Do not update page; only show what would happen.")
    args = parser.parse_args()

    base_url, username, api_token = confluence_auth()
    image_path = args.image_path.resolve()
    if not image_path.is_file():
        print(f"File not found: {image_path}", file=sys.stderr)
        return 1

    minor_edit = not args.no_minor_edit

    try:
        upload_result = upload_attachment(
            base_url=base_url,
            username=username,
            api_token=api_token,
            page_id=args.page_id,
            file_path=image_path,
            comment=args.comment,
            minor_edit=minor_edit,
        )
    except Exception as e:
        print(f"Upload failed: {e}", file=sys.stderr)
        return 1

    uploaded_title = image_path.name
    if isinstance(upload_result, dict):
        results = upload_result.get("results")
        if isinstance(results, list) and results:
            uploaded_title = results[0].get("title") or uploaded_title
        else:
            uploaded_title = upload_result.get("title") or uploaded_title

    print(f"Uploaded attachment: {uploaded_title}")

    try:
        title, version_number, storage_html = get_page_storage(
            base_url=base_url,
            username=username,
            api_token=api_token,
            page_id=args.page_id,
        )
    except Exception as e:
        print(f"Fetch page failed: {e}", file=sys.stderr)
        return 1

    new_storage, changed = insert_image(
        storage_html=storage_html,
        filename=uploaded_title,
        alt=args.alt,
        anchor=args.anchor or None,
        width=(args.width or None),
    )

    if not changed:
        print("Image already embedded; page update skipped.")
        return 0

    if args.dry_run:
        print("Dry-run: page would be updated (storage).")
        return 0

    try:
        update_page_storage(
            base_url=base_url,
            username=username,
            api_token=api_token,
            page_id=args.page_id,
            title=title,
            new_version_number=version_number + 1,
            storage_html=new_storage,
            version_message=args.message,
            minor_edit=minor_edit,
        )
    except Exception as e:
        print(f"Update page failed: {e}", file=sys.stderr)
        return 1

    print("Page updated: embedded image macro.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
