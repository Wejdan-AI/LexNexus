# Vercel Deployment Automation Examples

This directory contains examples demonstrating how to use the Vercel SDK for deployment automation.

## Examples

### 1. Create Deployment (`create-deployment.ts`)

A simple example that creates a new deployment from a GitHub repository.

```bash
pnpm run example:create-deployment
```

### 2. Create Deployment with Alias (`create-deployment-with-alias.ts`)

An advanced example that:
- Creates a deployment
- Monitors its status
- Assigns an alias when the deployment is ready

```bash
pnpm run example:deployment-with-alias
```

## Setup

1. **Set your Vercel API token:**

   ```bash
   export VERCEL_TOKEN=your_vercel_token_here
   ```

   Get your token from: https://vercel.com/account/tokens

2. **Configure the examples:**

   Edit the example files and update:
   - `name`: Your project name
   - `repo`: Your GitHub repository name
   - `org`: Your GitHub organization or username
   - `alias`: Your desired alias (only in the alias example)

3. **Install dependencies:**

   ```bash
   pnpm install
   ```

4. **Run an example:**

   ```bash
   pnpm run example:create-deployment
   # or
   pnpm run example:deployment-with-alias
   ```

## Documentation

For more detailed information, see the [Deployment Automation Documentation](../docs/deployment-automation.md).

## Additional Resources

- [Vercel API Documentation](https://vercel.com/docs/rest-api)
- [Vercel SDK GitHub Repository](https://github.com/vercel/sdk)
