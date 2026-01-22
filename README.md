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

## Tailwind CSS

This project comes with Tailwind CSS v3.3.2 pre-configured and ready to use.

### Configuration

Tailwind is configured via `tailwind.config.js`:

```js
module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./nuxt.config.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

The main CSS file (`assets/css/main.css`) includes the Tailwind directives:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Usage Examples

Tailwind utility classes can be used directly in your Vue components:

```vue
<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
    <div class="max-w-md p-6 bg-white rounded-lg shadow-lg dark:bg-gray-800">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
        Welcome to Tailwind!
      </h1>
      <p class="mt-2 text-gray-600 dark:text-gray-300">
        Start building with utility-first CSS classes.
      </p>
    </div>
  </div>
</template>
```

### Dark Mode Support

Dark mode is enabled by default using the `class` strategy. Toggle dark mode by adding the `dark` class to the root element:

```vue
<html class="dark">
  <!-- Your app with dark mode enabled -->
</html>
```

### Customization

To customize your Tailwind configuration, edit `tailwind.config.js`. For example, to add custom colors:

```js
theme: {
  extend: {
    colors: {
      primary: '#3b82f6',
      secondary: '#8b5cf6',
    },
  },
},
```

### Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Nuxt Tailwind Module](https://tailwindcss.nuxtjs.org/)
- [Tailwind UI Components](https://tailwindui.com/)

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
