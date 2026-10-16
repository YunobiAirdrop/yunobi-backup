# Getting Started with Antigravity Awesome Group Skills

Welcome! This guide will help you start using this skill library with your AI coding assistant.

## What Are Skills?

Skills are structured markdown files (`SKILL.md`) that teach AI coding assistants how to handle specific tasks. Each skill contains:

- **Frontmatter**: Metadata (name, description, source)
- **Instructions**: Step-by-step guidance
- **Examples**: Practical code snippets
- **Best Practices**: What to do and what to avoid

## Quick Start

### 1. Choose Your Tool

Antigravity Awesome Group Skills works with:
- **Antigravity IDE** — Place skills in `~/.gemini/skills/`
- **Antigravity CLI (agy)** — Place skills in `~/.gemini/antigravity-cli/skills/`
- **Claude Code** — Place skills in `~/.claude/skills/`
- **Cursor** — Place skills in `~/.cursor/skills/`
- **Gemini CLI** — Place skills in `~/.gemini/cli-skills/`
- **Any AI tool** — Use `--path` to specify a custom skills directory

### 2. Install Skills

**Method A: Clone the repo and copy**
```bash
git clone https://github.com/YOUR-USERNAME/antigravity-awesome-group-skills.git
cp -r skills/* ~/.gemini/skills/
```

**Method B: Use specific skills only**
```bash
cp -r skills/react-patterns ~/.gemini/skills/
cp -r skills/security-auditor ~/.gemini/skills/
```

### 3. Start Using Skills

In your AI coding assistant, mention a skill name:

```
Use the react-patterns skill to help me build this component
```

Or let the AI detect which skill is appropriate automatically.

## Next Steps

- Browse the [full skill catalog](../README.md) for available skills
- Learn how to [create your own skill](contributing.md)
- Check the [Usage Guide](usage.md) for advanced tips
