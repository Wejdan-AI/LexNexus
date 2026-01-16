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
        // Try to parse tasks from AI response with improved parsing
        // Look for JSON array or individual JSON objects
        let tasks: Array<{ title?: string; description?: string; content?: string }> = []
        
        // Try to find and parse a JSON array first
        const arrayMatch = aiResponse.match(/\[[\s\S]*?\]/)?.[0]
        if (arrayMatch) {
          try {
            const parsedArray = JSON.parse(arrayMatch)
            if (Array.isArray(parsedArray)) {
              tasks = parsedArray
            }
          } catch (err) {
            console.error('Failed to parse JSON array:', err)
          }
        }
        
        // If no array found, try individual JSON objects with better regex
        if (tasks.length === 0) {
          const jsonPattern = /\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}/g
          const taskMatches = aiResponse.match(jsonPattern)
          if (taskMatches) {
            for (const taskStr of taskMatches) {
              try {
                const parsed = JSON.parse(taskStr)
                if (parsed && (parsed.title || parsed.content)) {
                  tasks.push(parsed)
                }
              } catch (err) {
                // Skip invalid JSON
              }
            }
          }
        }

        // Create tasks in Taskade with validation
        if (tasks.length > 0) {
          const headers = {
            'Authorization': `Bearer ${taskadeKey}`,
            'Content-Type': 'application/json',
          }

          for (const task of tasks) {
            try {
              // Extract task content with fallbacks and validation
              const taskContent = task.title || task.content
              if (!taskContent || typeof taskContent !== 'string') {
                continue // Skip tasks without valid content
              }
              
              const taskNotes = task.description || undefined
              
              const response = await axios.post(
                `${TASKADE_API_BASE}/workspaces/${taskadeWorkspaceId}/tasks`,
                { 
                  content: taskContent,
                  notes: taskNotes 
                },
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
