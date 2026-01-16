import OpenAI from 'openai'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { prompt, model = 'gpt-4' } = body

  if (!prompt) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Prompt is required',
    })
  }

  const apiKey = process.env.OPENAI_API_KEY

  if (!apiKey) {
    throw createError({
      statusCode: 500,
      statusMessage: 'OpenAI API key not configured',
    })
  }

  try {
    const openai = new OpenAI({
      apiKey: apiKey,
    })

    const completion = await openai.chat.completions.create({
      model: model,
      messages: [
        {
          role: 'system',
          content: 'You are a helpful coding assistant powered by OpenAI Codex. You help with code generation, debugging, and technical questions.',
        },
        {
          role: 'user',
          content: prompt,
        },
      ],
      temperature: 0.7,
      max_tokens: 2000,
    })

    return {
      success: true,
      response: completion.choices[0]?.message?.content || '',
      model: completion.model,
      usage: completion.usage,
    }
  } catch (error: any) {
    console.error('OpenAI API Error:', error)
    throw createError({
      statusCode: 500,
      statusMessage: error.message || 'Failed to process request with OpenAI',
    })
  }
})
