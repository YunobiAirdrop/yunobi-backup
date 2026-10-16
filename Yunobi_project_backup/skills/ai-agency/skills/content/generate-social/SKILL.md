---
name: generate-social
description: "Writes LinkedIn and X posts from YouTube transcripts, ideas or client stories in the founder's own measured voice, holding the structural targets for length and block count and the ban on bait endings. Use when a transcript needs repurposing, when an idea, insight or client story should become posts, or on 'create posts', 'write content', '/generate-social'."
tags: [writes, social]
---

# Generate Social Content

One idea, many formats. Quality over quantity.

**A video beat is not a post.** `storytelling` owns the reason: the beat worked because he said it
while gesturing at a graphic, so transcribing it onto a slide or into a paragraph leaves only the
words and lands on rung 0, restating something the piece already said. Repurposing means re-deciding
what each unit does on the new surface, never porting the unit. Its `references/surfaces.md` holds
the row for a post, a thread and a carousel: the unit of change, where the loop lives, and the
rung-0 failure each one invites.

## Read what the feed rewards this month, before drafting

`social-engagement` derives it from competitor posts it collects itself, scored against each
account's own median so a 22,000-like account and a 21-like account contribute the same evidence:
`social-engagement`, `references/what-works.md`. It carries
its measurement date and a staleness ladder, because a feed re-ranks every month and a file does
not. Over 30 days old, collect the feed again before trusting the page.

It says what the feed rewards, never what is good. The bans in `@heyramzi/lint` and the voice in
`voice-dna` outrank every number on that page.

## Nothing goes out unless it has been through the gate

```bash
npx heyramzi-slop <file> --fix
```

Invisible characters removed, banned words, phrases and sentence patterns reported. The rule,
31 Aug 2026: *"anything before it gets published goes through there."* The reasoning belongs to
the `humanizer` skill's slop list; do not restate it here.

## Where the idea comes from, when nothing was handed to you

This skill starts from a source: a transcript, a story, a note. **When there is no
source and the ask is "write something", that is not a writing job yet.** Go to
`idea-mining`, which ranks the places a subject comes from and holds the pass over
the scored competitor catalogues, and come back with a topic and a seed. Writing
from a blank page is the lowest-yield source there is, and no amount of voice work
rescues a subject nobody wanted.


## Banned language

The auto-loaded `copy.md` rule carries the whole list, generated from `packages/lint/data/slop-words.js`, which is where a new ban goes. `humanizer` carries the reasoning and the judgement calls. Do not restate either here.

## When to Use

Not for: editing existing posts (edit directly), or for scheduling and analytics.
Distribution is `social-scheduling`, and it owns which network a post reaches and
through what. This skill stops at the draft and never names a scheduler, because
that stack has changed twice and a name written here goes stale in place.

## Workflow

### Phase 1: Load the Voice

Read all three, in this order:

1. The `voice-dna` skill, and its `references/measured.md`. That skill is the single
   home for what the author sounds like: the tics, the hook mechanisms, the anti-voice, and
   the counted targets for length, white space and question endings. Do not restate it
   here and defer to it on any conflict.
2. **The platform skill for each half, and neither is optional.**
   - LinkedIn: `linkedin-content`. `references/writing.md` holds the story shape and the
     ten-step anatomy the post is built on, and `references/images.md` holds the
     photograph it ships with. Ten posts written from this file without reading those two
     were killed on 19 Aug 2026.
   - X: `x-content`. `references/formats.md` holds the format ladder and the character
     rules, and `references/ranker.md` holds what the open-source ranker actually pays
     for. Before 23 Aug 2026 the X half was written from two templates in this skill
     while LinkedIn had eight reference files, and the account measures a median
     engagement of 1 across 147 posts.
3. [references/reach.md](references/reach.md) when the ask is reach rather than a draft,
   meaning "why did this get nothing" or "make this spread". It holds the stealable
   belief, audience width, the save-driver, and the trade between reach and pipeline.
4. [references/templates.md](references/templates.md), for the LinkedIn structure and a
   worked input/output example specific to this skill.

WHY `voice-dna` comes first: the qualitative profile had been broadly right for a while
and the posts still underperformed. The gap is structural (length, white space, question
endings), and structure is the part you can check before publishing.

Optional: the ClickUp "Learnings Log" / best-performing-examples doc, if it exists, for recent additions:

```
ClickUp Doc ID: <doc>  (may be deleted; do not block on it)
Workspace ID: <team-id>
```

WHY: this doc has been deleted before. The skill must not depend on it being reachable. If it 403s or is missing, the embedded profile is authoritative.

### Phase 2: Extract Core Value

From the source content, identify:

1. Pain point: What problem does this solve?
2. Story: Client example or personal experience?
3. Framework: 3-part solution?
4. Insight: Non-obvious takeaway?

### Phase 3: Generate Posts

Output format (always provide all three):

```markdown
## LinkedIn Post

[1200-1800 characters, 12-22 short paragraph blocks, mean sentence under 11 words,
story shape per linkedin-content references/writing.md]

**Image:** the photo library, `<setup>/<file>.jpg`
[one line saying which scene in the post the frame matches]

---

## X Post

[the shape named from the ladder in `x-content` references/formats.md, under 280
characters counting any URL as 23]
```

**The X shape is chosen from the ladder before drafting**, not after: value shape, tool
shape, thread, quote or reply. `x-content`, `references/formats.md`, holds all of them
and the counting rules. When the subject is something the author built, it is the tool shape,
meaning hook, three numbered steps, the outcome line, then a direct link to the thing
itself rather than to the repo that holds it. The build story goes in the research,
never in the post.

**When the ask is "post it on X", a reply may be the right output instead of a post.**
`x-content`, `references/replies.md`, has the test. Do not force a post shape onto an
idea that belongs under somebody else's.

**When the source carries five or more named things that stand on their own** (five
patterns, five failure modes, five levers), it is a long-form article, not a LinkedIn
post, and the three outputs above still ship alongside it. Use the "Long-form article"
shape in that file: 5 to 7 sections of 113 to 149 words, each headed `N: Named Thing`,
each closing on a measured claim. Do not force one into existence; a source with three
points is a LinkedIn post that would be padded to reach seven.

### Phase 4: Run the one-question ladder over the draft

Not the X format ladder, which is a different object. This one is a read of the draft line by line,
and it is the only audit here that finds the exact block where a reader leaves.

1. Read the first line and name the single question it opens in the reader's head.
2. If it opens none, the post is a statement and nobody is owed an answer. If it opens two of
   roughly equal pull, the reader picks neither. Either way, fix the line before reading on.
3. The next block answers that question and opens exactly one more.
4. To the end. The last block answers the last question and opens none, which is the same rule as
   ending on the idea rather than on a question.

**Where the ladder breaks is where the scroll resumes**, and it is visible on the page before
anything is published. Retention data can only confirm it afterwards.

**Cut for absorption, not to a character count.** The counts in the checklist below are budgets on
padding. A sentence that needs one more word to mean exactly one thing gets the word, and a
sentence trimmed until the reader has to guess has been trimmed past the point the count was
protecting. Ambiguity costs more readers than length does, because a reader who has to reread has
already half left.

## Quality Checklist

Before presenting output:

- [ ] LinkedIn post is 1200-1800 chars, broken into 12-22 short blocks, mean sentence under 11 words. Corrected 26 Aug 2026 from 2000-2500 / 35-50, which was set on one post and sits at the 90th and 99th percentile of 1,978 reference posts. Sentence length, not post length, is what separates a creator's best posts from their worst. The count is `linkedin-content`, `references/anatomy.md`
- [ ] LinkedIn post opens on a scene with people, a place and a time, carries one specific odd detail, and is not a stack of aphorisms
- [ ] LinkedIn post names its photograph, picked against the opening scene per `linkedin-content` `references/images.md`. A LinkedIn post with no image is not finished
- [ ] X post is under 280 chars, counting any URL as 23 whatever its length. Measure it: the cap is enforced at send, and a scheduler will hold an over-cap post looking perfectly scheduled until it dies
- [ ] X post names its shape from the `x-content` ladder, and passes the DM test: would a reader paste this to one named person. A post that can only be liked is priced at 0.5 against copy-link share's 20.0
- [ ] The one-question ladder was run: every block answers the question the one before it opened, and the first line opens exactly one
- [ ] Opens with pain or story (not generic intro)
- [ ] Contains specific numbers, at least one in the first two lines (not vague claims)
- [ ] Has clear structure (one idea, load-bearing lines only)
- [ ] Ends ON THE IDEA, not on a question or "book a call". No engagement bait: X ranks on predicted replies/reposts/dwell and pushes down posts people mute or mark "not interested" (see github.com/xai-org/x-algorithm), and bait earns exactly those negative signals. Add a closing ask only if the post really earned one specific invitation.
- [ ] NO hashtags, NO emojis (the voice never uses them)
- [ ] No banned words, phrases or sentence shapes. The auto-loaded `copy.md` rule holds all three
- [ ] Sounds like the author, not generic AI

## Self-Improvement Loop

After generating:

1. Ask which version he prefers.
2. If a post performs well later, note it in the ClickUp doc below when that doc
   exists. **`voice-dna` is the single home for the profile**, so a lesson about
   how he sounds goes there, not into a ClickUp page that has been deleted once.
3. If this run surfaced a failure mode not already listed below, append it to
   Learned Patterns with today's date.

## Resources

| Resource | Location |
| --- | --- |
| Socials List | the ClickUp list the posts are filed in |
| Learnings Log, optional | a ClickUp doc of what performed. Deleted before; never block on it |

The voice profile is not listed here on purpose. It is `voice-dna`, it is read in
Phase 1, and giving it a second address is how the two copies start to disagree.

Generate the way the profile writes: direct, specific, story-driven.

## Verification checklist

The gates are the Quality Checklist above; these are the ones about this file
rather than about the post.

- [ ] `voice-dna` and `references/measured.md` were read before drafting, not recalled
- [ ] `linkedin-content` was read for the LinkedIn half and `x-content` for the X half
- [ ] The subject came from a real source or from `idea-mining`, never from a blank page
- [ ] The draft went through `humanizer` before being shown
- [ ] Character counts and block counts were measured, not estimated
- [ ] Any new failure mode was appended to Learned Patterns

## Learned Patterns

What this skill's own runs have taught it, newest first, kept out of the body so the rules above carry the cost and the evidence does not. Append with `ai-architecture log`. See [`references/learned-patterns.md`](references/learned-patterns.md).
