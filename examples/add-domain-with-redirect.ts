import { Vercel } from '@vercel/sdk';

const vercel = new Vercel({
  bearerToken: process.env.VERCEL_TOKEN,
});

async function setupDomainWithRedirect() {
  const mainDomain = 'example.com';
  const subDomain = 'hello.example.com';
  const projectName = 'my-project'; //The project name used in the deployment URL

  try {
    // Add main domain
    const mainDomainResponse = await vercel.projects.addProjectDomain({
      idOrName: projectName,
      requestBody: {
        name: mainDomain,
      },
    });

    console.log(`Main domain added: ${mainDomainResponse.name}`);

    const checkConfiguration = await vercel.domains.getDomainConfig({
      domain: mainDomain,
    });

    if (mainDomainResponse.verified && !checkConfiguration.misconfigured) {
      // Add subdomain with 301 redirect to main domain
      const subDomainResponse = await vercel.projects.addProjectDomain({
        idOrName: projectName,
        requestBody: {
          name: subDomain,
          redirect: `https://${mainDomain}`,
          redirectStatusCode: 301,
        },
      });

      console.log(`Subdomain added and redirect set up: ${subDomain}`);
    }
  } catch (error) {
    console.error(
      error instanceof Error ? `Error: ${error.message}` : String(error),
    );
  }
}

setupDomainWithRedirect();
