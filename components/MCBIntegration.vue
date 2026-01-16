<template>
  <div class="mcb-integration bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
    <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
      MCB Integration
      <span class="text-sm font-normal text-gray-500 dark:text-gray-400">
        (Multi-Channel Bot: Codex GPT + Taskade)
      </span>
    </h2>

    <div class="workspace-selector mb-4">
      <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
        Taskade Workspace ID (Optional):
      </label>
      <input
        v-model="workspaceId"
        type="text"
        placeholder="Enter workspace ID for auto-task creation"
        class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
      />
    </div>

    <div class="mb-4">
      <label class="flex items-center text-gray-700 dark:text-gray-300">
        <input
          v-model="autoCreateTasks"
          type="checkbox"
          class="mr-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          :disabled="!workspaceId"
        />
        <span class="text-sm">
          Automatically create tasks in Taskade from AI response
        </span>
      </label>
    </div>

    <div class="request-input mb-4">
      <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
        Your Request:
      </label>
      <textarea
        v-model="prompt"
        @keydown.ctrl.enter="processRequest"
        placeholder="Example: 'Help me plan a new feature for user authentication' or 'Break down the task of building a REST API into actionable steps'"
        class="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        rows="4"
        :disabled="loading"
      ></textarea>
    </div>

    <button
      @click="processRequest"
      :disabled="loading || !prompt.trim()"
      class="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-md"
    >
      <span v-if="!loading">Process with MCB</span>
      <span v-else class="flex items-center justify-center">
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Processing...
      </span>
    </button>

    <div v-if="response" class="mt-6 space-y-4">
      <div class="response-section">
        <h3 class="text-lg font-semibold mb-2 text-gray-800 dark:text-white">
          AI Response:
        </h3>
        <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
          {{ response.aiResponse }}
        </div>
      </div>

      <div v-if="response.tasksCreated && response.tasksCreated.length > 0" class="tasks-created">
        <h3 class="text-lg font-semibold mb-2 text-gray-800 dark:text-white flex items-center">
          <svg class="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          Tasks Created in Taskade:
        </h3>
        <div class="space-y-2">
          <div
            v-for="(task, index) in response.tasksCreated"
            :key="index"
            class="p-3 bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 rounded-lg"
          >
            <div class="font-medium text-green-800 dark:text-green-200">
              ✓ {{ task.content || task.title }}
            </div>
          </div>
        </div>
      </div>

      <div v-if="response.usage" class="text-xs text-gray-500 dark:text-gray-400">
        Model: {{ response.model }} | Tokens: {{ response.usage.total_tokens }}
      </div>
    </div>

    <div v-if="error" class="mt-4 p-3 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded-lg">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const workspaceId = ref('')
const prompt = ref('')
const autoCreateTasks = ref(false)
const response = ref(null)
const loading = ref(false)
const error = ref('')

const processRequest = async () => {
  if (!prompt.value.trim() || loading.value) return

  loading.value = true
  error.value = ''
  response.value = null

  try {
    const result = await $fetch('/api/mcb-integration', {
      method: 'POST',
      body: {
        prompt: prompt.value,
        taskadeWorkspaceId: workspaceId.value || undefined,
        autoCreateTasks: autoCreateTasks.value
      }
    })

    response.value = result
  } catch (err) {
    error.value = err.data?.statusMessage || 'Failed to process request'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}
</script>
