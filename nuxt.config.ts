// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  css: ['~/assets/css/main.css'],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },

  runtimeConfig: {
    // Private keys (only available on server-side)
    openaiApiKey: process.env.OPENAI_API_KEY || '',
    taskadeApiKey: process.env.TASKADE_API_KEY || '',
    taskadeWebhookSecret: process.env.TASKADE_WEBHOOK_SECRET || '',
    
    // Public keys (exposed to client-side)
    public: {
      appName: 'LexNexus',
      description: 'Codex GPT & Taskade MCB Integration Platform',
    },
  },

  compatibilityDate: '2025-02-05',
})