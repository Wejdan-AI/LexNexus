// المساعد الذكي للبنك - يفهم العربية ويستجيب للطلبات
export interface BankIntent {
  type: 'check_balance' | 'transfer' | 'inquiry' | 'transaction_history' | 'open_account' | 'general'
  confidence: number
  entities: {
    amount?: number
    toAccount?: string
    accountType?: string
    date?: string
  }
}

export class BankAIAssistant {
  // تحليل نية المستخدم من الرسالة
  analyzeIntent(message: string): BankIntent {
    const lowerMessage = message.toLowerCase()

    // التحقق من الرصيد
    if (
      lowerMessage.includes('رصيد') ||
      lowerMessage.includes('balance') ||
      lowerMessage.includes('كم عندي') ||
      lowerMessage.includes('ما هو رصيدي')
    ) {
      return {
        type: 'check_balance',
        confidence: 0.95,
        entities: {},
      }
    }

    // التحويل المالي
    if (
      lowerMessage.includes('حول') ||
      lowerMessage.includes('transfer') ||
      lowerMessage.includes('أرسل') ||
      lowerMessage.includes('حويل')
    ) {
      const amountMatch = message.match(/(\d+(?:\.\d+)?)\s*(ريال|SAR|رس)?/)
      const accountMatch = message.match(/(?:إلى|الى|to)\s*(\d+)/)

      return {
        type: 'transfer',
        confidence: 0.9,
        entities: {
          amount: amountMatch ? parseFloat(amountMatch[1]) : undefined,
          toAccount: accountMatch ? accountMatch[1] : undefined,
        },
      }
    }

    // سجل المعاملات
    if (
      lowerMessage.includes('معاملات') ||
      lowerMessage.includes('transactions') ||
      lowerMessage.includes('حركات') ||
      lowerMessage.includes('السجل')
    ) {
      return {
        type: 'transaction_history',
        confidence: 0.9,
        entities: {},
      }
    }

    // فتح حساب جديد
    if (
      lowerMessage.includes('فتح حساب') ||
      lowerMessage.includes('open account') ||
      lowerMessage.includes('حساب جديد')
    ) {
      let accountType = 'checking'
      if (lowerMessage.includes('توفير') || lowerMessage.includes('savings')) {
        accountType = 'savings'
      } else if (lowerMessage.includes('استثمار') || lowerMessage.includes('investment')) {
        accountType = 'investment'
      }

      return {
        type: 'open_account',
        confidence: 0.85,
        entities: { accountType },
      }
    }

    // استفسار عام
    return {
      type: 'general',
      confidence: 0.7,
      entities: {},
    }
  }

  // توليد رد ذكي بناءً على النية
  generateResponse(intent: BankIntent, data?: any): string {
    switch (intent.type) {
      case 'check_balance':
        if (data?.balance !== undefined) {
          return `رصيدك الحالي هو ${data.balance.toLocaleString('ar-SA')} ريال سعودي 💰\n\nهل تحتاج إلى أي مساعدة أخرى؟`
        }
        return 'عذراً، لم أتمكن من استرجاع رصيدك. يرجى المحاولة مرة أخرى.'

      case 'transfer':
        if (data?.success) {
          return `✅ تم التحويل بنجاح!\n\nالمبلغ: ${data.amount.toLocaleString('ar-SA')} ريال\nإلى الحساب: ${data.toAccount}\nالرصيد المتبقي: ${data.remainingBalance.toLocaleString('ar-SA')} ريال`
        }
        if (!intent.entities.amount || !intent.entities.toAccount) {
          return 'من فضلك أدخل المبلغ ورقم الحساب المراد التحويل إليه.\nمثال: حول 1000 ريال إلى الحساب 123456'
        }
        return 'عذراً، فشلت عملية التحويل. يرجى التحقق من البيانات.'

      case 'transaction_history':
        if (data?.transactions && data.transactions.length > 0) {
          let response = '📊 آخر معاملاتك:\n\n'
          data.transactions.slice(0, 5).forEach((tx: any, i: number) => {
            response += `${i + 1}. ${tx.type === 'deposit' ? '➕' : '➖'} ${tx.amount.toLocaleString('ar-SA')} ريال - ${tx.description || 'معاملة'}\n`
          })
          return response
        }
        return 'لا توجد معاملات حالياً.'

      case 'open_account':
        if (data?.accountNumber) {
          return `🎉 مبروك! تم فتح حساب جديد\n\nرقم الحساب: ${data.accountNumber}\nنوع الحساب: ${data.accountType === 'savings' ? 'توفير' : data.accountType === 'investment' ? 'استثمار' : 'جاري'}\n\nيمكنك البدء في استخدامه الآن!`
        }
        return 'ما نوع الحساب الذي تريد فتحه؟ (جاري، توفير، استثمار)'

      case 'general':
        return `مرحباً بك في البنك الذكي 🏦

أنا مساعدك الشخصي، يمكنني مساعدتك في:

• التحقق من رصيدك
• تحويل الأموال
• عرض المعاملات الأخيرة
• فتح حساب جديد
• الإجابة على استفساراتك

كيف يمكنني مساعدتك اليوم؟`

      default:
        return 'عذراً، لم أفهم طلبك. هل يمكنك إعادة صياغته؟'
    }
  }
}
