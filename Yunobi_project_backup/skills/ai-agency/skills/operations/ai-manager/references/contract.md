# The asset contract

**Every skill and every agent is written through the `ai-manager` skill.** Invoke it before writing or editing one, including a small edit to an existing body: it owns the four kinds, the description contract, `references/skill-floor.md` (the quality bar its write, repair and clean paths all use) and the review that gates the ship. Editing a `SKILL.md` by hand is how two standards end up in one registry. This file holds the placement, the naming and the reconcilers; it does not restate the floor. Search first, before creating anything new under `ai-doc/` or `.claude/`, and extend what exists rather than duplicating.

## Check order

1. `ai-doc/skills/`: browse by business area (`ls ai-doc/skills`). Grep descriptions for the topic.
2. `ai-doc/agents/`: the specialists, each with a `skills:` line naming what it loads. `agents/README.md` is the table.
3. `ai-doc/references/`, and every skill's own `references/`: grep by topic, where a document with no owner ends up and a near-duplicate hides.
4. `.claude/skills/`, `.claude/agents/`: the flattened view used by Claude Code at runtime.

If a close match exists, extend it or note the overlap explicitly when proposing a new item.

## Creation criteria

A new skill, agent or reference is justified only when all of the following are true: no existing item covers the scope (similar is not the same; 70%+ coverage means extend instead); the topic is bounded enough to write a crisp one-line description with no overlap; and it fits a single responsibility (skills wrap workflows and one-shot actions, agents wrap personas, references wrap documents nothing loads).

## A skill is the third-best fix, so try the first two

Before writing a skill or a reference to stop a recurring agent mistake, work down this order and stop at the first level that ends the problem, because each level removes the failure instead of describing it.

1. **Architecture.** Change the code or the data structure so the mistake cannot be expressed: shared types across surfaces, one home for a value, a function that cannot be called wrongly. Always worth a second and a third attempt before moving on.
2. **A lint rule, a test, or a CI gate.** The agent hits the failure and fixes it before it reports back, so the mistake never reaches a human. A budget with a ceiling (bundle size, query count, bytes on the wire) catches a whole category, not one instance.
3. **A skill or a rule.** Only now, and best on the process around the code (how to expose a dev server, how to file the PR, how to drive a third-party tool), worst as a list of things not to do inside the code, since the code is where levels 1 and 2 belong.
4. **A human in the loop.** You should not get here.

Skip level 1 and the registry fills with workarounds for problems the code should have made impossible. When a new skill is proposed to prevent a recurring mistake, say in one line why levels 1 and 2 cannot hold it.

**Measured on this registry, 2 to 3 Sep 2026.** The corpus that bans em dashes held 2,208 of them across 248 files, written into 28 skills and checked in none. `slopGate` never looked at emoji or hashtags, so 13 skills wrote that ban out again as a checklist bullet covering for a gate that reported the draft clean. 15 files pointed at `copy.md`, deleted months earlier, calling it auto-loaded, which nothing has ever been. A thumbnail word cap lived in a doc comment and drifted into the wrong number while telling every reader to trust it over its own measured law. Every one of those is a level 3 answer to a level 2 problem. **The tell is a rule you can write a regex for**: if you can, the regex is the fix and the paragraph is the bug.

## Importing an external skill set

Borrowing from an outside pack (TopRank, a vendored repo, a plugin) is a surgical merge, never a
blanket rewrite: our skills are already tightened against the budgets above, and a wholesale
import regresses that work. Map every external piece onto an existing skill first and skip the
duplicates, split what is left into gaps, distinctive and overkill, prefer an additive edit to an
existing `SKILL.md` section over a new skill, and create one only when nothing here can hold the
pattern and the creation criteria above pass. Then sync, per [Syncing what you
changed](#syncing-what-you-changed).

**A skill whose core came from someone else carries `author: "<name>"`** in its frontmatter
(Matt Pocock, Emil Kowalski, Anthropic), and the ai-library table prints it in its By column. No
key means the author wrote it. A borrowed reference inside our own skill gets credit in that file, not
the key.

A vendored skill that tracks an upstream repo is a third case: copied verbatim and re-vendored, not edited. Record the refresh procedure in the skill's own `README.md`.

## A copy in a consumer's `.claude/skills/` is invisible rot

`vibekit sync` projects symlinks, and `--prune-legacy` only sweeps inside the directories a manifest subscribes to, so a pack copied in by hand sits in a repo forever: nothing updates it, nothing prunes it, and the model is offered it beside the live copy. It went unnoticed until a skills browser listed the whole machine and `adapt` appeared nine times.

**`pnpm vibekit doctor` is the check**, run from `CLIs/`. It scans every repo beside vibe-kit for real (non-symlink) skill directories and names three shapes: `plugin-shadow` (an installed plugin already provides it, descriptions agree), `cross-repo-copy` (one skill copied into 3+ repos with no vibe-kit source, compared by description since every app has its own `ship`), and `double-projection` (the same skill in `.claude` and a second projection folder; only the secondary copy is listed). `--fix` deletes, and refuses to run without `--only <kind>` or `--name <list>`, since clearing every shape at once would take packs that have no other source; deleted files are git-tracked, so `git checkout` brings them back. The first run cleared 145 directories: 139 impeccable **v2.1.1** sub-skills across 9 repos while the installed plugin had reached 4.1.2 and merged all 19 into one skill, plus 6 copies of impeccable 4.0.4 shadowing it.

**`.agents/skills/` is the cross-runtime skills projection.** `vibekit sync` projects skills into `.claude/skills/` and `.agents/skills/` (which Codex, Gemini CLI, Antigravity and OpenCode read). Non-skill directories under `.agents/` (agents, commands, rules, inspiration) are dead.

## Impeccable comes from the plugin, not from here

Impeccable is the installed plugin at `~/.claude/plugins/cache/impeccable/impeccable/<version>/` and never an entry in a project's `vibekit.json`. Enable it with `claude plugin install impeccable@impeccable --scope project`: the `claude` wrapper passes `--setting-sources project,local`, so a user install never loads.

Its scripts also exit silently when reached through a symlink: every version from 4.0.1 guards its entrypoint with `resolve(process.argv[1]) === fileURLToPath(import.meta.url)`, and since `import.meta.url` resolves through symlinks while `argv[1]` does not, a script reached through a vibekit projection never matches, prints nothing and exits 0, reading as broken rather than skipped. Run them at their real plugin path; the guard is upstream, so do not patch the plugin cache, an update overwrites it. `concept-seed.mjs` additionally resolves `PRODUCT.md` from the working directory, so run it where that file lives.

**Impeccable defaults to React and Next.js, and every Studio project is SvelteKit.** Its skills (distill, harden, arrange, clarify, polish) will create `page-client.tsx` and React shadcn/ui components unless told otherwise, since the skill text never mentions Svelte. A subagent spawned for impeccable work must be told: this is SvelteKit not React, the file is `.svelte` using Svelte 5 runes, use shadcn-svelte, and here is the exact path to edit. **It invokes the impeccable skill, it does not edit directly**: the skills carry the design principles, checklists and anti-pattern detection a raw edit skips, so the prompt says "use the Skill tool to invoke `impeccable:<command>` before making changes".

## There is no command kind. A one-shot action is a skill

Claude Code merged custom commands into skills. `.claude/skills/deploy/SKILL.md` and `.claude/commands/deploy.md` both produce `/deploy` and run the same way, and where both exist the skill wins and the command file never runs, so a command file could only ever be a skill that was harder to find.

`ai-doc/commands/` holds no shape you should author. Eleven wrapper commands were deleted on 17 Aug 2026, each duplicating a skill that already owned its `/command`, five of them printing the *skill's* name in their own usage block so the file could never be reached by the name it told you to type. The seven that carried real instructions became skills in their business area on 23 Aug 2026, and the kind was removed from the manifest schema, the sync and the library. What survives in that folder is five `agency-os` files that `plugins/agency-os/build.sh` copies into the plugin, since a command file is the shipping format of a distributed plugin; nothing there is projected into a `.claude/`, nothing new belongs there, and the routing rule carries no command row.

**A skill's command comes from its directory name**, not its frontmatter `name`: the way to type `/refactor` is to name the directory `refactor`. A skill also does what a command cannot: a directory for supporting files, `paths` to scope when it auto-loads, `disable-model-invocation` for a manual-only workflow, and `allowed-tools` to pre-approve the tools it needs.

## Commands invoke. They never restate

A command names the skill to run, the arguments it takes, and nothing else. It does not summarise the workflow, list the quality gates, repeat a banned-word list, or describe the output shape; every one of those already has an owner, and a command that copies them is a second copy nobody updates.

**This is not a style preference, it is measured.** `/publisher:social` carried a 149-line copy of the `generate-social` workflow. By 8 Aug 2026 every drifted line had inverted the skill it was supposed to invoke: a question CTA where the skill bans engagement bait, 800-1200 characters against a measured target of 1000-1500, and five banned words checked against a list of 156. `/publisher:linkedin` instructed 2-4 hashtags against an absolute no-hashtag rule. Both ran green for months, because a command that contradicts a skill produces confident output and no error.

So the test for a command is length: **if it is longer than its own usage table, it is holding something that belongs somewhere else.** Skills route onward to the skills they depend on, which is why the command does not need to: naming `social` reaches `humanizer` and `idea-mining` for free.

## Self-healing requirement

Every instruction file updates itself when a session teaches it something. The protocol (the four-part failure log, the entry format, the delete-first loop, the SSOT rules) lives in the `ai-manager` skill; `ai-doc/references/self-healing.md` holds what is specific to this workspace. A new skill ships the scaffold only when it already has real failures to seed the log with; an empty `## Learned Patterns` is worse than none.

## Quote the description, because a broken frontmatter block fails silently

A plain YAML scalar cannot contain `": "`, and a description is the one field long enough to hit it by accident: `patterns: backward-compat`, `in Remotion: subscribe`. When the block fails to parse **nothing warns at normal verbosity and every field is dropped**: the name falls back to the directory name, the description to the first line of the body, and `tags:`, `model:` and `allowed-tools:` quietly stop applying, so the skill stays in the listing, matched against arbitrary prose, and looks fine.

**Wrap every `description:` in double quotes.** It costs two characters and removes the whole class; the same goes for any value carrying a colon, a `#`, or a leading `[`, `{`, `*` or `&`.

The `` fences are **body syntax and never go inside the `---` block**: YAML has no comment of that shape, so a skill that varies its published wording writes one quoted `description:` (the public wording) and keeps the fences below the frontmatter. `boards:` cannot be fenced either: gluing the fence to the key gives a key named `` blocks removed, optionally carrying a
`<!--public …-->` sentence the public copy gets instead. A whole file stays home with
`<!--internal-only-->` on its first line, or a `<name>.internal.<ext>` filename where a data file
carries no comment. Editing the copy in `ai-agency` is lost on the next publish, and the two
checkers below are what say so before a push.

| Script | What it reconciles | Fails on |
| --- | --- | --- |
| `scripts/validate-architecture.mjs [--files ...]` | Every frontmatter block against the YAML parser the sync uses, every agent's `skills:` against the skills that exist and the ones its body names, the preload budget, and every Studio `vibekit.json` id | a block the sync cannot read, or an agent that cannot load a skill it relies on |
| `ai-doc/scripts/check-agent-readme.py [--fix]` | The master table and count in `agents/README.md`, against the filesystem | drift in membership **or in row text** |
| `ai-doc/scripts/check-descriptions.py [--files ...]` | Every skill and agent description against the contract above: a `Use when` trigger, the 300-char ceiling, no em dash, no banned word or phrase from `packages/lint/data/slop-words.js`, and an explicit non-Opus `model:` on an agent | a description the registry cannot route on |
| `scripts/check-slop.mjs [--all] [--fix]` | The corpus against the punctuation rule it teaches: em and en dashes, invisible characters. Staged runs judge added lines only, so a file is cleaned the next time somebody edits it | a dash or an invisible character on a line you wrote |
| `ai-doc/scripts/publish-public.mjs [--check]` | The skills on its manifest, scrubbed into the public `heyramzi/ai-agency` repo by post-commit, plus the `FROZEN` public-only set the course commands run; a write deletes any other public skill and rebuilds the zips | a stale public copy, a public skill with no source and no `FROZEN` entry, or a name, id, private path or monorepo-only command surviving the scrub |
| `clickup-utils/scripts/skills.mjs check` | The ClickUp and board skills, which `clickup-utils` owns and publishes itself, plus the symlinks that give vibe-kit one copy of each | a broken link, or the same leak list, which lives there and both publishers read |
| `skills/content/social/social/scripts/linkedin-scripts/copy-score.py --check --corpus <posts.json>` | The copy scorer against the corpus it was built from | the score no longer separating each creator's best posts from their worst |

The description contract is gated twice, at write time and at sync time:
`ai-doc/hooks/extensions/description-gate.sh` runs as a `PostToolUse` hook on `Write|Edit`
and refuses a skill or agent file whose description breaks the contract, and a copy under a
consumer's `.claude/` that shadows an asset vibe-kit already owns. It was added on 30 Aug
2026 after the contract, written in three files and checked in none, was found broken by 37
descriptions. That is the ladder above applied to the registry itself: the rule moved from
level 3, where it only held when a session read it, to level 2, where the session hits it
and fixes it before reporting back.

The row-text half of the first one was added on 26 Aug 2026 after it reported "in sync" while eight
leads restated descriptions that had changed months earlier. A reconciler that compares only names
is a reconciler that is wrong in the one way nobody checks.

The public twins are **supposed to differ**: the private copy names `humanizer`, the cost policy and
real paths, the public one is generalised for a stranger. What is not supposed to happen is a rule
learned once and written into only one of them. Read the line count gap before assuming the split is
still deliberate.

Write, heal and clean are one skill sharing one floor, per `SKILL.md`; when redundancy is found, `ai-manager clean` is the path, against `.claude/`, `ai-doc/` or any plugin folder.
