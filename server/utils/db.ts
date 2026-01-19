import postgres from 'postgres'

// Parse SSL configuration from environment variable
// Accepts: 'require', 'allow', 'prefer', 'disable', or a boolean
function getSSLConfig() {
  const sslEnv = process.env.POSTGRES_SSL || 'require'
  
  if (sslEnv === 'true' || sslEnv === 'require' || sslEnv === 'prefer') {
    return 'require'
  }
  if (sslEnv === 'false' || sslEnv === 'disable') {
    return false
  }
  if (sslEnv === 'allow') {
    return 'prefer'
  }
  
  return 'require' // Default to require for production safety
}

// Create a singleton database connection
let sqlInstance: ReturnType<typeof postgres> | null = null

export function getDatabase() {
  if (!sqlInstance) {
    const connectionString = process.env.POSTGRES_URL
    
    if (!connectionString) {
      throw new Error('POSTGRES_URL environment variable is not set')
    }
    
    const sslConfig = getSSLConfig()
    
    sqlInstance = postgres(connectionString, {
      ssl: sslConfig,
      max: parseInt(process.env.POSTGRES_MAX_CONNECTIONS || '10'),
      idle_timeout: parseInt(process.env.POSTGRES_IDLE_TIMEOUT || '30'),
    })
  }
  
  return sqlInstance
}

// Export the sql instance for convenience
export const sql = getDatabase()
