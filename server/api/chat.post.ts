/**
 * WejdanAI Chat API
 * Handles chat requests and routes to appropriate AI model
 */

interface ChatRequest {
  message: string
  force_model?: string | null
  use_rag?: boolean
  prefer_cost?: boolean
  prefer_privacy?: boolean
}

interface ChatResponse {
  answer: string
  model_used: string
  model_name: string
  confidence: number
  reasoning: string
}

// Model configurations
const MODELS: Record<string, { name: string; keywords: string[] }> = {
  deepseek: {
    name: 'DeepSeek Coder',
    keywords: ['code', 'function', 'python', 'javascript', 'debug', 'program', 'كود', 'برمجة', 'دالة'],
  },
  qwen: {
    name: 'Qwen 2.5',
    keywords: ['ترجم', 'عربي', 'translate', '翻译', '中文'],
  },
  perplexity: {
    name: 'Perplexity Sonar',
    keywords: ['search', 'news', 'research', 'latest', 'أخبار', 'بحث', 'ابحث'],
  },
  gemini: {
    name: 'Gemini Pro',
    keywords: ['image', 'photo', 'صورة', 'analyze image'],
  },
  venice: {
    name: 'Venice AI',
    keywords: ['private', 'confidential', 'secret', 'خاص', 'سري'],
  },
  chatgpt: {
    name: 'ChatGPT',
    keywords: ['creative', 'story', 'write', 'brainstorm', 'قصة', 'اكتب', 'إبداع'],
  },
  claude: {
    name: 'Claude',
    keywords: ['analyze', 'complex', 'document', 'تحليل', 'معقد'],
  },
  manus: {
    name: 'Manus AI',
    keywords: ['automate', 'workflow', 'multi-step', 'أتمتة'],
  },
}

// Detect language
function detectLanguage(text: string): string {
  const arabicChars = (text.match(/[\u0600-\u06FF]/g) || []).length
  const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length
  const totalChars = text.replace(/\s/g, '').length || 1

  if (arabicChars / totalChars > 0.3) return 'arabic'
  if (chineseChars / totalChars > 0.3) return 'chinese'
  return 'english'
}

// Route to best model
function routeMessage(message: string): { model: string; confidence: number; reasoning: string } {
  const messageLower = message.toLowerCase()
  const language = detectLanguage(message)

  // Language-based routing
  if (language === 'arabic' || language === 'chinese') {
    return {
      model: 'qwen',
      confidence: 0.85,
      reasoning: `${language} language detected → Qwen`,
    }
  }

  // Keyword-based routing
  for (const [modelId, config] of Object.entries(MODELS)) {
    for (const keyword of config.keywords) {
      if (messageLower.includes(keyword.toLowerCase())) {
        return {
          model: modelId,
          confidence: 0.75,
          reasoning: `Keyword "${keyword}" detected → ${config.name}`,
        }
      }
    }
  }

  // Default to Claude for general queries
  return {
    model: 'claude',
    confidence: 0.5,
    reasoning: 'No specific task detected → Claude (default)',
  }
}

// Demo responses (without actual API calls)
function getDemoResponse(message: string, model: string): string {
  const language = detectLanguage(message)
  const isArabic = language === 'arabic'

  const responses: Record<string, string> = {
    deepseek: isArabic
      ? '```python\ndef example():\n    # هذا مثال على كود\n    return "مرحباً"\n```\n\nهذا مثال على كود Python. لتفعيل الردود الحقيقية، أضف مفتاح DEEPSEEK_API_KEY.'
      : '```python\ndef example():\n    return "Hello"\n```\n\nThis is a code example. To enable real responses, add your DEEPSEEK_API_KEY.',

    qwen: isArabic
      ? 'مرحباً! أنا Qwen، متخصص في اللغة العربية والصينية. لتفعيل الردود الحقيقية، أضف مفتاح QWEN_API_KEY.'
      : 'Hello! I am Qwen, specialized in Arabic and Chinese. To enable real responses, add your QWEN_API_KEY.',

    perplexity: isArabic
      ? '🔍 هذا سؤال بحثي. لتفعيل البحث الحقيقي مع المصادر، أضف مفتاح PERPLEXITY_API_KEY.'
      : '🔍 This is a research query. To enable real search with citations, add your PERPLEXITY_API_KEY.',

    gemini: isArabic
      ? '✨ أنا Gemini، متخصص في تحليل الصور. لتفعيل الردود الحقيقية، أضف مفتاح GOOGLE_API_KEY.'
      : '✨ I am Gemini, specialized in image analysis. To enable real responses, add your GOOGLE_API_KEY.',

    venice: isArabic
      ? '🔒 رسالتك خاصة وآمنة. لتفعيل الردود الحقيقية، أضف مفتاح VENICE_API_KEY.'
      : '🔒 Your message is private and secure. To enable real responses, add your VENICE_API_KEY.',

    chatgpt: isArabic
      ? '✍️ أنا ChatGPT، متخصص في الكتابة الإبداعية. لتفعيل الردود الحقيقية، أضف مفتاح OPENAI_API_KEY.'
      : '✍️ I am ChatGPT, specialized in creative writing. To enable real responses, add your OPENAI_API_KEY.',

    claude: isArabic
      ? '🧠 أنا Claude، متخصص في التحليل المعقد. لتفعيل الردود الحقيقية، أضف مفتاح ANTHROPIC_API_KEY.'
      : '🧠 I am Claude, specialized in complex analysis. To enable real responses, add your ANTHROPIC_API_KEY.',

    manus: isArabic
      ? '🤖 أنا Manus، متخصص في الأتمتة. لتفعيل الردود الحقيقية، أضف مفتاح MANUS_API_KEY.'
      : '🤖 I am Manus, specialized in automation. To enable real responses, add your MANUS_API_KEY.',
  }

  return responses[model] || responses.claude
}

export default defineEventHandler(async (event) => {
  const body = await readBody<ChatRequest>(event)

  if (!body.message) {
    throw createError({
      statusCode: 400,
      message: 'Message is required',
    })
  }

  // Route to best model (or use forced model)
  let routingResult = routeMessage(body.message)

  if (body.force_model && MODELS[body.force_model]) {
    routingResult = {
      model: body.force_model,
      confidence: 1.0,
      reasoning: `Model forced to ${MODELS[body.force_model].name}`,
    }
  }

  const modelConfig = MODELS[routingResult.model] || MODELS.claude

  // Get demo response (replace with real API calls when keys are available)
  const answer = getDemoResponse(body.message, routingResult.model)

  return {
    answer,
    model_used: routingResult.model,
    model_name: modelConfig.name,
    confidence: routingResult.confidence,
    reasoning: routingResult.reasoning,
  } as ChatResponse
})
