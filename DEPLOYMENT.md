# Deployment Guide

## Vercel Deployment Setup

This project is configured to automatically deploy to Vercel using GitHub Actions.

### Prerequisites

1. A Vercel account
2. A Vercel project created for this repository
3. Vercel API token with deployment permissions

### Setting Up GitHub Secrets

To enable automated deployments, you need to add the following secrets to your GitHub repository:

1. **VERCEL_TOKEN**: Your Vercel API token
   - Get this from: https://vercel.com/account/tokens
   - The token format looks like: `ver_xxxxxxxxxxxxxxxxxxxxxxxx`

2. **VERCEL_ORG_ID**: Your Vercel organization ID
   - Find this in your Vercel project settings under "Project Settings" → "General"
   - Or run: `vercel project ls` after linking your project
   - You can also get it by running `vercel link` and checking `.vercel/project.json`

3. **VERCEL_PROJECT_ID**: Your Vercel project ID
   - Find this in your Vercel project settings under "Project Settings" → "General"
   - Or run: `vercel project ls` after linking your project
   - You can also get it by running `vercel link` and checking `.vercel/project.json`

### Adding Secrets to GitHub

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each of the three secrets listed above

### How It Works

The deployment workflow (`.github/workflows/vercel-deployment.yml`) will:

- **On Pull Requests**: Deploy a preview environment
- **On Push to Main**: Deploy to production

### Manual Deployment

You can also deploy manually using the Vercel CLI:

```bash
# Install Vercel CLI
pnpm install -g vercel

# Link your project (first time only)
vercel link --token YOUR_VERCEL_TOKEN

# Deploy to preview
vercel --token YOUR_VERCEL_TOKEN

# Deploy to production
vercel --prod --token YOUR_VERCEL_TOKEN
```

### Getting Your Project IDs

To get your `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID`:

```bash
# Link your project first
vercel link --token YOUR_VERCEL_TOKEN

# Check the generated .vercel/project.json file
cat .vercel/project.json
```

The file will contain both IDs in JSON format:
```json
{
  "orgId": "your-org-id",
  "projectId": "your-project-id"
}
```

### Project Configuration

The project uses the following Vercel configuration (see `vercel.json`):

- Build command: `pnpm turbo build`
- Ignore command: `pnpm dlx turbo-ignore`

This ensures efficient builds using Turborepo's caching system.
