/**
 * Example Usage: Deploy Files Action
 * 
 * This file demonstrates how to use the deployFiles action
 * to programmatically deploy files to Vercel.
 */

import { deployFiles } from '@/server/actions/deploy-files';
import type { InlinedFile } from '@vercel/sdk/models/createdeploymentop';

/**
 * Example 1: Deploy a simple HTML site
 */
export async function example1() {
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
    domain: 'test.com',
  });

  return deployment;
}

/**
 * Example 2: Deploy with custom configuration
 */
export async function example2() {
  const files: InlinedFile[] = [
    {
      file: 'index.html',
      data: '<html><body><h1>Hello World!</h1></body></html>',
    },
    {
      file: 'package.json',
      data: JSON.stringify({
        name: 'custom-deployment',
        version: '1.0.0',
      }),
    },
  ];

  const deployment = await deployFiles(files, {
    deploymentName: 'customer-deployment-1',
    domain: 'customer-site.com',
    config: {
      framework: 'nextjs',
      buildCommand: 'npm run build',
      outputDirectory: '.next',
    },
  });

  return deployment;
}

/**
 * Example 3: Deploy to an existing project
 */
export async function example3() {
  const files: InlinedFile[] = [
    {
      file: 'index.html',
      data: '<html><body><h1>Updated Content</h1></body></html>',
    },
  ];

  const deployment = await deployFiles(files, {
    projectId: 'existing-project-id',
    deploymentName: 'update-2024',
  });

  return deployment;
}

/**
 * Example 4: Deploy Next.js application with environment variables
 */
export async function example4() {
  const files: InlinedFile[] = [
    // Your application files here
    {
      file: 'package.json',
      data: JSON.stringify({
        name: 'nextjs-app',
        version: '1.0.0',
        scripts: {
          dev: 'next dev',
          build: 'next build',
          start: 'next start',
        },
      }),
    },
  ];

  const deployment = await deployFiles(files, {
    deploymentName: `deployment-${Date.now()}`,
    config: {
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
    },
    domain: 'app.customer-domain.com',
  });

  return deployment;
}

export default example1;
