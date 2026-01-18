<template>
  <div class="flex h-screen flex-col bg-slate-950">
    <!-- Header -->
    <header class="safe-top flex items-center justify-between border-b border-white/10 bg-slate-900/80 px-4 py-3 backdrop-blur-lg">
      <div class="flex items-center gap-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-violet-500 to-indigo-600">
          <span class="text-lg font-bold text-white">و</span>
        </div>
        <div>
          <h1 class="text-lg font-semibold text-white">WejdanAI</h1>
          <p class="text-xs text-slate-400">{{ currentModel.name }}</p>
        </div>
      </div>
      <button
        @click="showModelPicker = true"
        class="rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-sm text-slate-300 active:bg-white/10"
      >
        تغيير النموذج
      </button>
    </header>

    <!-- Messages -->
    <div
      ref="messagesContainer"
      class="flex-1 overflow-y-auto px-4 py-6"
    >
      <!-- Welcome -->
      <div v-if="messages.length === 0" class="flex h-full flex-col items-center justify-center text-center">
        <div class="mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500 to-indigo-600">
          <span class="text-3xl font-bold text-white">و</span>
        </div>
        <h2 class="mb-2 text-xl font-semibold text-white">مرحباً بك في WejdanAI</h2>
        <p class="mb-8 max-w-sm text-sm text-slate-400">
          نظام ذكي يوجه طلباتك تلقائياً للنموذج الأنسب
        </p>

        <!-- Quick Actions -->
        <div class="grid w-full max-w-sm gap-3">
          <button
            v-for="action in quickActions"
            :key="action.text"
            @click="sendMessage(action.prompt)"
            class="flex items-center gap-3 rounded-xl border border-white/10 bg-slate-900/60 p-4 text-right active:bg-slate-800"
          >
            <span class="text-2xl">{{ action.icon }}</span>
            <span class="flex-1 text-sm text-slate-300">{{ action.text }}</span>
          </button>
        </div>
      </div>

      <!-- Chat Messages -->
      <div v-else class="mx-auto max-w-2xl space-y-4">
        <div
          v-for="(msg, i) in messages"
          :key="i"
          :class="[
            'rounded-2xl px-4 py-3',
            msg.role === 'user'
              ? 'mr-0 ml-auto max-w-[85%] bg-violet-600 text-white'
              : 'ml-0 mr-auto max-w-[90%] border border-white/10 bg-slate-900/80 text-slate-100'
          ]"
        >
          <!-- Model Badge -->
          <div v-if="msg.role === 'assistant' && msg.model" class="mb-2 flex items-center gap-2">
            <span class="rounded-full bg-white/10 px-2 py-0.5 text-xs text-slate-400">
              {{ msg.model }}
            </span>
          </div>

          <!-- Message Content -->
          <div class="whitespace-pre-wrap text-sm leading-relaxed" dir="auto">
            {{ msg.content }}
          </div>
        </div>

        <!-- Loading -->
        <div v-if="isLoading" class="ml-0 mr-auto max-w-[90%] rounded-2xl border border-white/10 bg-slate-900/80 px-4 py-3">
          <div class="flex items-center gap-2">
            <div class="h-2 w-2 animate-bounce rounded-full bg-violet-500"></div>
            <div class="h-2 w-2 animate-bounce rounded-full bg-violet-500" style="animation-delay: 0.1s"></div>
            <div class="h-2 w-2 animate-bounce rounded-full bg-violet-500" style="animation-delay: 0.2s"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="safe-bottom border-t border-white/10 bg-slate-900/80 px-4 py-3 backdrop-blur-lg">
      <div class="mx-auto flex max-w-2xl gap-3">
        <input
          v-model="inputText"
          @keydown.enter="sendMessage()"
          type="text"
          dir="auto"
          placeholder="اكتب رسالتك..."
          class="flex-1 rounded-xl border border-white/10 bg-slate-800 px-4 py-3 text-sm text-white placeholder-slate-500 outline-none focus:border-violet-500"
          :disabled="isLoading"
        />
        <button
          @click="sendMessage()"
          :disabled="isLoading || !inputText.trim()"
          class="flex h-12 w-12 items-center justify-center rounded-xl bg-violet-600 text-white disabled:opacity-50"
        >
          <svg class="h-5 w-5 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Model Picker Modal -->
    <Teleport to="body">
      <div
        v-if="showModelPicker"
        class="fixed inset-0 z-50 flex items-end justify-center bg-black/60 backdrop-blur-sm"
        @click.self="showModelPicker = false"
      >
        <div class="safe-bottom w-full max-w-lg rounded-t-3xl bg-slate-900 p-6">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="text-lg font-semibold text-white">اختر النموذج</h3>
            <button @click="showModelPicker = false" class="text-slate-400">✕</button>
          </div>

          <div class="space-y-2">
            <button
              v-for="model in models"
              :key="model.id"
              @click="selectModel(model)"
              :class="[
                'flex w-full items-center gap-3 rounded-xl border p-4 text-right',
                currentModel.id === model.id
                  ? 'border-violet-500 bg-violet-500/10'
                  : 'border-white/10 bg-slate-800/50'
              ]"
            >
              <span class="text-2xl">{{ model.icon }}</span>
              <div class="flex-1">
                <p class="font-medium text-white">{{ model.name }}</p>
                <p class="text-xs text-slate-400">{{ model.desc }}</p>
              </div>
              <span v-if="model.free" class="rounded-full bg-emerald-500/20 px-2 py-0.5 text-xs text-emerald-400">
                مجاني
              </span>
            </button>
          </div>

          <button
            @click="currentModel = { id: 'auto', name: 'تلقائي', icon: '🤖' }; showModelPicker = false"
            class="mt-4 w-full rounded-xl bg-violet-600 py-3 text-center font-medium text-white"
          >
            توجيه تلقائي (موصى به)
          </button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const inputText = ref('')
const messages = ref([])
const isLoading = ref(false)
const showModelPicker = ref(false)
const messagesContainer = ref(null)

const currentModel = ref({ id: 'auto', name: 'توجيه تلقائي', icon: '🤖' })

const models = [
  { id: 'auto', name: 'توجيه تلقائي', icon: '🤖', desc: 'يختار النموذج الأنسب تلقائياً', free: true },
  { id: 'deepseek', name: 'DeepSeek', icon: '💻', desc: 'للبرمجة والكود', free: true },
  { id: 'qwen', name: 'Qwen', icon: '🌍', desc: 'للعربية والصينية', free: true },
  { id: 'gemini', name: 'Gemini', icon: '✨', desc: 'للصور والوسائط', free: true },
  { id: 'venice', name: 'Venice', icon: '🔒', desc: 'للخصوصية', free: true },
  { id: 'perplexity', name: 'Perplexity', icon: '🔍', desc: 'للبحث والمصادر', free: false },
  { id: 'chatgpt', name: 'ChatGPT', icon: '💬', desc: 'للإبداع والكتابة', free: false },
  { id: 'claude', name: 'Claude', icon: '🧠', desc: 'للتحليل المعقد', free: false },
]

const quickActions = [
  { icon: '💻', text: 'اكتب لي كود Python', prompt: 'اكتب لي دالة Python لترتيب قائمة' },
  { icon: '🌍', text: 'ترجم نص للإنجليزية', prompt: 'ترجم هذا النص للإنجليزية: مرحباً بك' },
  { icon: '🔍', text: 'ابحث عن معلومات', prompt: 'ما هي آخر أخبار الذكاء الاصطناعي؟' },
  { icon: '✍️', text: 'اكتب لي قصة قصيرة', prompt: 'اكتب لي قصة قصيرة عن الفضاء' },
]

const selectModel = (model) => {
  currentModel.value = model
  showModelPicker.value = false
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async (text = null) => {
  const messageText = text || inputText.value.trim()
  if (!messageText || isLoading.value) return

  // Add user message
  messages.value.push({ role: 'user', content: messageText })
  inputText.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    // Determine model
    const forceModel = currentModel.value.id !== 'auto' ? currentModel.value.id : null

    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: messageText,
        force_model: forceModel,
        use_rag: true,
      }),
    })

    if (!response.ok) throw new Error('API Error')

    const data = await response.json()

    messages.value.push({
      role: 'assistant',
      content: data.answer,
      model: data.model_name,
    })
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: 'عذراً، حدث خطأ. تأكد من تشغيل الخادم.',
      model: 'خطأ',
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.safe-top {
  padding-top: max(0.75rem, env(safe-area-inset-top));
}
.safe-bottom {
  padding-bottom: max(0.75rem, env(safe-area-inset-bottom));
}
</style>
