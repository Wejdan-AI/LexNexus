/**
 * Example API endpoint demonstrating secure usage of AI Gateway API key
 * The API key is accessed via runtime config and never exposed to the client
 */
export default defineEventHandler(async (event) => {
  // Access the AI Gateway API key from runtime config (server-side only)
  const config = useRuntimeConfig(event)
  const aiGatewayApiKey = config.aiGatewayApiKey

  // Validate that the API key is configured
  if (!aiGatewayApiKey) {
    throw createError({
      statusCode: 500,
      statusMessage: 'AI Gateway API key is not configured. Please set AI_GATEWAY_API_KEY in your .env file.',
    })
  }

  // Example: Return status without exposing the actual key
  return {
    status: 'configured',
    message: 'AI Gateway API key is properly configured',
    // Never return the actual API key in the response
    keyLength: aiGatewayApiKey.length,
    keyPrefix: aiGatewayApiKey.substring(0, 4) + '...',
  }
})
