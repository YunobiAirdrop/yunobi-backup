# Knowing whether any of it worked

Read this before promising a client a number, and before reporting on a quarter of SEO work. The
old scoreboard broke in a specific way, and reporting rank tracking against it is now the fastest
way to be wrong in a meeting.

## Why traffic stopped being the number

Impressions rise while clicks fall. Publishers call it the alligator graph, and it is structural
rather than a content problem.

| Finding | Source |
| --- | --- |
| **58.5% of US Google searches end with no click to anyone.** Of the 41.5% that click, 70.5% go organic, 28.5% to Google-owned properties, 1% to ads | SparkToro with Datos, 2024 clickstream |
| So **360 clicks per 1,000 searches reach the open web.** That is the whole addressable pool | Same |
| An AI Overview on the SERP costs the number-one page **58% of its clicks**, up from 35% eight months earlier | Ahrefs, measured twice |
| Zero-click moved from 57% to 59% when AI mode rolled out, and one 2026 reading puts it at 68% | NP Digital; industry tracking |
| Traffic across ~75,000 sites that are actively trying to grow fell about 5% in 18 months | Ahrefs global panel |

**HubSpot is the case that settles the argument.** Organic traffic fell roughly 80% in a year while
revenue reached an all-time high and grew over 20%. Two honest readings, and both are useful: brand
demand carried the business, and the lost traffic was never producing near-term revenue in the first
place. Either way, traffic and revenue moved in opposite directions, so one cannot proxy the other.

Attribution broke separately and for older reasons: roughly 30% cookie acceptance, 20-60% of
browsers blocking analytics, 3.6 devices per person, and privacy law. In one test, 100% of traffic
from TikTok, Slack, Discord, WhatsApp and Mastodon was reported as direct, plus 75% of Facebook
Messenger and 30% of Instagram DMs. Dropbox's published blackout experiments then showed attributed
ROAS of 1.53 against a **causal** 0.7 on mobile, attributed outcomes overstating causal impact by
two to ten times, and $25M reallocated on the strength of it.

So: correlate, do not attribute. Track leading indicators beside business outcomes and look for
patterns over months, never single-touch proof.

## The three things you can actually track

None is complete. Together they give a usable picture.

**1. AI referral traffic, direction only, never precision.**

In GA4: Admin → Data Display → Channel Groups, copy the default group, add a channel matching
`chatgpt.com|perplexity|gemini.google.com|copilot.microsoft.com|claude.ai|deepseek`. Then Reports →
Acquisition → Traffic Acquisition against the new group.

Every number it returns is an undercount, and the gaps are known: ChatGPT source links pass a
referrer but in-content links on paid accounts use `no-referrer`; Perplexity passes on web but not
its desktop app; Copilot passes on web but not on Windows; Grok passes nothing. Claude passes
correctly.

Read two things from it. Which pages already get AI traffic: keep those current, because a page
that goes stale stops being recommended. And which important pages get none, which is a content, a
crawl, or a not-yet-surfaced problem.

**2. AI bot activity in the logs.** Bots hit pages far more often than people do, so a citation bot
returning repeatedly to one page has found a source. Two kinds worth separating: training crawlers
(`GPTBot`, `Google-Extended`) and retrieval crawlers (`ChatGPT-User`, `OAI-SearchBot`), only the
second can send a visitor. Server logs work; Cloudflare's own analytics work on the free plan.

**3. Self-reported attribution, the smallest change with the largest payoff.** Add "How did you
hear about us?" to signup, checkout or a post-purchase survey, with ChatGPT, Perplexity and "AI
search" as named options. It is the only instrument that catches the buyer who read the
recommendation in an assistant and then typed the brand name into a browser, which analytics will
book as direct or organic forever.

## Why this is worth instrumenting at all

The volume argument says no: AI referrals average about 0.25% of a site's traffic and Google still
sends roughly 210 times more. The conversion argument says yes, loudly.

- Ahrefs: AI search was **0.5% of visits and 12.1% of signups, a 23x conversion rate against
  organic**. About 3% of conversions self-report as AI-sourced.
- Vercel: 10% conversion rate from AI traffic. Tally calls it their largest acquisition channel.
- AI referral traffic grew about 9.7x in a year; ChatGPT alone grew 85% in nine months and now sends
  more traffic than Reddit or LinkedIn.

The traffic arrives pre-qualified because the assistant already explained why the product fits.
That is the whole of the effect.

## The four-layer report that replaces a rank table

Track each layer alongside revenue and read the correlation, monthly:

1. **Audience**: followers, returning visitors, subscribers, keyword footprint.
2. **Reach**: impressions, AI share of voice, views.
3. **Interest**: engagement, product page views, **branded search volume** (the leading indicator
   that matters most, because it is demand you created rather than demand you captured).
4. **Sales**: conversions and incremental lift. This is the primary KPI; everything above tells
   you whether you are on track to it.

The reporting sentence is "we did more of X this month and Y moved", not "post 41 produced three
demos". One agency's employee-advocacy program on LinkedIn cannot name which post drove which
demo, and demo volume still rose sharply. That is a defensible report; pretending to
single-touch precision is not.

## The AI share-of-voice audit

Quarterly, on the brand and on the top three competitors. Any of the AI visibility trackers do
this; the free lane is running the prompts by hand and tallying who is named.

**Every prompt runs signed out, with history, memory and custom instructions off, or the number is
fiction.** An assistant returns what the asking account already believes, and the effect is not
subtle: the same prompt, asked in the same words from two accounts, returns opposing answers on
questions of fact, because each one has learned what its user wants to hear. Practically that means
an incognito window, a signed-out session or a temporary chat, and a different IP where the answer
still looks suspiciously friendly.

Three consequences worth stating to a client before the audit, not after:

- **A client's own screenshot is not evidence.** Someone who has asked ChatGPT about his category
  twenty times has trained it to agree with him, and will arrive convinced that reviews are the
  only thing that matters because the machine said so. Reproduce it cold before accepting it or
  arguing with it.
- **Reporting from a personalised session is reporting fake data**, and the client will eventually
  reproduce it and find a different answer.
- **The API is not a clean substitute.** It answers from a different model version and a different
  retrieval path than the product a buyer actually uses, so it measures subject well and standing
  badly. The same caveat, measured: [fan-out.md](fan-out.md).

Map the gaps in six buckets, because the fix differs by bucket:

| Gap | What it looks like | The fix |
| --- | --- | --- |
| Visibility | Named less often than competitors | Everything below, prioritised |
| Narrative | Described wrongly, "budget alternative" when you are premium | Publish specific, dated, official content that contradicts it |
| Topic | A subject you should own that AI attaches to someone else | Cover the topic properly, not one keyword of it |
| Format | It cites videos or comparisons and you make neither | Produce the format, or get placed in someone else's |
| Web mentions | Competitors are on the listicles and you are not | Outreach to those exact pages |
| Demand | Nobody searches your name alongside the category | Off-search brand work |

Then pick one of three actions per gap (**fix** an existing page, **build** a missing one, or
**influence** an off-site source) and start with the fix. A page that already ranks and only needs
a refresh is the cheapest win available, and freshness is a measured citation signal.

## The advisor report, for a tracked site

Tracked sites are measured in the app's own `/admin/seo` dashboard, and the report it draws is
written in the session, never generated: the agent that used to write it was deleted on
6 Sep 2026 under the words rule. The loop is three commands from the app CLI:

```bash
pnpm cli seo snapshot --site <id>          # only when the latest snapshot is stale
pnpm cli seo context  --site <id>          # the numbers: ranks, movement, GSC rows, YouTube
pnpm cli seo write    --site <id> --file report.json
```

**Write against the latest web snapshot.** The report is keyed to it, so one written against an
older snapshot is stored and never surfaces on the card.

Write the JSON against the report schema the dashboard reads: a 0-100 health score and five
sub-scores, a headline and summary, wins and losses **against the previous snapshot only**, first
appearances under `tooNewToJudge`, up to five actions each carrying its own evidence string, GEO
opportunities and risks. **Every text field is one plain string, not `{ en, fr }`.**
A one-reader report written in two languages is work with no reader: an action about the pages in
the second language says so in the sentence instead.
Every evidence line names a measured number, because the
reader's next question is always "says who". A site whose previous snapshot is missing gets empty
wins and losses, not invented movement.

Two paid reads carry the GEO half of the report, and both are worth pulling before writing:
`seo ai-visibility` for the ChatGPT and Google AI mention index, and `seo ai-answers --run` for
Claude, Gemini and Perplexity, which have no index and are asked the prompts in
the tracked-site config instead. The two disagree often.
On 6 Sep 2026 the index held zero mentions for one product domain while Claude and Perplexity both
named it when asked, and a second domain was named in three French answers of four and none of five
in English.
Report both, and say which one you are quoting.

## Cadence

- **Weekly:** publish, and check nothing broke.
- **Monthly:** the four-layer correlation read, and the AI-traffic page list.
- **Quarterly:** the full competitive share-of-voice audit, and a sentiment check on what the
  assistants say about the brand.

The Search Console side of this (orphans, cannibalisation, striking distance) belongs to the
`search-console` skill and is not repeated here.
