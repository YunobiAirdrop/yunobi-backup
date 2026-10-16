# Context Budget

## Contents

- What each level costs
- The registry that is not ours
- MCP servers, connectors and the rest of the session
- Zero-use is the prune list, not a retrieval problem
- Cutting a description
- Cutting a body
- Splitting to references
- Frontmatter levers that remove cost
- Anti-patterns from the standard

## What each level costs

Three loading levels, three different prices.

| Level | Loaded | Price | Budget |
| --- | --- | --- | --- |
| `name` + `description` | Every session, before anything is asked | About 100 tokens per asset | 500 chars, 1024 hard cap |
| `SKILL.md` body | When the skill fires | Under 5k tokens, and it stays in the conversation for the rest of the session | 250 lines |
| `references/`, `scripts/` | When read or run | Zero until touched. A script that runs costs only its output | None |

Two consequences drive every decision in this skill.

**Metadata is the only line item that every session pays.** A registry of 250 assets at 400 chars each spends 25k tokens before the user types a word. Cutting one description by 300 chars saves more real context than cutting 100 lines from a body that fires twice a month.

**A body does not unload.** Claude Code puts the rendered `SKILL.md` into the conversation as one message and never re-reads the file, so a 400-line body sits in context until the session ends. This is why the fix for a long body is to move material out, not to keep it and read it faster.

## The registry that is not ours

A plugin's skills are metadata in every session too, and a plugin can arrive without being
installed: a Claude account syncs org plugins into `~/.claude/plugins/synced/`, where neither
`enabledPlugins` nor `skillOverrides` reaches them and an edit to their `.meta.json` is rewritten
at the next startup. `claude plugin list` shows them as `<name>@synced`, `claude plugin details
<name>@synced` prints the always-on token cost, and `claude plugin disable <name>@synced` is the
one switch that works.

Measured 18 Sep 2026: `sales@synced` alone carried 36 skills for **~3,286 always-on tokens**, with
`brand-voice` and `cowork-plugin-management` beside it and no recorded use of any of the 43. All
three are off. For comparison, the 19 skills projected into sitehub cost about 1,500 tokens
together, so an unwatched plugin outweighed the whole project registry.

Check `~/.claude.json` `skillUsage` before turning anything off; it counts every invocation per
skill, which is what separates a plugin nobody opened from one that answers a third of the work.

## MCP servers, connectors and the rest of the session

The registry is the smallest part of a full context window. On 25 Sep 2026, `/context` read 83.6k used before a word was typed, and **223k
more sat in deferred MCP schemas**. Ten claude.ai connectors made up almost all of that, and
Make alone carried about 100 tools.

1. **Measure calls, not config.** `python3 scripts/mcp_usage.py 45` counts every MCP call,
   subagent and plugin skill in 45 days of transcripts, then lists each configured server that
   was never called. That day, 18 servers had zero calls. Gmail had 150, all from 4 repos.
2. **Interview on that evidence**, a few questions per round, each with a recommended default:
   dead cloud connectors, live ones scoped or replaced by a CLI, Claude in Chrome, local servers,
   then agents, plugins and instruction-file overlap. Ask. Don't guess. A connector with zero
   calls in Code can still be his daily tool on claude.ai web.
3. **Pull the lever that owns the cost.** They're all config, so nothing needs a click from him:

| Source | Lever |
| --- | --- |
| claude.ai connectors | `"ENABLE_CLAUDEAI_MCP_SERVERS": "false"` in `~/.claude/settings.json` `env` turns them all off, since a CLI covers each one (`gws`, `cu`, `make`, `pnpm descript`). One session opts back in with `ENABLE_CLAUDEAI_MCP_SERVERS=true claude` |
| Claude in Chrome | `claudeInChromeDefaultEnabled: false` in `~/.claude.json`, then `claude --chrome` for one session |
| User and per-project servers | `mcpServers` in `~/.claude.json`, top level and under each `projects[path]`. Prune the matching `disabledMcpServers` names too |
| Repo servers | every `.mcp.json`, including nested `web/` ones and `vibe-kit/starters/*`, which seed the next repo. A tracked one in a repo with worktrees comes back whenever a worktree gets rebuilt, so delete it in the main checkout and leave the worktrees to their session |
| Plugins | `~/.local/bin/claude plugin uninstall <name>@<marketplace>`. One plugin can ship a remote MCP server along with its skills |
| Agents | Nothing on Claude's side reads `.claude/agents`, because delegation goes through Orca, so `vibekit sync` doesn't project them there anymore. Delete stray copies from imported packs in `.claude/agents/` and `~/.claude/agents/` (a plugin's own agents already load from the plugin) |
| Instruction files | each rule gets one home: the conduct core for every repo, `Studio/AGENTS.md` for the workspace, nothing in `~/.claude/CLAUDE.md`. Two copies of a rule end up saying different things: on 25 Sep the home file said "leave the other repo alone" while the core said "fix it in every repo" |

4. **Reroute every caller before you call it done.** `grep -rnE "mcp__<server>|<Name> MCP"` over
   `ai-doc/` and every repo's `docs/`, then rewrite each hit to its CLI command. A skill left
   calling a disabled tool fails silently. When no CLI covers the job (Make's module schema),
   the line names the one-session opt-in instead.
5. **Re-run `mcp_usage.py`.** Its footer should read `connectors: off`, and nothing configured
   should show zero calls unless he chose to keep it.

## Zero-use is the prune list, not a retrieval problem

`~/.claude.json` `skillUsage` carries `usageCount` and `lastUsedAt` per skill, across every
project on the machine. Cross it against a repo's projection and the dead weight names itself.

Measured 18 Sep 2026 on the largest product repo: 120 skills projected, **~9,500 always-on tokens** for their
`name` + `description`, about 1% of a 1M window. **36 of those 120 have never fired once**,
worth ~2,800 tokens a session. The 1.14 MB of bodies costs nothing until a skill fires.

So a hosted skills library (Skillbox and the like: a Postgres service, an MCP `search_skills`
tool, an LLM scorer to rank) buys back under 1% of the window and charges for it: a second
source of truth outside git, a service that must be up before any session has skills, a search
round trip at every task start, and skills that fire only when the model chooses to search
instead of when a description matches. Rejected 18 Sep 2026. The prune is the whole win, and it
is free.

**`disable-model-invocation: true` is not free for a routed skill.** It removes the description
from the prompt and keeps `/name`, but a skill another skill dispatches into by name has to
stay model-invocable. Unsubscribe it in that repo's `vibekit.json` instead, or delete it.

## Cutting a description

Target shape, two sentences: what it does in third person, then `Use when <trigger>, when <trigger>, when <trigger>.`

Claude Code truncates `description` plus `when_to_use` at 1,536 chars in the skill listing, so anything past that is dropped silently. Put the strongest trigger first.

The cuts, in the order they pay:

1. **Delete the capability inventory.** Twenty comma-separated nouns describe the body, not the trigger. Keep the triggers.
2. **Delete the mechanism.** How the skill works is the body's job. "through a hybrid SQLite-index plus AppleScript bridge" never helped anyone pick it.
3. **Delete self-description.** "Self-healing", "appends new failure modes to its own pattern list after each run" is true of most skills here and separates none of them. It belongs in the body.
4. **Collapse near-identical triggers.** "when a post needs writing, when content needs creating, when copy needs drafting" is one trigger written three times.
5. **Keep the words a user would type.** Product names, file types, verbs. These carry the match.

Before (819 chars):

> Self-healing skill that manages a Descript project's media through the API and MCP, importing raw takes and b-roll, naming them, and foldering them one folder per video, and reorganises an existing library by driving the Project panel through Orca's browser, which is the only surface that can move media between folders. Covers the write-once naming constraint, the per-call media cap, the one-job-at-a-time lock, when direct upload beats URL import, the slow drag a drop needs, and how to pair a camera take with its screen recording. Appends new failure modes to its own pattern list after each run.

After (196 chars):

> Imports, names and folders media in a Descript project, and reorganises a messy media library. Use when footage or b-roll needs to land in Descript, or when a Descript project's media browser is full of loose files.

Everything cut is still in the body, where it is read only by the session that opened the skill.

## Cutting a body

The first question for every paragraph: **does the model already know this?** The base model knows what a PDF is, what a pivot table is, how HTTP works, what git does. Text that explains a general concept before giving the instruction is pure cost. Delete the explanation, keep the instruction.

The second question: **is this a fact or a feeling?** "Buffer accepts a 600-character tweet and lets it die at send" changes behaviour. "Be careful with character limits" does not.

The third: **is the specificity earned?** Match freedom to fragility.

| The task | Write it as |
| --- | --- |
| Many valid routes, context decides | Prose direction. Trust the model to route |
| A preferred pattern with variation | A template with parameters |
| Fragile, sequence matters, hard to undo | The exact command, with a line saying not to vary it |

An over-specified creative task wastes tokens and produces worse output. An under-specified migration corrupts data.

## Splitting to references

When a file is over 200 lines, move material out rather than compressing prose. What moves:

- Tables of values, schemas, API surfaces, command inventories
- Long examples and before/after pairs
- Anything used by one branch of the work and not the others. Split by domain so a task about sales never loads the finance file
- Learned Patterns logs past 25 entries. Fold the hardened ones into the body first (`node heal.cjs fold <skill>`), then delete the lines

What stays in `SKILL.md`: the flow, the decisions, the budgets, and one line per reference saying what is in it and when to open it.

Two rules from the standard govern the result:

- **One level deep.** Every file must be reachable from `SKILL.md` in one hop. Claude previews a file found only at the end of a chain with `head` instead of reading it, so the tail arrives truncated or not at all. Two references pointing at each other are fine as long as `SKILL.md` links both.
- **A reference over 100 lines with three or more sections opens with a `## Contents` list.** A partial read then still shows the full scope. A flat file, a dated log or a glossary has nothing to index and is exempt.

## Frontmatter levers that remove cost

Field names below are Claude Code's. The Agent Skills standard carries `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` only, so a skill meant to travel outside Claude Code has to survive on those.

| Field | What it does to context |
| --- | --- |
| `disable-model-invocation: true` | Drops the description out of the system prompt. The skill still runs as `/name`. Correct for anything with side effects that the user should time: deploys, publishes, sends |
| `user-invocable: false` | Keeps the description loaded and hides the skill from the `/` menu. For background knowledge with no meaningful command form |
| `paths: ["src/**/*.svelte"]` | Auto-loads only when the work touches matching files |
| `when_to_use` | Appended to the description and counted against the same 1,536-char cap. It buys nothing that a second sentence in the description does not |

A slash-command-only workflow that still advertises a 600-char description is paying rent on a listing nobody matches against. `disable-model-invocation: true` is the fix.

## Anti-patterns from the standard

| Anti-pattern | Fix |
| --- | --- |
| Several options offered for one job | Give one default. Name the escape hatch in one clause |
| Dated instructions ("before August 2025, use...") | State the current way. Put superseded ways in an `## Old patterns` section |
| Terms drifting inside one file (field, box, element) | Pick one term, use it everywhere |
| Bare MCP tool names | Fully qualify as `Server:tool_name`, or the lookup fails when several servers are connected |
| Backslash paths | Forward slashes everywhere |
| A tool assumed present | Name the install step before the usage |
| Magic constants in a bundled script | Say what the number is for, or delete it |
| A script that fails and leaves the model to work it out | Handle the error in the script |
| Vague names: `helper`, `utils`, `tools` | Name the activity |
| `name` not matching its directory, leading or trailing hyphen, double hyphen, over 64 chars, or containing "claude" or "anthropic" | Rename. The standard rejects all of these |
