# Installation Guide

## Method 1: Claude Code Plugin (Recommended)

```bash
/plugin marketplace add Autom8Minds/seo-skills
/plugin install seo-mcp-skills@seo-mcp-skills
```

Both steps are required. `marketplace add` registers this repo as a plugin catalog;
`install` then adds the plugin from it. Installing all 7 skills at once.

> **If the first command fails with an SSH key or permissions error:** GitHub
> `owner/repo` shorthand clones over SSH by default. Either start Claude Code with
> `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` set, or use the full HTTPS URL:
>
> ```bash
> /plugin marketplace add https://github.com/Autom8Minds/seo-skills.git
> ```

## Method 2: Manual Installation (Claude Code)

```bash
git clone https://github.com/Autom8Minds/seo-skills.git ~/.claude/skills/seo-skills
```

## Method 3: Individual Skills (Claude.ai)

1. Go to the [dist/](../dist/) folder
2. Download the zip for the skill(s) you want
3. In Claude.ai, go to **Settings > Capabilities > Skills**
4. Upload the zip file

## Setting Up seo-mcp MCP Server

The skills work best with the seo-mcp MCP server providing real-time analysis tools.

### Quick setup (npx)

Add to your `.mcp.json` (project root or `~/.claude/.mcp.json`):

```json
{
  "mcpServers": {
    "seo-mcp": {
      "command": "npx",
      "args": ["@autom8minds/seo-mcp"],
      "env": {
        "MCP_MODE": "stdio"
      }
    }
  }
}
```

### With optional API keys

```json
{
  "mcpServers": {
    "seo-mcp": {
      "command": "npx",
      "args": ["@autom8minds/seo-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "PAGESPEED_API_KEY": "your-key",
        "DATAFORSEO_LOGIN": "your-login",
        "DATAFORSEO_PASSWORD": "your-password"
      }
    }
  }
}
```

### What each API key unlocks

| API Key | Tools Unlocked | How to Get |
|---------|---------------|------------|
| None needed | 23 tools (analysis, accessibility, performance, generation, crawler) | N/A |
| `PAGESPEED_API_KEY` | Higher rate limits for PageSpeed | [Google Cloud Console](https://console.cloud.google.com/) |
| `DATAFORSEO_LOGIN` + `PASSWORD` | Keyword research, SERP analysis, backlinks, DA | [DataForSEO](https://app.dataforseo.com/) |
| `MOZ_ACCESS_ID` + `SECRET_KEY` | Alternative for backlinks and DA | [Moz](https://moz.com/products/api) |
| `GSC_CLIENT_ID` + `SECRET` + `TOKEN` | Search Console data | [Google Search Console API](https://developers.google.com/webmaster-tools/) |
