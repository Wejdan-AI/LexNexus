<template>
  <div class="codex-chat bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
    <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
      Codex GPT Assistant
    </h2>
    
    <div class="chat-messages mb-4 h-96 overflow-y-auto space-y-4">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="[
          'p-4 rounded-lg',
          message.role === 'user'
            ? 'bg-blue-100 dark:bg-blue-900 ml-8'
            : 'bg-gray-100 dark:bg-gray-700 mr-8'
        ]"
      >
        <div class="font-semibold mb-1 text-gray-800 dark:text-white">
          {{ message.role === 'user' ? 'You' : 'Codex GPT' }}
        </div>
        <div class="text-gray-700 dark:text-gray-200 whitespace-pre-wrap">
          {{ message.content }}
        </div>
      </div>
      
      <div v-if="loading" class="text-center text-gray-500 dark:text-gray-400">
        <span class="inline-block animate-pulse">Thinking...</span>
      </div>
    </div>

    <div class="chat-input flex gap-2">
      <textarea
        v-model="prompt"
        @keydown.ctrl.enter="sendMessage"
        placeholder="Ask Codex GPT anything... (Ctrl+Enter to send)"
        class="flex-1 p-3 border border-gray-300 dark:border-gray-600 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        rows="3"
        :disabled="loading"
      ></textarea>
      <button
        @click="sendMessage"
        :disabled="loading || !prompt.trim()"
        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        Send
      </button>
    </div>

    <div v-if="error" class="mt-4 p-3 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded-lg">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const messages = ref([
  {
    role: 'assistant',
    content: 'Hello! I\'m Codex GPT, your AI coding assistant. How can I help you today?'
  }
])
const prompt = ref('')
const loading = ref(false)
const error = ref('')

const sendMessage = async () => {
  if (!prompt.value.trim() || loading.value) return

  const userMessage = prompt.value.trim()
  messages.value.push({
    role: 'user',
    content: userMessage
  })
  
  prompt.value = ''
  loading.value = true
  error.value = ''

  try {
    const response = await $fetch('/api/codex', {
      method: 'POST',
      body: {
        prompt: userMessage,
        model: 'gpt-4'
      }
    })

    messages.value.push({
      role: 'assistant',
      content: response.response
    })
  } catch (err) {
    error.value = err.data?.statusMessage || 'Failed to get response from Codex GPT'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-messages::-webkit-scrollbar {
  width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
