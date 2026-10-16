---
paths:
  - "**/*.{ts,tsx,js,jsx,mjs,cjs,svelte,swift,py,go,rs,sh,css,sql}"
---
<!-- vibekit:rule -->
<!-- Generated. Edited in the source this repo is projected from, never here. -->

# Comments

**A whole comment block caps at 30 words, not each line.** A run of `//` lines with no blank line between them is one block, and `@heyramzi/lint` counts it that way before the pre-push hook fails the push. Ramzi, 19 Sep 2026: *"never have such long comments, should be ultra concise."*

Write one sentence naming the trap, then a path to the reference that holds the reasoning. Never a paragraph, never a numbered list of reasons, never a second "WHY" after the first.

**No gate keeps an allowlist.** Ramzi, 28 Sep 2026: every linter is a hard limit, and a violation gets fixed, never recorded. Never add an allowlist, baseline, ignore marker or `--update` mode to get a push through.
