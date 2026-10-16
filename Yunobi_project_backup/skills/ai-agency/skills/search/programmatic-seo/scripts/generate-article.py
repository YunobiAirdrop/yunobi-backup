#!/usr/bin/env python3
"""
SEO Article Draft Generator for Seam Blog

Generates SEO-optimized markdown article drafts with proper frontmatter,
structure, and placeholder content for the Seam website blog.

Usage:
    python generate-article.py --keyword "mac notch app" --title "Best Mac Notch Apps" --word-count 2000
    python generate-article.py -k "dynamic island mac" -t "Dynamic Island for Mac" -w 1500

Output:
    Creates a markdown file in web/content/blog/drafts/
"""

import argparse
import json
import re
from datetime import date
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


def generate_frontmatter(title: str, keyword: str, description: str, slug: str) -> str:
    """Generate YAML frontmatter for the article."""
    today = date.today().isoformat()

    # Extract tags from keyword
    tags = [keyword]
    if "mac" in keyword.lower():
        tags.append("macos")
    if "notch" in keyword.lower():
        tags.append("macbook pro")
    tags.append("productivity")

    return f'''---
title: "{title}"
description: "{description}"
slug: {slug}
publishedAt: {today}
updatedAt: {today}
author: Seam Team
tags: {json.dumps(tags)}
image: /blog/images/{slug}/hero.webp
imageAlt: {title} - Seam app demonstration
draft: true
---'''


def generate_article_structure(keyword: str, title: str, word_count: int) -> str:
    """Generate the article body structure with SEO-optimized sections."""

    sections = f'''

# {title}

**TL;DR**: [Write a 50-word summary that includes "{keyword}" and answers the reader's primary question. This should be compelling enough to keep them reading.]

## What Is a {keyword.title()}?

[150-200 words introducing the concept. Include "{keyword}" naturally in the first paragraph. Explain what it is, why it matters, and who it's for. Link to Apple's MacBook Pro page for context.]

A {keyword} is [definition]. Since Apple introduced the notch on MacBook Pro in 2021, users have been looking for ways to [benefit].

## Why You Need a {keyword.title()}

[200-250 words on benefits. Focus on pain points and solutions.]

### Productivity Benefits
- [Benefit 1 with specific example]
- [Benefit 2 with specific example]
- [Benefit 3 with specific example]

### Aesthetic Benefits
- [Benefit 1]
- [Benefit 2]

## Best {keyword.title()}s in {date.today().year}

[Main comparison section - this is the meat of the article]

### 1. Seam - Best Overall

**Price**: $XX (one-time purchase)
**Rating**: ⭐⭐⭐⭐⭐ (5/5)

[150 words describing Seam's features honestly. Mention specific features like music visualization, calendar integration, etc.]

**Pros:**
- Native macOS app (not Electron)
- Event-driven, no battery drain
- Beautiful animations
- One-time purchase

**Cons:**
- macOS only
- Newer to market

[Download Seam](https://getseam.app/download)

### 2. [Competitor A]

**Price**: $XX
**Rating**: ⭐⭐⭐⭐ (4/5)

[100 words - be fair and accurate]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

### 3. [Competitor B]

**Price**: $XX
**Rating**: ⭐⭐⭐ (3/5)

[100 words]

### 4. [Competitor C]

**Price**: Free / $XX
**Rating**: ⭐⭐⭐ (3/5)

[100 words]

## Comparison Table

| Feature | Seam | Competitor A | Competitor B | Competitor C |
|---------|------|--------------|--------------|--------------|
| Price | $XX | $XX | $XX | Free |
| Native App | ✅ | ❌ | ✅ | ❌ |
| Music Integration | ✅ | ✅ | ❌ | ❌ |
| Calendar | ✅ | ❌ | ✅ | ❌ |
| Battery Impact | Low | High | Medium | High |
| Updates | Active | Active | Slow | Abandoned |

## How to Choose the Right {keyword.title()}

[200 words with decision framework]

**Choose Seam if:**
- You want a native macOS experience
- Battery life matters to you
- You prefer one-time purchases over subscriptions

**Choose [Alternative] if:**
- [Specific use case]

## How to Install and Set Up

### Step 1: Download
[50 words]

### Step 2: Grant Permissions
[50 words - mention accessibility permissions for macOS]

### Step 3: Customize
[50 words]

## Frequently Asked Questions

### What is the best {keyword}?

Seam is our top pick for the best {keyword} in {date.today().year}. It offers [key differentiator] while maintaining [key benefit]. Unlike alternatives that [problem], Seam [solution].

### Is there a free {keyword}?

[Answer about free options, but explain value of paid options]

### Do {keyword}s affect battery life?

[Honest answer - explain that Seam is event-driven and has minimal battery impact]

### Can I hide the MacBook notch instead?

[Explain hiding options but position customization as better]

### Does {keyword} work on MacBook Air?

[Explain notch requirements - M1/M2 Pro, M3, etc.]

## Conclusion

[150 words wrapping up with clear call-to-action]

If you're looking for the best {keyword} in {date.today().year}, **Seam** stands out for its [top 3 features]. Unlike [competitor approaches], Seam [key differentiator].

Ready to transform your MacBook Pro's notch? [Download Seam](https://getseam.app/download) and see the difference for yourself.

---

*Last updated: {date.today().strftime("%B %d, %Y")}*

*This article contains our honest opinions. We believe in transparency - Seam is our product, but we've tried to give fair assessments of all alternatives.*
'''

    return sections


def generate_article(keyword: str, title: str, word_count: int, output_dir: Path) -> Path:
    """Generate a complete article draft."""

    slug = slugify(title)

    # Generate meta description (150-160 chars)
    description = f"Discover the best {keyword} options for your MacBook Pro. Compare features, pricing, and find the perfect app to transform your notch in {date.today().year}."
    if len(description) > 160:
        description = description[:157] + "..."

    # Build the article
    frontmatter = generate_frontmatter(title, keyword, description, slug)
    body = generate_article_structure(keyword, title, word_count)

    article_content = frontmatter + body

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write the file
    output_path = output_dir / f"{slug}.md"
    output_path.write_text(article_content)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate SEO-optimized article drafts for Seam blog"
    )
    parser.add_argument(
        "-k", "--keyword",
        required=True,
        help="Primary target keyword (e.g., 'mac notch app')"
    )
    parser.add_argument(
        "-t", "--title",
        required=True,
        help="Article title (e.g., 'Best Mac Notch Apps in 2026')"
    )
    parser.add_argument(
        "-w", "--word-count",
        type=int,
        default=2000,
        help="Target word count (default: 2000)"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("web/content/blog/drafts"),
        help="Output directory (default: web/content/blog/drafts)"
    )

    args = parser.parse_args()

    print(f"Generating article draft...")
    print(f"  Keyword: {args.keyword}")
    print(f"  Title: {args.title}")
    print(f"  Target words: {args.word_count}")

    output_path = generate_article(
        keyword=args.keyword,
        title=args.title,
        word_count=args.word_count,
        output_dir=args.output
    )

    print(f"\n✅ Article draft created: {output_path}")
    print("\nNext steps:")
    print("1. Review and fill in placeholder content")
    print("2. Add competitor research")
    print("3. Create/add images")
    print("4. Run SEO checklist")
    print("5. Move to published/ when ready")


if __name__ == "__main__":
    main()
