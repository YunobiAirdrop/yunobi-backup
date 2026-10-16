# SvelteKit Blog Infrastructure Setup

## Contents

- Prerequisites
- Step 1: Install Dependencies
- Step 2: Configure mdsvex
- Step 3: Create Content Directory Structure
- Step 4: Create Blog Types
- Step 5: Create Blog Loader
- Step 6: Create Blog Routes
- Step 7: Add RSS Feed
- Step 8: Update Sitemap
- Step 9: Add Prose Styles
- Checklist

This guide walks through setting up a markdown-based blog on the Seam SvelteKit website.

## Prerequisites

- Existing SvelteKit project (web/)
- pnpm package manager
- Cloudflare Pages deployment

## Step 1: Install Dependencies

```bash
cd web
pnpm add -D mdsvex shiki
```

**mdsvex**: Markdown preprocessor for Svelte (like MDX for React)
**shiki**: Syntax highlighting for code blocks

## Step 2: Configure mdsvex

Update `svelte.config.js`:

```javascript
import adapter from "@sveltejs/adapter-cloudflare";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";
import { mdsvex } from "mdsvex";

/** @type {import('mdsvex').MdsvexOptions} */
const mdsvexOptions = {
  extensions: [".md", ".svx"],
  highlight: {
    highlighter: async (code, lang = "text") => {
      const { codeToHtml } = await import("shiki");
      const html = await codeToHtml(code, {
        lang,
        theme: "github-dark",
      });
      return `{@html \`${html}\`}`;
    },
  },
  layout: {
    blog: "./src/lib/components/blog/BlogLayout.svelte",
  },
};

/** @type {import('@sveltejs/kit').Config} */
const config = {
  extensions: [".svelte", ".md", ".svx"],
  preprocess: [vitePreprocess(), mdsvex(mdsvexOptions)],
  kit: {
    adapter: adapter(),
  },
};

export default config;
```

## Step 3: Create Content Directory Structure

```
web/
├── content/
│   └── blog/
│       ├── drafts/              # Review queue
│       ├── published/           # Live articles
│       │   └── best-mac-notch-apps.md
│       └── images/              # Blog images
│           └── best-mac-notch-apps/
│               ├── hero.webp
│               └── comparison.webp
└── src/
    └── routes/
        └── blog/
            ├── +page.svelte     # Blog index
            ├── +page.server.ts  # Load all posts
            └── [slug]/
                ├── +page.svelte # Article view
                └── +page.server.ts
```

## Step 4: Create Blog Types

Create `src/lib/types/blog.ts`:

```typescript
export interface BlogPost {
  slug: string;
  title: string;
  description: string;
  publishedAt: string;
  updatedAt: string;
  author: string;
  tags: string[];
  image?: string;
  imageAlt?: string;
  draft?: boolean;
}

export interface BlogPostWithContent extends BlogPost {
  content: string;
}
```

## Step 5: Create Blog Loader

Create `src/lib/server/blog.ts`:

```typescript
import type { BlogPost, BlogPostWithContent } from "$lib/types/blog";
import { error } from "@sveltejs/kit";

// Import all published markdown files
const posts = import.meta.glob("/content/blog/published/*.md", { eager: true });

export function getAllPosts(): BlogPost[] {
  const allPosts: BlogPost[] = [];

  for (const path in posts) {
    const post = posts[path] as { metadata: BlogPost };
    const slug = path.split("/").pop()?.replace(".md", "") || "";

    // Skip drafts in production
    if (post.metadata.draft && import.meta.env.PROD) continue;

    allPosts.push({
      ...post.metadata,
      slug,
    });
  }

  // Sort by date, newest first
  return allPosts.sort(
    (a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime(),
  );
}

export async function getPost(slug: string): Promise<BlogPostWithContent> {
  const path = `/content/blog/published/${slug}.md`;

  if (!(path in posts)) {
    throw error(404, "Post not found");
  }

  const post = posts[path] as {
    metadata: BlogPost;
    default: { render: () => { html: string } };
  };

  const { html } = post.default.render();

  return {
    ...post.metadata,
    slug,
    content: html,
  };
}
```

## Step 6: Create Blog Routes

### Blog Index (`src/routes/blog/+page.server.ts`):

```typescript
import { getAllPosts } from "$lib/server/blog";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
  const posts = getAllPosts();
  return { posts };
};
```

### Blog Index (`src/routes/blog/+page.svelte`):

```svelte
<script lang="ts">
  import type { PageData } from './$types';
  import { formatDate } from '$lib/utils';

  let { data }: { data: PageData } = $props();
</script>

<svelte:head>
  <title>Blog | Seam - Mac Notch App</title>
  <meta name="description" content="Tips, guides, and updates about Mac notch apps and MacBook productivity." />
</svelte:head>

<main class="container mx-auto px-4 py-12 max-w-4xl">
  <h1 class="text-4xl font-bold mb-8">Blog</h1>

  <div class="space-y-8">
    {#each data.posts as post}
      <article class="border-b pb-8">
        <a href="/blog/{post.slug}" class="group">
          {#if post.image}
            <img
              src={post.image}
              alt={post.imageAlt || post.title}
              class="w-full h-48 object-cover rounded-lg mb-4"
              loading="lazy"
            />
          {/if}
          <h2 class="text-2xl font-semibold group-hover:text-primary transition-colors">
            {post.title}
          </h2>
          <p class="text-muted-foreground mt-2">{post.description}</p>
          <div class="flex items-center gap-4 mt-4 text-sm text-muted-foreground">
            <time datetime={post.publishedAt}>{formatDate(post.publishedAt)}</time>
            <span>•</span>
            <span>{post.author}</span>
          </div>
        </a>
      </article>
    {/each}
  </div>
</main>
```

### Article Page (`src/routes/blog/[slug]/+page.server.ts`):

```typescript
import { getPost } from "$lib/server/blog";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
  const post = await getPost(params.slug);
  return { post };
};
```

### Article Page (`src/routes/blog/[slug]/+page.svelte`):

```svelte
<script lang="ts">
  import type { PageData } from './$types';
  import { formatDate } from '$lib/utils';

  let { data }: { data: PageData } = $props();
  let post = $derived(data.post);
</script>

<svelte:head>
  <title>{post.title} | Seam Blog</title>
  <meta name="description" content={post.description} />

  <!-- Open Graph -->
  <meta property="og:title" content={post.title} />
  <meta property="og:description" content={post.description} />
  <meta property="og:type" content="article" />
  {#if post.image}
    <meta property="og:image" content={post.image} />
  {/if}

  <!-- Article Schema -->
  {@html `<script type="application/ld+json">${JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.description,
    image: post.image,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author
    },
    publisher: {
      '@type': 'Organization',
      name: 'Seam',
      logo: {
        '@type': 'ImageObject',
        url: 'https://getseam.app/logo.png'
      }
    }
  })}</script>`}
</svelte:head>

<article class="container mx-auto px-4 py-12 max-w-3xl">
  <header class="mb-8">
    <h1 class="text-4xl font-bold mb-4">{post.title}</h1>
    <div class="flex items-center gap-4 text-muted-foreground">
      <time datetime={post.publishedAt}>{formatDate(post.publishedAt)}</time>
      <span>•</span>
      <span>{post.author}</span>
    </div>
    {#if post.tags?.length}
      <div class="flex gap-2 mt-4">
        {#each post.tags as tag}
          <span class="px-2 py-1 bg-muted rounded-full text-xs">{tag}</span>
        {/each}
      </div>
    {/if}
  </header>

  {#if post.image}
    <img
      src={post.image}
      alt={post.imageAlt || post.title}
      class="w-full rounded-lg mb-8"
    />
  {/if}

  <div class="prose prose-lg dark:prose-invert max-w-none">
    {@html post.content}
  </div>

  <footer class="mt-12 pt-8 border-t">
    <p class="text-muted-foreground">
      Last updated: {formatDate(post.updatedAt)}
    </p>
    <a href="/blog" class="text-primary hover:underline mt-4 inline-block">
      ← Back to Blog
    </a>
  </footer>
</article>
```

## Step 7: Add RSS Feed

Create `src/routes/blog/rss.xml/+server.ts`:

```typescript
import { getAllPosts } from "$lib/server/blog";
import type { RequestHandler } from "./$types";

export const GET: RequestHandler = async () => {
  const posts = getAllPosts();

  const xml = `<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Seam Blog</title>
    <description>Tips, guides, and updates about Mac notch apps and MacBook productivity.</description>
    <link>https://getseam.app/blog</link>
    <atom:link href="https://getseam.app/blog/rss.xml" rel="self" type="application/rss+xml"/>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    ${posts
      .map(
        (post) => `
    <item>
      <title><![CDATA[${post.title}]]></title>
      <description><![CDATA[${post.description}]]></description>
      <link>https://getseam.app/blog/${post.slug}</link>
      <guid isPermaLink="true">https://getseam.app/blog/${post.slug}</guid>
      <pubDate>${new Date(post.publishedAt).toUTCString()}</pubDate>
    </item>`,
      )
      .join("")}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml",
      "Cache-Control": "max-age=3600",
    },
  });
};
```

## Step 8: Update Sitemap

Add blog URLs to your sitemap. Create or update `src/routes/sitemap.xml/+server.ts`:

```typescript
import { getAllPosts } from "$lib/server/blog";
import type { RequestHandler } from "./$types";

export const GET: RequestHandler = async () => {
  const posts = getAllPosts();

  const staticPages = ["", "/blog", "/download", "/changelog", "/faqs", "/terms"];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${staticPages
    .map(
      (page) => `
  <url>
    <loc>https://getseam.app${page}</loc>
    <changefreq>weekly</changefreq>
    <priority>${page === "" ? "1.0" : "0.8"}</priority>
  </url>`,
    )
    .join("")}
  ${posts
    .map(
      (post) => `
  <url>
    <loc>https://getseam.app/blog/${post.slug}</loc>
    <lastmod>${post.updatedAt}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>`,
    )
    .join("")}
</urlset>`;

  return new Response(xml, {
    headers: {
      "Content-Type": "application/xml",
    },
  });
};
```

## Step 9: Add Prose Styles

If using Tailwind, add prose plugin or custom styles for markdown content:

```css
/* In app.css or a component */
.prose {
  h1,
  h2,
  h3,
  h4 {
    font-weight: 700;
    margin-top: 2em;
    margin-bottom: 0.5em;
  }

  p {
    margin-bottom: 1em;
    line-height: 1.75;
  }

  ul,
  ol {
    margin-left: 1.5em;
    margin-bottom: 1em;
  }

  li {
    margin-bottom: 0.5em;
  }

  a {
    color: var(--color-primary);
    text-decoration: underline;
  }

  code {
    background: var(--color-muted);
    padding: 0.2em 0.4em;
    border-radius: 0.25em;
    font-size: 0.9em;
  }

  pre {
    background: var(--color-muted);
    padding: 1em;
    border-radius: 0.5em;
    overflow-x: auto;
  }

  img {
    border-radius: 0.5em;
    margin: 1em 0;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
  }

  th,
  td {
    border: 1px solid var(--color-border);
    padding: 0.5em;
    text-align: left;
  }
}
```

## Checklist

- [ ] Install mdsvex and shiki
- [ ] Configure svelte.config.js
- [ ] Create content directory structure
- [ ] Create blog types
- [ ] Create blog loader
- [ ] Create blog routes (index + [slug])
- [ ] Add RSS feed
- [ ] Update sitemap
- [ ] Add prose styles
- [ ] Test with sample article
- [ ] Deploy and verify
