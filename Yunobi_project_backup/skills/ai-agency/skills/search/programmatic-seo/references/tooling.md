# Tools, and what each one costs

The data policy: run the free lane first, buy a number only when a decision turns on it.

This section is the data cost policy for every SEO skill in the package. The others point here.

Most SEO work needs no paid data. Run the free lane first, every time. Buy a number only when
a decision turns on that number.

### Free lane, the default

| Source | What it gives |
| --- | --- |
| Search Console, through `gsc.py` or OpenSEO `get_search_console_performance` | Your own queries, positions, clicks and CTR. Always the first call |
| Google Ads Keyword Planner, `generateKeywordHistoricalMetrics` | **Search volume, competition and top-of-page bids, free.** This is where volume comes from; every paid tool resells this service |
| Google Autocomplete, `suggestqueries.google.com/complete/search?client=firefox` | Autocomplete, keyless and with no account. Branch it across the alphabet: 27 free calls beat one paid one |
| Open PageRank, `openpagerank.keywordseverywhere.com` | Domain authority, 0-10 over the Common Crawl link graph. Free to 30,000 domains a month, 100 per request. Read the caveat below before you swap it for a paid rating |
| OpenSEO `get_search_opportunities`, `inspect_urls` | Striking-distance queries, and index, crawl and canonical state for up to 10 URLs per call |
| OpenSEO `run_site_audit` with `runLighthouse: false`, then `get_audit_status`, `get_audit_issues`, `get_audit_pages` | Its own crawler over `robots.txt` and the sitemap. Typed issues carrying severity and fix, with thresholds at title 10-60, meta description 70-160, thin content under 150 words, response over 1500ms, and crawl depth over 5 |
| OpenSEO Google Analytics tools | Organic landing pages, traffic acquisition, key events, measurement health |
| Serper.dev | Related searches and PAA only, now that autocomplete comes free from Google. Free to 2,500 queries, then $0.001 each |
| WebSearch, or the browser | Read the SERP you want to enter |
| Ahrefs free keyword generator | Sanity check on a single phrase |

That lane answers what to write next, what is broken, what is cannibalised and what sits close
to page one. On a site that already has console history, it covers the work.

**Volume, autocomplete and domain authority all moved into this table on 7 Sep 2026.** Each of
the three had been a paid call for a number Google or Common Crawl gives away. Before writing
a new integration against a paid endpoint, check whether the vendor is reselling a free source:
DataForSEO's whole `keywords_data/google_ads/*` family is Keyword Planner with a bill attached.

### Metered lane, DataForSEO per call

These OpenSEO tools bill DataForSEO on every call: `research_keywords`, `get_keyword_metrics`,
`get_ranked_keywords`, `get_domain_overview`, `get_domain_keyword_suggestions`,
`get_serp_results`, `find_serp_competitors`, `get_backlinks_overview`, `get_backlinks_profile`,
the local SERP and Business tools, `run_rank_tracker`, and Lighthouse inside a site audit.

Two of those now have a free equivalent above and should not be the first call: keyword metrics
(Keyword Planner) and keyword research (Keyword Planner ideas plus autocomplete). A domain
rating has a free stand-in with the coverage limits above; buy the paid one when the answer has
to hold for every domain in a list. What has no free source at all is a SERP position for a
domain you do not own, a backlink profile beyond a single authority score, and the LLM-mention
index.

Spend there in four cases, and name the case before you spend:

1. The site has no Search Console history, so there is nothing to harvest.
2. A new cluster needs a size before weeks of writing go into it.
3. A client deliverable has to carry volume, difficulty or backlink numbers.
4. A competitor or backlink question that first-party data cannot answer.

Anything else pays to confirm what the console already said. `estimate_rank_tracker_cost`
prices a tracker before you start it.

### Running OpenSEO

`github.com/every-app/open-seo`, MIT licensed. It is not an alternative data source. Its
keyword volume, difficulty, backlink and rank numbers all come from DataForSEO, so moving to it
cannot change data quality in either direction. What it adds is a free surface over the free
sources, and one MCP endpoint Claude can query mid-task.

Self-host on one machine:

```bash
git clone https://github.com/every-app/open-seo && cd open-seo
cp .env.example .env      # DATAFORSEO_API_KEY only if you want the metered lane
docker compose up -d      # http://localhost:3001, AUTH_MODE=local_noauth, no auth
claude mcp add --transport http --scope user openseo http://localhost:3001/mcp
```

A missing `DATAFORSEO_API_KEY` is a startup warning, not a failure, so the whole free lane
runs on a container that holds no paid key at all. The key, when set, is the base64 of
`email:password` from DataForSEO, not the dashboard API key. Search Console and Analytics need
`GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`, per `docs/SELF_HOSTING_GOOGLE_SEARCH_CONSOLE.md`
in the checkout. Never expose the container beyond localhost: Docker mode disables auth.

The hosted plan at `openseo.so` is $10 a month and adds 28 per cent to every DataForSEO call it
makes for you. Take it only to skip Docker.

OpenSEO also ships its own skills, `keyword-research`, `keyword-clustering`,
`competitor-analysis`, `competitive-landscape`, `link-prospecting`, `seo-audit`, `seo-coach`
and `seo-project-setup`, installed with `npx skills add every-app/open-seo`. They reach for the
metered tools first. Install them only alongside this cost policy, which overrides them.

## Where the credentials actually live

Each of these costs a session to rediscover, because none of them sits in the repo being
worked on.

**Google Ads Keyword Planner** is the free source of volume. It needs a Google Ads account, an
OAuth refresh token, and `GOOGLE_ADS_DEVELOPER_TOKEN` with **Basic access**. A fresh developer
token is test-account-only and every call against a real account fails with
`DEVELOPER_TOKEN_NOT_APPROVED` (403), which is an application in the API Center, not a code
fix. Endpoint:
`POST https://googleads.googleapis.com/v25/customers/{id}:generateKeywordHistoricalMetrics`,
body `{keywords, language: "languageConstants/1000", geoTargetConstants: ["geoTargetConstants/2840"]}`.
Those geo numbers are the same ones DataForSEO calls `location_code`, because it copies them
from here. `generateKeywordIdeas` expands up to 20 seeds and returns each idea with its volume,
which is keyword research and volume in one free call.

**Google Autocomplete** needs nothing at all:
`https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q=...`.
`client=firefox` returns JSON rather than JSONP, and the suggestions are element `[1]`. Send a
browser `User-Agent` or Google answers an empty list.

**Open PageRank** is `OPENPAGERANK_API_KEY`, a free key from
`openpagerank.keywordseverywhere.com`, in the form `opr_live_…`. `POST /v1/domains/bulk` with
`Authorization: Bearer <key>` and `{"domains": [...], "include_history": false}`, up to 100 unique
domains, 60 requests a minute, 30,000 a month. History is on by default and is forty monthly points
a domain, so turn it off unless you are drawing the series.

**It is not a rescaled domain rating, and on small domains it is much weaker than a paid one.**
Measured across a 13-domain portfolio, 8 Sep 2026:

| Domain | Open PageRank 0-10 | DataForSEO 0-100 |
| --- | --- | --- |
| clickup.com | 8.5 | not measured |
| zenpilot.com | 3.6 | not measured |
| a consultancy domain | 1.2 | 32 |
| a young product domain | 1.1 | 30 |
| a 38-rated personal domain | 0.4 | 38 |
| two live products | no row at all | 26 and 14 |

Read that as two rules. Multiplying by ten is wrong: the scales are not the same curve, and the
same domain reads 1.2 against 32. And Common Crawl does not hold every small domain, so five of
thirteen came back rated and the rest had no row, where the paid call answered for all thirteen.
Open PageRank separates big sites well and small ones barely, so it is the right free call for
"is this a real domain or a parked scraper" and the wrong one for ranking a portfolio of young
products against each other.

**Serper.dev** is `SERPER_API_KEY`, kept in one env file and exported before the scripts run. It
is now optional in `scripts/keyword-research.py`, which takes autocomplete from Google directly
and calls Serper only for **related searches and People Also Ask**. No volume, no difficulty.
Picking article targets from Serper alone over-indexes on ultra-long-tail phrasings. Run it with
`--no-serper` to stay entirely on the free lane.

**DataForSEO**, which is where volume and competition come from, needs `DATAFORSEO_LOGIN`,
`DATAFORSEO_PASSWORD` and
`DATAFORSEO_AUTH_BASE64`. Use the base64 one directly as `Authorization: Basic <value>`. Both
endpoints below are Keyword Planner with a bill on top, so reach for them only when the Ads
developer token is not approved.

- Volume: `POST /v3/keywords_data/google_ads/search_volume/live`
- Expansion with volume: `POST /v3/keywords_data/google_ads/keywords_for_keywords/live`
- The body is a JSON **array** of task objects. Omit `location_code` for worldwide; `2840` is
  the US.
- "No volume" means below Google Ads' reporting floor, not zero demand. In a small niche that
  floor hides real traffic, so cross-check Search Console impressions before dropping a
  keyword.

**Google Search Console** authenticates with
`gcloud auth application-default print-access-token`, and every call needs a
`x-goog-user-project: $(gcloud config get-value project)` header or it 403s with "requires a
quota project". That error is about the missing header, not about scopes or permissions.
`scripts/gsc.py` in the `search-console` skill wraps the queries. Sitemap resubmit is
`PUT /webmasters/v3/sites/{urlencoded-site}/sitemaps/{urlencoded-feed}` and returns 204.
