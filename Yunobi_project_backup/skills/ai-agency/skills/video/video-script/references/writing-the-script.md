# Writing the script: bullets, beats, structure and the teach block

The craft half of this skill. `SKILL.md` holds what the measurements decided; this file holds how a script is actually written once those decisions are made.

## Every script ships as bullets

**A script is bullet points, never prose paragraphs.** The speaker reads from bullets on camera
and it comes out natural; prose makes them recite, and the recitation is audible in the take.
 Stated 19 Aug 2026 while M0 L1's open was being rewritten, after a
paragraph-shaped draft.

**A bullet is one sentence the way he'd say it out loud.** Under 25 words, contracted, chained
with "and", "so" and "because", and talking to "you". It fails in two directions. On 21 Aug 2026
every bullet was a 30 to 50 word sentence and he couldn't record it: "I'm literally not
understanding what I need to record." On 24 Sep 2026 the Claude Code course went the other way,
clipped fragments like "Paste the line. Press return. Let it run.", and his verdict was that it
didn't sound natural: "clean, conversational, and simple", the fix the Shorts got the day before.

| Too clipped | One spoken sentence | Too long |
| --- | --- | --- |
| `- Settings, App Center, MCP Servers. The panel is new.` | `- Open Settings, then App Center, and you'll see a panel called MCP Servers that's new this month.` | `- This one does not get finished on camera, and the reason is the point rather than a skipped step, because...` |

**The save is the gate.** `concepts script <id> --file` refuses a script whose beats carry a banned
phrase or miss the `spoken` register (16 to 34 words a sentence, contractions, chaining, "you"), and
names every hit. Rewrite what it names and save again.

- One bullet per beat, in the order the beat is spoken. Nest sub-bullets for the parts of a beat,
  the on-screen note, or an open question.
- **No stage directions.** A bullet is a thing said or done on camera, never an instruction about
  how to say it. "Land it:", "Say it plainly:", "Name the artefact:", "The turn:" and every cue of
  that family are cut: rejected on sight 19 Aug 2026 as a director talking to talent, and the
  talent is the author.
- **Three things are written out in full and wrapped in quotes**, the only lines allowed past the
  word cap: the cold open's own lines, the closing ask, and any measured number, spoken exactly and
  never rounded.
- Editorial notes ("On screen", "Why it is built this way", cut instructions) stay prose outside
  the bullet list, since nobody says them out loud.

## The beat budget

**The body is budgeted in beats, and a beat is one bullet.** A word budget cannot be spent any way
except by lengthening bullets, which is exactly how the 21 Aug 2026 script turned into prose: the
generator's expansion pass was told to hit a word count, and it hit it by growing the bullets it
already had rather than finding the steps it had skipped. Given a beat target the only way to hit
it is to add beats.

**One beat runs about seven seconds on camera.** Measured on the 21 Aug 2026 script, sized to 195
wpm before anybody looked at its bullets: 3,543 words over a planned 20:44, carried by 179
bullets, 6.95 seconds a bullet. The how-to rewrite of the same video lands at 169 beats. So the
winning nineteen minutes is roughly **158 to 185 beats**, the same evidence as the 3,600 to 4,200
words, converted.

- Short of the target means the block is **missing beats**, never missing words. Find the step it
  skipped: the exact click, the field name on screen, the number the viewer sees, the mistake
  most people make here and what it costs.
- The word count is still recorded, since it is what the three-run control measured, but is a
  reading of the script, not a target to hit.
- The teleprompter paces in **beats per minute**, not words per minute: the body is spoken around
  rather than read, so its word count says how much was typed, not how long the take runs.

## Structure

Nine blocks, and the hero's arc runs down the middle column. The beat budget is the constraint
that keeps them honest.

| Block | Share | Arc | What it does |
| --- | --- | --- | --- |
| Cold open | 0:00-0:30 | | Owned by `video-hooks`. Take it from there. |
| The why | ~6% | Ordinary world, call | Why they need this, and why now. The fear, named once, and already true. |
| The failure | ~6% | Refusal, ordeal | Your own, told in full. The buyer's life in your words. |
| The stakes | ~5% | The cost of the refusal | What it costs to keep doing it the current way. One real number, with its artefact. |
| The mechanism | ~14% | The gift | The thing that makes it work, named. Lead with this, never with the promise. |
| Build 1..n | ~50% | The road of trials | The teach. One idea per block, each ending in a state the viewer can see on screen. |
| The proof | ~11% | Return changed | The artefact doing the thing. Two configurations from one input beats one screenshot. |
| The honest limit | ~4% | | Who this does not work for, said plainly. It is what makes the rest credible. |
| The ask | last 20s | | One outbound ask. Named product, named price, one link. |

**The why is paid for out of the failure and the stakes**, which is where the shares moved from,
because those three are one family: the reason, the evidence, and the price. Before 19 Sep 2026
there was no why block and the other two were quietly doing its job, badly: a broken morning is
evidence, and evidence only means something to somebody who already agreed it matters.

**Every build block ends on a visible state change.** A block that ends on a
sentence is a paragraph; a block that ends on the board looking different is a
beat. This is what carries the open loop the completion data rewards.

**The why block's own beat sheet** (eleven beats: the object they own, their words for what is
broken, the consequence with a clock, the identity split, the turn) is in
[`why-and-hero.md`](why-and-hero.md), with the lever table and the arc mapping.

## The teach block, which is 53% of the script

Everything above governs the shape of a script. This governs what happens inside a
build block, which is where half the runtime is spent and where the skill was silent
until 23 Aug 2026.

Read off a full transcription of Nick Saraev's `CLAUDE CODE FULL COURSE 4 HOURS`
(`QoQBzR1NIqI`, 4:10:42, 62,139 words, 35 chapters, 2,314,591 views on 502k subs, a 4.6x channel
multiplier, read 23 Aug 2026). **Single source, no control test.** It sits below anything measured
on this channel, and it is here because the alternative was nothing.

- **One portable idea, restated at the close of every build.** His four hours run on a single
  loop, named once at 00:39:35: give it the task, let it do the task, make it verify the result.
  Every module afterwards is an instance of it, and he says the absence of that loop is why people
  fail. A script carrying one idea restated six times holds longer than one carrying six ideas
  listed once. Name the idea in the mechanism block, then point at it again as each build lands.
- **Say the block's line at the start as well as at its close**, so the block opens on a claim and
  every excursion has somewhere to return to instead of a summary it eventually reaches. At video
  scale this is the hook and belongs to `video-hooks`; the addition here is block scale, one line
  per build. The return sits on the beat where the build lands, never on the last beat, since the
  last beat is the seam and belongs to the next question.
- **The line carries a third to a half of the idea, never all of it.** A sentence written to hold
  the whole block becomes a slogan a speaker cannot say out loud and so never says. "Leadership is
  certainty" is enough to start on, the rest fed in as the block develops. **It comes back in
  nearly the same words**, since what a viewer repeats afterwards is a phrase, not a paragraph: one
  coached client closed a company speech on "we go where the money flows" five times unchanged,
  and that is the sentence the room left with. Single source and unmeasured, 31 Aug 2026, Joseph
  Tsar, `How To Never Ramble When You Speak`. Also the writing half of the recording habit in
  `video-edit`, what a take with nothing to return to costs in restarts.
- **Draw the abstraction.** Any idea not already a thing on screen gets drawn as one, on the same
  screen, mid-walkthrough: a ship crossing the Atlantic with a stiff rudder, for why the
  instruction file steers everything; a staircase from 80% to 100%, for why speed beats one-shot
  accuracy; a primacy curve, for why the important rule goes at the top. Highest-yield device in
  the reference video, costing nothing but the seconds. Drawing on the shared screen is
 The `whiteboard` skill builds them.
- **Define the term the moment it appears, in objects the viewer already owns.** "An IDE is a file
  explorer plus a notepad plus ChatGPT, in one." "A token is like a word, just a few more." "A dot
  in front of a folder hides it." Four seconds each, what lets a technical build stay legible to a
  non-technical buyer. A term used before it is defined loses the viewer silently: they leave.
- **Show it failing, once per build block, and do not cut it.** Broken buttons, cropped faces, an
  error message read out, 987 of 989 records processed and the number said. He fixes each one on
  camera: the trust engine of a walkthrough, the thing a demo cannot fake. Pairs with the existing
  rule: **a block that ends on the thing working, having shown it not working, is a visible state
  change twice over.**
- **When the block is a verdict on a tool, make the tool produce the number.** Do not argue the
  thing is bad, ask it to audit itself on camera and read the answer out. Theo's 39-minute memory
  video is the clean version: he asks Claude Code what it has stored, how much earns its keep, how
  often it is read, and the tool returns 3 writes for every read, 26 of 45 files never opened once.
  He arrives skeptical and leaves gutting the feature across his fleet, and the escalation is real
  because he did not know the number before asking. Two conditions: the question must be answerable
  by the tool from its own data, and asked before you have decided. A demo confirming a verdict
  already announced is a re-enactment, and reads as one.
- **The build is real work out of the business, never a toy.** His four hours build his own agency
  site, a PandaDoc replacement with signing and payment, a lead scraper, and a classifier run over
  989 real emails at 0.36 seconds each. Nothing is a to-do app, and the counts are said out loud. A
  build the founder was going to do anyway teaches the job, and is the only version
- **Cost in money and minutes, never a percentage.** $17 a month against the month's output. 35
  minutes without a plan against 10 with. A percentage is an argument; a number of minutes is a
  thing the viewer can picture losing. The truth rule binds hardest here.
- **Answer the dating problem out loud, in the mechanism block, in one sentence.** Any video about
  a tool that ships weekly decays from the day it publishes. He spends one sentence at 00:04:36:
  the screens will look different by the time you watch this, what matters is knowing where to
  find the current version. Costs nothing, widens the shelf life, the same trust move as refusing
  the category's promise in `video-hooks`.
- **Dictate the prompts on camera, and say why once.** Every substantial prompt in the reference
  video is spoken, with the arithmetic stated once: about 60 words a minute typed against about
  200 spoken. Turns prompting from writing into talking for a viewer who does not code.
- **A guide is navigated, not watched.** A four-hour guide carries about 35 chapters. Ship one chapter per block,
  named for the state the viewer reaches rather than the feature: "the Project that stops the
  re-explaining", never "Projects".

**When the body is an argument, not a build**: the eight blocks and the teach-block rules above
assume a build, a screen, a click, a state change. A thesis video has none of that, and its
failure mode is a chronology rather than a thin script. The dated chain, the motif that returns as
the answer, caveating a number in place, fencing a prediction, and the permission close:
[`references/argument-video.md`](argument-video.md).

## Camera language on the outside, mechanics on the inside

 and it binds every script that sells. On
camera the words are the ones a founder already uses: "batches, sprints of one week", "a clear view
on your team's capacity without hiring a project manager", "billable time". The named mechanics,
Points, the slipped tag, the space model, are explained **inside** the install, never in the part
that sells it.

A build walkthrough sits on both sides of that line, so the split is by block rather than by video:
a teach block may name a mechanic once it is showing it on screen, and the why, the failure, the
stakes and the ask stay in camera language throughout. A viewer who has to learn a vocabulary
before they understand the stakes has already left.

## Register

Spoken, not written. Out loud he runs 24.5 words a sentence against 7.5 written, chains with
"and", "so" and "because" at 2 to 3 times the written rate, then drops a short line for weight
(`humanizer`, `references/voice-measured.md`). A run of short declaratives is the written cadence
read out, and it's what made the 24 Sep 2026 script sound stiff. Use the real noun, not the
abstraction, and concrete numbers with the artefact that proves them. Contrast pairs still carry
the teaching: what most people do, what works, and why the difference is mechanical.

In `video-hooks`, `SKILL.md` section "The one rule that overrides the rest": the truth rule that
overrides register too.
