---
name: video-hooks
description: "Writes the opening of a video and the full structure of a Short, for both the 1-to-3-second Shorts window and the 30-second long-form open. Generates competing hook variants by named mechanism, rates each for drop-off risk, and holds every factual claim to something measured. Use when writing or fixing a hook, when restructuring a Short script, when a Short is being swiped away, or when a script opens weakly."
tags: [writes, video, youtube]
---

# Video Hooks

The opening decides whether people **stay**. It does not decide how many arrive.

That distinction was measured. Across 27 transcripts from Matt Gray's channel, the openings of his
hits and his flops are the same length (151 words against 156) and reach the viewer and their first
number at the same moment; the cleanest case is a pair opening on the identical sentence, "at the
time of this video, I'm 35 years old", sitting eleven times apart in views. It replicated on a
second channel in an opposite niche.

**Replicated again on 26 Aug 2026, across 627 whole transcripts and 13 channels**, winner band
against control band inside each channel: 107 words against 106, first number at 22.2 seconds
against 23.9, and a shorter opening is the winner's on 4 channels of 13, which is worse than a coin.
The most replicated finding in the corpus, and the reason a video that underperformed on views is
never fixed here. Evidence: a 627-video corpus read winner-band against control-band per channel.

**The hook opens the loop. It cannot close it.** What keeps somebody past the open is
`storytelling`: one question opened early and paid off late on the same object, the five moves, and
the ban on restating. A hook that lands on a body which then restates itself is a hook that bought
attention for nothing, and the loop it opened and never closed is the definition of bait.

**The subject decides reach, then the title and thumbnail, and only then is the
hook ever heard.** If a video underperformed on views, do not rewrite the hook.
Check the subject was worth making (`idea-mining` owns that choice and ranks the
places a validated one comes from), rewrite the title, and regenerate the
thumbnail (`youtube-thumbnail`). Read
`vibe-kit/ai-doc/references/competitor-evidence.md` for the two title levers that survived
the control test.

**A reference video's own opening is measurable on the same axes.**
`video-script/scripts/teardown.py <url>` prints its first 30 seconds verbatim and the moment it
reaches its first number, which are the two the Matt Gray finding is stated in. One home; not
repeated here.

Where this skill earns its keep is everything after the click: the swipe-away window on a Short,
and whether a long-form viewer is still there at ninety seconds. That is retention, it is what
completion rate measures, and on Shorts completion rate is what triggers promotion. So the hook
still matters enormously. It just cannot be held responsible for a number it never touched.

**A dip straight after an off-target spike is a cohort problem, not a hook problem.** When a video
reaches far outside the ICP, the next few get served to that borrowed audience and land flat, so do
not rewrite a format that was working. Judge the spike on joins rather than views: count views
to community joins for exactly this reason, and hold the congruence rule, which is the measured
version of the same idea.
Hypothesis from a short-form course newsletter, not control-tested here.

**This skill stops at 0:30.** Everything after the open, the teach blocks, the demo choreography, the
runtime budget and where the one commercial ask goes, is `video-script`, which carries the three-run
control that settles ask placement and takes its opening from here.

**Read what the feed rewards this month before drafting.** `social-engagement`,
`references/what-works.md`, derived from competitor posts scored against each account's own median.
It carries its measurement date; over 30 days old, regenerate it first. It says what the feed
rewards, never what is good, so the bans and `voice-dna` outrank every number on it.

## The one rule that overrides the rest

**Go as hard as you want on the mechanism. Every fact underneath it has to be true.**

These are two separate dials and they get confused constantly. The levers in the table below are neutral: use any of them. What is not available is inventing the material they operate on: a number nobody measured, a story that did not happen, a stake that does not exist. It is a positioning constraint before it is anything else. An account that sells on being the founder who shows the real numbers needs a proof table of measured evidence for exactly this purpose. One fabricated claim is the only thing that can actually cost that account. Read the proof table before writing, and pull from it.

The craft argument points the same way. Invented drama lands generic, because a model reaching for stakes reaches for the average stakes. A real number is specific, and specific is what stops a thumb. **"You lose about 24 hours a month" is weaker than "I lost 23 hours and 48 minutes this month, here is the screen."** Where the strategy doc says manufactured urgency feels fake, read that as a note about invented material, not a ban on emotion: it was written against fiction, not against feeling.

**Show the number, do not only say it.** Where a real artefact exists (a dashboard, a counter, a board, an invoice), the proof frame is that artefact, within two seconds of the claim.

**The strongest proof frame is two artefacts from one input.** One prompt, two configurations, both
outputs on screen, then a verdict that splits rather than crowns. Why it beats a single screenshot,
what the truth rule binds it to, and the source: [`references/proof-frames.md`](references/proof-frames.md).

## Banned constructions

The banned word and phrase list is enforced, not advisory. It lives in one place,
`vibe-kit/packages/lint/data/slop-words.js`, which backs the `no-ai-words` ESLint
rule and the ClickUp SOP page "List of AI expressions to Ban". Read it before
writing and add to it there, never to a local copy.

**The negation pivot is the one this skill gets wrong most often**: defining a thing by denying
another first, as in "it is not a project, it is a wish". One is a rhetorical beat, and several in a
ninety-second script is the loudest signal in the piece that a machine wrote it. **One per script,
maximum**, short and concrete, with every abstract pivot cut. Count them before shipping, because
the pattern is invisible while drafting and obvious on playback. Full treatment, including the
tailing-negation variant: `humanizer`, `references/patterns.md` section 9.

## Point at the viewer, and pick the register

A script addresses the viewer's situation rather than reporting yours, and the emotional register is chosen rather than defaulted. See [`references/register.md`](references/register.md).

**A hook is ultra specific or it is not a hook.** Stated 21 Aug 2026: "the hook needs to be ultra
specific always", and "people need to identify". The viewer has to be able to run the claim against
their own week and come back with yes or no. "Your business does not run without you" is a general
truth, so nobody answers it; "if you run an agency and it stops the week you go on holiday, you are
the system" names a week the viewer either had or did not. The shape that forces this is a
conditional: `if you <a situation with a number, a tool or a person in it>`, then the verdict.

The identifier is the audience filter as well. A hook that names the wrong people loses nobody worth
keeping, and a hook that names 28-year-olds in Minnesota working at Walmart keeps exactly them.
Losing the rest of the feed is the point of the line, not a cost of it.

**Then stop, because the hook must not answer itself.** Same day, on a hook that named the
situation and delivered the verdict in the same breath ("here is something you need to create
intrigue"): two mechanisms are running and the second dies on contact with a payoff.
Self-reference gets the sentence processed as being about the viewer (Kelley et al. 2002; the
recall effect goes back to Rogers 1977), and the missing main clause leaves it unfinished, which is
what keeps it live (Zeigarnik 1927) and what Loewenstein's information gap, 1994, calls the felt
distance between what you know and what you want to know. The gap has to be small, specific and
visible, so a general claim opens none. Say "if your account manager spends 2 hours a day updating
a sheet" and let the next line, the next slide or the next second carry the verdict.

**An open gap is not enough on its own. It has to look worth closing, and it has to be guessable.**
Almost anything withheld makes somebody want to know what comes next, so the test is **"does this
make somebody feel it is worth knowing"**, and bait is the line that passes the first and fails the
second. Then: "something happened on that call that changed everything" gives nothing to guess
with, so no prediction forms and the reveal has nothing to break, while "she said one thing in the
first 30 minutes that killed the retainer" runs predictions because it names the situation, the
number and the person. All three conditions, and seven open shapes that carry them:
[`references/gap-shapes.md`](references/gap-shapes.md).

**Harvest the phrase, do not invent it.** `customer-voice` holds the viewer's own words from 367
recorded calls, and `scripts/search-demand.py` reads what people actually type into the search bar.
Both, and what to file the result as: [`references/harvest.md`](references/harvest.md).

Numbers in a hook are digits, never words, on screen and in the caption alike (`humanizer` pattern
45). The carousel form of it, the influence ladder across six slides, and why scarcity is
deliberately unused: `slide-deck`, `references/native-campaigns.md`.

## Three surfaces, and the failure is that they disagree

A hook is written three times: the visual in the first frame, the title text on screen, and the
spoken line, and **they have to carry the same claim.** A viewer who sees one thing, reads a second
and hears a third assembles nothing, and confusion is what makes people leave. It is not boredom,
and on a retention chart the two are indistinguishable. The move that gets half-executed is
contrast: name the common belief out loud, then break it, rather than making a contrarian claim and
leaving the belief it flips in the writer's head. What each surface carries, which one is optional,
and the read-order evidence: [`references/three-surfaces.md`](references/three-surfaces.md).

## Confirm the click in the first five seconds

Separate from the hook and easy to confuse with it. The title and the thumbnail made a promise, and
the open has to show immediately that this is the video that promise came from: a viewer who clicked
on one subject and hears a different one in the first breath leaves before the hook has finished.

So on long-form the first line names the subject of the title in the viewer's own words. That is not
a restatement of the title, which `storytelling` puts on rung 0 and bans, it is the same subject
arriving from the viewer's side. `youtube-thumbnail`, `references/angle.md` records the claim the
frame made, and that claim is the debt this line settles. The packaging is spent once it has done
this: it gets the viewer to the open, the open gets them to the first usable thing, and from there
nobody remembers what the title said.

## Two windows, two jobs

The 1-to-3-second Shorts window and the 30-second long-form open, with the measurements behind each: [`references/two-windows.md`](references/two-windows.md).

## The whole Short, not just the hook

When the job is a full Short script rather than an opening line, read
`references/shorts-structures.md` before drafting: the skeleton (outcome hook → named method →
stepped body → mid-flip rehook at ~25 seconds → recap → reply-trigger CTA), the four retention
structures, a worked example and a template. From the @kallawaymarketing corpus, hypothesis rather
than measured; the truth rule and the voice pass apply to every line it produces.

## One creator's hooks taken apart, and the third replication of the finding above

[`references/hook-teardown.md`](references/hook-teardown.md): one creator's whole hook doctrine, his
"Viral Hooks" document verbatim off the frames where he screen-shares it, and the text hooks burned
into his picture that no caption track carries. A teardown of one person, not a bank to draw from.

**Read its measurement first.** 475 of his own openings, banded on era-adjusted breakout: **not one
of sixteen construction features separates his winners from his controls**, and the corpus holds
pairs where the same sentence ran 4x apart. Third replication of the finding this page opens on, the
first on short form, and the creator sells the hook course. Vocabulary, never levers.

## The six story locks, which are word swaps rather than structures

Run over a finished script, one pass per lock, no beat moving: **term branding**, **embedded
truths**, **thought narration**, **negative frames**, **loop openers**, **contrast words**. Contrast
is the engine under the other five, so it is the one to use when only one pass is affordable.
[`references/story-locks.md`](references/story-locks.md), which `video-script` reads too for the
body. They are the sentence-scale re-hook beat of `storytelling`, [`references/addiction-loop.md`](../../../content/writing/storytelling/references/addiction-loop.md).

**None of the six is judged by eye, and none of them is a lever.** `video-script`,
`scripts/story_metrics.py --grade` counts all six with the offending sentence attached, graded
against percentiles of 627 videos. That corpus was asked on 29 Aug 2026 whether any of them
separates a winner from its own channel's controls: the best held in 9 channels of 13, which is a
coin, so they buy retention and never reach. Two collide with rules already enforced here and the
reference resolves both. **A hedge is where the viewer leaves, and provenance is not a hedge.**
**A negative frame is not a negation pivot**, and the see-saw stays capped at one per script.

## The five mechanisms

Shock or contradiction, problem agitation, story open, curiosity gap, social proof. Name the
one before writing, because an unnamed hook usually turns out to be two fighting. How each
works, what it suits and how it fails: [references/mechanisms.md](references/mechanisms.md).

## Execution

0. **The open is written out in full, and the body it feeds is written as bullets.** The
   hook's opening lines are the one place in a script where the exact wording is
   load-bearing, so they ship verbatim and marked `Say this line as written`. Everything
   after them is bullets: `video-script`, "Every script ships as bullets".
1. **On long-form, write the open last, from the finished transcript.** Outline, record the body,
   then read what was actually said and write the open against that. A long recording goes where it
   goes, and an open written in advance ends up promising the video that was planned rather than the
   one that exists, which is a retention loss at the exact moment it costs most. This does not apply
   to a Short, where the hook is the plan.
2. **Find the true number first.** Before writing a word, ask what is already measured and screenshottable. If nothing is, say so and stop; that is the real blocker.
3. **Pick the window**, 1 to 3 seconds or 30 seconds, and hold the word budget. Going over is the most common failure.
4. **Write at least three variants on different mechanisms.** One variant is not a choice.
5. **Rate each one**: mechanism, word count, drop-off risk with a reason, and what makes it fail.
6. **Read them aloud.** A hook that cannot be said in one breath is not a hook.
7. **Run the voice pass.** Hand the winner to the `humanizer` skill with a sample of the person actually speaking. A mechanically correct hook in the wrong voice still loses.
8. If this run surfaced a failure mode not already listed below, append it to Learned Patterns with today's date.

## Verification checklist

- [ ] The first line describes the viewer's problem, not the author's history, and survives the stranger test
- [ ] The first-person count was taken across the whole script and it is zero, or every survivor is a hedge on his own number, the DM ask, an assignment, or a line somebody else said. The hook itself carries none: an opening about the writer spends the only attention the video is guaranteed. `humanizer`, "On camera, every I is a you"
- [ ] The closing line points at the viewer's next action, not at what the author did
- [ ] Every middle beat carries a consequence rather than a definition, and the close is a command rather than a recap
- [ ] An emotional lever was chosen by name before the hook was written, and the hook is not merely informative
- [ ] The subject was checked against harvested search demand rather than against what the writer assumed the viewer calls it
- [ ] The gap was tested for payoff, not only for suspense: the line answers "worth knowing", not just "want to know"
- [ ] The gap is guessable: a viewer can form a wrong prediction from the line, rather than only knowing an answer is being withheld
- [ ] On a Short, the stakes carry all three parts (a character, something at risk, a clock), and every re-hook survived having its transition deleted with a fact or a question still standing
- [ ] Every number in the hook is measured, not estimated, and is traceable to a source or a screen
- [ ] The first frame shows the proof where a real artefact exists, and any A/B claim puts both artefacts on screen from the same input
- [ ] Any counted promise in the open is paid by that many named, countable beats in the body
- [ ] All three hook surfaces were written, and the visual, the title text and the spoken line carry one claim rather than three
- [ ] Where the mechanism is contrast, the common belief is stated on screen or out loud before it is broken
- [ ] On long-form, the first five seconds name the subject the title promised, in the viewer's words rather than the title's
- [ ] Word count is inside the budget for the chosen window
- [ ] On long-form, the open was written against the recorded transcript rather than the plan, and past thirty minutes it answers the safe beat
- [ ] Three or more variants were written on different named mechanisms
- [ ] Each variant carries a drop-off risk rating with a reason
- [ ] The winner survived being read aloud in one breath
- [ ] The winner went through `humanizer` against a real speech sample
- [ ] Negation pivots were counted: at most one in the script, short and concrete
- [ ] Any new failure mode was appended to Learned Patterns

## Learned Patterns

What this skill's own runs have taught it, newest first, kept out of the body so the rules above carry the cost and the evidence does not. Append with `ai-architecture log`. See [`references/learned-patterns.md`](references/learned-patterns.md).
