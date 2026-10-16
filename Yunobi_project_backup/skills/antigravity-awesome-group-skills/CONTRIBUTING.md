# 🤝 Contributing Guide

**Thank you for wanting to make this repo better!** This guide shows you exactly how to contribute, whether you're fixing a typo, adding a new skill, or improving existing ones.

---

## Quick Start

```bash
# 1. Fork and clone
git clone https://github.com/YOUR-USERNAME/antigravity-awesome-group-skills.git
cd antigravity-awesome-group-skills

# 2. Create your skill
mkdir -p skills/my-awesome-skill

# 3. Use the canonical template
cp docs/contributors/skill-template.md skills/my-awesome-skill/SKILL.md

# 4. Edit your SKILL.md with your expertise

# 5. Open a PR
git add skills/my-awesome-skill/
git commit -m "feat: add my-awesome-skill for [purpose]"
git push origin my-branch
```

Open the PR with the default template.

---

## Ways to Contribute

You don't need to be an expert! Here are ways anyone can help:

### 1. Improve Documentation (Easiest!)
- Fix typos or grammar
- Make explanations clearer
- Add examples to existing skills
- Translate documentation to other languages

### 2. Report Issues
- Found a reproducible bug? Open an Issue.
- Need help, want feedback, or have an early-stage idea? Start a Discussion.
- Skill not working? If you can reproduce it, open an Issue.

### 3. Create New Skills
- Share your expertise as a skill
- Fill gaps in the current collection
- Improve existing skills

### 4. Review and Validate
- Try skills and report what works/doesn't work
- Suggest improvements
- Review open pull requests

---

## How to Create a New Skill

### What Makes a Good Skill?

A skill should:
- ✅ Solve a specific problem
- ✅ Be reusable across projects
- ✅ Have clear instructions
- ✅ Include examples when possible

### Step-by-Step: Create Your First Skill

#### Step 1: Choose Your Skill Topic

Ask yourself:
- What am I good at?
- What do I wish my AI assistant knew better?
- What task do I do repeatedly?

**Examples:**
- "I'm good at Docker, let me create a Docker skill"
- "I wish AI understood my company's coding standards"
- "I keep setting up the same testing patterns"

#### Step 2: Create the Folder Structure

```bash
cd skills/
mkdir my-awesome-skill
cd my-awesome-skill
touch SKILL.md
```

#### Step 3: Write Your SKILL.md

Every skill should start from the canonical template in [`docs/contributors/skill-template.md`](docs/contributors/skill-template.md).

Minimum frontmatter:

```markdown
---
name: my-awesome-skill
description: "Brief one-line description of what this skill does"
source: community
date_added: "2026-01-01"
---

# Skill Title

## Overview

Explain what this skill does and when to use it.

## When to Use This Skill

- Use when [scenario 1]
- Use when [scenario 2]

## How It Works

### Step 1: [First Step]
Explain what to do first...

### Step 2: [Second Step]
Explain the next step...

## Examples

### Example 1: [Common Use Case]
```
Show example code or commands here
```

## Best Practices

- ✅ Do this
- ❌ Don't do this

## Common Pitfalls

- **Problem:** Description of common issue
  **Solution:** How to fix it
```

#### Step 4: Test Your Skill

1. Copy it to your AI tool's skills directory:

   **For Antigravity IDE:**
   ```bash
   cp -r skills/my-awesome-skill ~/.gemini/skills/
   ```

   **For Claude Code:**
   ```bash
   cp -r skills/my-awesome-skill ~/.claude/skills/
   ```

   **For Cursor:**
   ```bash
   cp -r skills/my-awesome-skill ~/.cursor/skills/
   ```

   **For Gemini CLI:**
   ```bash
   cp -r skills/my-awesome-skill ~/.gemini/cli-skills/
   ```

2. Try using it:
   ```
   Use @my-awesome-skill to help me with [task]
   ```

3. Does it work? Great! If not, refine it.

#### Step 5: Submit Your Skill

1. Commit your skill:
   ```bash
   git add skills/my-awesome-skill/
   git commit -m "feat: add my-awesome-skill for [purpose]"
   ```

2. Push and open a Pull Request

---

## How to Improve Documentation

### Super Easy Method (No Git Knowledge Needed!)

1. **Find the file** you want to improve on GitHub
2. **Click the pencil icon** (✏️) to edit
3. **Make your changes** in the browser
4. **Click "Propose changes"** at the bottom
5. **Done!** We'll review and merge it

### Using Git

```bash
git clone https://github.com/YOUR-USERNAME/antigravity-awesome-group-skills.git
cd antigravity-awesome-group-skills
git checkout -b improve-docs
# Edit files in your favorite editor
git add .
git commit -m "docs: make XYZ clearer"
git push origin improve-docs
# Open a Pull Request on GitHub
```

---

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

---

## Need Help?

Open an Issue or start a Discussion on GitHub. We're here to help!
