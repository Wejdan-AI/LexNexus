import postgres from 'postgres'

const sql = postgres(process.env.POSTGRES_URL!, { ssl: 'require' })

async function seed() {
  const createTable = await sql`
    CREATE TABLE IF NOT EXISTS clauses (
      id SERIAL PRIMARY KEY,
      title VARCHAR(255) NOT NULL UNIQUE,
      content TEXT NOT NULL,
      category VARCHAR(100),
      "createdAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    `

  console.log(`Created "clauses" table`)

  const clauses = await Promise.all([
    sql`
          INSERT INTO clauses (title, content, category)
          VALUES ('Confidentiality Clause', 'The parties agree to maintain confidentiality of all proprietary information shared during the term of this agreement.', 'Contract Law')
          ON CONFLICT (title) DO NOTHING;
      `,
    sql`
          INSERT INTO clauses (title, content, category)
          VALUES ('Liability Limitation', 'Neither party shall be liable for any indirect, incidental, or consequential damages arising from this agreement.', 'Contract Law')
          ON CONFLICT (title) DO NOTHING;
      `,
    sql`
          INSERT INTO clauses (title, content, category)
          VALUES ('Termination Notice', 'Either party may terminate this agreement with 30 days written notice to the other party.', 'Employment Law')
          ON CONFLICT (title) DO NOTHING;
      `,
  ])
  console.log(`Seeded ${clauses.length} clauses`)

  return {
    createTable,
    clauses,
  }
}
export default defineEventHandler(async () => {
  const startTime = Date.now()
  try {
    const clauses = await sql`SELECT * FROM clauses`
    const duration = Date.now() - startTime
    return {
      clauses,
      duration: duration,
    }
  } catch (error) {
    if (
      error instanceof Error &&
      error?.message === `relation "clauses" does not exist`
    ) {
      console.log(
        'Table does not exist, creating and seeding it with dummy data now...'
      )
      // Table is not created yet
      await seed()
      const clauses = await sql`SELECT * FROM clauses`
      const duration = Date.now() - startTime
      return {
        clauses,
        duration: duration,
      }
    } else {
      throw error
    }
  }
})
