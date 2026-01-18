---
name: WejdanAI
slug: wejdanai
description: A comprehensive AI application with Nuxt.js frontend, Postgres database, AI logging API, and Notion integration.
framework: Nuxt
useCase: AI Application
css: Tailwind
database: Postgres
deployUrl: https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FMOTEB1989%2FWejdanAI&project-name=wejdanai&repository-name=wejdanai
demoUrl: https://wejdanai.vercel.app
relatedTemplates:
  - postgres-starter
  - postgres-prisma
  - postgres-sveltekit
---

# WejdanAI

A comprehensive AI application built with Nuxt.js, featuring a Postgres database, AI chat logging, and Notion integration for codex synchronization.

## Features

- **Frontend**: Nuxt 3 application with Tailwind CSS for a modern UI
- **Database**: Postgres for robust data storage and management
- **AI Logging**: REST API endpoint for logging AI queries and responses
- **Notion Integration**: Sync AI chats and codex data to Notion database
- **Automated Sync**: GitHub Actions workflow for daily Notion synchronization
- **Deployment Ready**: Configured for Vercel deployment with environment handling

## Prerequisites

- Node.js (v18 or higher)
- pnpm
- Python 3.8+
- Postgres database
- Notion account with integration token

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MOTEB1989/WejdanAI.git
   cd WejdanAI
   ```

2. Install Node.js dependencies:
   ```bash
   pnpm install
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup

### Database
Configure your Postgres database connection in `nuxt.config.ts` or environment variables.

### Notion Integration
1. Create a new integration in Notion: https://www.notion.so/my-integrations
2. Get your `NOTION_TOKEN` and `DATABASE_ID`
3. Set environment variables:
   ```bash
   export NOTION_TOKEN="your_notion_token"
   export DATABASE_ID="your_database_id"
   ```

## Development

Start the development server:
```bash
pnpm dev
```
The app will be available at `http://localhost:3000`

## Building for Production

```bash
pnpm build
pnpm preview
```

## Notion Database Setup

For Codex sync, create a Notion database with these properties:
- **Page Title** (Title)
- **AI Tool** (Select)
- **Category** (Select)
- **Status** (Status)
- **Conversation Content** (Rich text)
- **External ID** (Rich text)

## Python Scripts

### Notion Chat Importer
Import chat conversations from JSON to Notion:
```bash
python notion_importer.py
```

### Codex Sync
Synchronize codex data with Notion:
```bash
python codex.py sync --update-existing  # Update existing pages
python codex.py sync --dry-run          # Preview changes
```

## API Documentation

The logging API is documented in [LOGGING_API.md](LOGGING_API.md).

Base URL: `https://wejdanai.vercel.app/api/logs`

### POST /api/logs
Log a new AI interaction:
```json
{
  "user_id": 1,
  "query": "User's question",
  "response": "AI's response"
}
```

### GET /api/logs
Retrieve all logged interactions.

## GitHub Actions

The repository includes automated workflows in `.github/workflows/` for:
- Notion synchronization on pushes to JSON files
- Daily scheduled sync
- Manual dispatch option

## Deployment

Deploy to Vercel:
1. Connect your GitHub repo to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy

## Project Structure

- `app.vue` - Main Nuxt app entry
- `pages/` - Nuxt pages
- `components/` - Reusable Vue components
- `server/` - Server-side API routes
- `assets/` - Static assets
- `public/` - Public files
- `scripts/` - Additional scripts
- `codex.py` - Codex synchronization script
- `notion_importer.py` - Notion importer script
- `LLM` & `LordAI` - AI-related executables/scripts
- `README_CODEX.md` - Additional codex documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.