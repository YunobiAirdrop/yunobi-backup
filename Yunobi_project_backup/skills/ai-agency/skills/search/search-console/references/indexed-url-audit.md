# Indexed URL audit

Pulls every indexed page from Search Console, cross-references it against the actual
SvelteKit routes, sorts the differences into buckets and applies the fixes to
`hooks.server.ts` and `vercel.json`. Written against one bilingual SvelteKit site; the
buckets transfer, the route names are yours.

## Setup

```bash
GSC="python3 <skill-dir>/scripts/gsc.py"
SITE="sc-domain:example.com"
```

## Known Route Patterns

The site (`src/routes/`) uses SvelteKit with these patterns:

### Frontend routes (lang-prefixed)

All public pages live under `/(frontend)/[lang=lang]/` where `[lang]` is `en` or `fr`:

**Marketing pages:**

- `/[lang]/` (homepage)
- `/[lang]/about`
- `/[lang]/services`
- `/[lang]/call`
- `/[lang]/ai`
- `/[lang]/automations` (plural, NOT singular)
- `/[lang]/privacy`
- `/[lang]/cookies`
- `/[lang]/studio`

**Blog:**

- `/[lang]/blog` (listing)
- `/[lang]/blog/[slug]` (dynamic, individual posts)
- `/[lang]/blog/clickup-consultant` (special route with components)

**ClickUp pages:**

- `/[lang]/clickup`
- `/[lang]/clickup-discount`
- `/[lang]/clickup-coaching`
- `/[lang]/clickup-master`

**Products and purchasing:**

- `/[lang]/products`
- `/[lang]/products/[slug]`
- `/[lang]/products/success`
- `/[lang]/products/cancel`

**Case studies:**

- `/[lang]/case-studies`
- `/[lang]/case-studies/[slug]`

**Learning portal (auth required):**

- `/[lang]/portal`
- `/[lang]/portal/dashboard`
- `/[lang]/portal/learn/[productSlug]`

### Non-indexable paths

- `/admin/*` (CMS panel, protected)
- `/api/*` (server endpoints)
- `/(auth)/[lang]/login`, `/signup`, `/reset-password` (auth flows)
- `/auth/callback` (OAuth callback)
- `portal.example.com/*` (portal subdomain)
- `staging.example.com/*` (staging)
- `example.vercel.app/*` (Vercel preview)
- `/api/og-image` (OG image generation endpoint)

### Common legacy patterns that need redirects

- `/[lang]/automation` (singular) was never a route, use `/[lang]/automations`
- `/[lang]/agency-playbook` was removed, redirects to home
- `/[lang]/clickup-promo-code` was renamed to `/[lang]/clickup-discount`
- `/blog/[slug]` without lang prefix needs `/en/blog/[slug]`
- `/case-studies/[slug]` without lang prefix needs `/en/case-studies/[slug]`
- `/[lang]/blog-en/[slug]` legacy Next.js path needs `/[lang]/blog/[slug]`
- `/up-admin` shortcut redirects to `/admin`

## Workflow

### Step 1: Pull all indexed pages

Fetch every page GSC knows about over a 90-day window:

```bash
$GSC top-pages $SITE --days 90 --limit 500
```

Also pull pages with zero clicks but impressions (these are indexed but possibly broken):

```bash
$GSC query $SITE --dimensions "page" --days 90 --limit 500
```

Save the full URL list for analysis.

### Step 2: Cross-reference against SvelteKit routes

For each URL returned by GSC:

1. Parse the pathname from the full URL
2. Strip the domain and check if a matching route exists in `src/routes/`
3. Check the `src/routes/` directory structure to confirm valid routes

```bash
# List all +page.svelte routes to build the valid route map
find <repo-root>/website/src/routes -name "+page.svelte" -o -name "+page.server.ts" | sort
```

### Step 3: Categorize issues

Sort every indexed URL into one of these buckets:

| Category                | Description                                           | Example                            |
| ----------------------- | ----------------------------------------------------- | ---------------------------------- |
| **Valid**               | URL maps to an existing route                         | `/en/blog/my-post`                 |
| **Broken (404)**        | URL has no matching route, likely old/renamed content | `/en/services/old-service`         |
| **Missing redirect**    | Old URL pattern that should redirect to new location  | `/blog/post` (missing lang prefix) |
| **Wrong subdomain**     | Portal or staging subdomain indexed                   | `portal.example.com/...`           |
| **API URL indexed**     | Server endpoint showing in search results             | `/api/webhook`, `/api/og/...`      |
| **Missing lang prefix** | Page indexed without `/en/` or `/fr/` prefix          | `/about`, `/services`              |
| **OG image route**      | OpenGraph image generation endpoint indexed           | `/og/blog/my-post.png`             |
| **Admin route**         | Admin panel pages indexed                             | `/admin/dashboard`                 |

Print a summary table with counts per category before proceeding.

### Step 4: Add redirects for broken URLs and missing lang prefixes

For each URL that needs a redirect, add entries to both:

**`src/hooks.server.ts`** (SvelteKit server hook):

```typescript
// In the redirect map or handle function:
if (pathname === "/old-path") {
  redirect(301, "/en/new-path");
}

// For missing lang prefix pattern:
if (pathname === "/about") {
  redirect(301, "/en/about");
}
```

**`website/vercel.json`** (production redirects):

```json
{
  "redirects": [
    { "source": "/old-path", "destination": "/en/new-path", "permanent": true },
    { "source": "/about", "destination": "/en/about", "permanent": true }
  ]
}
```

Add redirects in both places so they work in dev (SvelteKit) and production (Vercel edge).

### Step 5: Add noindex headers for non-content URLs

For URLs that should not be indexed (OG images, portal subdomain, API routes, admin routes), add appropriate headers:

**`src/hooks.server.ts`**:

```typescript
// For API routes, OG image routes, admin routes:
if (pathname.startsWith("/api/") || pathname.startsWith("/og/") || pathname.startsWith("/admin/")) {
  const response = await resolve(event);
  return new Response(response.body, {
    ...response,
    headers: {
      ...Object.fromEntries(response.headers),
      "X-Robots-Tag": "noindex, nofollow",
    },
  });
}
```

**`website/vercel.json`** (for subdomain-level issues):

```json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [{ "key": "X-Robots-Tag", "value": "noindex, nofollow" }]
    },
    {
      "source": "/og/(.*)",
      "headers": [{ "key": "X-Robots-Tag", "value": "noindex, nofollow" }]
    },
    {
      "source": "/admin/(.*)",
      "headers": [{ "key": "X-Robots-Tag", "value": "noindex, nofollow" }]
    }
  ]
}
```

For portal subdomain issues, add a `robots.txt` rule or configure the subdomain separately.

### Step 6: Commit and push

After applying all fixes:

```bash
cd <repo-root>
git add src/hooks.server.ts vercel.json
git commit -m "fix(seo): add redirects and noindex headers from GSC audit"
git push
```

## Post-Audit Checklist

- [ ] All broken URLs have 301 redirects to valid pages
- [ ] All lang-prefix-missing URLs redirect to `/en/` equivalent
- [ ] API, OG, and admin routes return `X-Robots-Tag: noindex`
- [ ] Portal subdomain is blocked from indexing
- [ ] Redirects exist in both `hooks.server.ts` and `vercel.json`
- [ ] Changes are committed and pushed
- [ ] Consider submitting updated URLs for re-crawling in GSC (manual step)

## Troubleshooting

| Issue                    | Fix                                                                 |
| ------------------------ | ------------------------------------------------------------------- |
| GSC returns 403          | Re-run gcloud auth with `--scopes` flag from SKILL.md Prerequisites |
| Too many URLs to process | Increase `--limit` or run multiple queries with `--page-filter`     |
| Redirect loops           | Check that destination URLs actually exist before adding redirects  |
| Vercel config conflicts  | Merge with existing redirects/headers arrays, do not overwrite      |
