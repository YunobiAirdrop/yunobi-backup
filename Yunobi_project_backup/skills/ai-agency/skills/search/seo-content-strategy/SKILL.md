---
name: seo-content-strategy
description: When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when the user mentions "content strategy," "what should I write about," "content ideas," "blog strategy," "topic clusters," or "content planning." For writing the individual pages, see programmatic-seo.
metadata:
  version: "1.0.0"
---

# Content Strategy

Plan content that drives traffic, builds authority, and generates leads by being searchable, shareable, or both.

## Before Planning

If `.claude/product-marketing-context.md` exists, read first. Only ask for what's not covered.

Gather:
1. **Business**. what the company does, ideal customer, primary content goal (traffic/leads/awareness/thought leadership), problems product solves
2. **Customer research**. pre-buying questions, sales-call objections, support ticket patterns, customer language
3. **Current state**. existing content performance, resources (writers, budget, time), formats available
4. **Competitors**. main competitors, content gaps
5. **Whose voice the content ships in**. Name the voice profile before planning, and carry one
   finding into the plan rather than into the drafting: **subject beats craft by a wide margin.**
   Measured over one operator's corpus, operations topics performed at 1.2x the median while
   identity and discipline topics performed at 5x. Run the same count on your own numbers, then
   check the pillar mix against it before committing the calendar, not after.

## Searchable vs Shareable

Every piece must be searchable, shareable, or both. Prioritize search. it's the foundation.

**Searchable**. captures existing demand, optimized for active searchers.

**Writing it:** target specific keyword/question · match intent exactly · titles match queries · headings mirror search patterns · keywords in title/headings/first paragraph/URL · full coverage of the topic · data, examples, authoritative links · AI/LLM discovery (clear positioning, structured content, brand consistency).

**Shareable**. creates demand, spreads ideas.

**Writing it:** novel insight, original data, or counterintuitive take · challenge conventional wisdom with reasoning · stories that make people feel · help others or make them look smart · connect to trends · vulnerable, honest experiences.

## Content Types

### Searchable

**Use-case content**. formula: [persona] + [use-case]. Long-tail keywords. "Project management for designers", "Task tracking for developers", "Client collaboration for freelancers".

**Hub and spoke**. hub = broad overview page, spokes = related subtopics.
```
/topic (hub)
├── /topic/subtopic-1 (spoke)
├── /topic/subtopic-2 (spoke)
└── /topic/subtopic-3 (spoke)
```
Create hub first, build spokes, interlink. Most content fits under `/blog`; use dedicated hub structures only for major topics with layered depth (e.g., Atlassian's `/agile` guide).

**Template libraries**. high-intent keywords + product adoption. Target "marketing plan template", provide standalone value, show product enhancement.

### Shareable

**Thought leadership**. name concepts people feel but haven't named, challenge with evidence, share honest experiences.

**Data-driven**. product data analysis (anonymized), public data patterns, original research.

**Expert roundups**. 15-30 experts answering one specific question. Built-in distribution.

**Case studies**. Challenge → Solution → Results → Key learnings.

**Meta content**. behind-the-scenes transparency. "How We Got Our First $5k MRR", "Why We Chose Debt Over VC".

For scaled content, see **programmatic-seo**.

## Pillars & Topic Clusters

Content pillars = 3-5 core topics your brand owns. Each spawns a cluster.

Most content can live under `/blog` with internal linking. Dedicated pillar pages only when building multi-layer resources.

**Identify pillars by:** product-led (problems you solve), audience-led (what ICP needs to learn), search-led (topics with volume), competitor-led (what they rank for).

```
Pillar Topic (Hub)
├── Subtopic Cluster 1 → Articles A, B, C
├── Subtopic Cluster 2 → Articles D, E, F
└── Subtopic Cluster 3 → Articles G, H, I
```

**Good pillars:** align with product · match audience care · have volume/interest · broad enough for many subtopics.

## Keyword Research by Buyer Stage

Map topics to the journey using modifiers:

- **Awareness**. "what is", "how to", "guide to", "introduction to". Example: "What is Agile Project Management", "How to Run a Standup".
- **Consideration**. "best", "top", "vs", "alternatives", "comparison". Example: "Best Project Management Tools for Remote Teams", "Asana vs Trello vs Monday", "Basecamp Alternatives".
- **Decision**. "pricing", "reviews", "demo", "trial", "buy". Example: "Project Management Tool Pricing Comparison", "[Product] Reviews".
- **Implementation**. "templates", "examples", "tutorial", "how to use", "setup". Example: "Project Template Library", "Step-by-Step Setup Tutorial".

## Ideation Sources

**1. Keyword data** (Ahrefs, SEMrush, GSC): group into topic clusters, tag buyer stage, classify intent, find quick wins (low competition + decent volume + relevant), spot gaps (competitors rank, you don't). Output: Keyword · Volume · Difficulty · Buyer Stage · Content Type · Priority.

**2. Call transcripts** (sales/customer): questions → FAQ/blog · pain points → problems in their words · objections → proactive content · language patterns → voice of customer · competitor mentions → comparison content. Output with supporting quotes.

**3. Survey responses**. open-ended topics and language · themes with 30%+ mentions = high priority · requested resources · format preferences.

**4. Forum research**
- **Reddit:** `site:reddit.com [topic]`. top posts, questions/frustrations, upvoted answers
- **Quora:** `site:quora.com [topic]`. most-followed questions, upvoted answers
- **Other:** Indie Hackers, Hacker News, Product Hunt, industry Slack/Discord
Extract: FAQs, misconceptions, debates, problems, terminology.

**5. Competitor analysis**. `site:competitor.com/blog`. Analyze top performers, repeated topics, gaps, case study patterns, content structure. Identify: topics you can cover better, missing angles, outdated content to improve.

**6. Sales & support input**. objections, repeated questions, ticket patterns, success stories, feature requests + underlying problems.

## Prioritizing Ideas

Score on four factors:

1. **Customer Impact (40%)**. frequency in research, % of customers affected, emotional weight, LTV potential
2. **Content-Market Fit (30%)**. aligns with product problems, unique insights available, customer stories, leads to product interest
3. **Search Potential (20%)**. volume, competition, long-tail opportunities, trend
4. **Resource Requirements (10%)**. expertise available, research needed, assets required

| Idea | Impact (40%) | Fit (30%) | Search (20%) | Resources (10%) | Total |
| --- | --- | --- | --- | --- | --- |
| Topic A | 8 | 9 | 7 | 6 | 8.0 |
| Topic B | 6 | 7 | 9 | 8 | 7.1 |

## Output Format

**1. Content pillars**. 3-5 with rationale, subtopic clusters, connection to product.

**2. Priority topics (per piece):** topic/title · searchable/shareable/both · type (use-case, hub/spoke, thought leadership) · target keyword + buyer stage · why (research backing).

**3. Topic cluster map**. visual or structured representation.

## Diagnostic Questions

1. Patterns from last 10 customer conversations?
2. Recurring sales-call questions?
3. Where are competitors falling short?
4. Unique customer research insights not yet shared?
5. Which existing content drives conversions, and why?

## Related Skills

- **programmatic-seo**. the research, the page itself and scaled generation
- **seo-schema-markup**. the structured data once a page is written
- **search-console**. what the plan actually earned
- **generate-social**. social media
