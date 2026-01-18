# Logging System Documentation

This documentation describes the new logging system API endpoint for the WejdanAI project.

## API Endpoint

The logging system provides a REST API endpoint at `/api/logs` that supports both GET and POST methods.

### Base URL
```
https://wejdanai.vercel.app/api/logs
```

### Database Schema

The system creates a `logs` table with the following schema:

```sql
CREATE TABLE IF NOT EXISTS logs (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES profiles(id) ON DELETE SET NULL,
  query TEXT NOT NULL,
  response TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## API Methods

### GET /api/logs
Retrieves all logs from the database, ordered by creation date (newest first).

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "query": "ما هو الطقس اليوم؟",
    "response": "الجو مشمس في الرياض",
    "created_at": "2024-01-15T10:30:00.000Z"
  }
]
```

### POST /api/logs
Adds a new log entry to the database.

**Request Body:**
```json
{
  "user_id": 1,           // Optional: References profiles table
  "query": "User query",  // Required: The user's query
  "response": "AI response" // Required: The AI's response
}
```

**Success Response:**
```json
{
  "message": "✅ Log saved successfully",
  "log": {
    "id": 1,
    "user_id": 1,
    "query": "User query",
    "response": "AI response",
    "created_at": "2024-01-15T10:30:00.000Z"
  }
}
```

**Error Response:**
```json
{
  "error": "⚠️ Both 'query' and 'response' are required."
}
```

## Integration Examples

### Python Example

```python
import requests

BASE_URL = "https://wejdanai.vercel.app/api/logs"

# 1. Add a new log
response = requests.post(BASE_URL, json={
    "user_id": 1,
    "query": "ما هو الطقس اليوم؟",
    "response": "الجو مشمس في الرياض"
})
print(response.json())

# 2. Add a log without user_id (anonymous)
response = requests.post(BASE_URL, json={
    "query": "Translate hello to Arabic",
    "response": "مرحبا"
})
print(response.json())

# 3. Fetch all logs
logs = requests.get(BASE_URL).json()
print(f"Retrieved {len(logs)} logs")
for log in logs:
    print(f"Log {log['id']}: {log['query']} -> {log['response']}")
```

### Node.js Example

```javascript
import fetch from "node-fetch";

const BASE_URL = "https://wejdanai.vercel.app/api/logs";

// Add a new log with user_id
const addLogWithUser = await fetch(BASE_URL, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    user_id: 1,
    query: "Translate hello",
    response: "مرحبا"
  }),
});
console.log(await addLogWithUser.json());

// Add a log without user_id (anonymous)
const addAnonymousLog = await fetch(BASE_URL, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: "What is AI?",
    response: "AI stands for Artificial Intelligence"
  }),
});
console.log(await addAnonymousLog.json());

// Fetch all logs
const logsResponse = await fetch(BASE_URL);
const logs = await logsResponse.json();
console.log(`Retrieved ${logs.length} logs`);
logs.forEach(log => {
  console.log(`Log ${log.id}: ${log.query} -> ${log.response}`);
});
```

### cURL Examples

```bash
# Add a new log
curl -X POST https://wejdanai.vercel.app/api/logs \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "query": "What is the weather today?",
    "response": "It is sunny in Riyadh"
  }'

# Get all logs
curl https://wejdanai.vercel.app/api/logs
```

## Error Handling

The API handles the following error scenarios:

1. **Missing required fields**: Returns error if `query` or `response` is missing
2. **Database errors**: Returns appropriate error messages for database connectivity issues
3. **Invalid methods**: Returns "Method not allowed" for unsupported HTTP methods

## Usage in AI Applications

This logging system is designed to create a persistent memory system for AI platforms. Common use cases include:

- **Conversation History**: Store user queries and AI responses for context
- **Analytics**: Track common queries and response patterns
- **Debugging**: Monitor AI performance and response quality
- **Personalization**: Build user-specific interaction history
- **Training Data**: Collect real-world conversations for model improvement

## Notes

- The `user_id` field is optional and references the `profiles` table
- Logs are automatically timestamped with `created_at`
- The API supports both authenticated and anonymous logging
- All logs are retrieved in descending order by creation time