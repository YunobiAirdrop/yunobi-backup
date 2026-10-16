# Review Rubric

The judgement half of a skill review. Run `scripts/review_skill.py <dir>` first: it
settles frontmatter constraints, body size, dead links, unreachable references,
script ergonomics and the mechanical shapes the floor refuses, all without an
opinion. What is left needs a reader.

Scoring is the verdict on a finished skill. [skill-floor.md](skill-floor.md) is the
same bar stated as instructions, and it is what to read while writing rather than
while judging.

Score each dimension 1-5. A 3 is acceptable, not a failure. Score honestly; a
registry of 5s that nobody triggers is worth less than a 3 that runs every week.

Adapted from the MIT-licensed rubric in `agentskill-sh/ags`, cut to what the
script cannot check and extended with the three dimensions this registry cares
about (D6, D7, D8).

| Total | Verdict |
| --- | --- |
| 33-40 | Ship it. |
| 25-32 | Fix what scored 3 or below, then ship. |
| 17-24 | Rewrite the low dimensions before anyone runs it. |
| Below 17 | The skill has the wrong shape. Restart from the run that produced it. |

---

## D1: Triggering

Will the runtime pick this skill for the right prompts, and leave it alone for
adjacent ones? The description is the whole test: it is the only part preloaded
into every session.

| Score | Criteria |
| --- | --- |
| 5 | Says what it does **and** when to use it. Carries the words a user would actually type. Third person. Distinguishable from every neighbouring skill in its family. |
| 4 | Both halves present, one trigger word missing. |
| 3 | What without when, or when without what. Or first/second person. Or too generic to separate from a sibling. |
| 2 | Vague ("helps with files"), or would false-trigger on unrelated work. |
| 1 | Empty, one word, or misleading. |

Check it against the family, not in isolation: two descriptions that both fit the
same prompt are one merge, not two skills.

## D2: Conciseness

Does every token justify what it costs to read?

| Score | Criteria |
| --- | --- |
| 5 | Only what the model does not already know. Every paragraph survives "would the base model get this wrong without this sentence?" |
| 4 | One or two sections could go. |
| 3 | Explains things the model knows: what a CSV is, how HTTP works, what a migration does. |
| 2 | Several paragraphs of background before any instruction. |
| 1 | More explanation than instruction. |

Red flags: defining common terms, restating the filesystem, "In this section we
will", the same instruction said twice in different words.

## D3: Instruction Clarity

Can the skill be followed without interpretation?

| Score | Criteria |
| --- | --- |
| 5 | Sequential, unambiguous steps. One term per concept throughout. Concrete examples where the format matters. Edge cases named. |
| 4 | Clear, with one ambiguous area. |
| 3 | Followable but needs interpretation. Inconsistent terms, or no example where one is needed. |
| 2 | Could be followed two different ways. Key steps missing. |
| 1 | Contradictory or incomplete. |

No time-sensitive text: a date or a "as of August 2026" ages into a lie. Write
"current" and "legacy" sections instead.

## D4: Freedom Calibration

Is each part as prescriptive as its fragility deserves?

| Score | Criteria |
| --- | --- |
| 5 | Destructive or fragile steps carry exact commands. Creative steps give criteria, not a script. One default per choice, alternatives named in a clause. |
| 4 | One area slightly over or under constrained. |
| 3 | Presents a menu of equal options where a default belongs. Or scripts a judgement task rigidly. |
| 2 | Fragile operations with no guardrail, or creative work under a rigid template. |
| 1 | Every step treated the same regardless of what it touches. |

State the "why" behind a rigid rule, so the reader can tell an edge case from a
violation.

## D5: Progressive Disclosure

Does the skill load context only when it earns it?

| Score | Criteria |
| --- | --- |
| 5 | SKILL.md is overview plus navigation. Each reference carries a condition for loading it: "read `api-errors.md` when the API returns a non-200". |
| 4 | Good separation, one file loaded unconditionally that should not be. |
| 3 | References exist but SKILL.md never says when to open them. |
| 2 | Most detail still in the body; references are a dumping ground. |
| 1 | One long body, no references, despite the skill being complex. |

"See references/ for details" scores 3 at best. The condition is the point.

## D6: Placement

Does the skill belong where it sits, and does it need to exist?

| Score | Criteria |
| --- | --- |
| 5 | In the narrowest family that fits. Nothing else in the registry covers 70% of it. The scope is one coherent unit of work. |
| 4 | Right family, scope slightly wide or narrow. |
| 3 | Overlaps a sibling enough that a prompt could land on either. |
| 2 | Duplicates an existing skill, or sits loose in an area with no family. |
| 1 | Should be a paragraph in an existing skill, not a file. |

The registry-wide version of this is the clean path. Run it when D6 scores 3 or
below across several skills at once.

## D7: Provenance

Did the skill come from work already done twice?

| Score | Criteria |
| --- | --- |
| 5 | Written out of a real run. The examples are things that actually happened, with the real names, numbers and errors. |
| 4 | Real run, examples generalised past the point of being checkable. |
| 3 | Plausible but unrun: correct-sounding steps nobody has executed. |
| 2 | Designed in a planning session against an imagined need. |
| 1 | Describes a capability that already exists elsewhere in the repo as a script. |

A skill invented before its second run is the commonest way this registry grows
without getting better.

## D8: Self-Healing

Does the skill learn from its own failures?

| Score | Criteria |
| --- | --- |
| 5 | `heal.cjs check` passes: stated promise in the body, a closing step, a verification item, and a `## Learned Patterns` section seeded with real entries. |
| 4 | Scaffold present, log thin. |
| 3 | Scaffold present, log empty. An empty log is worse than none. |
| 2 | Promise made, nowhere to write it. |
| 1 | The skill has repeated a mistake and nothing records it. |

Score N/A for a skill with no failures to seed it. Do not ship an empty section
to score the point; see the failure log section in `SKILL.md`.

## Improving by outcome

Read this after a skill has run on real work and the output was wrong, thin, or slower than doing
it by hand. Also read it before shipping a skill that touches a client, a payment, credentials or
production. The rubric above scores a finished file; this loop judges a skill by what it produced.

### The loop

Run a real task, judge the output, say what was wrong, write the correction into the file, then
**start a new session and run the task again.** The last step is the whole test and the one that
gets skipped: a retest inside the session that wrote the fix proves nothing, because the model
complies with the correction whether or not the file carries any weight.

### How hard to hold the file

| Risk | Loop |
| --- | --- |
| Creative and reversible: copy, thumbnails, boards, drafts, research | Outcome only. Let it run, correct what came out, keep moving. The file is a means. |
| Anything touching a client, a payment, credentials, published output or production | Read the file, and give it a second pass before it ships. An instruction that quietly does the wrong thing costs more than any amount of iteration speed. |

Getting this backwards is expensive both ways: hand-tuning a thumbnail skill's wording is wasted
effort, and shipping an unread client-facing skill on one good output is how a bad instruction
reaches somebody else.

### The baseline is the only evidence a skill helps

A skill that produces a good result has not been shown to do anything, since the model might have
produced the same result alone. Run the same prompt twice in the same turn: once with the skill,
once without. For a revision, the baseline is the previous version of the file, snapshotted first.

Read the transcripts, never only the outputs. A skill that reaches the right answer after two dead
ends costs more than it saves; the fix is deleting the paragraph that opened the detour.

### Four ways to improve a file

1. **Generalise past the test cases.** A fix that only satisfies the examples in front of you is
   overfitting; try a different framing rather than a narrower rule.
2. **Cut what is not pulling its weight.** Deletion is the commonest correct edit.
3. **Say why.** A rule with its reason attached survives an edge case the rule did not foresee.
4. **Bundle the script three runs wrote independently.** A helper every run reinvented belongs in
   `scripts/`, named from the skill.

### Stop when

The output is right without the correction being in the conversation, the remaining feedback is
empty, or two iterations in a row have not moved anything.

### Wording rules age out

Advice that a skill must be phrased a particular way to perform is true of one model on one day.
Write for the reader, hold the outcome, and re-run the cleared-session test after a model change
rather than carrying a style rule forward on faith.
