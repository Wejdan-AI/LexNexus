<template>
  <div
    class="w-full max-w-2xl p-8 mx-auto rounded-lg shadow-xl bg-white/30 dark:bg-white/10 ring-1 ring-gray-900/5 backdrop-blur-lg"
  >
    <div class="space-y-6">
      <!-- Header -->
      <div class="space-y-2">
        <h2 class="text-2xl font-semibold">
          {{ title || 'Claim Your Deployment' }}
        </h2>
        <p class="text-sm text-gray-600 dark:text-gray-400">
          {{ description || 'Your deployment is ready. Click below to take ownership and manage it in your Vercel account.' }}
        </p>
      </div>

      <!-- Deployment Info -->
      <div
        class="p-4 space-y-3 rounded-lg bg-white/50 dark:bg-white/5 ring-1 ring-gray-900/5"
      >
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
            Deployment URL
          </span>
          <a
            :href="`https://${url}`"
            target="_blank"
            rel="noopener noreferrer"
            class="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 underline"
          >
            {{ url }}
          </a>
        </div>

        <div
          v-if="deploymentName"
          class="flex items-center justify-between"
        >
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
            Deployment Name
          </span>
          <span class="text-sm text-gray-600 dark:text-gray-400">
            {{ deploymentName }}
          </span>
        </div>

        <div v-if="projectId" class="flex items-center justify-between">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300">
            Project ID
          </span>
          <span
            class="text-sm font-mono text-gray-600 dark:text-gray-400"
          >
            {{ projectId }}
          </span>
        </div>
      </div>

      <!-- Status Message -->
      <div
        v-if="statusMessage"
        :class="[
          'p-4 rounded-lg text-sm',
          statusType === 'success'
            ? 'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-200'
            : statusType === 'error'
            ? 'bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-200'
            : 'bg-blue-50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200',
        ]"
      >
        {{ statusMessage }}
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center justify-end space-x-4">
        <button
          v-if="showCancelButton"
          @click="handleCancel"
          :disabled="loading"
          class="px-6 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 transition-all rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>

        <button
          @click="handleClaimClick"
          :disabled="loading || claimed"
          class="px-6 py-2 text-sm font-medium text-white transition-all rounded-lg shadow-sm bg-black dark:bg-white dark:text-black hover:shadow-lg active:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading">Claiming...</span>
          <span v-else-if="claimed">Claimed</span>
          <span v-else>{{ buttonText || 'Claim Deployment' }}</span>
        </button>
      </div>

      <!-- Additional Info -->
      <div
        v-if="showInfo"
        class="pt-4 text-xs text-gray-500 dark:text-gray-400 border-t border-gray-200 dark:border-gray-700"
      >
        <p>
          After claiming, this deployment will be transferred to your Vercel
          account. You'll have full control over its settings, domains, and
          deployments.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    /**
     * The deployment URL (without https://)
     */
    url: {
      type: String,
      required: true,
    },
    /**
     * Optional deployment name
     */
    deploymentName: {
      type: String,
      default: null,
    },
    /**
     * Optional project ID
     */
    projectId: {
      type: String,
      default: null,
    },
    /**
     * Custom title for the component
     */
    title: {
      type: String,
      default: null,
    },
    /**
     * Custom description text
     */
    description: {
      type: String,
      default: null,
    },
    /**
     * Custom button text
     */
    buttonText: {
      type: String,
      default: null,
    },
    /**
     * Whether to show the cancel button
     */
    showCancelButton: {
      type: Boolean,
      default: false,
    },
    /**
     * Whether to show additional information
     */
    showInfo: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      loading: false,
      claimed: false,
      statusMessage: '',
      statusType: '', // 'success', 'error', or 'info'
    };
  },
  methods: {
    async handleClaimClick() {
      if (this.loading || this.claimed) return;

      this.loading = true;
      this.statusMessage = 'Processing claim request...';
      this.statusType = 'info';

      try {
        // Emit event to parent component to handle the actual claim logic
        this.$emit('claim', {
          url: this.url,
          deploymentName: this.deploymentName,
          projectId: this.projectId,
        });

        // Simulate claim process (parent should handle actual API calls)
        await new Promise((resolve) => setTimeout(resolve, 1000));

        this.claimed = true;
        this.statusMessage = 'Deployment claimed successfully!';
        this.statusType = 'success';

        this.$emit('claimed', {
          url: this.url,
          deploymentName: this.deploymentName,
          projectId: this.projectId,
        });
      } catch (error) {
        this.statusMessage = `Failed to claim deployment: ${error.message}`;
        this.statusType = 'error';

        this.$emit('error', error);
      } finally {
        this.loading = false;
      }
    },
    handleCancel() {
      this.$emit('cancel');
    },
  },
};
</script>
