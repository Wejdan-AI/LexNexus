import axios from 'axios'

const TASKADE_API_BASE = 'https://www.taskade.com/api/v1'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { action, data } = body

  if (!action) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Action is required',
    })
  }

  const apiKey = process.env.TASKADE_API_KEY

  if (!apiKey) {
    throw createError({
      statusCode: 500,
      statusMessage: 'Taskade API key not configured',
    })
  }

  try {
    let response
    const headers = {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    }

    switch (action) {
      case 'getWorkspaces':
        response = await axios.get(`${TASKADE_API_BASE}/workspaces`, { headers })
        break

      case 'createTask':
        if (!data?.workspaceId || !data?.content) {
          throw createError({
            statusCode: 400,
            statusMessage: 'workspaceId and content are required for createTask',
          })
        }
        response = await axios.post(
          `${TASKADE_API_BASE}/workspaces/${data.workspaceId}/tasks`,
          { content: data.content, ...data.options },
          { headers }
        )
        break

      case 'getTasks':
        if (!data?.workspaceId) {
          throw createError({
            statusCode: 400,
            statusMessage: 'workspaceId is required for getTasks',
          })
        }
        response = await axios.get(
          `${TASKADE_API_BASE}/workspaces/${data.workspaceId}/tasks`,
          { headers }
        )
        break

      case 'updateTask':
        if (!data?.workspaceId || !data?.taskId) {
          throw createError({
            statusCode: 400,
            statusMessage: 'workspaceId and taskId are required for updateTask',
          })
        }
        response = await axios.put(
          `${TASKADE_API_BASE}/workspaces/${data.workspaceId}/tasks/${data.taskId}`,
          data.updates,
          { headers }
        )
        break

      default:
        throw createError({
          statusCode: 400,
          statusMessage: `Unknown action: ${action}`,
        })
    }

    return {
      success: true,
      data: response.data,
    }
  } catch (error: any) {
    console.error('Taskade API Error:', error.response?.data || error.message)
    throw createError({
      statusCode: error.response?.status || 500,
      statusMessage: error.response?.data?.message || error.message || 'Failed to process Taskade request',
    })
  }
})
