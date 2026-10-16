# Usage Guide

Tips and best practices for using Antigravity Awesome Group Skills effectively.

## Skill Activation

### Automatic Activation
When you describe a task, the AI agent automatically matches it to relevant skills. For example, if you say "Let me review the security of this codebase", the agent will activate security-related skills.

### Manual Activation
You can force a specific skill by mentioning it by name:

> "Use the **react-patterns** skill to build this component"
> "Run the **tdd-workflow** skill for this feature"
> "Apply the **security-auditor** skill on this codebase"

### Multiple Skills
Complex tasks often activate multiple skills simultaneously. For example, building a new API endpoint might trigger:
- `api-patterns` — API design decisions
- `auth-implementation-patterns` — Authentication
- `database-design` — Schema design
- `python-fastapi-development` — Implementation patterns
- `api-testing-observability-api-mock` — Testing

## Skill Categories

Skills are organized into mission-based workflows in the README. Start with the workflow that matches your current task:

1. **Pre-Deployment Checklist** — Before shipping to production
2. **Dev Environment Setup** — New project onboarding
3. **Bug Fixing/Debugging** — Finding and fixing issues
4. **Security Audit** — Security review
5. **Sprint Planning** — Architecture and planning
6. **Test-Driven Development** — Full TDD cycle
7. **CI/CD Pipeline Setup** — Automation
8. And many more...

## Best Practices

### Do
- ✅ Let the agent discover the right skills automatically
- ✅ Mention skill names explicitly for critical tasks
- ✅ Use multiple skills for complex workflows
- ✅ Review skill outputs critically

### Don't
- ❌ Don't load every skill into your tool at once
- ❌ Don't override skill recommendations without reason
- ❌ Don't ignore skill-provided best practices

## Troubleshooting

### Skill Not Detected
If the AI doesn't seem to recognize a skill:
1. Make sure the skill is in the correct directory
2. Explicitly mention the skill name in your prompt
3. Check that the SKILL.md has proper frontmatter

### Conflicts Between Skills
If multiple skills give conflicting advice:
1. Prioritize by relevance to your specific task
2. Use domain-specific skills over general ones
3. Ask the agent to explain its reasoning

## Need More Help?

Open an Issue or start a Discussion on the GitHub repository.
