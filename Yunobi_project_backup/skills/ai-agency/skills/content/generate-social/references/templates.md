# Templates and Examples

## Contents

- X post shapes: not here
- Long-form article
- Style Guide Quick Reference
- Example Input/Output

## X post shapes: not here

**`x-content` is the single home for every X format**, meaning the value shape, the tool
shape, threads, quote posts, replies, the character-counting rules and the t.co
23-character rule. See `x-content`, [references/formats.md](../../x-content/references/formats.md).

Those shapes lived in this file until 2026-08-23, which is why X was written from two
templates while LinkedIn had eight reference files behind it. A format that ships in the
same output block as a documented one is not itself documented.

The X half of this skill's output is drafted by reading that file. This one keeps the
LinkedIn structure and the worked example below.

## Long-form article

For an X article, a LinkedIn article or a newsletter issue. This is the surface that
gets bookmarked rather than liked, and the shape is what earns the save.

The spec is counted off a reference piece that did 1.27M views and 10,769 bookmarks
against 3,944 likes on 2026-08-15. `voice-dna/references/measured.md` holds the counts
and the reason each one is there.

```
[Opening: the reader's day in concrete nouns. 3 to 5 fragments, 3 to 6 words each]

[The belief most people hold, stated plainly]

[The reversal. Two or three words on their own line]

[The thesis: what the piece hands over, one line]

N: [Named Thing]

[The wrong default: "Most people..." or "The biggest mistake..."]
[The turn, one short sentence]

For example:

[Case 1, real objects and real numbers]
[Case 2, same syntactic frame]
[Case 3, same frame]

[Close: one sentence carrying a measured claim]

...repeated, 5 to 7 times

[Takeaway: the thing to do, addressed to the reader, declarative]
```

Counted targets, all from the reference piece:

| Target | Value |
| --- | --- |
| Sections | 5 to 7, each `N: Named Thing`, two or three words after the colon |
| Words per section | 113 to 149, and the band stays that tight all the way down |
| Blocks per section | 7 to 12 |
| Whole piece | roughly 1,000 words, 6,300 characters, 76 blocks |
| Block density | one block per 80 characters, the same white space as a long LinkedIn post |
| Sentence length | mean 8.5 words, median 8, and 42% at 6 words or shorter |
| Person | second person throughout, 48 `you` against 3 `I` |
| Close | declarative, never a question, even where questions run inside the body |

**The named unit is what gets saved.** Seven models with names is seven things a reader
can carry away and one thing they can file. A piece of the same length with no names is
read once. The named products this account already owns are under-used as the unit of
a piece, which `measured.md` records as a standing gap.

**Three slots decide whether it sounds like everyone else.** The architecture above is
free to take. These are the parts where the reference piece does what our rules ban, so
fill them from our own material instead:

- **The example slot.** The reference runs hypotheticals: the founder who later becomes
  your biggest client. We have 367 recorded calls and the client installs. Use a real
  case with the real number.
- **The close slot.** The reference closes each section on a moral aphorism with an
  abstract subject. Anti-voice 14 bans that shape, measured at 0 occurrences in 56,568
  words of his own writing. Close on something measured.
- **The turn.** The reference gets its reversals from negation pivots, 11 of them in
  1,005 words. `ai-doc/skills/content/writing/humanizer/references/slop-list.md` bans the shape in written copy. Get the turn from
  what actually happened instead of from "it is not X, it is Y".

## Style Guide Quick Reference

### Voice, hooks, closers, banned language

**Not here.** The `voice-dna` skill is the single home for all of it: register, sentence
shapes, signature tics, hook mechanisms, closers, and the anti-voice. Its
`references/measured.md` holds the counted targets. Read it before drafting and audit the
draft against it before shipping. `humanizer` and `ai-doc/skills/content/writing/humanizer/references/slop-list.md` own the generic
banned-word list on top.

What stays below is post *shape*: the structural templates specific to this skill.

### Structure (LinkedIn)

1. Pain hook (1 sentence)
2. Client story (2-3 sentences)
3. Framework intro
4. Three numbered points
5. Takeaway (1 sentence), land the idea

(Structure is a default, not a mold. One sharp idea beats a forced framework.)

## Example Input/Output

### Input

```
YouTube video about setting up ClickUp notifications properly.
Key points: Turn off first 4 notification settings, use guests vs members wisely, disable unused ClickApps.
```

### Output

LinkedIn Post:

Your ClickUp notifications are a mess for a reason.

Every new user gets bombarded with alerts they don't need. You become a "watcher" on tasks automatically. Your inbox fills with noise.

I tell every client the same thing on day one:

1. Turn off the first four notification settings
2. Disable every ClickApp you're not using
3. Use guests (free) instead of members when possible

One client reduced their daily notification volume by 80% in five minutes. They went from drowning in alerts to actually seeing what matters.

The tool isn't slow. It's bloated with features you enabled by default.

You don't have a software problem. You have a defaults problem.

X Value Tweet:

Your ClickUp feels slow because you have too much turned on.

Go to ClickApps → disable everything → only turn on what you actually use.

Workspace instantly feels faster. (89 chars)

X Promotional Tweet:

New to ClickUp? Before you touch anything else:
→ Turn off 4 notification settings
→ Disable unused ClickApps
→ Learn guests vs members

Full setup guide: [VIDEO LINK] (187 chars)
