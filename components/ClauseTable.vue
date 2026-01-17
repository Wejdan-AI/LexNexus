<template>
  <div
    class="w-full max-w-4xl p-12 mx-auto rounded-lg shadow-xl dark:bg-white/10 bg-white/30 ring-1 ring-gray-900/5 backdrop-blur-lg"
  >
    <div class="flex items-center justify-between mb-4">
      <div class="space-y-1">
        <h2 class="text-xl font-semibold">Legal Clauses</h2>
        <p class="text-sm text-gray-500">
          Fetched {{ clauses?.length }} clauses in {{ duration }}ms
        </p>
      </div>
      <button class="hover:opacity-80" @click="refreshPage">
        Refresh Page
      </button>
    </div>
    <div class="divide-y divide-gray-900/5">
      <div
        v-for="clause in clauses"
        :key="clause.id"
        class="flex flex-col py-4"
      >
        <div class="flex items-center justify-between mb-2">
          <h3 class="font-medium text-lg">{{ clause?.title }}</h3>
          <span class="text-xs px-2 py-1 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-100">
            {{ clause?.category }}
          </span>
        </div>
        <p class="text-sm text-gray-600 dark:text-gray-300 mb-2">
          {{ clause?.content }}
        </p>
        <p class="text-xs text-gray-500">Created {{ timeAgo(clause?.createdAt) }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import ms from 'ms'

export default {
  props: {
    clauses: {
      type: Array,
      required: true,
    },
    duration: {
      type: Number,
      required: true,
    },
  },
  methods: {
    timeAgo(timestamp, timeOnly) {
      if (!timestamp) return 'never'
      return `${ms(Date.now() - new Date(timestamp).getTime())}${
        timeOnly ? '' : ' ago'
      }`
    },
    refreshPage() {
      location.reload()
    },
  },
}
</script>
