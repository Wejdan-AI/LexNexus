// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  css: ['~/assets/css/main.css'],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },

  compatibilityDate: '2025-02-05',

  // PWA Configuration for iOS
  app: {
    head: {
      title: 'WejdanAI',
      meta: [
        { name: 'description', content: 'نظام ذكاء اصطناعي متعدد النماذج' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1, viewport-fit=cover' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },
        { name: 'apple-mobile-web-app-title', content: 'WejdanAI' },
        { name: 'theme-color', content: '#020617' },
      ],
      link: [
        { rel: 'apple-touch-icon', href: '/icon-192.png' },
        { rel: 'manifest', href: '/manifest.json' },
      ],
    },
  },
})