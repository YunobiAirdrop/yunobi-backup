#!/usr/bin/env python3
"""
Step 2: Categorize transcripts into 7 knowledge categories using Claude.

Usage:
    python scripts/02_categorize.py
    python scripts/02_categorize.py --file data/raw-transcripts/specific_video.txt

Requires: ANTHROPIC_API_KEY environment variable

Output:
    data/categorized/categories.json
"""

import argparse
import json
import os
import sys
from pathlib import Path

DATA_DIR = Path("data/raw-transcripts")
OUTPUT_DIR = Path("data/categorized")
OUTPUT_FILE = OUTPUT_DIR / "categories.json"

CATEGORIES = {
    "HOOKS": "Hook archetypes, scroll-stopping techniques, first 5 seconds, curiosity loops, re-hooking, hook psychology, 4 hook components, opening lines",
    "STORYTELLING": "Script structure, narrative arc, pacing, rhythm, story types (case study, breakdown, listicle), edutainment, Missy Elliott method, body of video",
    "VIRALITY": "Virality formula, 6 ingredients, topic validation, timing, outlier scores, what makes content spread, uncommon angles, trend analysis",
    "PACKAGING": "Titles, thumbnails, topic selection, angles, positioning, keyword research, CTR optimization, curiosity gap in packaging, search vs browse",
    "CONTENT_SYSTEM": "Production workflow, batch creation, team structure, tools, consistency cadence, content machine, automation, repurposing",
    "MONETIZATION": "Brand deals, own products, community building, The Academy, distribution era thesis, pricing, revenue models, creator economy business",
    "PLATFORM_STRATEGY": "Short vs long form, platform-native content, content minutes, YouTube SEO, algorithm, TikTok vs YouTube vs Instagram, repurposing clips"
}

CATEGORIZE_PROMPT = """Analyze this YouTube video transcript from Kallaway (@kallawaymarketing) and classify it.

CATEGORIES:
{categories}

TRANSCRIPT:
---
{transcript}
---

Respond in this exact JSON format (no markdown, no backticks, just raw JSON):
{{
    "primary_category": "CATEGORY_NAME",
    "secondary_categories": ["CATEGORY_NAME_2"],
    "frameworks_mentioned": ["Framework Name 1", "Framework Name 2"],
    "key_principles": ["principle 1", "principle 2", "principle 3"],
    "top_quotes": ["exact quote 1", "exact quote 2", "exact quote 3"],
    "importance_score": 4,
    "summary": "One paragraph summary of what this video teaches"
}}

Rules:
- primary_category: exactly ONE from the list above
- secondary_categories: 0-2 additional categories that also apply
- frameworks_mentioned: named frameworks, methods, or systems Kallaway references
- key_principles: the most important actionable takeaways
- top_quotes: 3 most impactful direct quotes from the transcript
- importance_score: 1-5, how critical this video is for building skills (5 = essential)
- summary: concise paragraph of the video's teaching
"""


def categorize_transcript(transcript_text: str, filename: str) -> dict:
    """Send transcript to Claude for categorization."""
    try:
        import anthropic
    except ImportError:
        print("Install: pip install anthropic")
        sys.exit(1)
    
    client = anthropic.Anthropic()
    
    # Format categories for prompt
    cats_text = "\n".join([f"- {k}: {v}" for k, v in CATEGORIES.items()])
    
    # Truncate very long transcripts to avoid token limits
    max_chars = 80000
    if len(transcript_text) > max_chars:
        transcript_text = transcript_text[:max_chars] + "\n\n[TRANSCRIPT TRUNCATED]"
    
    prompt = CATEGORIZE_PROMPT.format(
        categories=cats_text,
        transcript=transcript_text
    )
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = response.content[0].text.strip()
    
    # Parse JSON response
    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = {"error": "Failed to parse response", "raw": response_text}
    
    result["source_file"] = filename
    return result


def run_categorization(single_file: str = None):
    """Categorize all transcripts or a single file."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load existing results if any
    existing = {}
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as f:
            data = json.load(f)
            existing = {item["source_file"]: item for item in data.get("videos", [])}
    
    # Get files to process
    if single_file:
        files = [Path(single_file)]
    else:
        files = sorted(DATA_DIR.glob("*.txt"))
    
    results = list(existing.values())
    
    for filepath in files:
        if filepath.name == "manifest.json":
            continue
        
        if filepath.name in existing and not single_file:
            print(f"  SKIP (already categorized): {filepath.name}")
            continue
        
        print(f"  Categorizing: {filepath.name}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            result = categorize_transcript(content, filepath.name)
            
            # Remove old entry if re-categorizing
            results = [r for r in results if r.get("source_file") != filepath.name]
            results.append(result)
            
            print(f"    → {result.get('primary_category', 'UNKNOWN')} "
                  f"(importance: {result.get('importance_score', '?')}/5)")
        except Exception as e:
            print(f"    ERROR: {e}")
            results.append({"source_file": filepath.name, "error": str(e)})
    
    # Save results
    output = {
        "channel": "@kallawaymarketing",
        "total_videos": len(results),
        "category_counts": {},
        "videos": sorted(results, key=lambda x: x.get("source_file", ""))
    }
    
    # Count by category
    for r in results:
        cat = r.get("primary_category", "UNKNOWN")
        output["category_counts"][cat] = output["category_counts"].get(cat, 0) + 1
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nCategorization complete! Results: {OUTPUT_FILE}")
    print("Category distribution:")
    for cat, count in sorted(output["category_counts"].items()):
        print(f"  {cat}: {count} videos")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="Categorize a single file")
    args = parser.parse_args()
    
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    run_categorization(args.file)
