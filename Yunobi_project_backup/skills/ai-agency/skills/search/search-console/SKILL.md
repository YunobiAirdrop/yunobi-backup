---
name: search-console
description: "Queries Google Search Console for keyword performance, content gaps, cannibalisation and ranking analysis. Use when checking search performance, deciding what page to write next, finding queries that rank with no page behind them, or on 'GSC', 'check rankings', 'what am I ranking for'."
tags: [drives, seo, analytics]
---

# Google Search Console

Query GSC search analytics via the Search Console API using gcloud application-default credentials.

## Prerequisites

**A raw `curl` call needs `x-goog-user-project` or it 403s.** The client library reads the ADC
file's `quota_project_id`; curl does not, so it falls back to gcloud's shared project and returns a
403 that reads like a permissions error and is a quota-project error. `scripts/gsc.py` uses a
client library and picks the project up automatically; anything hand-rolled must pass the header.
Point it at the project that actually has `searchconsole.googleapis.com` enabled, which is not
necessarily the site's own GCP project. A project with the API switched off returns the same
403, so check the API is on before reading the error as a permissions problem.

**This skill is read-only by design.** Its auth uses `webmasters.readonly`. Submitting a sitemap
needs the full `https://www.googleapis.com/auth/webmasters` scope, so it takes an interactive
`gcloud auth application-default login` followed by
`gcloud auth application-default set-quota-project <project>`.

One-time auth setup (must include the `webmasters.readonly` scope):

```bash
gcloud auth application-default login \
    --scopes=openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/webmasters.readonly
```

If the script returns a 403 scope error, prompt the user to re-run the auth command interactively via `! gcloud auth application-default login ...`.

## CLI Reference

The script at `scripts/gsc.py` provides all GSC queries:

```bash
GSC="python3 <skill-dir>/scripts/gsc.py"
```

### Commands

| Command                   | Purpose                                     |
| ------------------------- | ------------------------------------------- |
| `$GSC sites`              | List verified sites                         |
| `$GSC top-queries <site>` | Top queries by clicks                       |
| `$GSC top-pages <site>`   | Top pages by clicks                         |
| `$GSC query <site>`       | Custom query with dimensions                |
| `$GSC compare <site>`     | Compare current vs previous period          |
| `$GSC gaps <site>`        | Find high-impression, low-CTR opportunities |
| `$GSC orphans <site>`     | Queries you rank for with no page targeting them |
| `$GSC cannibals <site>`   | Queries split across two or more of your own pages |
| `$GSC inspect <site> <urls-file>` | Google's per-URL index verdict, in bulk |

Requesting a crawl is not in that table because it is not in the API. See below.

### Common Flags

| Flag                        | Description                                    |
| --------------------------- | ---------------------------------------------- |
| `--days 28`                 | Lookback period (default: 28 days)             |
| `--limit 50`                | Max rows returned                              |
| `--query-filter "notch"`    | Filter queries containing string               |
| `--page-filter "/blog/"`    | Filter pages containing string                 |
| `--dimensions "query,page"` | Dimensions: query, page, country, device, date |
| `--start-date 2026-01-01`   | Custom start date                              |
| `--end-date 2026-01-31`     | Custom end date                                |

`orphans` adds `--min-impressions` (default 100), `--max-coverage` (default 0.5) and
`--max-position` (default 30). `cannibals` adds `--min-impressions` (default 100) and
`--min-share` (default 0.15, the impression share a page needs to count as competing).
`inspect` adds `--out` (a JSON cache that resumes a stopped run), `--workers` (default 8)
and `--state` (print the URL list for coverage states matching a string).

## Asking Google to crawl a page

There is no API for it. The Indexing API accepts **only** `JobPosting` and `BroadcastEvent`
embedded in a `VideoObject`, confirmed against Google's own quickstart on 2026-08-31, so no
scope and no token reaches an ordinary page. The button in URL Inspection is the only route,
so it takes browser automation against a Chrome that is already signed in to the property.

**The quota is 13 URLs a day per property**, measured rather than read: the fourteenth
request on 2026-08-31 returned "Quota Exceeded ... try submitting this again tomorrow". Stop the
run on that message rather than burning the rest of the list against it.

Three things cost a run each. Handle all three in whatever script drives the console.

- **`/search-console/inspect?...&id=<page url>` is a 404.** The `id` is an opaque hash Google
  mints for the query, so an inspection cannot be deep-linked. Type into the box instead:
  `input[aria-label^="Inspect any URL"]`, and use `fillInput`, because `typeText` into that
  field leaves the page on Overview.
- **The console never unmounts a previous inspection**, so after three URLs the document holds
  four `REQUEST INDEXING` buttons and "click the first one" resubmits a page already done. A
  full navigation back to the property root between URLs is what makes the run trustworthy; refuse
  to click unless exactly one button is on the page.
- **No backslash may appear inside an injected template literal.** The outer template eats it
  before the string reaches the page, so `split('\n')` arrives as a real newline and the
  expression dies with "Invalid or unexpected token". Match on text in the page, and do the
  whitespace work in Node.

A request is a queue position, never an indexing decision. It is worth spending only on pages
a crawl would actually reward, and it does nothing about *why* Google was not fetching them:
for that, read `references/indexed-url-audit.md` and check what links to the page.

## Workflows

Every workflow, from the orphan sweep to the cannibalisation check to the organic/paid gap matrix
when Google Ads is also in play: [`references/workflows.md`](references/workflows.md).

Auditing which URLs Google actually has indexed against the routes that exist, and fixing the
difference in `hooks.server.ts` and `vercel.json`: [`references/indexed-url-audit.md`](references/indexed-url-audit.md).

## Troubleshooting

| Error                   | Fix                                                                                    |
| ----------------------- | -------------------------------------------------------------------------------------- |
| 403 insufficient scopes | Re-run `gcloud auth application-default login` with `--scopes` flag from Prerequisites |
| 403 forbidden           | Verify site ownership in Search Console                                                |
| No sites found          | Add and verify the site at search.google.com/search-console                            |
| Empty results           | Check date range (GSC data has a 3-day lag)                                            |
