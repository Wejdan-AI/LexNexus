// نقطة الدخول للدردشة مع المساعد الذكي
import { BankAIAssistant } from './ai/assistant'
import { sql } from './database/schema'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { message, userId = 1 } = body // استخدام userId من الجلسة

  if (!message) {
    return { error: 'الرجاء إدخال رسالة' }
  }

  try {
    const assistant = new BankAIAssistant()
    const intent = assistant.analyzeIntent(message)

    let responseData: any = {}
    let response = ''

    // تنفيذ الإجراء بناءً على النية
    switch (intent.type) {
      case 'check_balance':
        // جلب رصيد المستخدم
        const accounts = await sql`
          SELECT * FROM accounts WHERE user_id = ${userId} AND status = 'active' LIMIT 1
        `
        if (accounts.length > 0) {
          responseData = { balance: parseFloat(accounts[0].balance) }
        }
        break

      case 'transfer':
        if (intent.entities.amount && intent.entities.toAccount) {
          // تنفيذ التحويل
          const [fromAccount] = await sql`
            SELECT * FROM accounts WHERE user_id = ${userId} AND status = 'active' LIMIT 1
          `

          const [toAccount] = await sql`
            SELECT * FROM accounts WHERE account_number = ${intent.entities.toAccount} LIMIT 1
          `

          if (fromAccount && toAccount && parseFloat(fromAccount.balance) >= intent.entities.amount) {
            // تنفيذ التحويل
            await sql.begin(async (sql) => {
              // خصم من الحساب المرسل
              await sql`
                UPDATE accounts
                SET balance = balance - ${intent.entities.amount}
                WHERE id = ${fromAccount.id}
              `

              // إضافة للحساب المستقبل
              await sql`
                UPDATE accounts
                SET balance = balance + ${intent.entities.amount}
                WHERE id = ${toAccount.id}
              `

              // تسجيل المعاملة
              await sql`
                INSERT INTO transactions (from_account_id, to_account_id, transaction_type, amount, description)
                VALUES (${fromAccount.id}, ${toAccount.id}, 'transfer', ${intent.entities.amount}, ${message})
              `
            })

            const newBalance = parseFloat(fromAccount.balance) - intent.entities.amount
            responseData = {
              success: true,
              amount: intent.entities.amount,
              toAccount: intent.entities.toAccount,
              remainingBalance: newBalance,
            }
          } else {
            responseData = { success: false }
          }
        }
        break

      case 'transaction_history':
        // جلب آخر المعاملات
        const [account] = await sql`
          SELECT id FROM accounts WHERE user_id = ${userId} LIMIT 1
        `
        if (account) {
          const transactions = await sql`
            SELECT
              t.*,
              CASE
                WHEN t.from_account_id = ${account.id} THEN 'withdraw'
                ELSE 'deposit'
              END as type
            FROM transactions t
            WHERE t.from_account_id = ${account.id} OR t.to_account_id = ${account.id}
            ORDER BY t.created_at DESC
            LIMIT 10
          `
          responseData = { transactions }
        }
        break

      case 'open_account':
        // فتح حساب جديد
        const accountNumber = `SAB${Date.now().toString().slice(-10)}`
        const [newAccount] = await sql`
          INSERT INTO accounts (user_id, account_number, account_type, balance)
          VALUES (${userId}, ${accountNumber}, ${intent.entities.accountType || 'checking'}, 0)
          RETURNING *
        `
        responseData = {
          accountNumber: newAccount.account_number,
          accountType: newAccount.account_type,
        }
        break
    }

    // توليد الرد
    response = assistant.generateResponse(intent, responseData)

    // حفظ المحادثة
    await sql`
      INSERT INTO chat_messages (user_id, message, response, intent, metadata)
      VALUES (${userId}, ${message}, ${response}, ${intent.type}, ${JSON.stringify(intent.entities)})
    `

    return {
      message,
      response,
      intent: intent.type,
      timestamp: new Date().toISOString(),
    }
  } catch (error) {
    console.error('خطأ في معالجة الرسالة:', error)
    return {
      error: 'حدث خطأ في معالجة طلبك. يرجى المحاولة مرة أخرى.',
    }
  }
})
