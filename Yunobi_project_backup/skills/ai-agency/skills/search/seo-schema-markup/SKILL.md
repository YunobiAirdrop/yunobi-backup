---
name: seo-schema-markup
description: When the user wants to add, fix, or optimize schema markup and structured data on their site. Also use when the user mentions "schema markup," "structured data," "JSON-LD," "rich snippets," "schema.org," "FAQ schema," "product schema," "review schema," or "breadcrumb schema."
metadata:
  version: "1.0.0"
tags: [makes, seo, code]
lane: general
---

# Schema Markup

Implement schema.org markup that helps search engines understand content and enables rich results.

## What to establish about the page
If `.claude/product-marketing-context.md` exists, read first. Only ask for what's not covered.

1. **Page Type** - what kind of page, primary content, what rich results are possible
2. **Current State** - existing schema, implementation errors, rich results already appearing
3. **Goals** - which rich results are targeted, business value
4. **Data & Stack** - what data is available to populate the schema, tech stack (static, React/Next.js, CMS)

---

## Core Principles

### 1. Accuracy First

- Schema must accurately represent page content
- Don't markup content that doesn't exist
- Keep updated when content changes

### 2. Use JSON-LD

- Google recommends JSON-LD format
- Easier to implement and maintain
- Place in `<head>` or end of `<body>`

### 3. Follow Google's Guidelines

- Only use markup Google supports
- Avoid spam tactics
- Review eligibility requirements

### 4. Validate Everything

- Test before deploying
- Monitor Search Console
- Fix errors promptly

### 5. Its effect on AI citations is contested, so do not sell it as one

SE Ranking measured a 30-40% AI Overviews lift for pages carrying Article, FAQPage, HowTo or
Product schema; Ahrefs found no confirmed link and treats schema as general hygiene. Both readings
agree it does not hurt, and Perplexity does favour FAQ pages because they hand it an
already-extracted question and answer. Justify a schema backlog on rich-result eligibility, which
is measurable, and take any AI-visibility gain as a bonus. The evidence on both sides is owned by
`programmatic-seo`, in its `references/geo-signals.md`.

---

## Common Schema Types

| Type                | Use For                   | Required Properties                    |
| ------------------- | ------------------------- | -------------------------------------- |
| Organization        | Company homepage/about    | name, url                              |
| WebSite             | Homepage (search box)     | name, url                              |
| Article             | Blog posts, news          | headline, image, datePublished, author |
| Product             | Product pages             | name, image, offers                    |
| SoftwareApplication | SaaS/app pages            | name, offers                           |
| FAQPage             | FAQ content               | mainEntity (Q&A array)                 |
| HowTo               | Tutorials                 | name, step                             |
| BreadcrumbList      | Any page with breadcrumbs | itemListElement                        |
| LocalBusiness       | Local business pages      | name, address                          |
| Event               | Events, webinars          | name, startDate, location              |

**For complete JSON-LD examples**: See [references/schema-examples.md](references/schema-examples.md)

---

## Recommended Properties

Beyond the required properties in the table above:

| Type | Recommended |
| --- | --- |
| Organization | logo, sameAs (social profiles), contactPoint |
| Article/BlogPosting | dateModified, publisher, description |
| Product | sku, brand, aggregateRating, review |

---

## Multiple Schema Types

You can combine multiple schema types on one page using `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", ... },
    { "@type": "WebSite", ... },
    { "@type": "BreadcrumbList", ... }
  ]
}
```

---

## Validation and Testing

### Tools

- **Google Rich Results Test**: https://search.google.com/test/rich-results
- **Schema.org Validator**: https://validator.schema.org/
- **Search Console**: Enhancements reports

### Common Errors

**Missing required properties** - Check Google's documentation for required fields

**Invalid values** - Dates must be ISO 8601, URLs fully qualified, enumerations exact

**Mismatch with page content** - Schema doesn't match visible content

---

## Implementation

### Static Sites

- Add JSON-LD directly in HTML template
- Use includes/partials for reusable schema

### Dynamic Sites (React, Next.js)

- Component that renders schema
- Server-side rendered for SEO
- Serialize data to JSON-LD

### CMS / WordPress

- Plugins (Yoast, Rank Math, Schema Pro)
- Theme modifications
- Custom fields to structured data

---

## Output Format

### Schema Implementation

```json
// Full JSON-LD code block
{
  "@context": "https://schema.org",
  "@type": "..."
  // Complete markup
}
```

### Testing Checklist

- [ ] Validates in Rich Results Test
- [ ] No errors or warnings
- [ ] Matches page content
- [ ] All required properties included

---

## Related Skills

- **programmatic-seo**: For templated schema at scale
