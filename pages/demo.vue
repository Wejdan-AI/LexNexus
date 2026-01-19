<template>
  <main
    class="relative flex flex-col items-center justify-center min-h-screen py-10"
  >
    <h1
      class="pt-4 pb-8 bg-gradient-to-br dark:from-white from-black via-[#707070] to-[#ffffff] bg-clip-text text-center text-4xl font-medium tracking-tight text-transparent md:text-7xl"
    >
      Vercel Platform Actions Demo
    </h1>

    <div class="w-full max-w-4xl space-y-8 px-4">
      <!-- Deploy Files Section -->
      <div
        class="w-full p-8 rounded-lg shadow-xl bg-white/30 dark:bg-white/10 ring-1 ring-gray-900/5 backdrop-blur-lg"
      >
        <h2 class="mb-4 text-2xl font-semibold">Deploy Files Action</h2>
        <p class="mb-4 text-sm text-gray-600 dark:text-gray-400">
          Server action for programmatically deploying files to Vercel. This
          enables platforms to create deployments on behalf of users.
        </p>
        <div class="space-y-2">
          <div class="p-4 rounded bg-gray-100 dark:bg-gray-800">
            <code class="text-sm">
              <pre>import { deployFiles } from '@/server/actions/deploy-files';

const files = [
  {
    file: 'index.html',
    data: '&lt;html&gt;&lt;body&gt;&lt;h1&gt;Hello!&lt;/h1&gt;&lt;/body&gt;&lt;/html&gt;'
  }
];

await deployFiles(files, {
  domain: 'test.com',
  deploymentName: 'my-deployment'
});</pre>
            </code>
          </div>
        </div>
      </div>

      <!-- Add Domain Section -->
      <div
        class="w-full p-8 rounded-lg shadow-xl bg-white/30 dark:bg-white/10 ring-1 ring-gray-900/5 backdrop-blur-lg"
      >
        <h2 class="mb-4 text-2xl font-semibold">Add Domain Action</h2>
        <p class="mb-4 text-sm text-gray-600 dark:text-gray-400">
          Server action for programmatically adding a custom domain to a Vercel
          project.
        </p>
        <div class="space-y-2">
          <div class="p-4 rounded bg-gray-100 dark:bg-gray-800">
            <code class="text-sm">
              <pre>import { addDomain } from '@/server/actions/add-domain';

await addDomain({
  projectId: 'prj_abc123',
  domain: 'custom-domain.com'
});</pre>
            </code>
          </div>
        </div>
      </div>

      <!-- Claim Deployment Component Demo -->
      <div>
        <h2 class="mb-4 text-2xl font-semibold text-center">
          Claim Deployment Component
        </h2>
        <ClaimDeployment
          url="example-deployment.vercel.app"
          deployment-name="example-deployment"
          project-id="prj_example123"
          :show-cancel-button="true"
          @claim="handleClaim"
          @claimed="handleClaimed"
          @cancel="handleCancel"
          @error="handleError"
        />
      </div>

      <!-- Status Display -->
      <div
        v-if="statusMessage"
        class="w-full p-4 rounded-lg"
        :class="statusClass"
      >
        {{ statusMessage }}
      </div>

      <!-- Documentation Link -->
      <div class="text-center">
        <a
          href="https://github.com/Wejdan-AI/LexNexus/blob/main/VERCEL_PLATFORM_ACTIONS.md"
          target="_blank"
          class="inline-flex items-center px-6 py-3 text-sm font-medium transition-all rounded-lg shadow-sm bg-black dark:bg-white text-white dark:text-black hover:shadow-lg active:shadow-sm"
        >
          View Full Documentation
        </a>
      </div>
    </div>

    <!-- Back to Home -->
    <div class="mt-8">
      <a
        href="/"
        class="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100"
      >
        ← Back to Home
      </a>
    </div>
  </main>
</template>

<script>
export default {
  data() {
    return {
      statusMessage: '',
      statusClass: '',
    };
  },
  methods: {
    handleClaim(data) {
      console.log('Claim initiated:', data);
      this.statusMessage = `Processing claim for ${data.url}...`;
      this.statusClass =
        'bg-blue-50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200';
    },
    handleClaimed(data) {
      console.log('Deployment claimed:', data);
      this.statusMessage = `✓ Successfully claimed deployment: ${data.url}`;
      this.statusClass =
        'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-200';
    },
    handleCancel() {
      console.log('Claim cancelled');
      this.statusMessage = 'Claim cancelled by user';
      this.statusClass =
        'bg-gray-50 dark:bg-gray-900/20 text-gray-800 dark:text-gray-200';
    },
    handleError(error) {
      console.error('Error:', error);
      this.statusMessage = `✗ Error: ${error.message}`;
      this.statusClass =
        'bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-200';
    },
  },
};
</script>
