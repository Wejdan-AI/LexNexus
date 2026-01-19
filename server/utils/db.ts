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
    
    // Parse numeric config with validation
    const maxConnections = Number(process.env.POSTGRES_MAX_CONNECTIONS) || 10
    const idleTimeout = Number(process.env.POSTGRES_IDLE_TIMEOUT) || 30
    
    sqlInstance = postgres(connectionString, {
      ssl: sslConfig,
      max: maxConnections,
      idle_timeout: idleTimeout,
    })
  }
  
  return sqlInstance
}

// Export the sql instance for convenience
// This will be lazily initialized on first access
export const sql = new Proxy({} as ReturnType<typeof postgres>, {
  get(target, prop) {
    const db = getDatabase()
    return (db as any)[prop]
  },
})
