#!/usr/bin/env python3
"""
Download an attachment from a Confluence page via REST API.

Uses: GET /rest/api/content/{page_id}/child/attachment (list) then download URL.

Requires: CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN (env or .env)

Usage:
  python download_confluence_attachment.py <page_id> <filename> [output_path]

Example:
  python download_confluence_attachment.py 123456789 diagram.png ./diagram.png
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


def main() -> int:
    load_env()

    parser = argparse.ArgumentParser(description="Download an attachment from a Confluence page.")
    parser.add_argument("page_id", help="Confluence page ID")
    parser.add_argument("filename", help="Attachment filename")
    parser.add_argument("output_path", nargs="?", type=Path, help="Output file path (default: ./filename)")
    args = parser.parse_args()

    base_url = os.environ.get("CONFLUENCE_URL", "").rstrip("/")
    username = os.environ.get("CONFLUENCE_USERNAME", "")
    api_token = os.environ.get("CONFLUENCE_API_TOKEN", "")

    if not base_url or not username or not api_token:
        print("Set CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN (env or .env in this directory).", file=sys.stderr)
        sys.exit(1)

    output_path = args.output_path or Path(args.filename)

    # Download URL: /wiki/download/attachments/{page_id}/{filename}
    download_url = f"{base_url}/download/attachments/{args.page_id}/{args.filename}"

    resp = requests.get(download_url, auth=(username, api_token), timeout=60)
    resp.raise_for_status()

    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(resp.content)

    print(f"Downloaded: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
