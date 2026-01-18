# Examples

This directory contains executable TypeScript examples demonstrating various features and integrations.

## Domain Management Examples

These examples demonstrate how to use the Vercel SDK to manage domains for your projects.

### Prerequisites

Before running these examples, you need:

1. Install the Vercel SDK dependency:
   ```bash
   pnpm add @vercel/sdk
   ```

2. Set your Vercel API token:
   ```bash
   export VERCEL_TOKEN=your_token_here
   ```

### Available Examples

- **add-domain.ts** - Add a new domain to a project and check its configuration
- **add-domain-with-redirect.ts** - Add a custom domain, verify it, and set up a redirect from a subdomain to the main domain

### Running Examples

You can run any example using:

```bash
npx tsx examples/add-domain.ts
```

Or with ts-node:

```bash
npx ts-node examples/add-domain.ts
```

### Documentation

For detailed documentation, see [docs/domain-management.md](../docs/domain-management.md).
