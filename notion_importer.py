import hashlib
import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

import requests

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")

PROP_TITLE = "Page Title"
PROP_AI_TOOL = "AI Tool"
PROP_CATEGORY = "Category"
PROP_STATUS = "Status"
PROP_CONTENT = "Conversation Content"
PROP_EXTERNAL_ID = "External ID"

DEFAULT_STATUS = "مكتمل"
RICH_TEXT_CHUNK = 1800

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def require_env() -> None:
    missing = []
    if not NOTION_TOKEN:
        missing.append("NOTION_TOKEN")
    if not DATABASE_ID:
        missing.append("DATABASE_ID")
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")


def stable_external_id(chat: Dict[str, Any]) -> str:
    explicit = str(chat.get("id") or chat.get("external_id") or "").strip()
    if explicit:
        return explicit
    title = str(chat.get("title", "")).strip()
    ai_tool = str(chat.get("ai_tool", "")).strip()
    category = str(chat.get("category", "")).strip()
    content = str(chat.get("content", "")).strip()
    payload = "\n".join([title, ai_tool, category, content]).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def chunk_rich_text(text: str, chunk_size: int = RICH_TEXT_CHUNK) -> List[Dict[str, Any]]:
    text = text or ""
    chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
    if not chunks:
        chunks = [""]
    return [{"text": {"content": chunk}} for chunk in chunks]


def request_with_retry(
    method: str,
    url: str,
    *,
    json_body: Optional[Dict[str, Any]] = None,
    max_retries: int = 5,
    base_sleep: float = 0.8,
) -> requests.Response:
    for attempt in range(max_retries):
        resp = SESSION.request(method, url, json=json_body, timeout=30)
        if resp.status_code in (200, 201):
            return resp
        if resp.status_code == 429 or 500 <= resp.status_code <= 599:
            retry_after = resp.headers.get("Retry-After")
            sleep_s = float(retry_after) if retry_after else base_sleep * (2**attempt)
            time.sleep(min(sleep_s, 20))
            continue
        return resp
    return resp


def notion_page_exists_by_external_id(external_id: str) -> Tuple[bool, Optional[str]]:
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    body = {"filter": {"property": PROP_EXTERNAL_ID, "rich_text": {"equals": external_id}}}
    resp = request_with_retry("POST", url, json_body=body)
    if resp.status_code != 200:
        print(f"❌ Query failed for External ID: {external_id}\n{resp.text}")
        return False, None
    results = resp.json().get("results", [])
    if not results:
        return False, None
    return True, results[0].get("id")


def add_chat_to_notion(chat: Dict[str, Any]) -> bool:
    title = str(chat.get("title", "محادثة غير معنونة"))
    ai_tool = str(chat.get("ai_tool", "Other"))
    category = str(chat.get("category", "بحث"))
    content = str(chat.get("content", ""))
    external_id = stable_external_id(chat)

    url = "https://api.notion.com/v1/pages"
    body = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            PROP_TITLE: {"title": [{"text": {"content": title}}]},
            PROP_AI_TOOL: {"select": {"name": ai_tool}},
            PROP_CATEGORY: {"select": {"name": category}},
            PROP_STATUS: {"status": {"name": DEFAULT_STATUS}},
            PROP_EXTERNAL_ID: {"rich_text": [{"text": {"content": external_id}}]},
            PROP_CONTENT: {"rich_text": chunk_rich_text(content)},
        },
    }
    resp = request_with_retry("POST", url, json_body=body)
    if resp.status_code in (200, 201):
        print(f"✅ Created: {title}")
        return True
    print(f"❌ Create failed: {title}\n{resp.text}")
    return False


def update_chat_in_notion(page_id: str, chat: Dict[str, Any]) -> bool:
    title = str(chat.get("title", "محادثة غير معنونة"))
    ai_tool = str(chat.get("ai_tool", "Other"))
    category = str(chat.get("category", "بحث"))
    content = str(chat.get("content", ""))

    url = f"https://api.notion.com/v1/pages/{page_id}"
    body = {
        "properties": {
            PROP_TITLE: {"title": [{"text": {"content": title}}]},
            PROP_AI_TOOL: {"select": {"name": ai_tool}},
            PROP_CATEGORY: {"select": {"name": category}},
            PROP_STATUS: {"status": {"name": DEFAULT_STATUS}},
            PROP_CONTENT: {"rich_text": chunk_rich_text(content)},
        }
    }
    resp = request_with_retry("PATCH", url, json_body=body)
    if resp.status_code == 200:
        print(f"♻️ Updated: {title} | page_id={page_id}")
        return True
    print(f"❌ Update failed: {title} | page_id={page_id}\n{resp.text}")
    return False


def load_chats_from_file(filepath: str) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("chats"), list):
        return data["chats"]
    return []


def collect_chat_files(repo_dir: str = ".", file_pattern: str = "chats.json") -> List[str]:
    found = []
    for root, _, files in os.walk(repo_dir):
        for name in files:
            if name.endswith(".json") and file_pattern in name:
                found.append(os.path.join(root, name))
    return sorted(found)
