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

Make sure to install the dependencies:

```bash
pnpm install
```

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

## Vercel Deployment Automation

This repository includes examples for automating deployments using the Vercel SDK.

### Quick Start

1. Set your Vercel API token:
   ```bash
   export VERCEL_TOKEN=your_vercel_token_here
   ```

2. Run an example:
   ```bash
   pnpm run example:create-deployment
   # or
   pnpm run example:deployment-with-alias
   ```

For more information, see:
- [Deployment Automation Documentation](docs/deployment-automation.md)
- [Examples Directory](examples/)

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.
