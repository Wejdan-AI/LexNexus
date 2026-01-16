<template>
  <div class="taskade-manager bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
    <h2 class="text-2xl font-bold mb-4 text-gray-800 dark:text-white">
      Taskade Task Manager
    </h2>

    <div class="workspace-selector mb-4">
      <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
        Workspace ID:
      </label>
      <input
        v-model="workspaceId"
        type="text"
        placeholder="Enter your Taskade workspace ID"
        class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
      />
    </div>

    <div class="task-creator mb-6">
      <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
        New Task:
      </label>
      <div class="flex gap-2">
        <input
          v-model="newTaskContent"
          @keydown.enter="createTask"
          type="text"
          placeholder="Enter task content..."
          class="flex-1 p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
          :disabled="loading || !workspaceId"
        />
        <button
          @click="createTask"
          :disabled="loading || !newTaskContent.trim() || !workspaceId"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          Add Task
        </button>
      </div>
    </div>

    <div class="tasks-list">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-lg font-semibold text-gray-800 dark:text-white">
          Tasks
        </h3>
        <button
          @click="loadTasks"
          :disabled="loading || !workspaceId"
          class="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          Refresh
        </button>
      </div>

      <div v-if="loading" class="text-center py-8 text-gray-500 dark:text-gray-400">
        <span class="inline-block animate-pulse">Loading...</span>
      </div>

      <div v-else-if="tasks.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
        No tasks found. Create your first task above!
      </div>

      <div v-else class="space-y-2">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="p-3 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <div class="text-gray-800 dark:text-white">{{ task.content }}</div>
          <div v-if="task.notes" class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ task.notes }}
          </div>
        </div>
      </div>
    </div>

    <div v-if="error" class="mt-4 p-3 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded-lg">
      {{ error }}
    </div>

    <div v-if="success" class="mt-4 p-3 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-200 rounded-lg">
      {{ success }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const workspaceId = ref('')
const newTaskContent = ref('')
const tasks = ref([])
const loading = ref(false)
const error = ref('')
const success = ref('')

const createTask = async () => {
  if (!newTaskContent.value.trim() || !workspaceId.value || loading.value) return

  loading.value = true
  error.value = ''
  success.value = ''

  try {
    const response = await $fetch('/api/taskade', {
      method: 'POST',
      body: {
        action: 'createTask',
        data: {
          workspaceId: workspaceId.value,
          content: newTaskContent.value
        }
      }
    })

    success.value = 'Task created successfully!'
    newTaskContent.value = ''
    
    // Refresh tasks list
    await loadTasks()
    
    setTimeout(() => {
      success.value = ''
    }, 3000)
  } catch (err) {
    error.value = err.data?.statusMessage || 'Failed to create task'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

const loadTasks = async () => {
  if (!workspaceId.value || loading.value) return

  loading.value = true
  error.value = ''

  try {
    const response = await $fetch('/api/taskade', {
      method: 'POST',
      body: {
        action: 'getTasks',
        data: {
          workspaceId: workspaceId.value
        }
      }
    })

    tasks.value = response.data || []
  } catch (err) {
    error.value = err.data?.statusMessage || 'Failed to load tasks'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}
</script>
