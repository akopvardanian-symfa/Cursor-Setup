#!/usr/bin/env python3
"""
Upload a file (e.g. image) to a Confluence page via REST API.

Uses Confluence REST API v1: PUT /rest/api/content/{id}/child/attachment
(see https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-content---attachments/)

Usage:
  export CONFLUENCE_URL="https://your-company.atlassian.net/wiki"
  export CONFLUENCE_USERNAME="your.email@company.com"
  export CONFLUENCE_API_TOKEN="your-api-token"
  python upload_confluence_attachment.py <page_id> <path_to_file>

Example:
  python upload_confluence_attachment.py 123456789 "../docs/diagram.png"
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests: pip install requests", file=sys.stderr)
    sys.exit(1)


def load_env():
    """Load optional .env from script directory (CONFLUENCE_* only)."""
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip().strip("'\"")
            if key.startswith("CONFLUENCE_") and key not in os.environ:
                os.environ[key] = value


def upload_attachment(
    base_url: str,
    username: str,
    api_token: str,
    page_id: str,
    file_path: Path,
    comment: str = "",
    minor_edit: bool = True,
) -> dict:
    url = f"{base_url.rstrip('/')}/rest/api/content/{page_id}/child/attachment"
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Prefer correct MIME type so Confluence treats images as images
    suffix = file_path.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }.get(suffix, "application/octet-stream")

    with open(file_path, "rb") as f:
        files = {"file": (file_path.name, f, mime)}
        data = {
            "minorEdit": "true" if minor_edit else "false",
        }
        if comment:
            data["comment"] = (None, comment, "text/plain; charset=utf-8")

        # Confluence requires this header for multipart to avoid XSRF block
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


def main():
    load_env()

    parser = argparse.ArgumentParser(
        description="Upload a file (e.g. image) to a Confluence page."
    )
    parser.add_argument(
        "page_id",
        help="Confluence page ID",
    )
    parser.add_argument(
        "file_path",
        type=Path,
        help="Path to the file to upload",
    )
    parser.add_argument(
        "--comment",
        default="",
        help="Optional comment for the attachment",
    )
    parser.add_argument(
        "--no-minor-edit",
        action="store_true",
        help="Record as a full version (default: minor edit)",
    )
    args = parser.parse_args()

    base_url = os.environ.get("CONFLUENCE_URL", "").rstrip("/")
    username = os.environ.get("CONFLUENCE_USERNAME", "")
    api_token = os.environ.get("CONFLUENCE_API_TOKEN", "")

    if not base_url or not username or not api_token:
        print(
            "Set CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN "
            "(env or .env in this directory).",
            file=sys.stderr,
        )
        sys.exit(1)

    file_path = args.file_path.resolve()
    if not file_path.is_file():
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        result = upload_attachment(
            base_url=base_url,
            username=username,
            api_token=api_token,
            page_id=args.page_id,
            file_path=file_path,
            comment=args.comment,
            minor_edit=not args.no_minor_edit,
        )
    except requests.HTTPError as e:
        print(f"HTTP error: {e.response.status_code}", file=sys.stderr)
        if e.response.text:
            print(e.response.text[:500], file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    # Response can be a single object or list under "results"
    results = result.get("results", [result]) if isinstance(result, dict) else result
    for att in results:
        title = att.get("title", file_path.name)
        print(f"Uploaded: {title}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
