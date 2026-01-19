/**
 * Add Custom Domain Action
 * 
 * Server action for programmatically adding a custom domain to a Vercel project.
 */

import { Vercel } from '@vercel/sdk';

export interface AddDomainArgs {
  /**
   * The project ID or name to add the domain to
   */
  projectId: string;
  
  /**
   * The custom domain to add (e.g., "example.com" or "subdomain.example.com")
   */
  domain: string;
  
  /**
   * Optional: Redirect configuration
   */
  redirect?: string;
  
  /**
   * Optional: Git branch for this domain
   */
  gitBranch?: string;
}

/**
 * Add a custom domain to a Vercel project
 * 
 * @param args - Configuration options for adding the domain
 * @returns Domain information including verification details
 */
export async function addDomain(args: AddDomainArgs) {
  const { projectId, domain, redirect, gitBranch } = args;
  
  // Initialize Vercel SDK with API token from environment
  const vercelToken = process.env.VERCEL_TOKEN || process.env.VERCEL_API_TOKEN;
  
  if (!vercelToken) {
    throw new Error(
      'VERCEL_TOKEN or VERCEL_API_TOKEN environment variable is required'
    );
  }
  
  if (!projectId) {
    throw new Error('projectId is required to add a domain');
  }
  
  if (!domain) {
    throw new Error('domain is required');
  }
  
  const vercel = new Vercel({
    bearerToken: vercelToken,
  });
  
  try {
    // Add the domain to the project
    const domainConfig: any = {
      idOrName: projectId,
      domain: domain,
    };
    
    if (redirect) {
      domainConfig.redirect = redirect;
    }
    
    if (gitBranch) {
      domainConfig.gitBranch = gitBranch;
    }
    
    const result = await vercel.projects.addDomain(domainConfig);
    
    return {
      name: result.name,
      apexName: result.apexName,
      projectId: result.projectId,
      verified: result.verified,
      verification: result.verification,
      createdAt: result.createdAt,
      updatedAt: result.updatedAt,
    };
  } catch (error) {
    console.error('Failed to add domain:', error);
    throw new Error(
      `Failed to add domain ${domain} to project ${projectId}: ${
        error instanceof Error ? error.message : 'Unknown error'
      }`
    );
  }
}
