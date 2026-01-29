// تهيئة قاعدة البيانات وبيانات تجريبية
import { sql } from './database/schema'
import crypto from 'crypto'

async function hashPassword(password: string): Promise<string> {
  return crypto.createHash('sha256').update(password).digest('hex')
}

async function checkMigrationApplied(name: string): Promise<boolean> {
  try {
    const result = await sql`
      SELECT 1 FROM migrations_applied WHERE name = ${name} LIMIT 1
    `
    return result.length > 0
  } catch (error) {
    // Table doesn't exist yet
    return false
  }
}

async function markMigrationApplied(name: string): Promise<void> {
  // Ensure migrations table exists
  await sql`
    CREATE TABLE IF NOT EXISTS migrations_applied (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) UNIQUE NOT NULL,
      applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
  `

  // Mark as applied
  await sql`
    INSERT INTO migrations_applied (name)
    VALUES (${name})
    ON CONFLICT (name) DO NOTHING
  `
}

export default defineEventHandler(async () => {
  const startTime = Date.now()

  try {
    const migrationName = '000_init_wejdanai'

    // Check if already applied
    const alreadyApplied = await checkMigrationApplied(migrationName)

    if (alreadyApplied) {
      // Already initialized, just return current data
      const users = await sql`SELECT id FROM users WHERE email = 'demo@wejdanai.com' LIMIT 1`

      if (users.length > 0) {
        const userId = users[0].id
        const accounts = await sql`SELECT * FROM accounts WHERE user_id = ${userId}`

        return {
          success: true,
          message: '✅ البنك جاهز بالفعل',
          alreadyInitialized: true,
          duration: Date.now() - startTime,
          data: {
            user: {
              id: userId,
              email: 'demo@wejdanai.com',
              password: 'demo123',
            },
            accounts: accounts.map((acc: any) => ({
              accountNumber: acc.account_number,
              type: acc.account_type,
              balance: parseFloat(acc.balance),
            })),
          },
        }
      }
    }

    // إنشاء الجداول
    await sql`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(20),
        national_id VARCHAR(50) UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `

    await sql`
      CREATE TABLE IF NOT EXISTS accounts (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        account_number VARCHAR(50) UNIQUE NOT NULL,
        account_type VARCHAR(50) NOT NULL,
        balance DECIMAL(15, 2) DEFAULT 0.00,
        currency VARCHAR(3) DEFAULT 'SAR',
        status VARCHAR(20) DEFAULT 'active',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `

    await sql`
      CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        from_account_id INTEGER REFERENCES accounts(id),
        to_account_id INTEGER REFERENCES accounts(id),
        transaction_type VARCHAR(50) NOT NULL,
        amount DECIMAL(15, 2) NOT NULL,
        currency VARCHAR(3) DEFAULT 'SAR',
        description TEXT,
        status VARCHAR(20) DEFAULT 'completed',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `

    await sql`
      CREATE TABLE IF NOT EXISTS chat_messages (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        message TEXT NOT NULL,
        response TEXT,
        intent VARCHAR(100),
        metadata JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `

    await sql`
      CREATE TABLE IF NOT EXISTS activity_logs (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        action VARCHAR(100) NOT NULL,
        details JSONB,
        ip_address VARCHAR(50),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
    `

    console.log('✅ تم إنشاء الجداول')

    // إضافة بيانات تجريبية
    const passwordHash = await hashPassword('demo123')

    // إضافة مستخدم تجريبي
    const [existingUser] = await sql`
      SELECT id FROM users WHERE email = 'demo@wejdanai.com'
    `

    let userId: number

    if (!existingUser) {
      const [user] = await sql`
        INSERT INTO users (name, email, phone, national_id, password_hash)
        VALUES ('مستخدم تجريبي', 'demo@wejdanai.com', '+966501234567', '1234567890', ${passwordHash})
        ON CONFLICT (email) DO NOTHING
        RETURNING id
      `
      userId = user?.id || 1

      // إضافة حساب بنكي رئيسي
      await sql`
        INSERT INTO accounts (user_id, account_number, account_type, balance)
        VALUES (${userId}, 'SAB1234567890', 'checking', 50000.00)
        ON CONFLICT (account_number) DO NOTHING
      `

      // إضافة حساب توفير
      await sql`
        INSERT INTO accounts (user_id, account_number, account_type, balance)
        VALUES (${userId}, 'SAB0987654321', 'savings', 100000.00)
        ON CONFLICT (account_number) DO NOTHING
      `

      console.log('✅ تم إضافة البيانات التجريبية')
    } else {
      userId = existingUser.id
      console.log('ℹ️ المستخدم موجود مسبقاً')
    }

    // جلب الحسابات
    const accounts = await sql`
      SELECT * FROM accounts WHERE user_id = ${userId}
    `

    // Mark migration as applied
    await markMigrationApplied(migrationName)

    const duration = Date.now() - startTime

    return {
      success: true,
      message: '✅ تم تهيئة البنك بنجاح',
      duration,
      data: {
        user: {
          id: userId,
          email: 'demo@wejdanai.com',
          password: 'demo123',
        },
        accounts: accounts.map((acc) => ({
          accountNumber: acc.account_number,
          type: acc.account_type,
          balance: parseFloat(acc.balance),
        })),
      },
    }
  } catch (error: any) {
    console.error('خطأ في التهيئة:', error)
    return {
      success: false,
      error: error.message,
    }
  }
})
