---
name: programmatic-seo
description: "The SEO and AI-search pipeline for one person: what page to write next, keyword and prompt research, the page itself, and the off-site mentions that decide whether an assistant names you. Use on 'SEO', 'AEO', 'GEO', 'rank on Google', 'get cited by ChatGPT', or keyword research."
tags: [plans, seo]
---

# Programmatic SEO

One person, a keyword file and a loop. The pipeline below produced 28 English articles and 112
pages across four languages on `getseam.app`, running at 180,000 impressions and 3,400 clicks over
three months. The order matters more than any single step: read where the brand already stands,
judge the cluster before entering it, write the three shapes that rank, then feed the result back.

## The split that reorders everything

**58.5% of Google searches now end without a click to anyone, and an AI Overview costs the
number-one page 58% of its clicks.** There is no rebound coming: Google answers on the page on
purpose, because the alternative is losing the user to an assistant. The numbers, the sources and
the HubSpot case that settles the traffic-versus-revenue argument:
[references/measurement.md](references/measurement.md).

So every target sorts into one of two jobs, on one question: **can an assistant fully satisfy this
searcher on the results page?** Answer it against a real SERP, never from the keyword's shape. That
is the AI filter, and it runs in Phases 2 and 3.

- **No, so earn the click.** Anything the searcher has to *do* rather than know: tools and
  calculators, transactional and commercial queries, and everything local. This lane is intact and
  traditional SEO works in it exactly as it always did.
- **Yes, so earn the mention.** Informational queries, question phrasings, long multi-clause asks.
  You will not get the click. You can be the brand named inside the answer, and that is won off
  your own site more than on it.

## Ranking and being cited are two scoreboards, and the gap is widening

**Do not plan the mention lane by planning to rank.** Traditional SEO is the foundation and is no
longer close to sufficient: ranking first gives roughly a 31% chance of appearing in an AI answer,
and most AI citations go to pages outside Google's top ten. One controlled split test moved LLM
traffic up and Google traffic down from the same single change. Six independent readings of the
overlap: [references/geo-signals.md](references/geo-signals.md).

Two consequences the whole pipeline runs on:

- **The unit is the brand, not the URL.** A model is deciding which company to name, not ordering
  pages. Ranking is an ingredient, and a site can hold position one and never be named.
- **Citation is probabilistic.** Ask the same question five times and you may be named three, so
  the metric is share of voice across many runs and a rank tracker aimed at prompts measures
  nothing.

AEO, GEO and LLMO name the same work. Sell it under the label the buyer already budgets for: a
client with a separate GEO line item does not hand it to the supplier who says the category does
not exist.

## Prerequisites

Search Console access (`gcloud auth application-default login` with the webmasters scope, per the
`search-console` skill). Nothing else: autocomplete is keyless from Google and volume comes from
the Keyword Planner, both free. `SERPER_API_KEY` is optional.
Keep one copy in your own env file and export it before the scripts run.
**Before writing against a paid SEO endpoint, check what it resells:** volume and autocomplete are
free at the source. Costs, coverage limits and the rule: [references/tooling.md](references/tooling.md).

## Phase 0. Harvest the console

Skip only when the site has no Search Console history. Everywhere else it beats keyword research:
Google has already told you which queries it associates with the domain.

```bash
GSC="python3 <search-console-skill>/scripts/gsc.py"
$GSC orphans <site> --days 90      # queries you rank for with no page targeting them
$GSC cannibals <site> --days 90    # queries your own pages are splitting
```

One run on `getseam.app` surfaced a query split across three of its own pages at 20,448 impressions
and position 9.1, plus five variants with no exact page. It pays for itself before a tool is opened.

**Run `cannibals` before Phase 2: a site can be losing the head query to itself, and no new page
fixes that.** `airtabletosheets.com` held position 66 to 71 on every head query while its own blog
posts held 7 to 31, because three pages split each one and the largest was `/setup`. A utility page
must never carry the head phrase in its title. The read order and why to fix a split before adding
a page: [`workflows.md`](../search-console/references/workflows.md).

## Phase 1. Read where the brand already stands

Diagnosis before production. Ask the assistants the questions a buyer would ask, tally who gets
named, and sort what is missing into the six gap kinds (visibility, narrative, topic, format, web
mentions, demand), because the fix differs by kind and only one of them is a writing job. The
buckets, the fix-build-influence choice and the cadence:
[references/measurement.md](references/measurement.md).

**Run every prompt signed out, with history and custom instructions off, or the reading is
fiction.** An assistant tells the account what that account already believes, and the same prompt
from two accounts returns opposing answers on questions of fact. A client who has asked ChatGPT
about his category twenty times has trained it to agree with him, and will bring that screenshot to
the meeting; reproduce it cold before accepting it or arguing with it.

Read three things and none of them is a rank: whether the brand is **named**, whether the naming is
**accurate** (a confident wrong description is a loss, not a neutral), and **which sources the
answer cited**, because those pages are the real target list for Phase 6.

## Phase 2. Judge the cluster before you enter it

The step that saves the most work is the one that stops a cluster from being written at all. Four
tests, all of which must pass, and each of them has cost a real cluster when it was skipped:
winnable volume rather than total, **which** slots are winnable rather than whether any are, a
qualifier people actually type, and the AI filter. The four with their worked failures, which
clusters to own at all, ranking the audience segments before a keyword tool opens, and the prompt
research that replaces keyword research in the mention lane:
[references/content-strategy.md](references/content-strategy.md).

## Phase 3. Keyword research

```bash
python scripts/keyword-research.py -s "your keyword" --depth 3 --brief -o keywords.json
```

Autocomplete is free, keyless and branched across the alphabet, so a seed returns the tail rather
than five phrasings; `--no-serper` drops related searches and PAA, and the run costs nothing.
Supplement through WebSearch for `[keyword] reddit`, `[keyword] alternative` and
`how to [keyword]`. Save it to a file: the `getseam.app` file holds 197 keywords and still plans
every article seven months later.

Vet each candidate on business potential, intent and difficulty, then apply the AI filter. To find
the click-lane survivors in bulk, filter for transactional intent and include modifiers naming an
action: `calculator`, `checker`, `generator`, `tool`, `template`, `finder`, `planner`, `maker`.
Write in the vocabulary of the forum threads, not of the category: buyers type "sync" and
"automatically update" where competitor pages say "ETL", which is why they lose the long tail.

**Query length is the cleanest signal of which lane a term sits in**, and long qualified questions
are mention-lane targets by default; the trigger rates by word count are in
[references/geo-signals.md](references/geo-signals.md).

## Phase 4. Intent, then shape

Order the four things a person can be doing by how close they are to paying, deciding then shopping
then escaping then learning, and choose the intent before the volume: the four with examples, and
why `getseam.app`'s traffic leader converts worst on the site, are in
[references/content-strategy.md](references/content-strategy.md).

Three shapes did the ranking across the 28 articles: 12 comparisons, 6 alternative pages, 10 guides
and roundups. **The same three are what assistants cite**, because a list hands the model a
ready-made consensus: 43.8% of pages ChatGPT cites are listicles, and it is the one artefact both
lanes want.

- **Comparison, `You vs Them`.** Table in the first screen, real measured numbers in it, honest
  where you lose. One row, CPU during dictation at 12 per cent against 25.6, outperformed the
  page around it, because nobody else in the category measured anything.
- **Alternative, `Them alternative`.** Same reader, one step earlier and angrier.
- **Roundup, `Best X for Y`.** Has to list tools you do not own, or it reads as an advert.
- **Case study, `How we did X for a Y`.** The shape with no competition. A buyer describes their
  own situation to an assistant in a sentence no keyword tool has ever seen, and a page carrying
  that situation with numbers on it is the only thing that matches.

One page per intent. Write only the shape you can support.

## Phase 5. Draft, illustrate, publish

```bash
python scripts/generate-article.py --keyword "your keyword" --title "Your Title" --word-count 2000
```

Drafts land in `web/content/blog/drafts/`. Structure, frontmatter, brief inputs and image guidance:
[assets/article-template.md](assets/article-template.md).

**The draft is the input, never the output.** A generated page agrees with everything already
ranking, which is exactly what a summariser replaces with one paragraph. The test is whether the
page is *informationally additive*: read the top three results, then name what this page carries
that none of them does, your measurement, your customer's words, your screenshot, your opinion.
Without that, do not publish. Nothing else here matters more; 96% of the web gets zero Google
traffic mostly for failing it.

Then rewrite it so a machine can lift a paragraph out and have that paragraph still be true and
still name you. That craft, with the worked before-and-afters, is where most of the measurable
citation lift sits: [references/write-like-a-source.md](references/write-like-a-source.md). Run
[references/seo-checklist.md](references/seo-checklist.md) before anything goes live.

**Do not answer a thin site with volume.** Authority divides across the pages it has to cover, so a
small site publishing hundreds of generated pages dilutes what little it has and cannibalises
itself; the programmatic lane is for sites with authority to spend. Ramp the cadence, and translate
last and only what works: it took 28 articles to 112 pages at almost no cost, and multiplies a
mistake as fast.


## Phase 6. The off-site half, which is now the larger half

**Branded mentions on other people's pages correlate with AI visibility above backlinks, referring
domains and domain rating**, and most of what a model knows about a brand sits off the brand's own
domain. A page nobody else talks about is invisible to the mention lane however good it is. Three
tiers in order of value, editorial third parties, then Reddit and forums, then your own other
properties, with YouTube as the strongest single factor anyone has measured and a budget line of
its own. The tier playbook, the YouTube checklist, the digital-PR campaign that bought 60 national
links for about $100, the Reddit dispute, and why a pile of spam links you did not build is left
alone: [references/earning-mentions.md](references/earning-mentions.md). **Buying links in volume is
still the fastest way to lose a site**, and white-hat and black-hat practitioners agree on it.

Before it writes, an assistant runs searches of its own. Those fan-out queries brief the page that
wins, and the pages it retrieved and *did not* cite are the sharper half. Read them from a
logged-in conversation, never from the paid API, which scored an incumbent at zero in a category it
appears in nine times of 24: [references/fan-out.md](references/fan-out.md).

## Phase 7. Feed the result back

Wait for indexing, filter the console to the new URL, record position and impressions, and run
Phase 0 again before the next batch so the cheapest opportunities enter the queue first. Rank
tracking alone no longer describes the outcome: the scored per-site advisor report, the three
trackable AI signals and the four-layer correlation report are in
[references/measurement.md](references/measurement.md).

**When the target is local, the playbook diverges completely** and the zero-click argument above
does not apply: [references/local.md](references/local.md).

## Boundaries

Structured data mechanics: `seo-schema-markup`. Console queries and index state: `search-console`.
App stores: `aso`. Page copy: `page-copy`, with `humanizer` for the voice. SvelteKit blog
infrastructure: [references/blog-setup.md](references/blog-setup.md). Auditing an existing brand's
citation gaps prompt by prompt is the `ai-citation-strategist` agent: this skill builds and places
pages, that agent diagnoses why a competitor is named instead.

## Verification

- [ ] Every target sorted into a lane, with the AI filter run against a real SERP rather than
      guessed from the keyword's shape
- [ ] Any claim about AI visibility read from a signed-out session with history off
- [ ] The page carries something the top three results do not
- [ ] `write-like-a-source.md` applied, `seo-checklist.md` passed, no AI crawler blocked
- [ ] Off-site mention targets named, not just on-site work
- [ ] Each failure mode folded into the phase that would have caught it

## Closing a run

This skill appends new failure modes to its own pattern list after each run. A failure mode goes
into the phase that would have caught it; if no phase owns it, append it to Learned Patterns with
today's date before finishing.

## Learned Patterns

- 2026-09-06: Plan the mention lane separately from the ranking lane. Ranking first gives about a 31% chance of an AI citation, and most citations sit outside the top ten. [ask: consolidate GEO/AEO learnings into one skill]
- 2026-09-06: Read AI visibility signed out, history and memory off. A signed-in account returns what it has already been trained to agree with. [ask: consolidate GEO/AEO learnings into one skill]
- 2026-09-06: Where two studies disagree, carry both and say so. A contested number quoted flat becomes a client promise: schema's AI lift is one study for, two against. [ask: consolidate SEO learnings into one skill]
