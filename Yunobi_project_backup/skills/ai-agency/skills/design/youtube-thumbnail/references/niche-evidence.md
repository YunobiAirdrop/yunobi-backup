# What separates a winner from a control in this niche

Read on 19 August 2026 over **270 thumbnails**: ten channels, each contributing 15
winners and 12 controls from the same channel, format and period. Nine competitors
(135 winners / 108 controls) plus the channel being worked on (15 / 12).
Banding holds budget, photographer and palette constant, so **a trait in both bands is
house style and copying it buys nothing**; only what separates the bands is a lever.
Counts are directional: nothing runs unless it holds on five or more channels, or is
flagged single-channel. Rebuild any sheet with:

```bash
npx tsx scripts/competitor-intel/thumbnails.ts <slug>
```

Slugs: `matt-gray`, `ali-abdaal`, `chase-ai`, `liam-ottley`, `systems-made-better`,
`nick-puru`, `ross-harkness`, `michele-torti`, `jordan-ross`, and your own. Same
findings, shared with `video-script`, `social`'s `references/shorts-production.md` and `social`'s `references/writing-posts.md`:
`vibe-kit/ai-doc/references/competitor-evidence.md`.

## Single-channel lever: the type sits in the top half

**Our own channel only**, re-read 28 Aug 2026, agreeing with a cause found separately: across our
15 winners and 12 controls, winners set words across the top (`ADVANCED TUTORIAL`, `TUTO
COMPLET 2025`, `HOW TO CLICKUP FORMS`, `CLICKUP CRM MADE EASY`, `LEARN IN 30 MINUTES`);
controls hang them low over a screenshot (`CLICKUP FEATURES FOR REMOTE TEAMS`
bottom-left, `ContentFlow` bottom-left, `La meilleure méthode de travail` bottom-right).
Not counted on the other nine, but found independently: TV shows only a frame's top
until the viewer presses down, and has passed mobile as the primary device. Check: the
50% test in `SKILL.md` step 5.

## Six findings that replicate across five or more channels

### 1. A second person in the frame is a control marker

**1 winner in 135. 12 controls in 108.** It never runs the other way on any channel.

| Channel | Winners with a second person | Controls with a second person |
| --- | --- | --- |
| Matt Gray | 0 | 5 |
| Jordan Ross | 1 | 3 |
| Liam Ottley | 0 | 2 |
| Nick Puru | 0 | 1 |
| Ross Harkness | 0 | 1 |

Strongest single count in the set. No guest, no client, no team shot, no
two-founders-at-a-whiteboard, no testimonial face beside yours.

### 2. Somebody else's money, shown as a receipt, is a control marker

Client MRR quotes, Stripe and PayPal notifications, revenue curves, fans of cash.

| Channel | Winners | Controls |
| --- | --- | --- |
| Liam Ottley | 2 | 5 |
| Jordan Ross | 2 | 5 |
| Nick Puru | 0 | 4 |
| Michele Torti | 1 | 2 |

Jordan Ross's control band is clearest: four of twelve controls are a client's face
beside a number they hit. `"ADDED $60,000 IN 8 MONTHS"`, `"WE WENT FROM $30K MRR TO
$250K MRR"`, `"I WENT FROM $20K TO $60K MRR"`, `"$0K -> $13M"`.

**The exception is exact.** Your own zero-to-X ladder wins, a transformation not a
proof: Ali Abdaal's `$0 -> $1M` in two winners, Matt Gray's `$0 | $10K | $1M` as one man
in three rooms, money as the axis, his change as the subject.

### 3. A numbered ramp of generic icons is a control marker

`PHASE 1..5`, `STEP 1..4`, `Stage 1 / 2 / 3`, `#1 .. #4`, each step an abstract glyph.
Control band on Ali Abdaal, Liam Ottley, Nick Puru, Jordan Ross, Michele Torti; not one
appears in a winner band.

**A numbered strip where every cell is a different real thing wins**: Matt Gray's
`1 LEVEL ... 7 LEVEL` is seven photographs of seven different people, Chase's is seven
different screenshots.

### 4. A bounded promise in the copy is a winner marker

Winner band on Liam Ottley, Michele Torti, Ross Harkness, Matt Gray and our own.
Verbatim: `full guide` / `FULL COURSE 4 HOURS` / `LEARN NO-CODE CHATBOTS IN 3 HOURS` /
`LEARN IN 30 MINUTES` / `10 minutes/day` / `2 MINUTES A DAY` / `finish everything by
10:00am` / `ONLY 1 PROMPT` / `A CEO ONLY HAS 3 JOBS` / `BUILD THESE 3 SYSTEMS` / `MASTER
THESE N8N NODES` / `2026 FULL TOUR`. The promise names the whole scope or the exact
cost. Full formulas in [`copy.md`](copy.md).

### 5. An adjective with no object is a control marker

Control band on Michele Torti, Nick Puru, Ross Harkness, Jordan Ross and Matt Gray.
Verbatim: `INSANE AGENTS` / `UNLIMITED CONTENT` / `THE NEW AI ERA` / `GAMECHANGER` /
`ADAPT OR DIE` / `Thank Me Later` / `SET KPIs LIKE A PRO` / `BUSINESS SHOULDN'T BE
STRESSFUL` / `AIR TIME?` / `it does everything`.

### 6. A readable screenshot as the subject is a control marker

A dashboard, chart, spreadsheet or app window the viewer is asked to read: control on
Chase (a SWE-bench chart and two dashboards), Systems Made Better, Michele Torti, Jordan
Ross and Liam Ottley. Winners use the same screenshots **as texture**: blurred, cropped
hard, or dimmed to 30% behind three big words, as in Nick Puru's and Michele Torti's n8n
canvases. Nothing readable survives 320px anyway.

## Faces: the rule is size and role, not presence

A face appears in both bands on eight of nine channels: **not a lever anywhere in this niche**. What separates is size and job.

**Systems Made Better is the faceless case**, closest to "systems" as a subject: 12 of
15 winners have no person, a real desk shot cleanly, one white label block; 10 of 12
controls are his face beside a floating app screenshot. Strongest faceless result here.

**Matt Gray is the small-figure case**: face close up, 1 winner, 3 controls. Winners put
him small in a real room, a lake, a desert: the environment is the subject, he is the
scale reference.

**Ali Abdaal is the holding case**, present and mid-sized, given something he made to
hold: a filled notebook, a hand-drawn poster, a book. The hands prove it is real.
Everywhere else the face is house style and changes nothing.

## Seven general archetypes, and where this niche departs from them

The general-YouTube catalogue, measured against the ten-channel bands rather than taken
on faith: kept because two of the seven survive the control.

| Archetype | Composition | Status in this niche |
| --- | --- | --- |
| Reaction face | Face left/right, eyes to focal object, mouth open | **Refuted.** No shocked face appears in any winner band, on any of the ten channels. |
| Juxtaposition | Split frame, two contrasting halves | **Holds**, as negation: crossed-out options and one survivor. Nick Puru, Michele Torti, Liam Ottley. |
| Single hero object | Object centre-right, clean background | **Holds, and is the strongest.** The faceless variant. Systems Made Better, Ross Harkness, Jordan Ross. |
| Before / after | Left bad, right good | **Holds**, as `OLD -> NEW` and `SLOP -> FIXED`. |
| Numbered stakes | Giant number, face reacting | **Split.** A strip where every cell is a different real thing wins; a ramp of generic step icons is a control marker on five channels. |
| Mystery / question | Object partly hidden, hand reaching | Not observed either way. Untested here. |
| Forbidden / danger | Red tint, caution tape, hazard | Not observed. The niche's version is the negation, above. |

Pick exactly one and name it in the build order: blending two is the most common way a
thumbnail says nothing, and no max-saturation MrBeast palette appears in any winner band.

## Per-channel lever

What does not generalise still tells you what that channel's audience rewards, ordered by median, highest first.

| Channel | Median (long) | What separates its winners |
| --- | --- | --- |
| Ali Abdaal | 312,027 | An artifact he made and holds up: a filled notebook, a hand-drawn framework poster, a book. Or his own `$0 -> $1M` ladder with a green arrow. Controls float UI cards (comment screenshots, a Tinder notification) and review other people's products. |
| Liam Ottley | 43,716 | A completeness promise on a flat white or yellow plate with a named row of tool logos. One winner has no photo at all: black and blue type on solid yellow. Controls are money screenshots, lifestyle, and 5-phase ramps. |
| Systems Made Better | 23,054 | No person. Object photography of a real desk or device, one white label block, statement copy that ends in a full stop: `YOUR IPAD. BUT BETTER.` `GET THE IPAD RIGHT.` `Desk Candy.` Controls are his face pointing at an app screenshot. |
| Chase (AI) | 16,960 | Two app icons and a plus sign on the house terracotta, plus a two-word benefit in caps: `GOD MODE`, `INFINITE MEMORY`, `MAX POWER`, `BROWSER SWARM`. Three or more logos, a versus, or a chart drops to control. |
| Matt Gray | 15,600 | One person, small, in a real place. Two to four lowercase white words. A number rendered as an object rather than written in the title. One hand-drawn arrow. |
| Michele Torti | 5,186 | Curriculum scope (`FULL COURSE 4 HOURS`), a countable set (`MASTER THESE N8N NODES`, ten node icons), effort collapse (`ONLY 1 PROMPT`), `OLD` crossed out into `NEW`. Controls are adjective hype and icon halos. |
| Nick Puru | 3,742 | A row of crossed-out options and one survivor: `THEY ALL LOST`, `IT'S A TRAP`, `NO SETUP!`, `Stop Paying For APIs`. Controls are money receipts, 12-logo grids and a robot mascot. |
| Ross Harkness | 4,059 | Both bands are the same overhead photograph of a notebook full of hand-drawn system diagrams, so **the composition is not the lever, the label is**: a quantity and a timeframe (`THE 2 MINUTE HABIT`, `A CEO ONLY HAS 3 JOBS`, `DO IT ALL BY 10AM`) beat `COPY THIS` and `CEO DASHBOARD`. |
| Jordan Ross | 405 | A named artifact the viewer could copy: an SOP document, a client portal, a five-line automation list, a checkbox list of business systems. Controls are client testimonial income and guest faces. |
| Ours | 715 |
 Completeness promises win the little we win (`TUTO COMPLET 2025`, `LEARN IN 30 MINUTES`, `2026 FULL TOUR`). Series numbering (`MINI COURSE DAY 1`), scolding (`NE FAITES PAS ÇA!`) and category labels (`Tout sur les Docs`) sit in the control band. |

## What our own wall says about us

Read against the nine, our 27 frames share three faults **on both bands**, which makes
them house style and not bad luck, and not what is holding the channel at a 715 median:

1. **Five to eight elements** where a winner carries one or two: a cut-out face, a
   gradient plate, a floating app window, a logo badge, two text blocks, an arrow, a
   sticker, all in one frame.
2. **A cut-out face at constant size and saturation on every frame**: no different job
   in the winners than the controls, so it costs space and buys nothing.
3. **Copy that names a category where a winner makes a claim.** `CLICKUP CRM`,
   `Tout sur les Docs`, `DOCS`, `MINI COURSE DAY 1`.

Fixes, in order: cut to one focal element, replace category labels with bounded claims,
take the faceless variant whenever a board, a workflow or a document can be the subject.

Craft (not claims) transfers from a channel this study never sampled: the rule and the
Higgsfield AI worked example are in [`craft.md`](craft.md).

## Method notes, so this can be argued with

- Bands come from `scripts/competitor-intel/sample.ts`: views against that channel's own
  median for the same format, never raw views. Shorts are scored separately.
- 15 against 12 per channel is a small sample; five-channel replication compensates.
- Nine of ten channels are English; our own French uploads sit inside our 27,
  untested for a language split.
- One reader, one sitting: counts are exact for what was seen; a borderline frame is a
  judgement call.
