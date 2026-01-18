---
name: LexNexus
slug: lexnexus
description: Nuxt + Postgres starter configured for LexNexus.
framework: Nuxt
useCase: Starter
css: Tailwind
database: Postgres
deployUrl: https://vercel.com/new/clone?repository-url=https://github.com/Wejdan-AI/LexNexus
demoUrl: https://github.com/Wejdan-AI/LexNexus
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

## Project naming

هذا المستودع مبني على قالب Nuxt 3 مع Postgres لتطبيق LexNexus. تمت إزالة ملف `LordAI` لأنه كان مجرد ملاحظات تمهيدية. إذا أردت تغيير اسم المشروع (مثلًا من Wejdan-AI إلى أي اسم آخر)، حدّث حقل `name` في `package.json` وأعد تشغيل الأدوات.

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.
