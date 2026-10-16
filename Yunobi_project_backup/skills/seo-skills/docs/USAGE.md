# Usage Guide

## How Skills Work

Skills activate automatically based on your questions. You don't need to invoke them manually.

### Examples

| You say... | Skills that activate |
|------------|---------------------|
| "Audit this URL for SEO" | seo-mcp-tools-expert + seo-on-page-optimization + seo-technical-audit |
| "Check my page speed" | seo-mcp-tools-expert + seo-technical-audit |
| "Help me with keyword research" | seo-content-strategy |
| "Add FAQ schema to my page" | seo-schema-structured-data + seo-mcp-tools-expert |
| "Analyze my backlink profile" | seo-off-page-backlinks + seo-mcp-tools-expert |
| "Optimize my Google Business Profile" | seo-local-seo |
| "Improve my meta tags" | seo-on-page-optimization + seo-mcp-tools-expert |

## Common Workflows

### 1. Quick Page Audit
```
"Check the SEO of https://example.com/page"
```
Claude will run `analyze_page`, identify issues, and provide recommendations.

### 2. Full Technical Audit
```
"Do a full technical SEO audit of example.com"
```
Claude will check robots.txt, sitemaps, page analysis, Core Web Vitals, mobile-friendliness, and structured data.

### 3. Content Optimization
```
"Help me optimize this page for the keyword 'best project management software'"
```
Claude will analyze the page, check headings for keyword presence, and suggest meta tag improvements.

### 4. Schema Implementation
```
"Add Product schema to https://mystore.com/product/widget"
```
Claude will extract existing schema, generate correct JSON-LD, and validate it.

### 5. Competitive Analysis
```
"Compare my site's SEO to competitor1.com and competitor2.com"
```
Claude will analyze all sites, compare on-page elements, and (with API keys) compare domain authority and backlinks.

## Tips

1. **Be specific** — "Check the heading structure of this page" gets more targeted results than "check SEO"
2. **Provide keywords** — when you mention your target keyword, tools like `analyze_headings` and `generate_meta_suggestions` give better results
3. **Start broad, then narrow** — let Claude run `analyze_page` first, then ask to deep-dive into specific issues
4. **API keys are optional** — 23 of 29 tools work without any API keys
