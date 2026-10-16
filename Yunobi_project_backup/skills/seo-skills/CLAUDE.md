# SEO Skills for Claude Code

This repository contains **7 complementary Claude Code skills** that teach AI assistants how to perform comprehensive SEO analysis, optimization, and strategy using the **seo-mcp** MCP server.

## The 7 Skills

1. **seo-on-page-optimization** — Meta tags, title tags, headings, content optimization, image SEO, internal linking, URL structure
2. **seo-technical-audit** — Crawlability, indexing, Core Web Vitals, page speed, mobile, HTTPS, robots.txt, sitemaps, redirects
3. **seo-content-strategy** — Keyword research, content clusters, search intent, E-E-A-T, content briefs, gap analysis
4. **seo-schema-structured-data** — JSON-LD, Schema.org types, Google rich results, validation rules
5. **seo-off-page-backlinks** — Backlink analysis, domain authority, link building, toxic links, anchor text, competitor gaps
6. **seo-local-seo** — Google Business Profile, NAP consistency, citations, local keywords, reviews, multi-location
7. **seo-mcp-tools-expert** (HIGHEST PRIORITY) — How to use all seo-mcp tools effectively, workflows, parameter formats

## Available MCP Tools

### Page Analysis (always available — 11 tools)
- `analyze_page` — Comprehensive on-page SEO analysis with scoring, Flesch-Kincaid readability, thin content detection
- `analyze_headings` — Heading structure validation
- `analyze_images` — Image alt text, size, format audit
- `analyze_internal_links` — Link mapping, anchor text, broken links
- `extract_schema` — Structured data extraction + validation
- `analyze_robots_txt` — robots.txt parsing and analysis
- `analyze_sitemap` — XML sitemap validation
- `audit_security_headers` — HSTS, CSP, X-Frame-Options, X-Content-Type-Options, mixed content detection
- `analyze_url_structure` — URL length, depth, uppercase, underscores, parameters, file extensions
- `validate_hreflang` — Hreflang language codes, x-default, return link verification
- `audit_accessibility` — WCAG checks: lang, form labels, empty buttons/links, headings, ARIA, skip nav, tabindex

### Performance (free, optional API key — 2 tools)
- `check_core_web_vitals` — LCP, INP, CLS + Lighthouse scores
- `check_mobile_friendly` — Mobile usability evaluation

### Research (requires DataForSEO/Moz API key — 4 tools)
- `research_keywords` — Search volume, difficulty, related keywords
- `analyze_serp` — SERP features, top results
- `analyze_backlinks` — Backlink profile, referring domains
- `analyze_domain_authority` — DA/DR metrics

### Google Search Console (requires OAuth2 — 3 tools)
- `gsc_performance` — Clicks, impressions, CTR, position
- `gsc_index_coverage` — Index status, errors
- `gsc_sitemaps` — Sitemap submission status

### Generation (always available — 3 tools)
- `generate_schema` — Create JSON-LD markup
- `generate_robots_txt` — Create robots.txt
- `generate_meta_suggestions` — Suggest improved meta tags

### Site Crawler (always available — 6 tools)
- `crawl_site` — Start BFS site crawl, returns crawl ID (async job pattern)
- `crawl_status` — Check crawl progress (pages crawled/queued/errored)
- `crawl_results` — Aggregated issues, duplicates, near-duplicates, redirect chains, orphan pages
- `detect_orphan_pages` — Cross-reference crawl with sitemap for orphan/unlisted pages
- `compare_crawls` — Diff two crawls: new/removed pages, changed elements, new/resolved issues
- `list_crawls` — List all crawl sessions (in-memory + saved to disk)

### System
- `seo_tools_documentation` — Tool docs and quick reference

## Critical Patterns

- **Most common workflow:** `analyze_page` → drill down with specific tools → `generate_meta_suggestions`
- **Site-wide audit:** `crawl_site` → `crawl_status` (poll) → `crawl_results` (retrieve issues, duplicates, redirects)
- **Always start with:** `analyze_page` for single URL analysis, `crawl_site` for full site audit
- **Performance testing:** Always test mobile first (mobile-first indexing)
- **Schema workflow:** `extract_schema` → `generate_schema` → `extract_schema` (verify)
- **Security check:** `audit_security_headers` for HSTS, CSP, mixed content

## Skill Activation

Skills activate automatically based on user queries:
- Asking about meta tags → `seo-on-page-optimization`
- Asking about page speed → `seo-technical-audit`
- Asking about keywords → `seo-content-strategy`
- Asking about JSON-LD → `seo-schema-structured-data`
- Asking about backlinks → `seo-off-page-backlinks`
- Asking about local SEO → `seo-local-seo`
- Asking about tools → `seo-mcp-tools-expert`
