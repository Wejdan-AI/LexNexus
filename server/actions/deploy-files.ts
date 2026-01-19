/**
 * Deploy Files Action
 * 
 * Server action for programmatically deploying files to Vercel.
 * Enables platforms to create deployments on behalf of users.
 */

import { Vercel } from '@vercel/sdk';
import type { 
  InlinedFile, 
  UploadedFile, 
  ProjectSettings 
} from '@vercel/sdk/models/createdeploymentop';

export interface DeployFilesArgs {
  /**
   * Optional project ID to deploy to. If not provided, a new project will be created.
   */
  projectId?: string;
  
  /**
   * Optional deployment name. If not provided, a UUID will be generated.
   */
  deploymentName?: string;
  
  /**
   * Optional project configuration (framework, build settings, env variables, etc.)
   */
  config?: ProjectSettings;
  
  /**
   * Optional custom domain for the deployment
   */
  domain?: string;
}

/**
 * Deploy files to Vercel programmatically
 * 
 * @param files - Array of InlinedFile or UploadedFile objects containing file contents
 * @param args - Configuration options for the deployment
 * @returns Deployment information including URL and project details
 */
export async function deployFiles(
  files: (InlinedFile | UploadedFile)[],
  args: DeployFilesArgs = {}
) {
  // Initialize Vercel SDK with API token from environment
  const vercelToken = process.env.VERCEL_TOKEN || process.env.VERCEL_API_TOKEN;
  
  if (!vercelToken) {
    throw new Error(
      'VERCEL_TOKEN or VERCEL_API_TOKEN environment variable is required for deployments'
    );
  }
  
  const vercel = new Vercel({
    bearerToken: vercelToken,
  });
  
  const { projectId, deploymentName, config, domain } = args;
  
  // Generate a unique deployment name if not provided
  const finalDeploymentName = deploymentName || `deployment-${crypto.randomUUID()}`;
  
  try {
    let targetProjectId = projectId;
    
    // Create a new project if projectId is not provided
    if (!targetProjectId) {
      const projectName = finalDeploymentName.toLowerCase().replace(/[^a-z0-9-]/g, '-');
      
      const createProjectResponse = await vercel.projects.create({
        name: projectName,
        framework: config?.framework || undefined,
        buildCommand: config?.buildCommand || undefined,
        outputDirectory: config?.outputDirectory || undefined,
        installCommand: config?.installCommand || undefined,
        devCommand: config?.devCommand || undefined,
      });
      
      targetProjectId = createProjectResponse.id;
    }
    
    // Prepare deployment configuration
    const deploymentConfig: any = {
      name: finalDeploymentName,
      files: files,
      projectSettings: config || undefined,
      target: 'production',
    };
    
    // Make preview deployments public (bypass SSO protection)
    deploymentConfig.public = true;
    
    // Create the deployment
    const deployment = await vercel.deployments.create(deploymentConfig);
    
    // Add custom domain if provided
    if (domain && targetProjectId) {
      try {
        await vercel.projects.addDomain({
          idOrName: targetProjectId,
          domain: domain,
        });
      } catch (error) {
        console.warn(`Failed to add custom domain ${domain}:`, error);
        // Don't fail the entire deployment if domain addition fails
      }
    }
    
    return {
      id: deployment.id,
      url: deployment.url,
      projectId: targetProjectId,
      deploymentName: finalDeploymentName,
      state: deployment.readyState,
      createdAt: deployment.createdAt,
    };
  } catch (error) {
    console.error('Deployment failed:', error);
    throw new Error(
      `Failed to deploy files: ${error instanceof Error ? error.message : 'Unknown error'}`
    );
  }
}
