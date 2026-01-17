# Codex (WejdanAI) — Notion Sync

## What it does
- Reads chats JSON from repo
- Deduplicates using External ID
- Creates or Updates pages in Notion
- Runs locally or via GitHub Actions

## Notion setup (required)
Create these properties in your Notion database:
- Page Title (Title)
- AI Tool (Select)
- Category (Select)
- Status (Status)
- Conversation Content (Rich text)
- External ID (Rich text)

## GitHub Secrets
Add:
- NOTION_TOKEN
- DATABASE_ID

## Local run
```bash
export NOTION_TOKEN="..."
export DATABASE_ID="..."
python codex.py sync --update-existing
python codex.py sync --dry-run
```

## Actions
Workflow: .github/workflows/notion-sync.yml
- runs on push to json files
- schedule daily
- manual dispatch supported
- concurrency prevents duplicate runs
