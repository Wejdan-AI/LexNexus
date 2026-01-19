---
name: Postgres + Nuxt Starter
slug: postgres-nuxt
description: Simple Nuxt template that uses a Postgres database.
framework: Nuxt
useCase: Starter
css: Tailwind
database: Postgres
deployUrl: https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FWejdan-AI%2FLexNexus&project-name=lexnexus&repository-name=LexNexus&demo-title=LexNexus&demo-description=LexNexus%20platform
demoUrl: https://postgres-nuxt.vercel.app/
relatedTemplates:
  - postgres-starter
  - postgres-prisma
  - postgres-sveltekit
---

# Nuxt 3 Minimal Starter

Look at the [Nuxt 3 documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

### 1. Install Dependencies

Make sure to install the dependencies:

```bash
pnpm install
```

### 2. Environment Variables

Create a `.env` file in the root directory based on the `.env.example` template:

```bash
cp .env.example .env
```

Then update the `.env` file with your actual credentials:
- `POSTGRES_URL`: Your PostgreSQL database connection string
- `AI_GATEWAY_API_KEY`: Your AI Gateway API key (keep this secure and never commit it)

**Important**: Never commit your `.env` file to version control. It contains sensitive credentials.

**Important**: Never commit your `.env` file to version control. It contains sensitive credentials.

## Development Server

Start the development server on `http://localhost:3000`

```bash
pnpm dev
```

## Production

Build the application for production:

```bash
pnpm build
```

Locally preview production build:

```bash
pnpm preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.
