<template>
  <div class="chat-container" dir="rtl">
    <!-- Header -->
    <header class="chat-header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">🤖</span>
          <span class="logo-text">WejdanAI</span>
        </div>
        <div class="model-badge">Qwen3</div>
      </div>
    </header>

    <!-- Chat Messages -->
    <main class="chat-messages" ref="messagesContainer">
      <div v-if="messages.length === 0" class="welcome-message">
        <div class="welcome-icon">✨</div>
        <h2>مرحباً بك في WejdanAI</h2>
        <p>مدعوم بنموذج Qwen3 من Alibaba Cloud</p>
        <div class="quick-actions">
          <button
            v-for="suggestion in suggestions"
            :key="suggestion"
            @click="sendSuggestion(suggestion)"
            class="suggestion-btn"
          >
            {{ suggestion }}
          </button>
        </div>
      </div>

      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.role]"
      >
        <div class="message-avatar">
          {{ message.role === 'user' ? '👤' : '🤖' }}
        </div>
        <div class="message-content">
          <div class="message-text" v-html="formatMessage(message.content)"></div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
        </div>
      </div>

      <div v-if="isLoading" class="message assistant">
        <div class="message-avatar">🤖</div>
        <div class="message-content">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </main>

    <!-- Input Area -->
    <footer class="chat-input-area">
      <div class="input-container">
        <textarea
          v-model="userInput"
          @keydown="handleKeydown"
          placeholder="اكتب رسالتك هنا..."
          rows="1"
          ref="inputField"
          :disabled="isLoading"
        ></textarea>
        <button
          @click="sendMessage"
          :disabled="!userInput.trim() || isLoading"
          class="send-btn"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M3.478 2.404a.75.75 0 0 0-.926.941l2.432 7.905H13.5a.75.75 0 0 1 0 1.5H4.984l-2.432 7.905a.75.75 0 0 0 .926.94 60.519 60.519 0 0 0 18.445-8.986.75.75 0 0 0 0-1.218A60.517 60.517 0 0 0 3.478 2.404Z" />
          </svg>
        </button>
      </div>
    </footer>

    <!-- Settings Modal -->
    <div v-if="showSettings" class="settings-modal" @click.self="showSettings = false">
      <div class="settings-content">
        <h3>الإعدادات</h3>
        <div class="setting-item">
          <label>مفتاح DashScope API</label>
          <input
            type="password"
            v-model="apiKey"
            placeholder="أدخل مفتاح API الخاص بك"
          />
        </div>
        <div class="setting-item">
          <label>النموذج</label>
          <select v-model="selectedModel">
            <option value="qwen-max">Qwen Max (الأقوى)</option>
            <option value="qwen-plus">Qwen Plus (متوازن)</option>
            <option value="qwen-turbo">Qwen Turbo (الأسرع)</option>
          </select>
        </div>
        <div class="settings-actions">
          <button @click="saveSettings" class="save-btn">حفظ</button>
          <button @click="showSettings = false" class="cancel-btn">إلغاء</button>
        </div>
      </div>
    </div>

    <!-- Settings Button -->
    <button @click="showSettings = true" class="settings-fab">
      ⚙️
    </button>

    <!-- Error Toast -->
    <div v-if="errorMessage" class="error-toast">
      {{ errorMessage }}
      <button @click="errorMessage = ''" class="close-toast">×</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'

// State
const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const showSettings = ref(false)
const apiKey = ref('')
const selectedModel = ref('qwen-max')
const errorMessage = ref('')
const messagesContainer = ref(null)
const inputField = ref(null)

// Suggestions
const suggestions = [
  'ما هي الذكاء الاصطناعي؟',
  'اكتب قصة قصيرة',
  'ساعدني في حل مشكلة برمجية',
  'ترجم نص إلى الإنجليزية'
]

// Load settings from localStorage
onMounted(() => {
  if (typeof window !== 'undefined') {
    const savedKey = localStorage.getItem('dashscope_api_key')
    const savedModel = localStorage.getItem('qwen_model')
    const savedMessages = localStorage.getItem('chat_messages')

    if (savedKey) apiKey.value = savedKey
    if (savedModel) selectedModel.value = savedModel
    if (savedMessages) {
      try {
        messages.value = JSON.parse(savedMessages)
      } catch (e) {
        console.error('Failed to parse saved messages')
      }
    }
  }
})

// Save messages to localStorage
watch(messages, (newMessages) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('chat_messages', JSON.stringify(newMessages))
  }
}, { deep: true })

// Save settings
const saveSettings = () => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('dashscope_api_key', apiKey.value)
    localStorage.setItem('qwen_model', selectedModel.value)
  }
  showSettings.value = false
}

// Format message with basic markdown
const formatMessage = (text) => {
  if (!text) return ''
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>')
}

// Format timestamp
const formatTime = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleTimeString('ar-SA', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Auto-scroll to bottom
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Handle keyboard events
const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

// Send suggestion
const sendSuggestion = (suggestion) => {
  userInput.value = suggestion
  sendMessage()
}

// Send message
const sendMessage = async () => {
  const text = userInput.value.trim()
  if (!text || isLoading.value) return

  if (!apiKey.value) {
    showSettings.value = true
    errorMessage.value = 'يرجى إدخال مفتاح API أولاً'
    setTimeout(() => errorMessage.value = '', 3000)
    return
  }

  // Add user message
  messages.value.push({
    role: 'user',
    content: text,
    timestamp: new Date().toISOString()
  })

  userInput.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    const response = await fetch('/api/qwen', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        apiKey: apiKey.value,
        model: selectedModel.value,
        messages: messages.value.map(m => ({
          role: m.role,
          content: m.content
        }))
      })
    })

    const data = await response.json()

    if (data.error) {
      throw new Error(data.error)
    }

    // Add assistant message
    messages.value.push({
      role: 'assistant',
      content: data.content,
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('Error:', error)
    errorMessage.value = error.message || 'حدث خطأ في الاتصال'
    setTimeout(() => errorMessage.value = '', 5000)
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

// Page meta
useHead({
  title: 'WejdanAI - Qwen Chat',
  meta: [
    { name: 'description', content: 'Chat with Qwen3 AI on your iPhone' },
    { name: 'apple-mobile-web-app-capable', content: 'yes' },
    { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' },
    { name: 'apple-mobile-web-app-title', content: 'WejdanAI' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover' },
    { name: 'theme-color', content: '#1e3a5f' }
  ],
  link: [
    { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' }
  ]
})
</script>

<style scoped>
/* Base styles */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  height: 100dvh;
  background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #fff;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

/* Header */
.chat-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 16px 20px;
  padding-top: calc(env(safe-area-inset-top, 20px) + 16px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #60a5fa, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.model-badge {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

/* Messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  padding-bottom: 100px;
  -webkit-overflow-scrolling: touch;
}

.welcome-message {
  text-align: center;
  padding: 40px 20px;
}

.welcome-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.welcome-message h2 {
  font-size: 24px;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #60a5fa, #34d399);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.welcome-message p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 30px;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.suggestion-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 10px 16px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.suggestion-btn:hover,
.suggestion-btn:active {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.02);
}

/* Message bubbles */
.message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.message-content {
  max-width: 80%;
}

.message-text {
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.5;
  font-size: 15px;
  word-wrap: break-word;
}

.message.user .message-text {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 18px 4px 18px 18px;
}

.message.assistant .message-text {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 4px 18px 18px 18px;
}

.message-text code {
  background: rgba(0, 0, 0, 0.3);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'SF Mono', Monaco, monospace;
  font-size: 13px;
}

.message-time {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 4px;
  padding: 0 4px;
}

.message.user .message-time {
  text-align: left;
}

/* Typing indicator */
.typing-indicator {
  display: flex;
  gap: 6px;
  padding: 16px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Input area */
.chat-input-area {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(13, 27, 42, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 16px;
  padding-bottom: calc(env(safe-area-inset-bottom, 16px) + 16px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: flex-end;
  max-width: 800px;
  margin: 0 auto;
}

.input-container textarea {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  padding: 14px 20px;
  color: #fff;
  font-size: 16px;
  resize: none;
  outline: none;
  font-family: inherit;
  max-height: 120px;
  direction: rtl;
}

.input-container textarea::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.input-container textarea:focus {
  border-color: #3b82f6;
  background: rgba(255, 255, 255, 0.15);
}

.send-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.send-btn:not(:disabled):hover,
.send-btn:not(:disabled):active {
  transform: scale(1.05);
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
}

.send-btn svg {
  width: 22px;
  height: 22px;
  transform: rotate(180deg);
}

/* Settings */
.settings-fab {
  position: fixed;
  top: calc(env(safe-area-inset-top, 20px) + 70px);
  left: 16px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s;
  z-index: 100;
}

.settings-fab:hover,
.settings-fab:active {
  background: rgba(255, 255, 255, 0.25);
  transform: rotate(90deg);
}

.settings-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.settings-content {
  background: linear-gradient(135deg, #1e3a5f, #0d1b2a);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 24px;
  width: 100%;
  max-width: 400px;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.settings-content h3 {
  font-size: 20px;
  margin-bottom: 20px;
  text-align: center;
}

.setting-item {
  margin-bottom: 16px;
}

.setting-item label {
  display: block;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
}

.setting-item input,
.setting-item select {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 12px 16px;
  color: #fff;
  font-size: 16px;
  outline: none;
  direction: ltr;
}

.setting-item input:focus,
.setting-item select:focus {
  border-color: #3b82f6;
}

.setting-item select option {
  background: #1e3a5f;
  color: #fff;
}

.settings-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.save-btn,
.cancel-btn {
  flex: 1;
  padding: 12px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.save-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #fff;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.save-btn:hover,
.cancel-btn:hover {
  transform: scale(1.02);
}

/* Error toast */
.error-toast {
  position: fixed;
  bottom: calc(env(safe-area-inset-bottom, 16px) + 100px);
  left: 50%;
  transform: translateX(-50%);
  background: #ef4444;
  color: #fff;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  animation: slideUp 0.3s ease;
  z-index: 1000;
  max-width: calc(100% - 40px);
}

.close-toast {
  background: none;
  border: none;
  color: #fff;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

/* Scrollbar */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}
</style>
