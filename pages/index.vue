<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-blue-900">
    <!-- الهيدر -->
    <header class="bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3 rtl:space-x-reverse">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                بنك وجدان الذكي
              </h1>
              <p class="text-sm text-gray-600 dark:text-gray-400">مساعدك المالي الشخصي</p>
            </div>
          </div>

          <div v-if="accountInfo" class="hidden md:flex items-center space-x-4 rtl:space-x-reverse">
            <div class="text-right rtl:text-left">
              <p class="text-sm text-gray-600 dark:text-gray-400">رصيدك الحالي</p>
              <p class="text-2xl font-bold text-green-600">{{ formatCurrency(accountInfo.balance) }}</p>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- المحتوى الرئيسي -->
    <main class="container mx-auto px-4 py-8 max-w-6xl">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- بطاقات الحسابات -->
        <div class="lg:col-span-1 space-y-4">
          <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6">
            <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">حساباتك</h2>

            <div v-if="!initialized" class="text-center py-8">
              <button
                @click="initializeBank"
                :disabled="isInitializing"
                class="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="!isInitializing">بدء استخدام البنك</span>
                <span v-else class="flex items-center justify-center space-x-2 rtl:space-x-reverse">
                  <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>جاري التهيئة...</span>
                </span>
              </button>

              <!-- رسائل النجاح والخطأ -->
              <div v-if="successMessage" class="mt-4 p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700 rounded-lg">
                <p class="text-green-800 dark:text-green-200 text-sm">{{ successMessage }}</p>
              </div>

              <div v-if="errorMessage" class="mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg">
                <p class="text-red-800 dark:text-red-200 text-sm">{{ errorMessage }}</p>
                <button
                  @click="errorMessage = ''"
                  class="mt-2 text-xs text-red-600 dark:text-red-400 hover:underline"
                >
                  إخفاء
                </button>
              </div>
            </div>

            <div v-else class="space-y-3">
              <div v-for="account in accounts" :key="account.accountNumber"
                   class="bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl p-4 text-white">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <p class="text-sm opacity-80">{{ getAccountTypeName(account.type) }}</p>
                    <p class="text-lg font-bold">{{ account.accountNumber }}</p>
                  </div>
                  <div class="text-right">
                    <p class="text-2xl font-bold">{{ formatCurrency(account.balance) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- إرشادات سريعة -->
          <div class="bg-blue-50 dark:bg-blue-900/20 rounded-2xl p-6">
            <h3 class="font-bold text-blue-900 dark:text-blue-100 mb-3">💡 جرب هذه الأوامر:</h3>
            <ul class="space-y-2 text-sm text-blue-800 dark:text-blue-200">
              <li>• "ما هو رصيدي؟"</li>
              <li>• "حول 1000 ريال إلى 1234567890"</li>
              <li>• "أظهر آخر معاملاتي"</li>
              <li>• "افتح حساب توفير جديد"</li>
            </ul>
          </div>
        </div>

        <!-- واجهة الدردشة -->
        <div class="lg:col-span-2">
          <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col h-[600px]">
            <!-- منطقة الرسائل -->
            <div ref="messagesContainer" class="flex-1 overflow-y-auto p-6 space-y-4">
              <!-- رسالة الترحيب -->
              <div v-if="messages.length === 0" class="text-center py-12">
                <div class="w-20 h-20 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">مرحباً بك! 👋</h3>
                <p class="text-gray-600 dark:text-gray-400 max-w-md mx-auto">
                  أنا مساعدك الذكي في بنك وجدان. يمكنني مساعدتك في إدارة حساباتك وإجراء المعاملات المالية.
                </p>
              </div>

              <!-- الرسائل -->
              <div v-for="(msg, index) in messages" :key="index">
                <!-- رسالة المستخدم -->
                <div class="flex justify-end mb-4">
                  <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 max-w-md">
                    <p class="whitespace-pre-wrap">{{ msg.message }}</p>
                  </div>
                </div>

                <!-- رد المساعد -->
                <div v-if="msg.response" class="flex justify-start mb-4">
                  <div class="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-2xl rounded-tl-sm px-4 py-3 max-w-md">
                    <p class="whitespace-pre-wrap">{{ msg.response }}</p>
                  </div>
                </div>
              </div>

              <!-- مؤشر الكتابة -->
              <div v-if="isTyping" class="flex justify-start">
                <div class="bg-gray-100 dark:bg-gray-700 rounded-2xl px-4 py-3">
                  <div class="flex space-x-2">
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- منطقة الإدخال -->
            <div class="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-900">
              <form @submit.prevent="sendMessage" class="flex space-x-3 rtl:space-x-reverse">
                <input
                  v-model="currentMessage"
                  type="text"
                  placeholder="اكتب رسالتك هنا..."
                  class="flex-1 px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  :disabled="isTyping"
                />
                <button
                  type="submit"
                  :disabled="!currentMessage.trim() || isTyping"
                  class="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  إرسال
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'

interface Message {
  message: string
  response?: string
  timestamp: string
}

interface Account {
  accountNumber: string
  type: string
  balance: number
}

const messages = ref<Message[]>([])
const currentMessage = ref('')
const isTyping = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const initialized = ref(false)
const accounts = ref<Account[]>([])
const accountInfo = ref<any>(null)
const errorMessage = ref('')
const successMessage = ref('')
const isInitializing = ref(false)

const initializeBank = async () => {
  isInitializing.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await $fetch('/api/init')

    if (response.success) {
      initialized.value = true
      accounts.value = response.data.accounts

      if (accounts.value.length > 0) {
        accountInfo.value = accounts.value[0]
      }

      successMessage.value = response.alreadyInitialized
        ? 'البنك جاهز ومُهيأ مسبقاً ✓'
        : 'تم تهيئة البنك بنجاح! يمكنك الآن البدء ✓'

      setTimeout(() => {
        successMessage.value = ''
      }, 5000)
    } else {
      errorMessage.value = response.error || 'حدث خطأ أثناء التهيئة'
    }
  } catch (error: any) {
    console.error('خطأ في التهيئة:', error)

    if (error.data?.error) {
      errorMessage.value = error.data.error
    } else if (error.message?.includes('fetch')) {
      errorMessage.value = 'تعذر الاتصال بالخادم. تحقق من اتصال الإنترنت'
    } else if (error.message?.includes('Database')) {
      errorMessage.value = 'خطأ في قاعدة البيانات. تحقق من إعدادات POSTGRES_URL'
    } else {
      errorMessage.value = 'حدث خطأ غير متوقع. حاول مرة أخرى'
    }
  } finally {
    isInitializing.value = false
  }
}

const sendMessage = async () => {
  if (!currentMessage.value.trim()) return

  const userMessage = currentMessage.value
  messages.value.push({
    message: userMessage,
    timestamp: new Date().toISOString(),
  })

  currentMessage.value = ''
  isTyping.value = true
  scrollToBottom()

  try {
    const response = await $fetch('/api/chat', {
      method: 'POST',
      body: {
        message: userMessage,
        userId: 1,
      },
    })

    if (response.response) {
      messages.value[messages.value.length - 1].response = response.response

      // تحديث معلومات الحساب
      if (response.intent === 'check_balance' || response.intent === 'transfer') {
        const initData = await $fetch('/api/init')
        if (initData.success) {
          accounts.value = initData.data.accounts
          accountInfo.value = accounts.value[0]
        }
      }
    }
  } catch (error) {
    console.error('خطأ في الإرسال:', error)
    messages.value[messages.value.length - 1].response = 'عذراً، حدث خطأ. يرجى المحاولة مرة أخرى.'
  } finally {
    isTyping.value = false
    scrollToBottom()
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatCurrency = (amount: number) => {
  return `${amount.toLocaleString('ar-SA')} ريال`
}

const getAccountTypeName = (type: string) => {
  const types: Record<string, string> = {
    checking: 'حساب جاري',
    savings: 'حساب توفير',
    investment: 'حساب استثماري',
  }
  return types[type] || type
}

onMounted(() => {
  // التحقق من التهيئة
  $fetch('/api/init').then((response) => {
    if (response.success && response.data.accounts.length > 0) {
      initialized.value = true
      accounts.value = response.data.accounts
      accountInfo.value = accounts.value[0]
    }
  })
})
</script>
