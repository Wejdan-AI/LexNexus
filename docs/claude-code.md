# Claude Code

AI Gateway provides [Anthropic-compatible API endpoints](/docs/ai-gateway/anthropic-compat) so you can use [Claude Code](https://www.claude.com/product/claude-code) through a unified gateway.

## Configuring Claude Code

[Claude Code](https://code.claude.com/docs) is Anthropic's agentic coding tool. You can configure it to use Vercel AI Gateway, enabling you to:

*   Route requests through multiple AI providers
*   Monitor traffic and spend in your AI Gateway Overview
*   View detailed traces in Vercel Observability under AI
*   Use any model available through the gateway

### 1. Configure environment variables

First, log out if you're already logged in:

```bash
claude /logout
```

Next, ensure you have your AI Gateway API key handy, and configure Claude Code to use the AI Gateway by adding this to your shell configuration file, for example in `~/.zshrc` or `~/.bashrc`:

```bash
export ANTHROPIC_BASE_URL="https://ai-gateway.vercel.sh"
export ANTHROPIC_AUTH_TOKEN="your-ai-gateway-api-key"
export ANTHROPIC_API_KEY=""
```

Setting `ANTHROPIC_API_KEY` to an empty string is important. Claude Code checks this variable first, and if it's set to a non-empty value, it will use that instead of `ANTHROPIC_AUTH_TOKEN`.

### 2. Run Claude Code

Run `claude` to start Claude Code with AI Gateway:

```bash
claude
```

Your requests will now be routed through Vercel AI Gateway.

### 3. (Optional) Use different models

You can override the default models that Claude Code uses by setting additional environment variables:

```bash
export ANTHROPIC_DEFAULT_SONNET_MODEL="kwaipilot/kat-coder-pro-v1"
export ANTHROPIC_DEFAULT_OPUS_MODEL="zai/glm-4.7"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="minimax/minimax-m2.1"
```

This allows you to use any model available through the AI Gateway while still using Claude Code's familiar interface.

**Note:** Models vary widely in their support for tools, extended thinking, and other features that Claude Code relies on. Performance may differ significantly depending on the model and provider you select.

### 4. (Optional) macOS: Secure token storage with Keychain

If you're on a Mac and would like to manage your API key through a keychain for improved security, set your API key in the keychain with:

```bash
security add-generic-password -a "$USER" -s "ANTHROPIC_AUTH_TOKEN" \
  -w "your-ai-gateway-api-key"
```

and edit the `ANTHROPIC_AUTH_TOKEN` line above to:

```bash
export ANTHROPIC_AUTH_TOKEN=$(
  security find-generic-password -a "$USER" -s "ANTHROPIC_AUTH_TOKEN" -w
)
```

If you need to update the API key value later, you can do it with:

```bash
security add-generic-password -U -a "$USER" -s "ANTHROPIC_AUTH_TOKEN" \
  -w "new-ai-gateway-api-key"
```
