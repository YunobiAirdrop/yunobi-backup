# What actually earns an AI citation, measured

The evidence file for the AI-search half of `SKILL.md`. Every number here is somebody's published
study, attributed, because the field is full of confident claims with nothing under them. Where two
studies disagree, both are here and the disagreement is the finding.

**Weight follows independent agreement.** A finding that four unconnected studies reach is worth
building a quarter on; a finding one vendor reports about its own customers is worth a test. Each
section says which it is.

Sources: Ahrefs' AEO research (75,000 brands, 174,000 cited pages, 140M robots.txt files), NP
Digital (500 commercial keywords, 4,300 prompts), SearchPilot's controlled split tests, Google's
own AI mode usage report, Princeton's GEO paper (KDD 2024, run against Perplexity), SE Ranking,
ZipTie (400,000 pages), Seer Interactive with Nectaf, SparkToro with Datos, Conductor.

## How the machine assembles an answer

Two sources feed a response and they are influenced by different work. **Training data** is a
frozen snapshot refreshed on the order of months, and you reach it only by being mentioned widely
enough, for long enough, that the brand is baked in. **Retrieval** is a live search fired at answer
time, and you reach it with ordinary SEO plus the technical checks below. A brand that launched
last week can win retrieval this week and cannot win training for a year.

**One prompt becomes many searches.** The assistant does not look up what the buyer typed. It fans
the prompt out into sub-queries and runs them at once: 9 to 11 on average (Seer/Nectaf), as high as
28, and ChatGPT's deep research mode was measured at 420 searches for one shopping prompt.

Three consequences, and they are the whole strategy:

1. **Topic coverage beats keyword targeting.** A page that answers one query in a fan-out loses to
   a page that answers most of it. One page, one target keyword is a losing shape.
2. **Fan-out queries are not a keyword list.** Over 95% carry zero search volume, they are
   generated in the moment, and the same prompt fans out differently on the next run. Read them as
   a brief, never as targets. Harvesting them from a real session: [fan-out.md](fan-out.md).
3. **Citation is probabilistic, not a ranking.** Ask the same question five times and you may be
   named three times. Roughly 40% of prompts return the same answer on a second run. There is no
   position to hold, so the metric is share of voice across many runs, never a rank, and a rank
   tracker aimed at prompts is measuring an object that does not exist.

## Ranking is the foundation and it is not the mechanism

This is the finding that moved most, and it moved in one direction across every independent
reading. Treat the old "rank first and citations follow" line as retired.

| Reading | Overlap between ranking and being cited | Source |
| --- | --- | --- |
| AI Overview citations that came from Google's top 10 | 76%, and a later measurement puts it near 38% | Ahrefs, twice |
| AI Overview citations from pages not in Google's top 100 at all | 14% | Ahrefs |
| Chance of appearing in an AI answer when you rank #1 | **31%**, falling to 2.6% by rank 4 | NP Digital, 4,300 prompts |
| AI citations going to sources outside Google's top 10 | **75%** | NP Digital |
| Sources cited inside AI mode answers that rank top 10 for the same query | **under 10%** | Google's own AI mode report |
| ChatGPT-cited pages that do not rank in Google's top 100 | 80% | Ryan Robinson, citing platform data |
| ChatGPT's own overlap with Google's top 10 | 8 to 10% | Ahrefs |

The readings disagree on the number and agree on the shape: **the two scoreboards have separated,
and a site can hold position one in its category and never be named.** When that happens the
missing input is almost always off-page validation rather than anything on the page.

**And the two can actively conflict.** SearchPilot ran controlled split tests on a travel site,
same template, one change at a time, with a control group to factor out seasonality and algorithm
updates. Adding a brand-USP module was positive for LLM traffic and inconclusive for Google, so it
shipped. Adding substantial extra explanatory copy was **statistically positive for LLM traffic and
statistically negative for Google**, both bounds clear of zero. Google was 10 to 100 times larger
for that site, so the change was not shipped. Two things follow: the lanes are not one lane, and a
change that helps one can be a real cost in the other. Where the trade-off appears, iterate for the
version that keeps the LLM gain without the Google loss rather than picking a side once.

Statistical testing at that grade needs enterprise traffic. A small site's edge is pace of
execution and quality of ideas, not a significance threshold it can never reach; read the published
results from large sites instead of running underpowered tests of your own.

## Query length decides which lane a term is in

Overviews fire on 23% of one-to-three word queries, 48% at four or five, and 77% at six or more,
and separately on nearly 58% of question-phrased queries. So the long, qualified, multi-clause
questions that carry the most buying intent are almost always answered by a machine: they are
mention-lane targets by default, and depth of topic coverage is what wins them rather than a page
aimed at the phrase.

The inverse is the click lane's boundary. Overviews appear on about 21% of all keywords and 99.9%
of the ones that trigger them are informational, so anything the searcher has to *do* rather than
know is intact.

## The strongest signal is a mention on somebody else's page

Four independent sources reach this, and one of them is the CMO of the company that measured it.

In the 75,000-brand study, **branded web mentions correlate with AI Overview visibility at 0.664,
above backlinks, referring domains and domain rating.** Mentions on heavily linked pages reach
0.70. A German link-building agency puts the same finding the blunt way: about **85% of what an LLM
knows about a brand sits on third-party sites, not on the brand's own domain.** A separate reading
attributes about 84% of AI citations to user-generated and community sources.

Ahrefs' own line for the mechanism: links were how Google saw that other people vouched for a
site, and brand mentions are how a model sees it. The playbook that follows, the three tiers and
the campaigns that earn them: [earning-mentions.md](earning-mentions.md).

**Being mentioned and being linked are different outcomes.** Only about 28% of AI mentions carry a
link: Perplexity 51.6%, AI mode 36.8%, ChatGPT 26.9%, AI Overviews 10.7%. The unlinked seven in ten
still work: each one is another training example binding the brand to the topic. But they will
never appear in analytics. This is why [measurement.md](measurement.md) exists.

Weighted by search volume the picture improves: on Perplexity, links appear in 51% of mentions but
78% of impressions, and on Gemini in 16.8% of mentions but 71% of impressions. Citations are rare
and they cluster on the queries with the most eyeballs.

## What the cited page looks like

| Finding | Number | What it means |
| --- | --- | --- |
| Word count vs citation | r = 0.04 across 174,000 pages | Length is not a lever. **53.4% of cited pages are under 1,000 words** |
| Freshness | AI-cited pages are 25.7% fresher than pages ranking organically | For ChatGPT's top-cited pages, 89.7% were updated within the year and 76% within 30 days |
| Format | 43.8% of ChatGPT-cited pages are listicles | Best-X, top-X, versus and review pages. They hand the model a ready-made consensus |
| Churn | Over 45% of AI Overview citations change on refresh, roughly every two days | A citation audit is a standing job, not a project |
| Factual density | Content carrying statistics, data points and attributable claims measured 30-50% higher visibility | Conductor benchmarks; the Princeton table below agrees |
| Structure | Question-based headings, comparison tables and FAQ blocks measured 73-89% higher citation probability | Vendor-reported, so treat the direction as settled and the magnitude as unproven |

**Freshness is the cheapest lever on this list and the one with the shortest half-life.** Three
independent readings put the decay window between 30 and 90 days, and a fourth finds pages
untouched for 18 months losing citations they used to win even with their backlinks intact. A page
that used to rank and has gone stale is the fastest win available: it already has the authority, it
needs a real update rather than a touched date, which Google detects.

How to write the page so a chunk of it survives being lifted out, with the before-and-afters:
[write-like-a-source.md](write-like-a-source.md).

## The platforms do not overlap, so pick two

Of the top 50 most-cited domains across AI Overviews, ChatGPT and Perplexity, **only seven appear on
all three.** Google's own AI Overviews and AI mode share just 13.7% of their citations while giving
86% semantically similar answers.

| Platform | Pulls from | Traditional-SEO overlap |
| --- | --- | --- |
| Google AI Overviews | YouTube, Reddit, Quora, encyclopedic and Google-owned properties | Was 76% of citations from Google's top 10; a later study puts it near 38% and falling |
| Google AI mode | YouTube by a wide margin, then Google and Wikipedia; cites Quora 3.5x more than AI Overviews, and pulls from Facebook and Instagram | Low. Under 10% of its cited sources rank top 10 for the same query |
| ChatGPT | Publishers and media: Reddit, Wikipedia, Amazon, Forbes. Median domain rating of its top-cited pages is 90 | 8-10%. Runs on Bing's index, so Bing visibility is the gate |
| Perplexity | Niche and regional sites, FAQ-schema pages, ungated PDFs | 28.6%, the most Google-aligned of the four, so the fastest win if you already rank |
| Claude | Brave Search when web search is on | Low and selective; factual density tips it |

Market share decides the order: Google's AI surfaces and ChatGPT hold the large majority of AI
search volume, so they are the two unless the niche says otherwise. If the site already ranks well,
Perplexity converts that into AI visibility with no extra work and is the cheapest first win.

## The Princeton technique table, still the best per-edit guide

Percentage visibility lift per rewrite technique, measured against Perplexity:

| Technique | Lift |
| --- | --- |
| Cite sources | +40% |
| Add statistics | +37% |
| Add quotations, named and titled | +30% |
| Authoritative tone | +25% |
| Improve clarity | +20% |
| Explained technical terms | +18% |
| Keyword stuffing | **-10%** |

Best measured pair: fluency plus statistics. A low-ranking site gains more than a high-ranking one,
up to 115% with citations, because it has more headroom. SE Ranking's separate AI Overviews numbers
put cited sources at +132% and authoritative tone at +89%.

Note the shape of the winner: **citing other people's sources is what makes a model cite you.**
That is counterintuitive enough that people skip it, and it is the largest single lift on the
table.

## Misinformation is the risk nobody budgets for

Ahrefs planted three contradicting sources about an invented luxury brand across a blog, Reddit and
Medium. **Gemini and Perplexity repeated the fiction in 37-39% of their answers**, citing invented
founders and pricing as fact. ChatGPT stayed under 7% and cited the brand's official FAQ in 84%.

Seer Interactive found a single negative review theme resurfacing **67 times** across branded AI
outputs. Publishing real data that contradicted it displaced the theme after two citations, and it
crept back when the data was not refreshed.

The defence is specificity, because when a model chooses between a vague truth and a specific
fiction it takes the specific one. Fill every information gap about the brand with dated, numbered,
official content, and re-publish it on a schedule rather than once.

## Technical: what actually blocks a citation

- **Check `yourdomain.com/robots.txt` for `GPTBot`, `OAI-SearchBot`, `ClaudeBot` and
  `Google-Extended` before anything else.** 5.9% of 140 million sites block GPTBot, almost none of
  them on purpose. **Cloudflare's "manage AI bot traffic with robots.txt" is on by default** and
  writes the block for you. `CCBot` is training-only and safe to block; every other bot above mixes
  training and citation, so blocking it forfeits the citation too.
- **ChatGPT's crawler does not render JavaScript.** Gemini and Copilot do. A client-rendered page
  is an empty shell to the largest assistant, so server-render or statically generate. Test by
  disabling JS and loading your own page, or by reading view-source and looking for the body copy.
- **Speed matters more here than for ranking.** Retrieval fetches, parses and chunks in real time,
  and a slow page is dropped before it is ever scored.
- **`llms.txt` is not supported by any major provider.** Not OpenAI, not Google; Anthropic publishes
  one without confirming its crawlers read it. Harmless, not a priority, and no substitute for the
  off-site work people reach for it to avoid.
- **Schema is hygiene, not an AI lever.** SE Ranking measured a 30-40% AI Overviews lift for pages
  carrying Article, FAQPage, HowTo or Product markup, and it is the only study that finds an
  effect; Ahrefs finds no confirmed link and recommends against spending time on it for AEO
  specifically, and a separate published test found no need to restructure content into
  question-answer shapes for a model to read it. Implement it for rich-result eligibility, which
  justifies it on its own, and do not sell it as an AI play. Mechanics belong to the
  `seo-schema-markup` skill. The one exception worth the effort is `Organization` schema with
  `sameAs` pointing at every profile the brand owns, because that is entity resolution rather than
  markup: it tells a model the site, the LinkedIn page and the YouTube channel are one company.
- **Redirect the URLs the assistants invent.** They send visitors to 404s **2.87 times more often
  than Google does**, ChatGPT worst at about 1% of its clicked URLs. Any hallucinated path taking
  repeat traffic gets a redirect to the nearest real page.

## Google's own position, and why it is not the last word

John Mueller's line is that there is nothing special to do for generative responses beyond ordinary
SEO. Take it as a floor rather than a ceiling: it says nothing about the off-site mention work
above, which is where the measured correlation actually sits, and the ranking-to-citation table
above shows ordinary SEO is not carrying the mention lane on its own.

Treat vendor guidance as a hypothesis with an interest. SearchPilot, which runs controlled tests
for enterprise retailers, names "listening to Google" as the practice to stop following blindly,
having run tests Google has not and found published advice to be neutral at best on real sites. The
same scepticism applies to the tool vendors selling AI-visibility trackers, whose infographics
outrun the data underneath them.

**AI-written content is not itself a ranking liability.** Google's documented position permits
automation and judges the output. The strongest available evidence is the image case: SynthID has
marked Google's generated images since 2023, free detectors identify them in seconds, and it has
never been what decides whether a page ranks. Do not strip a text watermark to be safe, the
character-swap method substitutes homoglyphs from other alphabets, which breaks the entity
resolution the page depends on, and mixed-script text is a spam signal Google has run for years.
The rule that survives is the same one as ever: generic output loses because it is generic, not
because a machine typed it.
