# Skill floor

Load this once the shape is settled and immediately before writing a `SKILL.md`, an agent, or a
rewrite of one. It carries the quality bar, the shapes to refuse, and the reflexes no script
catches. Do not load it for planning-only work.

`python3 scripts/review_skill.py <dir>` already settles the mechanical half. Act on its findings
rather than re-checking each one by hand; what follows is what it cannot see.

## Verify

Each of these is a check on the written file, never on the intention behind it. Read the file back
and answer with the line that satisfies the check, or with the edit that will.

- **Trigger.** The description says what the skill does and when to reach for it, in the third
  person, in the words a user would actually type. The full contract, the 300-character ceiling
  and the eval for a description that fires wrong: [Triggering](#triggering) below.
- **Provenance.** Every example is something that happened, with the real path, number, error or
  name. An invented example teaches the reader to trust none of them.
- **Altitude.** The body routes; the references do. If a section can be lifted whole into a
  reference with a one-line pointer left behind, it belongs there. Every markdown file in a skill
  stays under 200 lines, references included, and a body that is mostly reference material is
  failing at 120. Ten markdown files per skill is the other ceiling, and both are gated: `humanizer` ran 247 lines pointing at 21 files totalling 330 KB, and a session read the
  body, opened none of them, and shipped the slop the skill exists to stop.
- **Disclosure.** Every reference link carries the condition that opens it: "read `api-errors.md`
  when the call returns a non-200". A pointer with no condition is loaded always or never, and
  which one is a coin toss.
- **Freedom.** Fragile and one-way steps carry the exact command. Craft steps carry criteria and a
  default, so the reader can tell an edge case from a violation. State the reason behind a hard
  rule in the same breath as the rule. A craft number is a default the model may depart from.
- **Verdict.** Every check has a pass condition a reader can answer. "Improve the hierarchy" has
  none. "Blur the detail and name the primary element, the secondary, and the groups in order" has
  one. A named test that returns an answer beats a paragraph describing quality.
- **Enforcement.** A skill that sets a standard ships the standard as an eval: numbered checks,
  each answered pass or fail on the finished output in a fresh read, looped until all pass, with a
  stated round ceiling and an exit for the draft that cannot pass without inventing facts. Prose
  describing an audit is not an audit, and that sentence sat in `humanizer` from the day it was
  written while every session skipped the pass it named. The eval lives in its own reference, not
  in the body: the body is read before the work and the eval after it.
- **Shape.** Every rule carries something the reader can apply: a before and an after, a string to
  grep, a number to measure. A rule that names a category is a description of the failure, not a
  removal of it. The comparison worth holding is `no-ai-slop`, 97 lines where every line is a rule
  with a rewrite beside it, routing nowhere.
- **Coherence.** Read the skill's own rules against each other before shipping, and read any gate
  it ships against the rule the gate claims to enforce. Two first-party rules contradicted each
  other in `humanizer`, and its pronoun lint failed a ledger at parity while the rule it cited
  asks only that the first person outnumber the second.
- **Cost.** The skill states its own ceiling where a loop could open: how many passes, how many
  reads, when to stop. Work with no stated ceiling runs until the context does.
- **Boundaries.** The skill names what it does not own and names the skill that does. Name the
  other skill; never link to it by path, because a path that resolves in `ai-doc/` breaks in every
  flattened `.claude/skills/` projection.
- **Handoff.** The last line says where the work goes next, or says the work is done.
- **Frontmatter.** `name` equals the directory. `description` under 300 characters and free of
  angle brackets. `allowed-tools` only where it removes a prompt the skill hits every run.
  `disable-model-invocation: true` on anything that should only ever be typed.
- **Self-healing.** The four parts, seeded with real entries, or the section is absent.
  `ai-manager` owns the format and `heal.cjs check <dir>` owns the verdict.

## Refuse

These are the defaults a body falls into when nobody decided, and the run's own evidence can earn
any of them back. Reaching for one while the choice was free means the decision was skipped;
recognising that means cutting the section, not softening it.

Shapes that look like a skill:

- **A skill designed before its second run.** A planning session that asks "what skills should
  exist" produces files nobody triggers. The signal to write one is having just done the thing for
  the second time, and that run is the draft.
- **A persona in a `SKILL.md`.** "Expert X specialising in Y" with no procedure is an agent
  wearing the wrong extension. The reverse also holds: an agent whose body is a checklist with no
  judgment is a skill in a costume.
- **A registry of the filesystem.** A hand-maintained list of what is in the next directory goes
  stale in silence, because nothing reconciles it. Generate it or delete it.
- **A wrapper that restates the skill it calls.** Naming the skill reaches everything that skill
  reaches. A file longer than its own usage table is holding something with an owner elsewhere.

Sentences that cost more than they carry:

- Prose the base model already knows. What a CSV is, what a migration does, what good typography
  looks like in general. What survives is what this workspace decided: a number, a path, a name, a
  preference, a thing that went wrong once.
- `ALWAYS` and `NEVER` in capitals where the reason would do the same work better. A reader who
  knows why can handle the case the rule did not foresee; a reader holding a shouted rule cannot.
- A menu of equal options where a default belongs. Pick one, name the alternative in a clause.
- An anti-pattern stated abstractly. "Avoid generic output" is unfalsifiable. "A colored
  `border-left` above 1px on a card" can be checked by grep.
- "See `references/` for details." The condition is the whole pointer.
- A line announcing that a tool, skill or stack is gone, or that one skill was merged into
  another. Delete every mention of the thing instead, so no file ever has to say it left. The author,
  23 Sep 2026: *"it's about removing mentions of it."* `check-skill-length.mjs` fails the words.
- A date, a version, or "as of August 2026" inside a claim. It ages into a lie that reads as
  current. Write the current shape and, where the old one still exists somewhere, a labelled
  legacy section.
- Filler headings from an imported pack: "Initial Assessment", "Best Practices", "Common
  Mistakes", a Success Metrics table nobody measures.
- A `## Learned Patterns` section shipped empty. It teaches the reader to skip the section.

One of these is a ban rather than a default, and no evidence earns it back:

- **A second copy of a fact that already has a home.** Every fact lives in exactly one file and
  every other mention is a pointer to it. Two copies do not disagree on the day they are written;
  they disagree three months later, both read as current, and the reader has no way to tell which
  one won. Grep for the fact before writing it anywhere.

## Triggering

Read this when writing a description, when a skill keeps getting picked for the wrong prompt, or
when one that should have fired stayed quiet. The description is the only part of a skill
preloaded into every session, read against every other description in the registry at once, so it
is written against its siblings rather than in isolation.

**Undertriggering is the common failure, not overtriggering.** A description that reads as a
neutral summary loses to the model's own confidence. Lean on the trigger half: name the contexts,
name the phrasings, and say plainly that the skill covers them.

**A one-step task will not trigger a skill however good the description is.** "Read this PDF" is
handled directly. This makes simple prompts worthless as tests, and it means a skill whose whole
job is one tool call has a shape problem the description cannot fix.

The description contract, two halves, both required, in the third person:

1. **What it does**, concretely enough to separate it from its siblings.
2. **When to reach for it**, in the words a user types. Include the casual phrasing, the tool or
   file names, and the moment in a workflow, rather than the formal name of the task alone.

A third part earns its place only sometimes: **what it is not for**, when a sibling is close
enough that a prompt could land on either. `impeccable` ends with "Not for backend-only or
non-UI tasks", and that clause does more separating work than another sentence of scope.

**Ceiling is 300 characters, and `check-descriptions.py` refuses the commit above it.** It was a
500-character budget behind a 1024 cap nothing could reach, so 135 of 186 assets sat over budget
and the registry spent 67,000 characters, about 17k tokens, before the user asked anything.
Rewrite in this order when it is over: cut the mechanism (how it works belongs in the body), cut
the inventory (a list of what is inside), cut the self-description ("this skill provides"). Keep
what plus when.

**Trigger evals**, worth running when a skill sits next to close siblings or fires on the wrong
prompts, skippable when nothing competes with it: write 20 realistic queries, 8 to 10
should-trigger (different phrasings, an uncommon use, one that beats a sibling) and 8 to 10
should-not-trigger (near-misses that share keywords but need something else), store them as
`evals/trigger.json` (`{"query": "...", "should_trigger": true}`), and run each three times. Score
the should-not-trigger half first: a description that fires on everything is worse than one that
fires on nothing, since it displaces the correct skill in every neighbouring session. Split the
set before optimising, tune against 60% and judge on the rest, or the description gets rewritten to
match the examples instead of the intent.

**Two skills whose descriptions keep matching the same prompts are usually one skill with two
branches.** Merging is the fix; see [critique.md](critique.md#doing-the-merge). Rewriting both
descriptions to be more specific about the same territory produces two narrower descriptions that
still overlap.

The floor holds the mechanics. It never decides what the skill is for. With every check green,
spend the file on what only this workspace knows.
