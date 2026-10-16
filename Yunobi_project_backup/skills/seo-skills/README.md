# SEO Skills for Claude Code

Expert Claude Code skills for comprehensive SEO — on-page, off-page, technical, local, content strategy, and schema markup. Powered by [seo-mcp](https://github.com/Autom8Minds/seo-mcp) MCP server.

## The 7 Skills

| Skill | Description |
|-------|-------------|
| **seo-on-page-optimization** | Meta tags, headings, content, images, internal linking, URL structure |
| **seo-technical-audit** | Crawlability, indexing, Core Web Vitals, speed, mobile, HTTPS, sitemaps |
| **seo-content-strategy** | Keyword research, content clusters, search intent, E-E-A-T, content briefs |
| **seo-schema-structured-data** | JSON-LD, Schema.org types, rich results, validation |
| **seo-off-page-backlinks** | Backlink analysis, DA/DR, link building, toxic links, competitor gaps |
| **seo-local-seo** | Google Business Profile, citations, NAP, reviews, multi-location |
| **seo-mcp-tools-expert** | How to use seo-mcp tools effectively (workflows, parameters, best practices) |

## Installation

### Claude Code (Recommended)

```bash
/plugin marketplace add Autom8Minds/seo-skills
/plugin install seo-mcp-skills@seo-mcp-skills
```

Both steps are required — `marketplace add` registers the catalog, `install` adds the plugin.

> **If the first command fails with a key or permissions error:** GitHub `owner/repo`
> shorthand clones over SSH by default. Run Claude Code with
> `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` set, or use the full URL:
> `/plugin marketplace add https://github.com/Autom8Minds/seo-skills.git`

### Manual Installation

```bash
git clone https://github.com/Autom8Minds/seo-skills.git ~/.claude/skills/seo-skills
```

### Claude.ai

Download individual skill zips from the [dist/](dist/) folder and upload via **Settings > Capabilities > Skills**.

## Prerequisites

### Required
- Claude Code, Claude.ai, or Claude API access

### Recommended
- [seo-mcp](https://github.com/Autom8Minds/seo-mcp) MCP server installed — gives Claude real-time SEO analysis tools

### MCP Configuration

Copy `.mcp.json.example` to `.mcp.json` and configure:

```json
{
  "mcpServers": {
    "seo-mcp": {
      "command": "npx",
      "args": ["@autom8minds/seo-mcp"],
      "env": {
        "PAGESPEED_API_KEY": "optional-for-higher-rate-limits"
      }
    }
  }
}
```

## What You Can Do

### Without any API keys (23 tools available)
- Full on-page SEO audits (meta tags, headings, images, links)
- Site crawling with BFS discovery, near-duplicate detection, redirect chain mapping
- Accessibility auditing (WCAG: lang, form labels, headings, ARIA, skip nav)
- Orphan page detection (cross-reference crawl with sitemap)
- Crawl comparison (diff two crawls over time)
- Security header auditing (HSTS, CSP, mixed content)
- URL structure analysis (length, depth, uppercase, underscores)
- Hreflang validation (language codes, return links)
- Technical audits (robots.txt, sitemaps, redirects)
- Core Web Vitals analysis
- Mobile-friendliness checks
- Schema/structured data validation
- JSON-LD markup generation
- Meta tag improvement suggestions

### With DataForSEO API key (+4 tools)
- Keyword research with search volume and difficulty
- SERP analysis with feature detection
- Backlink profile analysis
- Domain authority metrics

### With Google Search Console OAuth (+3 tools)
- Real search performance data (clicks, impressions, CTR)
- Index coverage status
- Sitemap health monitoring

## Example Usage

```
"Audit https://example.com for SEO issues"
→ Skills activate: seo-mcp-tools-expert, seo-on-page-optimization, seo-technical-audit
→ Tools used: analyze_page, check_core_web_vitals, extract_schema, generate_meta_suggestions

"Help me build a content cluster around 'project management'"
→ Skill activates: seo-content-strategy
→ Tools used: research_keywords, analyze_serp

"Add FAQ schema to my help center page"
→ Skill activates: seo-schema-structured-data
→ Tools used: extract_schema, generate_schema

"Optimize my Google Business Profile for a restaurant"
→ Skill activates: seo-local-seo
→ Reference: GBP checklist, local schema templates
```

## Project Structure

```
seo-skills/
├── .claude-plugin/          Plugin configuration
├── skills/                  7 skill folders
│   ├── seo-on-page-optimization/
│   ├── seo-technical-audit/
│   ├── seo-content-strategy/
│   ├── seo-schema-structured-data/
│   ├── seo-off-page-backlinks/
│   ├── seo-local-seo/
│   └── seo-mcp-tools-expert/
├── evaluations/             Test scenarios per skill
├── docs/                    Additional documentation
├── dist/                    Built zip packages
├── CLAUDE.md                Claude Code guidance
└── build.sh                 Build script for packages
```

## License

MIT License — see [LICENSE](LICENSE) for details.

## Author

[Anurag Kalita](https://github.com/Autom8Minds)
