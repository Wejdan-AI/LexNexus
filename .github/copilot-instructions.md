# Copilot Instructions for LexNexus

## Project Overview
LexNexus is a Nuxt 3 application that uses PostgreSQL as the database. It's built on the Vercel Postgres + Nuxt starter template and provides a legal/compliance platform interface.

## Tech Stack
- **Framework**: Nuxt 3
- **Language**: TypeScript/JavaScript
- **Styling**: Tailwind CSS
- **Database**: PostgreSQL (via `postgres` npm package)
- **Package Manager**: pnpm
- **Deployment**: Vercel

## Project Structure
- `/pages` - Nuxt pages (file-based routing)
- `/components` - Vue components
- `/server/api` - Server API endpoints
- `/assets` - Static assets (CSS, images)
- `/public` - Public static files
- `app.vue` - Main app component
- `nuxt.config.ts` - Nuxt configuration

## Development Commands
- **Install dependencies**: `pnpm install`
- **Start dev server**: `pnpm dev` (runs on http://localhost:3000)
- **Build for production**: `pnpm build`
- **Preview production build**: `pnpm preview`
- **Generate static site**: `pnpm generate`

## Coding Conventions
- Use TypeScript for all `.ts` files and `<script setup>` blocks in Vue components
- Follow Vue 3 Composition API patterns with `<script setup>` syntax
- Use Tailwind CSS utility classes for styling
- Use `useFetch` composable for API calls in components
- Server API routes should be placed in `/server/api` directory
- Use kebab-case for component file names

## Database
- PostgreSQL connection is handled via the `postgres` npm package
- Database queries should be performed in server API routes (`/server/api`)
- Connection configuration is managed through Vercel environment variables

## Best Practices
- Keep components focused and reusable
- Use Nuxt's auto-imports feature for composables and utilities
- Leverage server-side rendering (SSR) capabilities of Nuxt
- Use Tailwind's responsive design utilities (e.g., `md:`, `dark:`)
- Follow accessibility best practices in Vue templates

## Testing
- Currently no test infrastructure is set up in this repository
- When adding tests, consider using Vitest (recommended for Nuxt 3)

## Notes
- The project uses Turbo for build optimization
- PostCSS is configured with Tailwind CSS and Autoprefixer
- The app is optimized for deployment on Vercel
