<template>
  <div class="min-h-screen py-10">
    <div class="container mx-auto">
      <h1 class="mb-8 text-3xl font-bold text-center">
        Deployment Claim Example
      </h1>

      <!-- Example 1: Basic Usage -->
      <ClaimDeployment
        url="my-deployment.vercel.app"
        @claim="handleClaim"
        @claimed="handleClaimed"
        @error="handleError"
      />

      <!-- Example 2: With Custom Props -->
      <div class="mt-8">
        <ClaimDeployment
          url="custom-deployment.vercel.app"
          deployment-name="my-custom-deployment"
          project-id="prj_abc123xyz"
          title="Take Ownership"
          description="This deployment was created for you. Claim it to manage it in your Vercel dashboard."
          button-text="Transfer to My Account"
          :show-cancel-button="true"
          :show-info="true"
          @claim="handleClaim"
          @claimed="handleClaimed"
          @cancel="handleCancel"
          @error="handleError"
        />
      </div>

      <!-- Status Display -->
      <div v-if="statusMessage" class="mt-8">
        <div
          class="p-4 mx-auto max-w-2xl rounded-lg"
          :class="statusClass"
        >
          {{ statusMessage }}
        </div>
      </div>
    </div>
  </div>
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
    async handleClaim(data) {
      console.log('Claim initiated:', data);
      this.statusMessage = 'Processing claim request...';
      this.statusClass = 'bg-blue-100 text-blue-800';

      // Here you would make the actual API call to transfer ownership
      // For example:
      // try {
      //   const response = await fetch('/api/claim-deployment', {
      //     method: 'POST',
      //     body: JSON.stringify(data),
      //   });
      //   if (!response.ok) throw new Error('Claim failed');
      // } catch (error) {
      //   console.error('Claim error:', error);
      // }
    },
    handleClaimed(data) {
      console.log('Deployment claimed:', data);
      this.statusMessage = `Successfully claimed deployment: ${data.url}`;
      this.statusClass = 'bg-green-100 text-green-800';

      // Optionally redirect user to their Vercel dashboard
      // setTimeout(() => {
      //   window.location.href = `https://vercel.com/dashboard`;
      // }, 2000);
    },
    handleCancel() {
      console.log('Claim cancelled');
      this.statusMessage = 'Claim cancelled';
      this.statusClass = 'bg-gray-100 text-gray-800';
    },
    handleError(error) {
      console.error('Error:', error);
      this.statusMessage = `Error: ${error.message}`;
      this.statusClass = 'bg-red-100 text-red-800';
    },
  },
};
</script>
