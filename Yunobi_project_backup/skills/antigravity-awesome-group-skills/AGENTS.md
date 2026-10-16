# AGENTS.md — Instructions for AI Coding Assistants

This file provides context for AI agents (Claude Code, Gemini CLI, Cursor, etc.) when working with this repository.

## What Is This Repository?

**Antigravity Awesome Group Skills** is a curated collection of reusable `SKILL.md` playbooks for AI coding assistants. Skills are organized by domain (frontend, backend, security, testing, AI/ML, DevOps, etc.) and can be used across multiple AI tools.

## Repository Structure

```
├── skills/           # Individual skill folders with SKILL.md files
├── plugins/          # Plugin bundles for specific domains
├── docs/             # User and contributor documentation
├── scripts/          # Automation and validation scripts
├── assets/           # Images, social cards, branding
├── AGENTS.md         # This file — agent instructions
├── CATALOG.md        # Full skill catalog
├── CONTRIBUTING.md   # How to contribute skills
└── README.md         # Landing page and reference
```

## How Skills Work

1. **Automatic Detection**: The agent reads your task and matches it to the most relevant skill(s)
2. **Skill Loading**: The agent reads the skill's `SKILL.md` file for detailed instructions
3. **Guided Execution**: The skill provides step-by-step patterns, best practices, and code templates
4. **Multiple Skills**: Several skills can activate simultaneously for complex tasks

## When to Reference a Skill

- You want the agent to use a specific approach
- You're curious about best practices for a specific technology
- You want to ensure a security audit is performed

**Tip**: Mention the skill name in your request to force activation:
> "Use the **react-patterns** skill to build this component"
> "Run the **security-auditor** skill on this codebase"

## Compatible Tools

- **Antigravity IDE** — Place skills in `~/.gemini/skills/`
- **Claude Code** — Place skills in `~/.claude/skills/`
- **Cursor** — Place skills in `~/.cursor/skills/`
- **Gemini CLI** — Place skills in `~/.gemini/cli-skills/`
- **Custom path** — Use `--path` flag with the installer
