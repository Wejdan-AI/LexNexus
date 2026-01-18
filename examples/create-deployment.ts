import { Vercel } from '@vercel/sdk';

const vercel = new Vercel({
  bearerToken: process.env.VERCEL_TOKEN,
});

async function createAndCheckDeployment() {
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

    console.log(
      `Deployment created: ID ${createResponse.id} and status ${createResponse.status}`,
    );
  } catch (error) {
    console.error(
      error instanceof Error ? `Error: ${error.message}` : String(error),
    );
  }
}

createAndCheckDeployment();
