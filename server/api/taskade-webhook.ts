/**
 * Webhook endpoint for receiving Taskade events
 * This can trigger automated actions when tasks are created/updated in Taskade
 */
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  
  // Log the webhook event
  console.log('Received Taskade webhook:', {
    timestamp: new Date().toISOString(),
    event: body,
  })

  // Verify webhook signature if configured
  const webhookSecret = process.env.TASKADE_WEBHOOK_SECRET
  if (webhookSecret) {
    const signature = getHeader(event, 'x-taskade-signature')
    // Add signature verification logic here if needed
    if (!signature) {
      throw createError({
        statusCode: 401,
        statusMessage: 'Missing webhook signature',
      })
    }
  }

  // Process different event types
  const { eventType, workspace, task } = body

  try {
    switch (eventType) {
      case 'task.created':
        console.log(`New task created: ${task?.content}`)
        // Add custom logic here (e.g., trigger AI analysis)
        break

      case 'task.updated':
        console.log(`Task updated: ${task?.content}`)
        // Add custom logic here
        break

      case 'task.completed':
        console.log(`Task completed: ${task?.content}`)
        // Add custom logic here
        break

      case 'task.deleted':
        console.log(`Task deleted: ${task?.id}`)
        // Add custom logic here
        break

      default:
        console.log(`Unknown event type: ${eventType}`)
    }

    return {
      success: true,
      message: 'Webhook processed successfully',
    }
  } catch (error: any) {
    console.error('Error processing webhook:', error)
    throw createError({
      statusCode: 500,
      statusMessage: 'Failed to process webhook',
    })
  }
})
