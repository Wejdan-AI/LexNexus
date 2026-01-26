# Vercel Platform Actions

Server-side utilities and components for programmatically deploying files to Vercel and managing deployments on behalf of users.

## Overview

The Vercel Platform Actions provide the core functionality behind platforms like Mintlify and Hashnode that create Vercel deployments for their users without requiring direct Vercel account access.

## Features

- **Programmatic Deployment**: Deploy files directly to Vercel using the SDK
- **Custom Domain Support**: Automatically configure custom domains for deployments
- **Project Configuration**: Pass custom build settings and environment variables
- **SSO Protection Handling**: Optionally make preview deployments public
- **Unique Deployment Naming**: Automatic UUID generation for deployment identification
- **Claim Deployment UI**: Ready-to-use component for ownership transfer

## Installation

### Install Dependencies

```bash
pnpm add @vercel/sdk
```

### Environment Variables

Set your Vercel API token in your environment:

```bash
VERCEL_TOKEN=your_vercel_api_token
# or
VERCEL_API_TOKEN=your_vercel_api_token
```

You can obtain an API token from [Vercel Dashboard](https://vercel.com/account/tokens).

## Usage

### Deploy Files Action

The `deployFiles` action allows you to programmatically deploy files to Vercel.

#### Basic Example

```typescript
import { deployFiles } from '@/server/actions/deploy-files';
import type { InlinedFile } from '@vercel/sdk/models/createdeploymentop';

const files: InlinedFile[] = [
  {
    file: 'index.html',
    data: '<html><body><h1>Hello from my platform!</h1></body></html>',
  },
  {
    file: 'package.json',
    data: JSON.stringify({
      name: 'my-deployment',
      version: '1.0.0',
    }),
  },
];

const deployment = await deployFiles(files, {
  domain: 'customer-site.com',
});

console.log(`Deployed to: ${deployment.url}`);
```

#### Advanced Example with Configuration

```typescript
import { deployFiles } from '@/server/actions/deploy-files';
import type { InlinedFile, ProjectSettings } from '@vercel/sdk/models/createdeploymentop';

const files: InlinedFile[] = [
  // Your application files
];

const config: ProjectSettings = {
  framework: 'nextjs',
  buildCommand: 'npm run build',
  outputDirectory: '.next',
  installCommand: 'npm install',
  devCommand: 'npm run dev',
  env: {
    API_KEY: 'your-api-key',
    DATABASE_URL: 'your-database-url',
  },
  buildEnv: {
    NODE_ENV: 'production',
  },
};

const deployment = await deployFiles(files, {
  deploymentName: `deployment-${Date.now()}`,
  config,
  domain: 'app.customer-domain.com',
});
```

#### Parameters

##### `files`

Array of files to deploy. Can be either:

- **InlinedFile**: File content provided directly as a string
- **UploadedFile**: File content uploaded separately and referenced by SHA

##### `args`

Configuration object with the following options:

| Property | Type | Description |
|----------|------|-------------|
| `projectId` | `string` (optional) | Existing project ID to deploy to. If not provided, a new project is created. |
| `deploymentName` | `string` (optional) | Custom deployment name. If not provided, a UUID is generated. |
| `config` | `ProjectSettings` (optional) | Project configuration including framework, build settings, and environment variables. |
| `domain` | `string` (optional) | Custom domain to add to the deployment. |

### Add Domain Action

The `addDomain` action allows you to add a custom domain to an existing Vercel project.

#### Example

```typescript
import { addDomain } from '@/server/actions/add-domain';

const domainInfo = await addDomain({
  projectId: 'prj_abc123xyz',
  domain: 'custom-domain.com',
});

console.log(`Domain verified: ${domainInfo.verified}`);
```

#### Parameters

| Property | Type | Description |
|----------|------|-------------|
| `projectId` | `string` (required) | The project ID or name to add the domain to. |
| `domain` | `string` (required) | The custom domain to add (e.g., "example.com"). |
| `redirect` | `string` (optional) | Redirect configuration. |
| `gitBranch` | `string` (optional) | Git branch for this domain. |

### Claim Deployment Component

The `ClaimDeployment` component provides a user interface for claiming ownership of deployments.

#### Basic Usage

```vue
<template>
  <ClaimDeployment
    url="my-deployment.vercel.app"
    @claim="handleClaim"
    @claimed="handleClaimed"
  />
</template>

<script>
export default {
  methods: {
    handleClaim(data) {
      console.log('Claim initiated:', data);
      // Make API call to transfer ownership
    },
    handleClaimed(data) {
      console.log('Deployment claimed:', data);
      // Handle successful claim
    },
  },
};
</script>
```

#### Props

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `url` | `string` (required) | - | The deployment URL (without https://). |
| `deploymentName` | `string` | `null` | Optional deployment name to display. |
| `projectId` | `string` | `null` | Optional project ID to display. |
| `title` | `string` | `'Claim Your Deployment'` | Custom title for the component. |
| `description` | `string` | Default message | Custom description text. |
| `buttonText` | `string` | `'Claim Deployment'` | Custom button text. |
| `showCancelButton` | `boolean` | `false` | Whether to show a cancel button. |
| `showInfo` | `boolean` | `true` | Whether to show additional information. |

#### Events

| Event | Payload | Description |
|-------|---------|-------------|
| `claim` | `{ url, deploymentName, projectId }` | Emitted when user clicks claim button. |
| `claimed` | `{ url, deploymentName, projectId }` | Emitted after successful claim. |
| `cancel` | - | Emitted when user clicks cancel. |
| `error` | `Error` | Emitted when an error occurs. |

## Integration Example

Here's a complete example showing how to deploy files and show the claim interface:

```typescript
// Server-side: Deploy files
import { deployFiles } from '@/server/actions/deploy-files';

export default defineEventHandler(async (event) => {
  const files = [
    {
      file: 'index.html',
      data: '<html><body><h1>Hello!</h1></body></html>',
    },
  ];

  const deployment = await deployFiles(files, {
    domain: 'user-site.com',
  });

  return deployment;
});
```

```vue
<!-- Client-side: Show claim interface -->
<template>
  <div>
    <ClaimDeployment
      :url="deployment.url"
      :deployment-name="deployment.deploymentName"
      :project-id="deployment.projectId"
      @claim="handleTransferOwnership"
    />
  </div>
</template>

<script setup>
const { data: deployment } = await useFetch('/api/create-deployment');

async function handleTransferOwnership(data) {
  // Call your API to transfer deployment ownership to the user
  await $fetch('/api/transfer-ownership', {
    method: 'POST',
    body: data,
  });
}
</script>
```

## Security Considerations

- This action requires Vercel API credentials with deployment permissions
- Always validate and sanitize file contents before deployment
- Consider implementing rate limiting to prevent abuse
- Store API credentials securely using environment variables
- Never expose your Vercel API token in client-side code

## Error Handling

All actions throw errors that should be caught and handled appropriately:

```typescript
try {
  const deployment = await deployFiles(files, { domain: 'example.com' });
} catch (error) {
  console.error('Deployment failed:', error.message);
  // Handle error appropriately
}
```

## File Structure

```
server/
└── actions/
    ├── deploy-files.ts      # Main deployment action
    └── add-domain.ts        # Domain management action

components/
└── ClaimDeployment.vue      # Claim deployment UI component

examples/
├── deploy-files-example.ts  # Usage examples for deployFiles
└── claim-deployment-example.vue  # Usage examples for ClaimDeployment
```

## License

MIT

## Related Actions

- **Deploy Files** - Deploy files programmatically to Vercel
- **Add Custom Domain** - Add custom domains to Vercel projects
- **Claim Deployment** - UI component for ownership transfer
