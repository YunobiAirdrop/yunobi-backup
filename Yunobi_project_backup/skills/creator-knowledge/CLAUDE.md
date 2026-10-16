# CLAUDE.md — Kallaway Knowledge Extraction System

## Project Purpose

Extract, categorize, and transform Kane Kallaway's (@kallawaymarketing) YouTube content into reusable Claude Skills for content marketing. The end goal is 7 specialized skills that encode Kallaway's frameworks, templates, and principles — applied to DeFi, AI, and LATAM market content creation.

## Project Owner

Anthony (@anthonysurfermx) — Founder of DeFi Mexico Hub. Bilingual content operation: LinkedIn (EN), Twitter/X (ES), YouTube (ES). Uses Claude Code Max with a Content Machine system that converts daily info consumption into multi-format output.

## Architecture

```
kallaway-knowledge-system/
├── CLAUDE.md                          ← You are here
├── scripts/
│   ├── 01_fetch_transcripts.py        ← Pull all 78 videos from @kallawaymarketing
│   ├── 02_categorize.py               ← AI-powered categorization into 7 categories
│   ├── 03_consolidate.py              ← Merge transcripts per category into reference docs
│   ├── 04_build_skills.py             ← Generate SKILL.md files from consolidated docs
│   └── 05_package_skills.sh           ← Zip each skill into .skill files
├── data/
│   ├── raw-transcripts/               ← Individual .txt files per video
│   │   └── manifest.json              ← Video metadata (title, url, views, duration)
│   ├── categorized/                   ← Transcripts sorted into category folders
│   │   └── categories.json            ← Classification results
│   └── consolidated/                  ← One reference doc per category
│       ├── hooks.md
│       ├── storytelling.md
│       ├── virality.md
│       ├── packaging.md
│       ├── content-system.md
│       ├── monetization.md
│       └── platform-strategy.md
├── skills/                            ← Final output — 7 Claude Skills
│   ├── kallaway-hooks/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── hook-archetypes.md
│   ├── kallaway-storytelling/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── kallaway-virality/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── kallaway-packaging/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── kallaway-content-system/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── kallaway-monetization/
│   │   ├── SKILL.md
│   │   └── references/
│   └── kallaway-platform-strategy/
│       ├── SKILL.md
│       └── references/
└── prompts/
    ├── categorize.md                  ← Prompt template for step 2
    ├── consolidate.md                 ← Prompt template for step 3
    └── skill-template.md              ← Base template for generating skills
```

## Pipeline — 5 Steps

### Step 1: Fetch Transcripts
**Script:** `scripts/01_fetch_transcripts.py`
**Input:** Channel URL `https://www.youtube.com/@kallawaymarketing`
**Output:** `data/raw-transcripts/` — 78 .txt files + `manifest.json`

Two methods available (pick one):

**Method A — TranscriptAPI MCP (preferred if configured)**
```bash
claude mcp add --transport http transcript-api https://transcriptapi.com/mcp
```
Then Claude Code can fetch transcripts directly via MCP tool calls. No script needed.

**Method B — Python script with youtube-transcript-api + scrapetube**
```bash
pip install youtube-transcript-api scrapetube
python scripts/01_fetch_transcripts.py
```
Uses free open-source libraries. No API key needed. May get rate-limited by YouTube.

**Method C — downloadyoutubetranscripts.com API**
Requires API key from https://www.downloadyoutubetranscripts.com/
Set env var: `export DYT_API_KEY=your_key`

**Method D — Manual upload**
If transcripts were downloaded from the web UI, place the file(s) in `data/raw-transcripts/` and run:
```bash
python scripts/01_fetch_transcripts.py --parse-bulk data/raw-transcripts/bulk_transcripts.txt
```
This parses a concatenated bulk file into individual transcript files.

### Step 2: Categorize
**Script:** `scripts/02_categorize.py`
**Input:** `data/raw-transcripts/`
**Output:** `data/categorized/categories.json`

Reads every transcript and classifies it into one primary category + up to 2 secondary categories. Uses the Anthropic API (Claude) for classification.

**The 7 Categories:**
| ID | Category | What belongs here |
|----|----------|-------------------|
| 1 | HOOKS | Hook archetypes, scroll-stopping, first 5 seconds, curiosity loops, re-hooking |
| 2 | STORYTELLING | Script structure, narrative arc, pacing, rhythm, story types, edutainment |
| 3 | VIRALITY | Virality formula, 6 ingredients, topic selection, timing, outlier scores |
| 4 | PACKAGING | Titles, thumbnails, angles, positioning, keyword research, CTR optimization |
| 5 | CONTENT_SYSTEM | Production workflow, batch creation, team structure, tools, consistency |
| 6 | MONETIZATION | Brand deals, own products, community building, distribution era, pricing |
| 7 | PLATFORM_STRATEGY | Short vs long form, platform-native, content minutes, YouTube SEO, algorithm |

### Step 3: Consolidate
**Script:** `scripts/03_consolidate.py`
**Input:** `data/categorized/` + `data/raw-transcripts/`
**Output:** `data/consolidated/` — 7 markdown files

For each category, merges all classified transcripts into a single structured reference document:
- Fundamental principles
- Named frameworks with steps + examples
- Reusable templates
- Anti-patterns (what NOT to do)
- Real examples Kallaway mentions
- Metrics / benchmarks

### Step 4: Build Skills
**Script:** `scripts/04_build_skills.py`
**Input:** `data/consolidated/`
**Output:** `skills/*/SKILL.md` + `skills/*/references/*.md`

Generates Claude Skill files from consolidated docs. Each skill follows this structure:

```yaml
---
name: kallaway-[category]
description: "Trigger description — when to use this skill..."
---
# [Category] — Kallaway Method
## Core Philosophy
## Frameworks
## Process
## Anti-Patterns
## Output Format
## Application to DeFi/AI/LATAM
```

SKILL.md must stay under 500 lines. Detailed frameworks go in `references/`.

### Step 5: Package
**Script:** `scripts/05_package_skills.sh`
**Output:** 7 `.skill` files ready to install

```bash
for skill_dir in skills/kallaway-*/; do
  skill_name=$(basename "$skill_dir")
  cd skills && zip -r "../${skill_name}.skill" "$skill_name/" && cd ..
done
```

## Key Frameworks from Kallaway (Known from Research)

These are confirmed through public sources. Transcripts will reveal many more.

### 6 Hook Archetypes
1. Fortune Teller — future predictions
2. Experimenter — process/experiment shows
3. Teacher — methods/solutions
4. Magician — visual/audio stun
5. Investigator — secrets/hidden insights
6. Contrarian — challenge conventional wisdom

### 4 Hook Components (must align)
- Visual hook (what you show)
- Spoken hook (what you say)
- Text hook (overlay on screen)
- Audio hook (sound/music)

### 6 Ingredients of Virality
5 controllable + luck. Common idea first-to-market vs uncommon angle. Source ideas from under-viewed places.

### Re-Hooking Pattern
Setup → Rehook → Setup → Rehook → Final hook (for shares)

### Content Minutes Framework
Accumulated watch time needed for a stranger to become a superfan. Short-form = thousands of reps. Long-form = faster trust building.

### Distribution Era Thesis
"2025+: Content is hard, products are easy." Distribution > building. Own product > brand deals.

## Skill Writing Rules

When generating SKILL.md files, follow these rules:
- Frontmatter: `name` and `description` are required
- Description should be "pushy" — list many trigger phrases so Claude uses the skill
- SKILL.md body: under 500 lines
- Detailed content goes in `references/` subdirectory
- Use imperative form in instructions
- Include examples with Input/Output format
- Define explicit output formats Claude should follow
- Add anti-patterns section (what NOT to do)
- Include DeFi/AI/LATAM niche application section
- Spanish and English templates where applicable

## Environment

- Python 3.10+
- Dependencies: `youtube-transcript-api`, `scrapetube`, `anthropic` (for categorization)
- Optional MCP: `transcript-api` at `https://transcriptapi.com/mcp`
- API keys needed: `ANTHROPIC_API_KEY` (for categorization step)
- Optional: `TRANSCRIPT_API_KEY` from transcriptapi.com

## Commands Quick Reference

```bash
# Full pipeline
python scripts/01_fetch_transcripts.py
python scripts/02_categorize.py
python scripts/03_consolidate.py
python scripts/04_build_skills.py
bash scripts/05_package_skills.sh

# Or if transcripts already downloaded manually:
python scripts/01_fetch_transcripts.py --parse-bulk data/raw-transcripts/all_transcripts.txt

# Individual video test
python scripts/01_fetch_transcripts.py --video-id VIDEO_ID

# Re-categorize a single transcript
python scripts/02_categorize.py --file data/raw-transcripts/specific_video.txt
```

## Quality Checks

After building skills, verify:
- [ ] Each SKILL.md has valid YAML frontmatter
- [ ] Each SKILL.md is under 500 lines
- [ ] Each skill has at least one reference doc in references/
- [ ] Descriptions include trigger phrases for the target use cases
- [ ] Anti-patterns section exists in every skill
- [ ] Output format section defines exact structure Claude should produce
- [ ] DeFi/AI/LATAM application section exists with Spanish + English templates
- [ ] No hallucinated frameworks — everything comes from actual transcripts
