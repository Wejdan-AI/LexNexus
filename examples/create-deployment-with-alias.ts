import { Vercel } from '@vercel/sdk';

const vercel = new Vercel({
  bearerToken: process.env.VERCEL_TOKEN,
});

async function createDeploymentAndAlias() {
  try {
    // Create a new deployment
    const createResponse = await vercel.deployments.createDeployment({
      requestBody: {
        name: 'my-project', //The project name used in the deployment URL
        target: 'production',
        gitSource: {
          type: 'github',
          repo: 'repo-name',
          ref: 'main',
          org: 'org-name', //For a personal account, the org-name is your GH username
        },
      },
    });

    const deploymentId = createResponse.id;

    console.log(
      `Deployment created: ID ${deploymentId} and status ${createResponse.status}`,
    );

    // Check deployment status
    let deploymentStatus;
    let deploymentURL;
    do {
      await new Promise((resolve) => setTimeout(resolve, 5000)); // Wait 5 seconds between checks

      const statusResponse = await vercel.deployments.getDeployment({
        idOrUrl: deploymentId,
        withGitRepoInfo: 'true',
      });

      deploymentStatus = statusResponse.status;
      deploymentURL = statusResponse.url;
      console.log(`Deployment status: ${deploymentStatus}`);
    } while (
      deploymentStatus === 'BUILDING' ||
      deploymentStatus === 'INITIALIZING'
    );

    if (deploymentStatus === 'READY') {
      console.log(`Deployment successful. URL: ${deploymentURL}`);

      const aliasResponse = await vercel.aliases.assignAlias({
        id: deploymentId,
        requestBody: {
          alias: `my-project-alias.vercel.app`,
          redirect: null,
        },
      });

      console.log(`Alias created: ${aliasResponse.alias}`);
    } else {
      console.log('Deployment failed or was canceled');
    }
  } catch (error) {
    console.error(
      error instanceof Error ? `Error: ${error.message}` : String(error),
    );
  }
}

createDeploymentAndAlias();
