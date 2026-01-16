<template>
  <main class="relative min-h-screen py-10 px-4">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1
          class="pt-4 pb-4 bg-gradient-to-br dark:from-white from-black via-[#707070] to-[#ffffff] bg-clip-text text-center text-4xl font-medium tracking-tight text-transparent md:text-6xl"
        >
          LexNexus Platform
        </h1>
        <p class="text-gray-600 dark:text-gray-300 text-lg">
          Codex GPT & Taskade MCB Integration
        </p>
      </div>

      <!-- Tab Navigation -->
      <div class="flex justify-center mb-8 border-b border-gray-200 dark:border-gray-700">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'px-6 py-3 font-medium transition-colors',
            activeTab === tab.id
              ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
          ]"
        >
          {{ tab.name }}
        </button>
      </div>

      <!-- Tab Content -->
      <div class="max-w-4xl mx-auto">
        <MCBIntegration v-if="activeTab === 'mcb'" />
        <CodexChat v-else-if="activeTab === 'codex'" />
        <TaskadeManager v-else-if="activeTab === 'taskade'" />
        <div v-else-if="activeTab === 'database'">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
              Database Demo
            </h2>
            <Table :users="data?.users" :duration="data?.duration" />
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-12 text-center">
        <div class="flex items-center justify-center space-x-4 text-gray-600 dark:text-gray-400">
          <span>Built with</span>
          <a
            href="https://nuxt.com/docs"
            class="flex items-center font-medium underline transition-colors underline-offset-4 hover:text-black dark:hover:text-white"
          >
            <img src="/nuxt.svg" class="h-6 mx-2" />
            <p>Nuxt</p>
          </a>
          <span>+</span>
          <span class="font-medium">OpenAI Codex</span>
          <span>+</span>
          <span class="font-medium">Taskade</span>
        </div>
        <a
          href="https://github.com/Wejdan-AI/LexNexus"
          class="inline-flex items-center mt-4 space-x-2 text-gray-600 dark:text-gray-400 hover:text-black dark:hover:text-white"
        >
          <img src="/github.svg" alt="GitHub Logo" class="h-6 dark:invert" />
          <p class="font-light">View on GitHub</p>
        </a>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'

const { data } = useFetch('/api/get-users')

const activeTab = ref('mcb')
const tabs = [
  { id: 'mcb', name: 'MCB Integration' },
  { id: 'codex', name: 'Codex GPT' },
  { id: 'taskade', name: 'Taskade' },
  { id: 'database', name: 'Database' }
]
</script>
