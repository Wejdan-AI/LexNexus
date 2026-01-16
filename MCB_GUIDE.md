# MCB Integration Guide

## What is MCB?

MCB (Multi-Channel Bot) is an intelligent automation system that combines OpenAI's Codex GPT with Taskade's task management platform. It enables automated workflows where AI-generated insights can be instantly converted into actionable tasks.

## Architecture

```
User Request → OpenAI Codex GPT → AI Analysis → Taskade Task Creation → Task Management
     ↓                ↓                  ↓              ↓                    ↓
  Prompt          Processing        Parse Tasks    Create Tasks        Track Progress
```

## How It Works

### 1. OpenAI Codex GPT Integration

The Codex GPT integration provides:
- **Intelligent Code Assistance**: Get help with coding questions, debugging, and best practices
- **Task Breakdown**: Automatically break down complex projects into manageable tasks
- **Context-Aware Responses**: Receive responses that understand your specific needs

**Endpoint**: `/api/codex`

**Example Request**:
```json
{
  "prompt": "How do I implement JWT authentication in Node.js?",
  "model": "gpt-4"
}
```

**Example Response**:
```json
{
  "success": true,
  "response": "To implement JWT authentication in Node.js...",
  "model": "gpt-4",
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 200,
    "total_tokens": 215
  }
}
```

### 2. Taskade Integration

The Taskade integration enables:
- **Task Management**: Create, read, update tasks in your Taskade workspace
- **Workspace Organization**: Connect to specific workspaces
- **Real-time Sync**: Changes reflect immediately in Taskade

**Endpoint**: `/api/taskade`

**Supported Actions**:
- `getWorkspaces`: List all available workspaces
- `getTasks`: Get tasks from a specific workspace
- `createTask`: Create a new task
- `updateTask`: Update an existing task

**Example Request** (Create Task):
```json
{
  "action": "createTask",
  "data": {
    "workspaceId": "workspace_123",
    "content": "Implement user authentication",
    "options": {
      "priority": "high"
    }
  }
}
```

### 3. MCB Combined Integration

The MCB integration combines both services for powerful automation:

**Endpoint**: `/api/mcb-integration`

**Features**:
1. Send a request to AI
2. Get intelligent breakdown of tasks
3. Automatically create tasks in Taskade
4. Track everything in one place

**Example Request**:
```json
{
  "prompt": "I need to build a REST API with authentication. Break this down into tasks.",
  "taskadeWorkspaceId": "workspace_123",
  "autoCreateTasks": true
}
```

**Example Response**:
```json
{
  "success": true,
  "aiResponse": "Here's a breakdown of building a REST API with authentication:\n\n1. Set up project structure\n2. Implement database schema\n3. Create authentication endpoints\n4. Add JWT middleware\n5. Write API tests",
  "tasksCreated": [
    {
      "id": "task_1",
      "content": "Set up project structure"
    },
    {
      "id": "task_2",
      "content": "Implement database schema"
    }
  ]
}
```

### 4. Webhook Integration

Receive real-time updates from Taskade:

**Endpoint**: `/api/taskade-webhook` (POST)

**Supported Events**:
- `task.created`: When a new task is created
- `task.updated`: When a task is modified
- `task.completed`: When a task is marked as complete
- `task.deleted`: When a task is removed

**Setup**:
1. Go to your Taskade workspace settings
2. Add webhook URL: `https://your-domain.com/api/taskade-webhook`
3. Set webhook secret in `.env` as `TASKADE_WEBHOOK_SECRET`

## Usage Examples

### Example 1: Project Planning

**Request**:
```
"I need to create a new feature for user profile management. 
Help me plan this out and create tasks."
```

**AI Response**:
- Analyzes the requirement
- Breaks it down into specific tasks
- Creates tasks in Taskade automatically

### Example 2: Code Review

**Request**:
```
"Review my authentication implementation and suggest improvements"
```

**AI Response**:
- Provides detailed code review
- Suggests security enhancements
- Can create improvement tasks if needed

### Example 3: Bug Investigation

**Request**:
```
"I have a memory leak in my Node.js application. 
Help me debug and create investigation tasks."
```

**AI Response**:
- Provides debugging strategy
- Creates investigation checklist in Taskade
- Suggests tools and approaches

## Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...
TASKADE_API_KEY=your_key_here

# Optional
TASKADE_WEBHOOK_SECRET=your_secret_here
```

### Runtime Configuration

The application uses Nuxt's runtime config for secure API key management:

```typescript
// nuxt.config.ts
runtimeConfig: {
  openaiApiKey: process.env.OPENAI_API_KEY,
  taskadeApiKey: process.env.TASKADE_API_KEY,
  taskadeWebhookSecret: process.env.TASKADE_WEBHOOK_SECRET,
}
```

## Best Practices

1. **API Key Security**
   - Never commit API keys to version control
   - Use environment variables for all secrets
   - Rotate keys regularly

2. **Task Creation**
   - Be specific in prompts for better task breakdown
   - Review AI-generated tasks before creating them
   - Use workspace IDs to organize tasks properly

3. **Rate Limiting**
   - Respect OpenAI rate limits
   - Cache responses when appropriate
   - Implement retry logic for failed requests

4. **Error Handling**
   - Always handle API errors gracefully
   - Provide meaningful error messages to users
   - Log errors for debugging

## Troubleshooting

### "OpenAI API key not configured"
- Ensure `OPENAI_API_KEY` is set in your `.env` file
- Restart the development server after adding environment variables

### "Taskade API key not configured"
- Ensure `TASKADE_API_KEY` is set in your `.env` file
- Verify your API key is valid at taskade.com

### Tasks not creating automatically
- Verify `autoCreateTasks` is set to `true`
- Check that `taskadeWorkspaceId` is provided
- Ensure workspace ID is correct and accessible

### Webhook not receiving events
- Verify webhook URL is publicly accessible
- Check webhook secret matches configuration
- Review Taskade webhook logs in their dashboard

## API Rate Limits

### OpenAI
- GPT-4: ~40,000 requests/day (varies by tier)
- Monitor usage in OpenAI dashboard

### Taskade
- Varies by plan
- Check Taskade documentation for current limits

## Future Enhancements

Potential improvements for the MCB system:

1. **Advanced AI Features**
   - Code generation from natural language
   - Automatic bug detection and fixing
   - Smart task prioritization

2. **Enhanced Taskade Integration**
   - Calendar sync
   - Team collaboration features
   - Progress tracking and analytics

3. **Multi-Channel Support**
   - Slack integration
   - Discord bot
   - Email notifications

4. **Automation Rules**
   - Trigger AI analysis on specific events
   - Automatic task assignment
   - Smart notifications

## Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Taskade API Documentation](https://www.taskade.com/developers)
- [Nuxt 3 Documentation](https://nuxt.com/docs)

## Support

For issues or questions:
1. Check this documentation first
2. Review the main README.md
3. Open an issue on GitHub
4. Contact the development team

---

**Last Updated**: 2026-01-16
