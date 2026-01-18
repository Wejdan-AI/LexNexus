import { Vercel } from '@vercel/sdk';

const vercel = new Vercel({
  bearerToken: process.env.VERCEL_TOKEN,
});

async function addAndReviewDomain() {
  const domain = 'www.example.com';

  try {
    // Add a new domain
    const addDomainResponse = await vercel.projects.addProjectDomain({
      idOrName: 'my-project', //The project name used in the deployment URL
      requestBody: {
        name: domain,
      },
    });

    console.log(`Domain added: ${addDomainResponse.name}`);
    console.log('Domain Details:', JSON.stringify(addDomainResponse, null, 2));
  } catch (error) {
    console.error(
      error instanceof Error ? `Error: ${error.message}` : String(error),
    );
  }
}

addAndReviewDomain();
