import json
import os
import requests

# ⚙️ معلومات التكامل
NOTION_TOKEN = os.getenv("NOTION_TOKEN", "secret_xxxxxxxxxx")  # Internal Integration Token
DATABASE_ID = os.getenv("DATABASE_ID", "abc123def456")  # معرف قاعدة البيانات

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def add_chat_to_notion(title, ai_tool, category, content):
    url = "https://api.notion.com/v1/pages"

    data = {
        "parent": {"database_id": DATABASE_ID},
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
                "status": {"name": "مكتمل"},
            },
            "Conversation Content": {
                "rich_text": [
                    {"text": {"content": content}},
                ]
            },
        },
    }

    response = requests.post(url, headers=headers, json=data, timeout=30)

    if response.status_code in (200, 201):
        print(f"✅ تم حفظ المحادثة: {title}")
    else:
        print(f"❌ خطأ في حفظ: {title}")
        print(response.text)


def import_chats_from_json(file_path):
    """استيراد المحادثات من ملف JSON إلى Notion"""
    if not os.path.exists(file_path):
        print(f"❌ الملف غير موجود: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        chats = json.load(file)

    for chat in chats:
        title = chat.get("title", "محادثة غير معنونة")
        ai_tool = chat.get("ai_tool", "Other")
        category = chat.get("category", "بحث")
        content = chat.get("content", "")

        add_chat_to_notion(title, ai_tool, category, content)


if __name__ == "__main__":
    # 📁 ضع اسم الملف هنا
    file_path = "chats.json"
    import_chats_from_json(file_path)
