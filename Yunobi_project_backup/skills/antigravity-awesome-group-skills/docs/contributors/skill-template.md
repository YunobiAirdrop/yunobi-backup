# Skill Template

Use this template when creating a new skill. Copy this file as `SKILL.md` in your skill folder.

```markdown
---
name: my-awesome-skill
description: "A brief one-line description of what this skill does"
source: community
date_added: "2026-01-01"
risk: safe
tags:
  - development
  - frontend
  - react
---

# My Awesome Skill

## Overview

Explain what this skill does, when to use it, and what problems it solves.
Keep this section concise — 2-3 sentences max.

## When to Use This Skill

- Use when [scenario 1]
- Use when [scenario 2]
- Use when [scenario 3]
- Do NOT use when [anti-scenario]

## How It Works

### Step 1: [First Step]
Explain what to do first...

```bash
# Example command
command --option value
```

### Step 2: [Second Step]
Explain the next step...

```javascript
// Example code
const result = doSomething();
```

### Step 3: [Final Step]
Explain how to finish...

## Examples

### Example 1: [Common Use Case]

```
Show example code or commands here
```

### Example 2: [Advanced Use Case]

```
More examples...
```

## Best Practices

- ✅ Do this
- ✅ Also do this
- ❌ Don't do this
- ❌ Avoid this

## Common Pitfalls

- **Problem:** Description of common issue
  **Solution:** How to fix it

- **Problem:** Another common mistake
  **Solution:** How to avoid it

## Integration with Other Skills

This skill pairs well with:
- [Skill Name 1] — For related tasks
- [Skill Name 2] — For complementary workflows

## Additional Resources

- [Link to documentation](https://example.com)
- [Tutorial](https://example.com)
- [Reference](https://example.com)
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Lowercase-hyphenated unique identifier |
| `description` | ✅ | One-line description (max 120 chars) |
| `source` | ✅ | `community` or `official` |
| `date_added` | ✅ | Date in YYYY-MM-DD format |
| `risk` | Optional | `safe`, `shell`, `network`, `credential`, or `mutation` |
| `tags` | Optional | List of lowercase tags for categorization |
