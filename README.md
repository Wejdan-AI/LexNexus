# LexNexus - Codex GPT & Taskade MCB Integration Platform

A powerful integration platform that combines **OpenAI Codex GPT** with **Taskade** for intelligent task management and automation through Multi-Channel Bot (MCB) capabilities.

## 🌟 Features

- **Codex GPT Assistant**: Interactive AI-powered coding assistant using OpenAI's GPT-4
- **Taskade Integration**: Full task management capabilities with Taskade API
- **MCB Integration**: Multi-Channel Bot that combines AI intelligence with automated task creation
- **Webhook Support**: Receive and process Taskade events in real-time
- **Modern UI**: Clean, responsive interface built with Nuxt 3 and Tailwind CSS
- **Database Integration**: PostgreSQL integration for data persistence

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ or npm
- OpenAI API key (get one at [platform.openai.com](https://platform.openai.com))
- Taskade API key (get one at [taskade.com/developers](https://www.taskade.com/developers))
- PostgreSQL database (optional, for database features)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Wejdan-AI/LexNexus.git
cd LexNexus
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory:
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Taskade Configuration
TASKADE_API_KEY=your_taskade_api_key_here
TASKADE_WEBHOOK_SECRET=your_webhook_secret_here

# Database Configuration (optional)
POSTGRES_URL=your_postgres_connection_string_here
```

4. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 📖 Usage

### MCB Integration

The Multi-Channel Bot (MCB) combines Codex GPT with Taskade for intelligent automation:

1. Navigate to the **MCB Integration** tab
2. (Optional) Enter your Taskade Workspace ID
3. Enable "Automatically create tasks" if you want AI responses to generate tasks
4. Enter your request (e.g., "Help me plan a new feature for user authentication")
5. Click "Process with MCB" to get AI-generated responses and automatic task creation

### Codex GPT Assistant

Direct interaction with OpenAI's Codex GPT:

1. Navigate to the **Codex GPT** tab
2. Type your coding questions or requests
3. Press Ctrl+Enter or click Send
4. Get intelligent, context-aware responses

### Taskade Manager

Manage your Taskade tasks directly:

1. Navigate to the **Taskade** tab
2. Enter your Workspace ID
3. Create new tasks or view existing ones
4. Refresh to sync with Taskade

## 🔧 API Endpoints

### `/api/codex` (POST)
Interact with OpenAI Codex GPT
```json
{
  "prompt": "Your question or request",
  "model": "gpt-4"
}
```

### `/api/taskade` (POST)
Manage Taskade tasks
```json
{
  "action": "createTask|getTasks|updateTask",
  "data": {
    "workspaceId": "your_workspace_id",
    "content": "Task content"
  }
}
```

### `/api/mcb-integration` (POST)
Combined MCB integration
```json
{
  "prompt": "Your request",
  "taskadeWorkspaceId": "workspace_id",
  "autoCreateTasks": true
}
```

### `/api/taskade-webhook` (POST)
Webhook endpoint for Taskade events

## 🏗️ Architecture

```
LexNexus/
├── server/
│   └── api/
│       ├── codex.ts              # OpenAI Codex GPT endpoint
│       ├── taskade.ts            # Taskade API integration
│       ├── mcb-integration.ts    # Multi-Channel Bot logic
│       ├── taskade-webhook.ts    # Webhook handler
│       └── get-users.ts          # Database demo
├── components/
│   ├── CodexChat.vue             # Codex GPT chat interface
│   ├── TaskadeManager.vue        # Taskade task management
│   ├── MCBIntegration.vue        # MCB integration UI
│   └── Table.vue                 # Database table component
├── pages/
│   └── index.vue                 # Main application page
└── nuxt.config.ts                # Nuxt configuration
```

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `TASKADE_API_KEY` | Yes | Your Taskade API key |
| `TASKADE_WEBHOOK_SECRET` | No | Secret for webhook verification |
| `POSTGRES_URL` | No | PostgreSQL connection string for database features |

## 🚢 Deployment

### Vercel

1. Push your code to GitHub
2. Import your repository to Vercel
3. Add environment variables in Vercel dashboard
4. Deploy

### Other Platforms

Build the application for production:

```bash
npm run build
```

Preview production build locally:

```bash
npm run preview
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT

## 🔗 Links

- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Taskade API Documentation](https://www.taskade.com/developers)

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ by the Wejdan-AI team
