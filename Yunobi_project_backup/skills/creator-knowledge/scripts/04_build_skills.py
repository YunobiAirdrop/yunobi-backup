#!/usr/bin/env python3
"""
Step 4: Generate Claude Skills from consolidated reference documents.

Usage:
    python scripts/04_build_skills.py
    python scripts/04_build_skills.py --category hooks

Requires: ANTHROPIC_API_KEY environment variable

Output:
    skills/kallaway-{category}/SKILL.md
    skills/kallaway-{category}/references/{category}-reference.md
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

CONSOLIDATED_DIR = Path("data/consolidated")
SKILLS_DIR = Path("skills")

SKILL_CATEGORIES = {
    "hooks": {
        "name": "kallaway-hooks",
        "trigger_phrases": "hook, opening, scroll-stop, first 5 seconds, curiosity loop, attention, intro, viral hook, re-hook, hook archetype, opening line, stop the scroll",
        "purpose": "Write viral video hooks using Kallaway's Hook Archetypes framework"
    },
    "storytelling": {
        "name": "kallaway-storytelling",
        "trigger_phrases": "script, story structure, narrative, pacing, rhythm, video script, write a script, storytelling, edutainment, re-hooking, script structure, video body",
        "purpose": "Write complete video scripts using Kallaway's storytelling and narrative frameworks"
    },
    "virality": {
        "name": "kallaway-virality",
        "trigger_phrases": "viral, virality, will this go viral, topic validation, trending, outlier, viral formula, content spread, reach, impressions, 6 ingredients",
        "purpose": "Validate and optimize content ideas for viral potential using Kallaway's Virality Formula"
    },
    "packaging": {
        "name": "kallaway-packaging",
        "trigger_phrases": "title, thumbnail, topic selection, angle, positioning, CTR, click-through, headline, YouTube title, video title, packaging, content angle",
        "purpose": "Create high-CTR titles, thumbnails concepts, and content angles using Kallaway's packaging methodology"
    },
    "content-system": {
        "name": "kallaway-content-system",
        "trigger_phrases": "content workflow, batch, content calendar, production, team, posting schedule, content machine, repurpose, content system, publishing cadence",
        "purpose": "Design and run a content production system using Kallaway's workflow and team structure frameworks"
    },
    "monetization": {
        "name": "kallaway-monetization",
        "trigger_phrases": "monetize, revenue, brand deal, own product, community, academy, distribution era, creator business, pricing, income, creator economy",
        "purpose": "Build revenue models and monetization strategies using Kallaway's distribution-era business frameworks"
    },
    "platform-strategy": {
        "name": "kallaway-platform-strategy",
        "trigger_phrases": "short form, long form, platform, YouTube SEO, TikTok, Instagram, algorithm, content minutes, platform native, repurpose, shorts vs long",
        "purpose": "Optimize content for specific platforms using Kallaway's platform strategy and content minutes framework"
    }
}

BUILD_SKILL_PROMPT = """You are building a Claude Skill from a consolidated reference document containing Kallaway's (@kallawaymarketing) knowledge on {category}.

REFERENCE DOCUMENT:
{reference}

Create a SKILL.md file following this exact structure. The SKILL.md must be UNDER 500 lines — put detailed content in references/ instead.

```
---
name: {skill_name}
description: "{description}"
---

# {title}

## Core Philosophy
[2-3 paragraphs of the foundational principles. Write in imperative form.]

## Key Frameworks
[List each framework with a brief summary. Point to references/ for full detail.]
[For each framework: name, one-line description, when to use it]

## Process
[Step-by-step process for using this skill. Numbered steps.]

## Anti-Patterns
[What NOT to do. Be specific.]

## Output Format
[Define the EXACT format Claude should produce when using this skill.]
[Use a code block template showing the structure.]

## Application to DeFi / AI / LATAM Content
[Specific templates and examples for Anthony's niches]
[Include both English (LinkedIn) and Spanish (Twitter/YouTube) variants]
```

RULES:
- Keep SKILL.md under 500 lines total
- Write in imperative form ("Do X" not "You should do X")
- Include specific output format Claude must follow
- Add DeFi/AI/LATAM examples in both English and Spanish
- The description field must include many trigger phrases: "{triggers}"
- Be concrete and actionable — no vague advice
- Every framework needs a "When to use" note
- Include at least 3 anti-patterns
"""


def build_skill(category: str, config: dict):
    """Generate a skill from its consolidated reference doc."""
    try:
        import anthropic
    except ImportError:
        print("Install: pip install anthropic")
        sys.exit(1)
    
    # Find the consolidated reference
    ref_filename = f"{category.replace('_', '-')}.md"
    ref_path = CONSOLIDATED_DIR / ref_filename
    
    if not ref_path.exists():
        print(f"  Reference doc not found: {ref_path}")
        print(f"  Run consolidation first: python scripts/03_consolidate.py --category {category.upper()}")
        return
    
    with open(ref_path, 'r', encoding='utf-8') as f:
        reference_content = f.read()
    
    client = anthropic.Anthropic()
    
    skill_name = config["name"]
    description = f"Use this skill to {config['purpose']}. Trigger whenever the user mentions or asks about: {config['trigger_phrases']}. Works for ANY niche — DeFi, AI, tech, lifestyle, etc."
    
    prompt = BUILD_SKILL_PROMPT.format(
        category=category.upper(),
        reference=reference_content,
        skill_name=skill_name,
        description=description,
        title=f"{category.replace('-', ' ').title()} — Kallaway Method",
        triggers=config["trigger_phrases"]
    )
    
    print(f"  Generating SKILL.md for {skill_name}...")
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    skill_content = response.content[0].text
    
    # Clean up — remove markdown code fences if present
    if skill_content.startswith("```"):
        lines = skill_content.split("\n")
        skill_content = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    
    # Save SKILL.md
    skill_dir = SKILLS_DIR / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    
    with open(skill_dir / "SKILL.md", 'w', encoding='utf-8') as f:
        f.write(skill_content)
    
    # Copy the full reference doc
    shutil.copy2(ref_path, skill_dir / "references" / f"{category.replace('_', '-')}-reference.md")
    
    print(f"  Saved: {skill_dir}/SKILL.md")
    print(f"  Reference: {skill_dir}/references/{category.replace('_', '-')}-reference.md")


def run_build(single_category: str = None):
    """Build all skills or a single one."""
    if single_category:
        key = single_category.lower().replace("_", "-")
        if key not in SKILL_CATEGORIES:
            print(f"Unknown category: {key}")
            print(f"Available: {list(SKILL_CATEGORIES.keys())}")
            sys.exit(1)
        build_skill(key, SKILL_CATEGORIES[key])
    else:
        for key, config in SKILL_CATEGORIES.items():
            print(f"\n[{key.upper()}]")
            build_skill(key, config)
    
    print(f"\nSkill generation complete! Files in {SKILLS_DIR}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", type=str, help="Build a single skill")
    args = parser.parse_args()
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    run_build(args.category)
