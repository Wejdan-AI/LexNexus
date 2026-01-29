// معمارية قاعدة البيانات - نظام البنك المصغر الذكي
import postgres from 'postgres'

const sql = postgres(process.env.POSTGRES_URL!, { ssl: 'require' })

export async function initDatabase() {
  // جدول المستخدمين
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

  // جدول الحسابات البنكية
  await sql`
    CREATE TABLE IF NOT EXISTS accounts (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
      account_number VARCHAR(50) UNIQUE NOT NULL,
      account_type VARCHAR(50) NOT NULL, -- savings, checking, investment
      balance DECIMAL(15, 2) DEFAULT 0.00,
      currency VARCHAR(3) DEFAULT 'SAR',
      status VARCHAR(20) DEFAULT 'active', -- active, frozen, closed
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
  `

  // جدول المعاملات المالية
  await sql`
    CREATE TABLE IF NOT EXISTS transactions (
      id SERIAL PRIMARY KEY,
      from_account_id INTEGER REFERENCES accounts(id),
      to_account_id INTEGER REFERENCES accounts(id),
      transaction_type VARCHAR(50) NOT NULL, -- transfer, deposit, withdraw, payment
      amount DECIMAL(15, 2) NOT NULL,
      currency VARCHAR(3) DEFAULT 'SAR',
      description TEXT,
      status VARCHAR(20) DEFAULT 'completed', -- pending, completed, failed, cancelled
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
  `

  // جدول رسائل الدردشة مع AI
  await sql`
    CREATE TABLE IF NOT EXISTS chat_messages (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
      message TEXT NOT NULL,
      response TEXT,
      intent VARCHAR(100), -- check_balance, transfer, inquiry, complaint
      metadata JSONB, -- بيانات إضافية مثل المبالغ والحسابات
      created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
  `

  // جدول سجل الأنشطة (للأمان والمراقبة)
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

  console.log('✅ تم إنشاء قاعدة البيانات بنجاح')
}

export { sql }
