#!/usr/bin/env python3
"""
Step 3: Consolidate transcripts per category into reference documents.

Usage:
    python scripts/03_consolidate.py
    python scripts/03_consolidate.py --category HOOKS

Requires: ANTHROPIC_API_KEY environment variable

Output:
    data/consolidated/{category}.md — one reference doc per category
"""

import argparse
import json
import os
import sys
from pathlib import Path

TRANSCRIPTS_DIR = Path("data/raw-transcripts")
CATEGORIES_FILE = Path("data/categorized/categories.json")
OUTPUT_DIR = Path("data/consolidated")

CONSOLIDATE_PROMPT = """You are extracting knowledge from multiple YouTube video transcripts by Kallaway (@kallawaymarketing), all classified under the category: {category}.

Your job: Create a single, comprehensive reference document that synthesizes ALL the knowledge from these transcripts into an organized, actionable reference.

TRANSCRIPTS:
{transcripts}

Create a markdown document with this EXACT structure:

# {category} — Kallaway Method Reference

## Core Philosophy
The foundational beliefs and principles Kallaway holds about this topic. Only include what he explicitly states or clearly demonstrates.

## Frameworks
Every named framework, method, or system he teaches. For each:
### [Framework Name]
- **What it is:** one sentence
- **Steps:** numbered steps
- **Example:** how he applies it
- **When to use:** context

## Templates
Reusable templates, formulas, or fill-in-the-blank structures. Write them as copy-paste-ready templates.

## Anti-Patterns
What Kallaway explicitly says NOT to do. Include his reasoning.

## Real Examples
Specific case studies, videos, brands, or creators he references as examples. Include context.

## Metrics & Benchmarks
Any numbers, KPIs, or benchmarks he mentions (view rates, engagement targets, posting frequency, etc.)

## Key Quotes
The 10 most impactful direct quotes from across all the transcripts. These should be memorable, actionable, and representative of his thinking.

RULES:
- Do NOT add your own interpretations or knowledge. Only synthesize what's in the transcripts.
- If something appears in multiple transcripts, consolidate it (don't repeat).
- If frameworks evolve across videos, show the most recent/complete version.
- Be comprehensive — this document replaces reading all the individual transcripts.
- Use his exact terminology and naming conventions.
"""


def consolidate_category(category: str, video_entries: list):
    """Merge all transcripts for a category into one reference doc."""
    try:
        import anthropic
    except ImportError:
        print("Install: pip install anthropic")
        sys.exit(1)
    
    client = anthropic.Anthropic()
    
    # Load and concatenate transcripts
    all_transcripts = []
    for entry in video_entries:
        filepath = TRANSCRIPTS_DIR / entry["source_file"]
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            title = entry.get("summary", entry["source_file"])
            all_transcripts.append(f"### Video: {entry['source_file']}\n{content}")
    
    if not all_transcripts:
        print(f"  No transcripts found for {category}")
        return
    
    combined = "\n\n---\n\n".join(all_transcripts)
    
    # Truncate if too long (Claude's context)
    max_chars = 180000
    if len(combined) > max_chars:
        combined = combined[:max_chars] + "\n\n[REMAINING TRANSCRIPTS TRUNCATED — PROCESS IN BATCHES IF NEEDED]"
    
    print(f"  Processing {len(all_transcripts)} transcripts for {category} ({len(combined)} chars)...")
    
    prompt = CONSOLIDATE_PROMPT.format(
        category=category,
        transcripts=combined
    )
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    result = response.content[0].text
    
    # Save
    output_path = OUTPUT_DIR / f"{category.lower().replace('_', '-')}.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"  Saved: {output_path}")


def run_consolidation(single_category: str = None):
    """Consolidate all categories or a single one."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load categorization results
    if not CATEGORIES_FILE.exists():
        print(f"Run categorization first: python scripts/02_categorize.py")
        sys.exit(1)
    
    with open(CATEGORIES_FILE, 'r') as f:
        data = json.load(f)
    
    # Group videos by primary category
    by_category = {}
    for video in data["videos"]:
        cat = video.get("primary_category", "UNKNOWN")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(video)
        
        # Also add to secondary categories
        for sec_cat in video.get("secondary_categories", []):
            if sec_cat not in by_category:
                by_category[sec_cat] = []
            by_category[sec_cat].append(video)
    
    # Process
    categories_to_process = [single_category] if single_category else sorted(by_category.keys())
    
    for category in categories_to_process:
        if category not in by_category:
            print(f"Category '{category}' not found. Available: {list(by_category.keys())}")
            continue
        
        entries = by_category[category]
        print(f"\n[{category}] — {len(entries)} videos")
        consolidate_category(category, entries)
    
    print(f"\nConsolidation complete! Files in {OUTPUT_DIR}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", type=str, help="Consolidate a single category")
    args = parser.parse_args()
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    run_consolidation(args.category)
