# Domain Management

> Learn how to use the Vercel SDK through real-life examples.

## Add a domain

In this example, you will add a new domain to a project and check its configuration.

```ts run.ts theme={"system"}
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
```

## Add a domain, verify it and setup a redirect

In this example, you will add a custom domain, verify it, and set up a redirect from a subdomain to the main domain.

```ts run.ts theme={"system"}
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
```

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://vercel.mintlify.app/docs/rest-api/reference/llms.txt
