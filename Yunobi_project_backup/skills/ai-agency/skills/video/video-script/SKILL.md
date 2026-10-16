---
name: video-script
description: "Writes a video's words: the long-form body, the opening hook, or a whole Short filed in CutKit. Use when a video needs a script or a hook, when a script runs long or asks too early, when an open reads weak, or on create a short, script a short, make a TikTok about."
tags: [writes, video, youtube]
lane: judgment
---

# Video Script

3 branches, one job: nothing ships until every fact underneath it is true, the feed evidence
is fresh, and the voice pass has run. **The opening line**, for a Short's 1-3s window or
long-form's 30s open: [references/video-hooks.md](references/video-hooks.md), with the bank of
shapes in [references/hook-library.md](references/hook-library.md) and the four ways a hook fails,
and the fix for each, in [references/hook-diagnosis.md](references/hook-diagnosis.md). **A whole
Short**, scripted and filed into CutKit end to end: [references/shorts-script.md](references/shorts-script.md).
**The long-form body**, everything below, is this file's own branch: whether the viewer is still
there at minute twelve, and whether the one ask at the end lands on somebody who has already
decided.

## The trunk: true before written, voiced before shot

**Every script, Short or long-form, starts from an anchor and ends with a cold read.** The author, 4 Oct
2026: **"I need to stay humble and copy before I become good."**

- **The anchor.** Before the first line, pick one competitor video on the subject that beat its
  own channel (`scripts/top-band.mjs` for a Short, `idea-mining` pipes 1 to 3 for long-form) and
  put its transcript beside the draft. Match its moves beat for beat: where it names the tool,
  where it counts, how long a step runs, where it asks. Swap in his substance and his proof, never
  its words. A model copies one real example far better than it follows rules. The Sofiane batch
  had 40,000 words of rules behind 130-word scripts and no anchor, and it came out unreadable.
- **The cold read.** Give the finished script to a fresh Haiku subagent with no context, as a
  stranger in the buyer's seat hearing it once. It names the action with its tools, says whether it
  could do it tonight and who it would send it to, and quotes its hardest sentence. Rewrite whatever
  it can't name. It reads and never writes, so the "words are written" rule holds. On 4 Oct it rated
  old S12 3/5 and quoted the exact sentence the author had flagged, where CutKit gave B-, and rated the
  rewrite 5/5. It tests whether people understand you, not reach (a 66x breakout got 2/5, because
  that video shows its code on screen), so the anchor decides the structure.

**Go as hard as you want on the mechanism; every fact underneath still has to be true.** A number
nobody measured, a story that did not happen, a stake that does not exist: none of it is available,
on any branch. Invented drama also reads generic, since a model reaching for stakes reaches for the
average ones, and a real number is specific enough to stop a thumb. Proof frame and evidence source:
[references/proof-and-surfaces.md](references/proof-and-surfaces.md).

**Read what the feed rewards this month, before drafting anything.** `community`'s
`references/engagement-what-works.md` derives it from competitor posts scored against each
account's own median, so a 22,000-like account and a 21-like account contribute the same
evidence. It carries its measurement date and a staleness ladder, because a feed re-ranks every
month and a file does
not. Over 30 days old, collect the feed again before trusting the page.
It says what the feed rewards, never what is good; the bans in `@heyramzi/lint` and the voice in
`humanizer` outrank every number on it.

**Run the six story locks over the finished bullets, one pass each, no beat moving**: term
branding, embedded truths, thought narration, negative frames, loop openers, contrast words.
Contrast is the engine under the other five, so it is the one to use when only one pass is
affordable. None of the six is judged by eye or is a lever; asked whether any separates a winner
from its own channel's controls, the best held in 9 of 13, a coin, so they buy retention and never
reach. [references/story-locks.md](references/story-locks.md), which every branch below runs. On a
body three land hardest: **thought narration** (the viewer's own thought, in their words out of
`conversion`), **embedded truths** (hedge the provenance, never the instruction), **contrast
words** (split the sentences carrying the main points).
**The negation pivot is the one this skill gets wrong most often**: defining a thing by denying
another first, as in "it is not a project, it is a wish". Several in a ninety-second script is the
loudest signal in the piece that a machine wrote it. **One per script, maximum**, short and
concrete, counted before shipping. Full treatment: `humanizer`, `references/patterns.md` section 9.

**Voice is `humanizer`. Do not restate it, do not soften it, and run it over the finished script
before it is read on camera.** Count the first-person pronouns first: the target is zero on a
hook, and the section below says where a few are allowed in a long-form body.

## The body opens on why, and the hero is the viewer

The author, 19 Sep 2026, on a Claude guide whose body opened straight into the broken morning:
**"We always should start with why when we record a video."** So the first block after the cold
open is **the why**: why you need to master this, and why now. Not what the video covers, but what
is still true for them in a year if they skip it. The lever is fear and the fear has to be already
true; the hero is the viewer and you're the mentor; the emotion is spent in the why, the stakes and
the close of the proof, never inside a build.

`reviewScript` fails a body that opens on anything but the why, and any block whose first-person
pronouns outnumber its second-person ones. The levers, the arc mapped onto the blocks, the beat
sheet and what each check caught: [`references/why-and-hero.md`](references/why-and-hero.md).

## Decide the subject on a number before writing a beat

`idea-mining` chooses the subject; the SERP decides whether it is worth a recording day, and it
decides alone, since `yt-dlp` returns no volume and the app's keyword report is quarantined for
inventing its own. **Two conditions open a lane**: the unserved query (a first page of clips under
150 views each) and the **stale head**, the commoner case, where two or three old videos hold a
commercial phrase and every entrant since is under a thousand. **Never take the runtime off the
SERP**, since the thin clips crowding a commercial phrase are the ones losing. The two `yt-dlp`
passes, the Search Console rows a product demo also reads, and the fabrication finding:
[`references/reading-the-serp.md`](references/reading-the-serp.md).

## Where the script goes, and what checks it

A video has exactly one script and it lives on its record. Saving it runs the arithmetic half of this
page: beats against the floor and ceiling, the word cap per beat, a why block first, second person
outnumbering first in every block, one action in the ask, no throat-clearing transition, a visible
state change ending each one. **Change one and change the other in the same session.** Slop and an
off-register take are refused on save.
 A script that fails the arithmetic still stores, because 300 words over is worth
trimming rather than losing.

**A build video carries its prompts.** Each block's `prompts` holds what gets pasted into Claude in
that block, `{ step, prompt }`, in the order used, and the Prompts tab lists them for copy-paste
while recording. Write them progressive: each adds one thing to what the last built, and says in
plain words what it wants and why.

**A take too long for one sitting is recorded in parts.** Set `part` (1, 2, 3) on each block, and
the Script tab heads each part. The author, 24 Sep 2026, on the Claude Code course: three parts, "because
it would be super long otherwise." Cut where the recording actually stopped. Each part ships as its
own upload.

**The description is stored with the script, one per upload, before the take.** The Description tab
is read-only and shows only what's stored there. Write the composer's plan (asks, contents line,
chapters planned from `startsAt`, `durationSeconds`, plus `part` and `title` for a split video) and
store it as `{"description": [...]}` through `concepts set <id> --metadata-file`. The rules are
`youtube`'s `references/description-block.md`; run `heyramzi-slop` over the composed text.

**The three-run control is the spine of this skill.** Runtime, beat budget and ask placement were each measured across three runs of the channel, and the numbers are what this skill enforces. Read [`references/three-run-control.md`](references/three-run-control.md) before writing the beat sheet, or when a script has come out long and the budget has to be argued with.

## The ask rule, where two sources of evidence disagree

The generic retention literature says never save the only CTA for the end; the three-run control
says the winners held every outbound ask to the last 2%. Both are right, because they count
different asks: the in-platform ask (subscribe, like, comment, never breaking the teach), the
outbound ask (buy, book, go to a page, exactly one, in the last twenty seconds), and the native
embed, a real thing named because the argument arrived at it, which was never counted. The taxonomy,
the evidence and the sponsor-read exception: [`references/three-run-control.md`](references/three-run-control.md).

## Nothing here is judged by eye

```bash
python3 .claude/skills/video-script/scripts/story_metrics.py <script.json|take.txt> --duration <s> --grade
python3 .claude/skills/video-script/scripts/teardown.py <url>          # a reference video, same axes
```

`story_metrics.py --grade` returns seven rules in two tiers: **FAIL** is a banned construction or a
number outside what the niche tolerates, **WARN** is inside the niche and short of the house target.
Every threshold prints its source, three being percentiles of 627 measured videos and four doctrine.
59% of that corpus passes clean and each rule fires on 5 to 20%, so a fail means something. The
rules, what `teardown.py` prints, the norms and the four draft audits: [`references/measuring.md`](references/measuring.md).

## The script names the overlays, and only its own

The CTA shelf at `/design` carries one clip per sellable product plus the on-camera asks, and the ask
this script writes decides which an edit needs. So the script names them in `overlays` and the
concept page shows those files alone: one clip for the outbound ask, naming what it names, plus a
subscribe, like or comment clip only where a block makes that ask on camera. Handing the editor the
whole shelf hands them somebody else's product. **Check each name against the shelf before
storing**: a name not on it is dropped silently, and the 19 Sep 2026 Claude guide named a clip for a
product that has never existed.

**What a series buys**: episode one is the reach event, later episodes convert the audience it captured. Six ran 17,874, 11,425, 4,144, 5,209, 960, 2,258, episode five below the channel median. Front-load accordingly. **The script is one of five surfaces**: a recorded video is cut into five and the long-form script is only the first. What each takes from it and must not repeat: [`references/five-surfaces.md`](references/five-surfaces.md), read once the video goes into production.

## Writing it

The bullet rule, the beat budget, the structure, the teach block that is 53% of the script, the camera-language line and the register: [`references/writing-the-script.md`](references/writing-the-script.md). **The argument video** (no build to teach): the dated chain, motif, caveat, fenced prediction and permission close, [`references/argument-video.md`](references/argument-video.md), whenever the body makes a claim about the world rather than clicking through a screen.

## Before it ships

- Beat count inside 158-185, runtime stated at the top, no bullet past 25 words unless it is a quotation.
- The body opens on the why, with one consequence the viewer can check against their own year.
- Second person outnumbers first in every block, and the payoff replays the opening object changed.
- Exactly one outbound ask, inside the final twenty seconds. Native embeds are not counted, and any non-native sponsor read sits after the channel's average view duration.
- The four draft audits ran (two usable things early, the eyes-closed pass on the first assembly,
  tolerance reset before judging, one debatable question left open), and the seam where a block ends
  and the viewer remembers they have work to do was checked: [`references/measuring.md`](references/measuring.md).
- `story_metrics.py --grade` run, with zero fails and every warn either fixed or answered in a line.
- One point where the viewer forms a prediction and one where it breaks, clues already on screen.
  The six locks were run, and every hedge left in is provenance rather than instruction.
- The failure told in full, every number traced to something measured with the artefact named for
  the edit, and no arithmetic performed on camera.
- One portable idea, named in the mechanism and pointed at as each build lands, and every build
  block opening on its own one-sentence claim at a third to a half of the block.
- An argument video ran the essay checks: every history link ends on the lack that forces the next,
  any prediction block is fenced out loud, and the close gives permission before the ask.
- At least one abstraction drawn on screen rather than described, and every term defined the first
  time it is said, in objects the viewer owns. One thing shown failing inside each build block,
  uncut, and the dating answer present wherever the subject is a tool that ships weekly.
- One chapter per block, named for a state rather than a feature (78% of the corpus publish chapters,
  median 7, 3.9 per ten minutes, titled in 4 words, the first ending at 4.7% of runtime).
- `humanizer` run over the whole thing, then `concepts script` stored it (it refuses a banned phrase
  or beats off the `spoken` register).
- `pnpm jev loop short` and `pnpm jev score opening` are hints only: the opening model failed its
  held-out test, and the Shorts grader (jev-1.13.0, CutKit's too) didn't track breakout on 20
  competitor Shorts (rank correlation -0.06), per `references/shorts-script.md` step 5. The loop and
  round 5: `vibe-kit/ai-doc/references/content-grade.md`.

## Self-Healing

New failure modes go to `references/learned-patterns.md` after each run, newest first. A stale finding
is corrected here in the same session, along with
if `reviewScript` checks the rule.
