"""Utility to store chat conversations in a Notion database."""

import json
import os

import requests

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"


def build_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def add_chat_to_notion(
    *,
    database_id: str,
    token: str,
    title: str,
    ai_tool: str,
    category: str,
    content: str,
    status: str = "مكتمل",
) -> requests.Response:
    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Page Title": {
                "title": [
                    {"text": {"content": title}},
                ]
            },
            "AI Tool": {
                "select": {"name": ai_tool},
            },
            "Category": {
                "select": {"name": category},
            },
            "Status": {
                "status": {"name": status},
            },
            "Conversation Content": {
                "rich_text": [
                    {"text": {"content": content}},
                ]
            },
        },
    }

    response = requests.post(
        NOTION_API_URL,
        headers=build_headers(token),
        json=payload,
        timeout=30,
    )
    return response


def main() -> int:
    token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not token or not database_id:
        print("❌ Missing NOTION_TOKEN or NOTION_DATABASE_ID environment variables.")
        return 1

    response = add_chat_to_notion(
        database_id=database_id,
        token=token,
        title=os.getenv("CHAT_TITLE", "تحليل بيانات مالية"),
        ai_tool=os.getenv("CHAT_AI_TOOL", "ChatGPT"),
        category=os.getenv("CHAT_CATEGORY", "تحليل"),
        content=os.getenv("CHAT_CONTENT", "المحادثة الكاملة هنا..."),
    )

    if response.status_code in (200, 201):
        print("✅ تم حفظ المحادثة في Notion بنجاح!")
        return 0

    print(f"❌ خطأ: {response.status_code}")
    try:
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print(response.text)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
