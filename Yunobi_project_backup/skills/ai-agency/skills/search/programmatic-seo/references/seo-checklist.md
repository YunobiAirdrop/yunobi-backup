# The pre-publish gate

Run this on every page before it goes live. It is a gate, not a tutorial: each line is checkable in
seconds and fails loudly. The evidence behind the content rules is in
[geo-signals.md](geo-signals.md); nothing here restates it.

## Before you write

- [ ] The target keyword was Googled and the top five results were read, not skimmed
- [ ] You can name what all five cover (the table stakes) and what none of them covers (your angle)
- [ ] The page carries at least one thing a model cannot generate: your measurement, your customer's
      words, your screenshot, your number. **Without this the page is a duplicate of the consensus,
      and the consensus is what gets summarised and discarded**
- [ ] Answer out loud: could another site in this category have published this exact page? A yes
      fails the gate
- [ ] The AI filter passed: you Googled the query, read the AI Overview, and either it does not
      satisfy the searcher, or you are targeting the query for a mention rather than a click

## Title, meta, URL

- [ ] Title tag under 60 characters, keyword front-loaded, and it promises something
- [ ] Meta description 150-160 characters. Not a ranking factor; it decides the click. Write it as
      ad copy
- [ ] URL is lowercase, hyphenated, keyword-bearing, three to five words. No CMS-generated ids
- [ ] Title, H1 and URL agree with each other and with what the page actually delivers

## Structure

- [ ] Exactly one H1. H2s for sections, H3s nested under them, no level skipped
- [ ] **Every H2 section reads correctly with nothing around it.** Take one and read it cold; if it
      needs three earlier paragraphs, rewrite it
- [ ] Every section opens with its conclusion, not its background
- [ ] Keyword appears in the H1, in the first 100 words, and in at least one H2. Placed, not dosed.
      There is no density target and stuffing measurably *reduces* AI visibility
- [ ] Entities are named: products, people, places, versions, numbers. Not "this tool" and "the platform"
- [ ] A comparison on the page is a table
- [ ] Four to eight real questions answered, phrased as somebody would ask them, taken from call
      logs, DMs or tickets rather than invented, and placed **high on the page** rather than under
      the testimonials
- [ ] No claim of standing without its evidence in the same breath. "Fully licensed and insured"
      with no number, insurer or document is cut, not softened
- [ ] No marketing adjective doing the work of a fact. "Expert", "premier", "years of experience"
      and "dedicated team" appear on every competitor page, so they distinguish nothing. Rewrites:
      [write-like-a-source.md](write-like-a-source.md)
- [ ] Every item in a list is a standalone fact. A list where none of them is loses the whole block,
      not one line
- [ ] **Length is whatever the answer needs.** Word count does not correlate with citation and over
      half of cited pages run under 1,000 words. Match the depth the top results reach, then add the
      angle; do not pad to a target

## Links

- [ ] Three to five internal links with descriptive anchors, and at least one to a money page
- [ ] The relevant money page or cluster hub links *back* to this page. An orphan is not discovered
- [ ] Two to three external links to authoritative sources, supporting specific claims
- [ ] Every link target returns 200. A route that exists in the working tree may not be deployed

## Images

- [ ] WebP or AVIF, under 200KB, correct dimensions, lazy-loaded below the fold. Stock from
      Unsplash or Pexels, converted with `cwebp input.jpg -q 80 -o output.webp`
- [ ] Filenames describe the image. `IMG_1234.jpg` tells nothing to anyone
- [ ] Alt text describes the picture to somebody who cannot see it; that is the job, and the
      keyword only appears if it genuinely belongs. The same alt text repeated across every image is
      a wasted field
- [ ] Social share image present, 1200x630

## Technical

- [ ] Server-rendered or statically generated. **ChatGPT's crawler does not run JavaScript**;
      disable JS in the browser and confirm the content is still there
- [ ] Article schema with author, published and modified dates; FAQPage schema if there is a real
      FAQ; `Organization` with `sameAs` pointing at every profile the brand owns. Ship it for
      rich-result eligibility, which justifies it alone, and do not count it as an AI lever: the
      evidence there is one study for and two against. Mechanics belong to the `seo-schema-markup`
      skill
- [ ] Lighthouse: 100 on SEO, best practices and accessibility; performance as close as the stack
      allows. Paste the failing audits straight into the agent rather than reading them yourself
- [ ] Page is in `sitemap.xml`, and `robots.txt` blocks nothing you want crawled, including
      `GPTBot`, `OAI-SearchBot`, `ClaudeBot` and `Google-Extended`
- [ ] Mobile: readable without zoom, no horizontal scroll, touch targets sized

## Ship

- [ ] Facts verified, links tested, preview checked on a phone
- [ ] Schema validated in Google's Rich Results Test
- [ ] Sitemap submitted, then the URL itself submitted for indexing in Search Console, which turns
      weeks into about a day. The daily quota is roughly ten
- [ ] **Cadence respected.** Publishing a hundred pages in a day is a spike Google reads as what it
      is. Ramp: one a day, then two, then more, over weeks

## Afterwards

- [ ] Diarised for a refresh. Freshness is a measured citation signal and a stale page stops being
      recommended; a real update, not a touched date
- [ ] Position and impressions recorded once indexed, so the next batch is planned against a number
