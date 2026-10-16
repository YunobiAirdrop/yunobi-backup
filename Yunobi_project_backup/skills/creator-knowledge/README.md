# Creator Knowledge Engine

**Extract a creator's entire YouTube library and transform it into reusable AI skills.**

> I watched 69 Kallaway videos so you don't have to. Then I taught an AI everything he knows.

---

## The Story

Kane Kallaway ([@kallawaymarketing](https://youtube.com/@kallawaymarketing)) went from 0 to 1M followers in under a year. Billions of views. And he documented every framework, psychology hack, and content system he used along the way — across 69 YouTube videos totaling 50+ hours of content.

The problem? Nobody has 50 hours to watch, take notes, cross-reference frameworks, and build a system from scattered video lessons.

So we built a pipeline that does it automatically:

1. **Fetched** all 69 transcripts via API
2. **Categorized** each video into 7 knowledge domains using AI
3. **Consolidated** each domain into a single reference document — extracting every framework, template, anti-pattern, and metric
4. **Generated** 7 Claude Skills that encode Kallaway's methodology
5. **Packaged** them as installable `.skill` files

The result: **4,180+ lines of distilled knowledge** across 7 skills, with 90+ frameworks you can apply immediately to DeFi, AI, tech, or any niche — in English or Spanish.

---

## The 7 Skills

| Skill | What It Does | Key Frameworks | Size |
|-------|-------------|----------------|------|
| **kallaway-hooks** | Write viral hooks using 6 archetypes + psychology | Three-Step Formula, 6 Archetypes, Desire-Based Hooks, Fear Framework | 235 + 746 ref |
| **kallaway-storytelling** | Script complete videos with narrative structure | Story Ladder (6 levels), Dopamine Ladder, Story Loops, But/Therefore | 339 + 766 ref |
| **kallaway-virality** | Validate ideas for viral potential before producing | Virality Formula, 9 Content Attributes, Outlier Research, Content Diagnostic | 374 + 589 ref |
| **kallaway-packaging** | Create high-CTR titles, thumbnails, and angles | 3-Step Psychology Flow, 7 Stun Gun Categories, Trust Score Model | 280 + 211 ref |
| **kallaway-content-system** | Design production workflows and content machines | Bad Sampling Model, Idea Trinity, Content Seasons, SuperUGC | 339 + 961 ref |
| **kallaway-monetization** | Build creator business revenue models | Creator Money Ladder, Internet Money Machine, Modern Marketing Funnel | 309 + 419 ref |
| **kallaway-platform-strategy** | Optimize content per platform and algorithm | Two Games Framework, Fan Funnel, Trust Equation, Game Theory Playbook | 331 + 692 ref |

---

## Quick Start

> **👋 Don't code? Start here:** [QUICKSTART.md](QUICKSTART.md) — step-by-step guide for non-technical creators (use it with Claude.ai, no terminal required).

### Install All Skills

```bash
git clone https://github.com/anthonysurfermx/creator-knowledge-engine.git
cd creator-knowledge-engine

# Install all 7 skills into Claude Code
for f in packaged/*.skill; do
  claude skill install "$f"
done
```

### Use Them

Just talk to Claude naturally. The skills auto-trigger based on what you ask:

- *"Write me 3 hook variations for a video about DeFi yield farming"* -> kallaway-hooks
- *"Is this video idea viral enough? Topic: How AI is replacing content agencies"* -> kallaway-virality
- *"Write a complete script for a 60-second Reel about Bitcoin L2s"* -> kallaway-storytelling
- *"Design a thumbnail concept for my YouTube video about Claude Code"* -> kallaway-packaging
- *"How should I monetize my 50K follower AI content brand?"* -> kallaway-monetization
- *"I'm posting on LinkedIn, Twitter, and YouTube -- what's my optimal strategy?"* -> kallaway-platform-strategy
- *"Build me a weekly content production workflow for a 1-person team"* -> kallaway-content-system

---

## The Full Video Catalog (69 Videos)

Every video Kallaway has published, categorized and rated by importance.

### HOOKS (7 videos)

| Video | Score |
|-------|-------|
| [I Studied 100 Viral Hooks, These 6 Will Make You Go Viral](https://youtube.com/watch?v=xnOe8aA9Pmw) | 5/5 |
| [How to Create a Killer Hook (Impossible to Skip)](https://youtube.com/watch?v=onQoYdxWXdA) | 5/5 |
| [Give me 15 mins, and I'll make your hooks impossible to skip](https://youtube.com/watch?v=2byPP_9F0-Q) | 5/5 |
| [How to Create Irresistible Hooks (and blow up your content)](https://youtube.com/watch?v=LmXpbP7dD48) | 5/5 |
| [If You Don't Understand Psychology, You Don't Understand Social Media](https://youtube.com/watch?v=7pCEsr-0KIw) | 5/5 |
| [Copy This Hook, It'll Blow Up Your Social Media](https://youtube.com/watch?v=8VolLwMCLuY) | 4/5 |
| [How to use psychology to hack viewers brains (& make more money)](https://youtube.com/watch?v=IywTdYKncqY) | 4/5 |

### STORYTELLING (14 videos)

| Video | Score |
|-------|-------|
| [6 Levels of Storytelling Every Creator MUST Master](https://youtube.com/watch?v=9K1b6dSdc50) | 5/5 |
| [How To Become A Master Storyteller](https://youtube.com/watch?v=t5Z-Q1bg1tU) | 5/5 |
| [How To Write A Killer Script That Keeps Viewers Hooked](https://youtube.com/watch?v=7I50PECz7SU) | 5/5 |
| [How to Become a Storytelling Genius (Dopamine Ladders)](https://youtube.com/watch?v=jtmstMt4WLc) | 5/5 |
| [How to Script Viral Videos 10x Faster (Nobody Teaches This)](https://youtube.com/watch?v=_Z11mjFh2zY) | 5/5 |
| [Say This in Your Videos, It'll Improve Your Storytelling by 10x](https://youtube.com/watch?v=pcnrzBwoVUk) | 5/5 |
| [Storytelling Is Easier Than You Think](https://youtube.com/watch?v=SDHKQbKC7gA) | 5/5 |
| [7 Storytelling Mistakes That Are KILLING Small Creators](https://youtube.com/watch?v=wgXGimZvDa4) | 4/5 |
| [Give me 18 minutes, and I'll improve your video by 193%](https://youtube.com/watch?v=i7upRL4H1FM) | 4/5 |
| [How to Make Addictive Videos (and blow up your social media)](https://youtube.com/watch?v=p4W23V_LLvE) | 4/5 |
| [How to Master the Art of Speaking (and blow up your content)](https://youtube.com/watch?v=35SPFdc1eXY) | 4/5 |
| [How to write a script so good viewers can't stop watching](https://youtube.com/watch?v=0f6_pRAIJjI) | 4/5 |
| [Speaking Like This Gives You an Unfair Advantage on Social Media](https://youtube.com/watch?v=ZM3elcBE48I) | 4/5 |
| [Watch Me Write a VIRAL Tiktok Script (Full Breakdown)](https://youtube.com/watch?v=_GGVRM0nQy8) | 4/5 |

### VIRALITY (7 videos)

| Video | Score |
|-------|-------|
| [How I Got 46 Million Views From ONE Short-Form Video (Copy Me)](https://youtube.com/watch?v=VEcU_VnlX7c) | 5/5 |
| [I Made 367 Videos and Here's What I Discovered](https://youtube.com/watch?v=yrqysKjqtfw) | 5/5 |
| [The Science-Based Method To Create Irresistible Ideas](https://youtube.com/watch?v=pirnGDCZD3Y) | 5/5 |
| [This Video Will Change How You View Social Media](https://youtube.com/watch?v=_60qFNsymcs) | 5/5 |
| [Why Your Content Isn't Getting Views (and how to fix it)](https://youtube.com/watch?v=YD2vbag4X8Y) | 5/5 |
| [Everything you know about content is (probably) wrong](https://youtube.com/watch?v=acEJRhZBSVk) | 4/5 |
| [The 'Viral' Trap, Explained](https://youtube.com/watch?v=vb-2eZX_B0M) | 4/5 |

### PACKAGING (2 videos)

| Video | Score |
|-------|-------|
| [How to Create Irresistible Thumbnails (and blow up your content)](https://youtube.com/watch?v=Iqy644uOOqM) | 5/5 |
| [Why The Smartest Creators I Know Focus on Packaging, Not Content](https://youtube.com/watch?v=jZCupmAOMAE) | 5/5 |

### CONTENT SYSTEM (13 videos)

| Video | Score |
|-------|-------|
| [How Steven Bartlett Built a Content Machine That Makes $25M/Year](https://youtube.com/watch?v=wjQpFgLRSCw) | 5/5 |
| [I Failed at Social Media, Until I Understood This](https://youtube.com/watch?v=MP0eEXUjhhs) | 5/5 |
| [I Studied 10,000+ Videos, These Mistakes Are Killing Your Content](https://youtube.com/watch?v=tVZOS5Z019U) | 5/5 |
| [It took me 1,000+ hours to learn this about content, but I'll teach you in 31 minutes](https://youtube.com/watch?v=Xz0H6TA9F6A) | 5/5 |
| [6 Content Mistakes That Are KILLING Small Creators (Nobody Teaches This)](https://youtube.com/watch?v=cAEYGdSnt9M) | 4/5 |
| [Brutally Honest Truths That Give You an Unfair Advantage on Social Media](https://youtube.com/watch?v=viT-_SjCs5I) | 4/5 |
| [Do THIS To Blow Up Your Brand in 2025 (SuperUGC Strategy)](https://youtube.com/watch?v=Aca1lAe0Mgo) | 4/5 |
| [How to Blow Up on Social Media (even if you don't have time)](https://youtube.com/watch?v=_GPSfzoVvC4) | 4/5 |
| [How to Create Any Content 10x Faster With AI](https://youtube.com/watch?v=1q__Vs2JqbI) | 4/5 |
| [I Tested 100+ AI Tools, These 9 Will Blow Up Your Content](https://youtube.com/watch?v=_SpyH8wTA-4) | 4/5 |
| [Stop Playing Social Media on 'Hard Mode' (6 Cheat Codes to Win in 2025)](https://youtube.com/watch?v=YQeC4SXBqP4) | 4/5 |
| [How to Edit VIRAL Short-Form Videos (Step by Step)](https://youtube.com/watch?v=YmeqSYQi7g0) | 3/5 |
| [How to Reprogram Your Brain to Stop Overthinking](https://youtube.com/watch?v=8clpw1WgJ5g) | 3/5 |

### MONETIZATION (6 videos)

| Video | Score |
|-------|-------|
| [How To Make 6-Figures With Content In 2025 (Full Breakdown)](https://youtube.com/watch?v=ububZUnpi3E) | 5/5 |
| [How to Get Rich on Social Media (Without Luck, Time, or Being a Genius)](https://youtube.com/watch?v=Lf7ZXu4WiUs) | 5/5 |
| [How to WIN on Social Media as a Business Owner in 2026 (Nobody Teaches this)](https://youtube.com/watch?v=SnUZdT3EpPg) | 5/5 |
| [How To Make Money As A Creator From Day 1](https://youtube.com/watch?v=FFVlKn0CskI) | 4/5 |
| [Social Media Expert Breaks Down $100M Content Strategy (Full Case Study)](https://youtube.com/watch?v=8Js_X-64JSM) | 4/5 |
| [What I Learned After 1 Year Of Being A Full-Time Creator](https://youtube.com/watch?v=urR7yqZ6iDA) | 4/5 |

### PLATFORM STRATEGY (20 videos)

| Video | Score |
|-------|-------|
| [Game Theory Is The Cheat Code to Social Media](https://youtube.com/watch?v=o2nP0lfIsso) | 5/5 |
| [How I Grew from 0 to 100K Subscribers in 5 Months](https://youtube.com/watch?v=3y-WiiUaqb4) | 5/5 |
| [How I Grew from 0 to 250,000 Subscribers in 1 Year](https://youtube.com/watch?v=z8j3PupS5gc) | 5/5 |
| [How Social Media Algorithms Actually Work (And How to Beat Them)](https://youtube.com/watch?v=8cQidXgtGmU) | 5/5 |
| [How to ACTUALLY Grow on Social Media in 2025 (Evidence-Based)](https://youtube.com/watch?v=V923wjDhscA) | 5/5 |
| [How to Build a Cult-Like Personal Brand on Social Media](https://youtube.com/watch?v=auPtvaoibgk) | 5/5 |
| [Social Media Has an AI Problem](https://youtube.com/watch?v=bjiqj-fxFPw) | 5/5 |
| [Social Media Is A Video Game (Here Are The Cheat Codes)](https://youtube.com/watch?v=sCcU6eKY8iQ) | 5/5 |
| [Social Media Is About to Change Forever](https://youtube.com/watch?v=Vcqgw5zWtDQ) | 5/5 |
| [THIS is how social media will change in 2025](https://youtube.com/watch?v=ONquL-tGn-M) | 5/5 |
| [The Easiest Way to Make Viral Content (For ANY Business)](https://youtube.com/watch?v=mbX4W5G0BPs) | 5/5 |
| [The Future Of Social Media Is Here](https://youtube.com/watch?v=vX-inQa3MKk) | 5/5 |
| [44 Tricks To Instantly Get More Views on Social Media](https://youtube.com/watch?v=u7Sb-GIdBqw) | 4/5 |
| [AI is About to Change Social Media Forever. Be Prepared](https://youtube.com/watch?v=DSDNiug5EH4) | 4/5 |
| [How to Speedrun Social Media](https://youtube.com/watch?v=fk6LExgMPxI) | 4/5 |
| [If I Started Social Media From Scratch in 2026, I'd Do This](https://youtube.com/watch?v=o_n5ED5fE1I) | 4/5 |
| [Linkedin Shorts Is A Cheat Code For Fast Growth & More Leads](https://youtube.com/watch?v=3Do4jRaVq40) | 4/5 |
| [Social Media Is Evolving](https://youtube.com/watch?v=AsKD_YPxnbw) | 4/5 |
| [Social Media Is Now On 'Easy Mode'](https://youtube.com/watch?v=I4bES-sGzdM) | 4/5 |
| [The NEW Way to Win On Social Media in 2025](https://youtube.com/watch?v=maS69HnjXME) | 4/5 |

---

## By the Numbers

| Metric | Value |
|--------|-------|
| Videos processed | 69 |
| Total transcript content | 1.8 MB |
| Categories | 7 |
| Consolidated reference lines | 4,298 |
| SKILL.md total lines | 2,207 |
| Reference doc total lines | 4,266 |
| Packaged .skill files | 7 |
| Frameworks extracted | 90+ |
| Templates (copy-paste ready) | 50+ |
| Anti-patterns documented | 80+ |

---

## Adapt It For Any Creator

This pipeline works for any YouTube creator. Swap the channel handle and categories:

1. Update `scripts/01_fetch_transcripts.py` with the new channel
2. Adjust the 7 categories in `scripts/02_categorize.py` to match the creator's domains
3. Run the pipeline

The architecture is creator-agnostic. The Kallaway skills are the first implementation.

---

## Credits

- **Kallaway** ([@kallawaymarketing](https://youtube.com/@kallawaymarketing)) -- All frameworks, methods, and knowledge come directly from his YouTube content
- **Transcript API** -- [downloadyoutubetranscripts.com](https://www.downloadyoutubetranscripts.com/) for transcript extraction
- **Built with** -- [Claude Code](https://claude.ai/claude-code) by Anthropic

---

## License

MIT. The skills encode Kallaway's publicly shared knowledge from YouTube. All credit for the frameworks and methodology belongs to him.

Built by [@anthonysurfermx](https://github.com/anthonysurfermx) as part of the Content Machine project.
