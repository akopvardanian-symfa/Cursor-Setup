#!/usr/bin/env python3
"""
Delete attachments from a Confluence page via REST API.

Uses: DELETE /rest/api/content/{attachment_id}
(see https://support.atlassian.com/confluence/kb/how-to-delete-an-attachment-from-a-confluence-page-using-the-rest-api/)

Requires: CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN (env or .env)

Usage:
  python delete_confluence_attachment.py <page_id> <filename1> [filename2 ...]

Example:
  python delete_confluence_attachment.py 123456789 old-diagram.png photo.jpg
"""

import argparse
import json
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


def get_page_attachments(base_url: str, username: str, api_token: str, page_id: str) -> list:
    """Fetch page metadata with attachments."""
    url = f"{base_url.rstrip('/')}/rest/api/content/{page_id}"
    params = {"expand": "metadata.labels"}
    resp = requests.get(url, auth=(username, api_token), params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Attachments come from metadata in some APIs; try alternative
    if "metadata" in data and "attachments" in data["metadata"]:
        return data["metadata"]["attachments"]
    # Fallback: fetch child attachments
    child_url = f"{base_url.rstrip('/')}/rest/api/content/{page_id}/child/attachment"
    child_resp = requests.get(child_url, auth=(username, api_token), timeout=30)
    child_resp.raise_for_status()
    result = child_resp.json()
    return result.get("results", result) if isinstance(result, dict) else result


def delete_attachment(base_url: str, username: str, api_token: str, attachment_id: str) -> bool:
    """Delete attachment by content ID. Returns True on success."""
    # Use numeric ID if id is like "att123456"
    aid = attachment_id
    if aid.startswith("att"):
        aid = aid[3:]
    url = f"{base_url.rstrip('/')}/rest/api/content/{aid}"
    resp = requests.delete(url, auth=(username, api_token), params={"status": "current"}, timeout=30)
    if resp.status_code in (200, 204):
        return True
    # Try with full att prefix
    if not attachment_id.startswith("att"):
        url = f"{base_url.rstrip('/')}/rest/api/content/{attachment_id}"
        resp = requests.delete(url, auth=(username, api_token), params={"status": "current"}, timeout=30)
        return resp.status_code in (200, 204)
    resp.raise_for_status()
    return False


def main():
    load_env()

    parser = argparse.ArgumentParser(description="Delete attachments from a Confluence page.")
    parser.add_argument("page_id", help="Confluence page ID")
    parser.add_argument("filenames", nargs="+", help="Attachment filenames to delete")
    args = parser.parse_args()

    base_url = os.environ.get("CONFLUENCE_URL", "").rstrip("/")
    username = os.environ.get("CONFLUENCE_USERNAME", "")
    api_token = os.environ.get("CONFLUENCE_API_TOKEN", "")

    if not base_url or not username or not api_token:
        print(
            "Set CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN (env or .env).",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        attachments = get_page_attachments(base_url, username, api_token, args.page_id)
    except requests.HTTPError as e:
        print(f"HTTP error fetching page: {e.response.status_code}", file=sys.stderr)
        sys.exit(1)

    by_title = {a.get("title", ""): a for a in attachments}
    to_delete = []
    for fn in args.filenames:
        if fn in by_title:
            to_delete.append((fn, by_title[fn].get("id")))
        else:
            print(f"Warning: attachment '{fn}' not found on page", file=sys.stderr)

    if not to_delete:
        print("No matching attachments to delete.", file=sys.stderr)
        sys.exit(1)

    for title, att_id in to_delete:
        try:
            delete_attachment(base_url, username, api_token, att_id)
            print(f"Deleted: {title}")
        except requests.HTTPError as e:
            print(f"Failed to delete {title}: {e.response.status_code} {e.response.text[:200]}", file=sys.stderr)
            sys.exit(1)

    return 0


if __name__ == "__main__":
    sys.exit(main())
