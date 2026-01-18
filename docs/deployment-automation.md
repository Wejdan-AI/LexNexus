# Deployment Automation

> Learn how to use the Vercel SDK through real-life examples.

## Prerequisites

Before running these examples, make sure you have:

1. A Vercel account
2. A Vercel API token (create one at https://vercel.com/account/tokens)
3. Set the `VERCEL_TOKEN` environment variable with your token

```bash
export VERCEL_TOKEN=your_token_here
```

## Installation

Install the required dependencies:

```bash
pnpm install
```

## Create a deployment

In this example, you will trigger a new deployment from a GitHub repository and then retrieve its status.

**Example**: `examples/create-deployment.ts`

```typescript
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
```

**Run the example:**

```bash
pnpm run example:create-deployment
```

## Create a deployment with alias

In this example, you will create a deployment, wait for it to complete, and then create an alias if successful.

**Example**: `examples/create-deployment-with-alias.ts`

```typescript
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
```

**Run the example:**

```bash
pnpm run example:deployment-with-alias
```

## Configuration

Before running the examples, you need to update the following values in the example files:

- `name`: Your project name
- `repo`: Your GitHub repository name (e.g., 'my-repo')
- `org`: Your GitHub organization or username
- `alias`: Your desired alias (e.g., 'my-project-alias.vercel.app')

## Additional Resources

- [Vercel API Documentation](https://vercel.com/docs/rest-api)
- [Vercel SDK GitHub Repository](https://github.com/vercel/sdk)
- To find navigation and other pages in this documentation, fetch the llms.txt file at: https://vercel.mintlify.app/docs/rest-api/reference/llms.txt
