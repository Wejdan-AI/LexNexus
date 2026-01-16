import OpenAI from 'openai'
import axios from 'axios'

const TASKADE_API_BASE = 'https://www.taskade.com/api/v1'

/**
 * Multi-Channel Bot (MCB) Integration Endpoint
 * Combines OpenAI Codex GPT with Taskade for automated task management
 */
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { taskadeWorkspaceId, prompt, autoCreateTasks = false } = body

  if (!prompt) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Prompt is required',
    })
  }

  const openaiKey = process.env.OPENAI_API_KEY
  const taskadeKey = process.env.TASKADE_API_KEY

  if (!openaiKey) {
    throw createError({
      statusCode: 500,
      statusMessage: 'OpenAI API key not configured',
    })
  }

  try {
    // Step 1: Get AI response from OpenAI Codex
    const openai = new OpenAI({ apiKey: openaiKey })
    
    const completion = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: 'You are a helpful assistant that analyzes requests and breaks them down into actionable tasks. When asked to create tasks, format your response as a JSON array of tasks with "title" and "description" fields.',
        },
        {
          role: 'user',
          content: prompt,
        },
      ],
      temperature: 0.7,
      max_tokens: 2000,
    })

    const aiResponse = completion.choices[0]?.message?.content || ''

    // Step 2: If autoCreateTasks is enabled and Taskade is configured, create tasks
    let tasksCreated = []
    if (autoCreateTasks && taskadeKey && taskadeWorkspaceId) {
      try {
        // Try to parse tasks from AI response
        const taskMatches = aiResponse.match(/\{[^}]*"title"[^}]*\}/g)
        if (taskMatches) {
          const headers = {
            'Authorization': `Bearer ${taskadeKey}`,
            'Content-Type': 'application/json',
          }

          for (const taskStr of taskMatches) {
            try {
              const task = JSON.parse(taskStr)
              const response = await axios.post(
                `${TASKADE_API_BASE}/workspaces/${taskadeWorkspaceId}/tasks`,
                { content: task.title, notes: task.description },
                { headers }
              )
              tasksCreated.push(response.data)
            } catch (err) {
              console.error('Failed to create task:', err)
            }
          }
        }
      } catch (error) {
        console.error('Error creating tasks in Taskade:', error)
      }
    }

    return {
      success: true,
      aiResponse,
      model: completion.model,
      usage: completion.usage,
      tasksCreated: tasksCreated.length > 0 ? tasksCreated : undefined,
    }
  } catch (error: any) {
    console.error('MCB Integration Error:', error)
    throw createError({
      statusCode: 500,
      statusMessage: error.message || 'Failed to process MCB request',
    })
  }
})
