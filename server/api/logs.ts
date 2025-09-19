import { defineEventHandler, readBody } from 'h3'
import postgres from 'postgres'

// Initialize database connection - will fail gracefully if no connection string
let sql: any = null
if (process.env.POSTGRES_URL) {
  sql = postgres(process.env.POSTGRES_URL, { ssl: 'require' })
}

// Function to ensure logs table exists and references the correct user table
async function ensureLogsTable() {
  if (!sql) {
    throw new Error('Database connection not configured')
  }
  
  try {
    await sql`
      CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES profiles(id) ON DELETE SET NULL,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
      );
    `
    console.log('Logs table created or verified')
  } catch (error) {
    console.error('Error creating logs table:', error)
    throw error
  }
}

export default defineEventHandler(async (event) => {
  if (event.node.req.method === 'GET') {
    // Retrieve all logs
    try {
      if (!sql) {
        return { error: 'Database connection not configured' }
      }
      await ensureLogsTable()
      const result = await sql`SELECT * FROM logs ORDER BY created_at DESC`
      return result
    } catch (error) {
      console.error('Error fetching logs:', error)
      return { error: 'Failed to fetch logs' }
    }
  }

  if (event.node.req.method === 'POST') {
    // Add a new log (required fields: query, response; user_id is optional)
    try {
      const body = await readBody(event)
      const { user_id, query, response } = body

      if (!query || !response) {
        return { error: "⚠️ Both 'query' and 'response' are required." }
      }

      if (!sql) {
        return { error: 'Database connection not configured' }
      }

      await ensureLogsTable()
      const result = await sql`
        INSERT INTO logs (user_id, query, response) 
        VALUES (${user_id || null}, ${query}, ${response}) 
        RETURNING *
      `

      return { message: '✅ Log saved successfully', log: result[0] }
    } catch (error) {
      console.error('Error saving log:', error)
      return { error: 'Failed to save log' }
    }
  }

  return { error: 'Method not allowed' }
})