# Categorization Prompt

Use this prompt when manually categorizing transcripts with Claude Code instead of running the script.

## Usage

After placing transcripts in `data/raw-transcripts/`, tell Claude Code:

```
Read all transcripts in data/raw-transcripts/ and categorize each one into these 7 categories. Save results to data/categorized/categories.json.

Categories:
1. HOOKS — Hook archetypes, scroll-stopping, first 5 seconds, curiosity loops, re-hooking
2. STORYTELLING — Script structure, narrative arc, pacing, rhythm, story types, edutainment
3. VIRALITY — Virality formula, 6 ingredients, topic validation, timing, outlier scores
4. PACKAGING — Titles, thumbnails, angles, positioning, keyword research, CTR
5. CONTENT_SYSTEM — Production workflow, batch creation, team structure, tools, consistency
6. MONETIZATION — Brand deals, own products, community building, distribution era, pricing
7. PLATFORM_STRATEGY — Short vs long form, platform-native, content minutes, YouTube SEO

For each transcript, extract:
- Primary category (exactly one)
- Secondary categories (0-2)
- Named frameworks mentioned
- Top 3 actionable principles
- Top 3 direct quotes
- Importance score (1-5)
- One paragraph summary
```

## For Consolidation

```
Take all transcripts classified as [CATEGORY] from categories.json, read them, and create a single consolidated reference document in data/consolidated/[category].md that includes:

1. Core Philosophy — fundamental principles
2. Frameworks — every named method with steps + examples
3. Templates — reusable fill-in-the-blank formulas
4. Anti-Patterns — what NOT to do
5. Real Examples — specific cases Kallaway references
6. Metrics — benchmarks and KPIs he mentions
7. Key Quotes — top 10 most impactful direct quotes

Only synthesize what's in the transcripts. Don't add outside knowledge.
```

## For Skill Building

```
Read the consolidated reference doc at data/consolidated/[category].md and create a Claude Skill at skills/kallaway-[category]/SKILL.md following the structure in CLAUDE.md. Keep SKILL.md under 500 lines, put detailed frameworks in references/ subdirectory. Include DeFi/AI/LATAM examples in Spanish and English.
```
