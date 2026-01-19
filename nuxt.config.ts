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
    // Private keys that are only available on the server
    aiGatewayApiKey: process.env.AI_GATEWAY_API_KEY || '',
    // Public keys that are exposed to the client
    public: {
      // Add public runtime config here if needed
    },
  },

  compatibilityDate: '2025-02-05',
})