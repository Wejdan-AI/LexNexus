import { defineEventHandler, readBody, createError } from 'h3'

interface Message {
  role: 'user' | 'assistant' | 'system'
  content: string
}

interface QwenRequest {
  apiKey: string
  model: string
  messages: Message[]
}

interface QwenResponse {
  output?: {
    choices?: Array<{
      message?: {
        content: string
      }
    }>
    text?: string
  }
  message?: string
  code?: string
}

export default defineEventHandler(async (event) => {
  // Only allow POST requests
  if (event.method !== 'POST') {
    throw createError({
      statusCode: 405,
      statusMessage: 'Method Not Allowed'
    })
  }

  try {
    const body = await readBody<QwenRequest>(event)

    // Validate required fields
    if (!body.apiKey) {
      return {
        error: 'مفتاح API مطلوب. يرجى إدخاله في الإعدادات.'
      }
    }

    if (!body.messages || body.messages.length === 0) {
      return {
        error: 'لا توجد رسائل للإرسال.'
      }
    }

    // Prepare the request to DashScope API
    const model = body.model || 'qwen-max'

    // Format messages for DashScope API
    const formattedMessages = body.messages.map(msg => ({
      role: msg.role,
      content: msg.content
    }))

    // Add system message for Arabic support
    const systemMessage = {
      role: 'system',
      content: 'أنت مساعد ذكي ومفيد. تجيب باللغة العربية بشكل افتراضي إلا إذا طلب المستخدم لغة أخرى. كن ودوداً ومختصراً في إجاباتك.'
    }

    const messagesWithSystem = [systemMessage, ...formattedMessages]

    // Call DashScope API
    const response = await fetch(
      'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${body.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: model,
          input: {
            messages: messagesWithSystem
          },
          parameters: {
            result_format: 'message',
            temperature: 0.7,
            top_p: 0.8,
            max_tokens: 2000
          }
        })
      }
    )

    if (!response.ok) {
      const errorText = await response.text()
      console.error('DashScope API error:', errorText)

      if (response.status === 401) {
        return {
          error: 'مفتاح API غير صالح. يرجى التحقق من المفتاح في الإعدادات.'
        }
      }

      if (response.status === 429) {
        return {
          error: 'تم تجاوز الحد المسموح للطلبات. يرجى المحاولة لاحقاً.'
        }
      }

      return {
        error: `خطأ في الخادم: ${response.status}`
      }
    }

    const data: QwenResponse = await response.json()

    // Extract the response content
    let content = ''

    if (data.output?.choices?.[0]?.message?.content) {
      content = data.output.choices[0].message.content
    } else if (data.output?.text) {
      content = data.output.text
    } else if (data.code) {
      // Handle API error responses
      console.error('DashScope error:', data)
      return {
        error: data.message || 'حدث خطأ غير متوقع.'
      }
    }

    if (!content) {
      console.error('Unexpected response format:', data)
      return {
        error: 'تنسيق الاستجابة غير متوقع.'
      }
    }

    return {
      content: content,
      model: model
    }

  } catch (error) {
    console.error('Qwen API error:', error)

    if (error instanceof Error) {
      if (error.message.includes('fetch')) {
        return {
          error: 'فشل الاتصال بالخادم. تحقق من اتصالك بالإنترنت.'
        }
      }
    }

    return {
      error: 'حدث خطأ أثناء معالجة طلبك.'
    }
  }
})
