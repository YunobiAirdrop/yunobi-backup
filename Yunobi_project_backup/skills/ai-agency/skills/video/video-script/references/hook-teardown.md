# One creator's hooks, taken apart

Not a library: nothing here is a bank of hooks to draw from. It is a teardown of one creator, his
complete hook doctrine and 475 of his openings measured against his own control band. Read the
measurement first, because it changes what the rest of the file is for.

## Provenance, and how much to trust it

Source: **Mino (@mino.mp4)**, TikTok-first personal-brand teaching, 531 posts between
25 Sep 2022 and 27 Aug 2026, 41.5M lifetime views, median 13,100. He coaches creators on hooks
and sells a content programme, so the hook advice is his product rather than an aside.
`tiktok.ts mino` (531 posts with views, likes, comments, duration, to `data/mino/tiktok.json`),
`tiktok-transcripts.ts mino --all` (504 transcripts with word-level timings), and
`tiktok-text-hooks.ts mino --top 60` (text hooks off the first frames, same files, `textHook`).
**TikTok publishes its own caption track with word-level timings**, which no other surface in the
directory does, which is why the first 1.5 seconds is a quoted object here rather than a paraphrase.

Two honesty notes, the same two that govern the Kallaway corpus in `shorts-script`'s [`shorts-structures.md`](~/Studio/vibe-kit/ai-doc/skills/video/scripting/shorts-script/references/shorts-structures.md): **he is off-ICP**
 so `idea-mining` should not
read this file; what transfers is construction), and **import the structures, never the
register** (his lines run on "fucking crazy", "dogshit", "literally life-changing", which
`humanizer` rejects and the truth rule in `SKILL.md` bans; every shape below survives translation
into calm evidenced speech). Unlike the Kallaway corpus, this one **is banded**.

## The finding: none of it separates his own bands

475 openings carry a caption inside the first 1.5 seconds. Split on **era-adjusted breakout**,
views over the median of the 40 videos nearest in time, so four years of follower growth cannot
pose as technique: **winners** are 134 videos at 2.0x their era or better (his own threshold: he
tells viewers to treat any video at 2x their average as the signal worth pattern-matching), and
**controls** are 221 videos between 0.5x and 1.5x.

Sixteen construction features were counted on the first sentence of each (table abridged to 8).
**Not one separates the bands at p<0.05**, on a test where sixteen comparisons would be expected
to throw up roughly one significant result by chance alone.

| Feature | Winners | Controls | p |
| --- | --- | --- | --- |
| Opens "here's" | 15% | 10% | 0.16 |
| Opens with I / my | 19% | 13% | 0.11 |
| Second person anywhere | 52% | 46% | 0.23 |
| First person anywhere | 49% | 54% | 0.40 |
| Negation or prohibition | 25% | 25% | 0.96 |
| An extremity word ("exactly", "only", "literally") | 34% | 28% | 0.27 |
| Promises a method ("how to", "how I") | 17% | 10% | 0.07 |
| A niche keyword | 48% | 46% | 0.77 |

Length does not separate them either: 9.9 words against 10.2 inside the first 1.5 seconds, 21.6
against 24.0 in the first sentence. Nor does runtime, at 83 seconds against 82. **Read that the way this skill reads every band
comparison: a trait present in both bands is house style, and copying it buys nothing.** Every
shape in the rest of this file is house style, not why any particular video worked.

Third independent replication of the finding `SKILL.md` opens on: Matt Gray's hits and flops open
identically across 27 transcripts, 627 transcripts across 13 channels put the winner band at 107
words against the control's 106, now one creator's 475 openings from the one who sells the hook
course. **The hook decides whether people stay. It does not decide how many arrive.**

## Matched pairs, the cheapest way to see it

The corpus contains near-duplicate openings that landed in different bands, as close to a natural
control as an observational corpus gets, since construction is held still and everything else is
free to vary. Thirteen such pairs exist above 0.62 similarity; the pattern holds across all of them.

| | Winner | Control |
| --- | --- | --- |
| Same sentence, twice | "here's how to edit your TikTok video so you go viral", **3.3x**, 33,700, Nov 2022 | "Here's how to Edit Your TikTok videos so you go viral.", **0.8x**, 7,556, Mar 2023 |
| Same month, same subject | "Can't afford to pay rent for me and my girlfriend.", **246x**, 3.1M, Jun 2026 | "I can't afford to pay rent for me and my girlfriend but I don't have the balls to ask her to split the rent with me", **1.0x**, 12,000, Jun 2026 |
| The framework, textbook-executed | "Stop deleting your videos.", **28.5x**, 311,100, Oct 2022 | "In the next 60 seconds I'm going to guarantee that you never struggle to come up with viral content ideas ever again.", **1.0x**, 13,600, May 2024 |

The last row is the one to sit with: the control is his own framework executed perfectly (a
duration bound, a guarantee, an extreme result, the word "you", an objection-proof promise), and
it did its channel's median. The winner is four words with no mechanism in it at all.

## What he says the hook is made of

Kept because it is the best-articulated statement of short-form hook craft in the corpus, and a
shape you can name is a shape you can audit. Not because any of it is a lever.

- **The three-part hook** (Jun 2023, 631k views): target viewer stated specifically enough the
  right person feels addressed, the dream result for that viewer, the specific solution that gets
  them there. "The only way you make somebody feel this video is for me is by being extremely
  specific."
- **The two-sentence pattern** (Oct 2023, 574k), from 15 viral videos: sentence one is an extreme
  result or problem, addressed to "you", carrying an extremity word; **sentence two destroys the
  objection**, saying the viewer's own doubt back to them before they can act on it.
- **The three boxes** (Feb 2023, 113k): fast (no "hey guys welcome back"), clear (the viewer can
  answer "what do I get" inside three seconds), shocking or unique against the feed.
- **The four Lego pieces** (Jul 2026, 46k): an emotion, a visual proof it is not clickbait, a
  specific example or number, **a rehook that hints at a payoff at the end**.
- **Three forms of specificity** (May 2026, 94k), the most portable thing he says: niche keywords
  over category words ("300 view jail" beats "content creation advice"), numbers, and named
  people or faces.
- **The three levels of mastery** (Feb 2026, 7.8k): beginners steal a hook word for word; then
  **concision** (the commonest coached fault is 20 seconds to the point when it should be three to
  five); then **tonality** (push energy reads as desperation on screen).
- **The ideal viewer persona** (Jul 2026, 57k; Feb 2026, 13.6k): a document naming who the viewer
  is, their pains and desires, before the hook or the idea. **Every idea is a problem that persona
  has, stated in their own words in the hook.**
- **Where the hook comes from** (May 2026, 30k; Aug 2026, 28k): search YouTube, not the feed,
  because the highest-effort concepts are built there first. **A short's hook is a YouTube title
  and thumbnail**: the spoken line is the title, the on-screen text the thumbnail text, the first
  frame the thumbnail image. And "scrolling like an artist": train the feed with "not interested",
  then read only the first sentence of a competitor's video and stop.

## His hook document, verbatim

He screen-shares his "Viral Hooks" Google Doc on camera in the Oct 2023 video, read off the frames
with Vision OCR: his own two-sentence structure, in his own words, transcription errors his.

**SENTENCE 1: HOOK**

*Content creation* (abridged, 2 of 6 kept)

1. Here's how I add captions to my TikToks so they go viral every single time. I use a formula I like to call SLC. Now what the hell does that mean?
2. I scripted out every single one of the hooks to my TikTok videos on this TikTok account for a month using the same exact hook structure, and in that month, I went from 0 to 100,000 followers.

*Self-improvement* (abridged, 2 of 7 kept)

1. Here's how to stop waking up in the morning, looking in the mirror, and hating what you see. Stop using your phone for the first hour of the day.
2. Here's the ABSOLUTE key to destroying the inner nice guy inside of you FOREVER.

*Lifestyle*: "Here's a day in the life of a 22 year-old entrepreneur making $100k per month with
his agency." *Hot takes*: "This is exactly why days don't even exist, and if you can get rid of
days altogether you're gonna be a lot more productive in your life."

**SENTENCE 2: OBLITERATE OBJECTIONS** (abridged, 6 of 14 kept)

1. Since this is TikTok, your attention span is probably dogshit, so try to make it through the rest of this video because I guarantee it will change your life.
2. What the HELL does that mean?
3. No, I'm not talking about {insert CLICHE, OVERUSED answers}.
4. Now I know what you're probably thinking: ***
5. You're REALLY gonna watch this one because it's fucking crazy.
6. If you want to [outcome], just implement this ONE little tactic.

**Shapes 2 and 3 are the two worth having.** "What the hell does that mean?" is the speaker asking
the viewer's question out loud, the cheapest way to keep a named method from reading as jargon.
"No, I'm not talking about {the cliché}" pre-empts the answer the viewer has already dismissed,
and is the only one on the list that makes the video *more* honest. The rest of sentence two is a
promise about the video's own value, a claim, and on this channel a claim has to be true.

## The second surface: what he burns into the picture

The caption track carries the spoken hook. It does not carry the **text hook**, the words burned
into the frame, which exist only as pixels. `tiktok-text-hooks.ts` reads them by OCRing a frame at
0.4s and one at 3.0s, keeping the lines present in both (captions advance every word or two and
survive one frame; a static title survives both). **Exactly half do not have one**: of his top 60
by era-adjusted breakout, 30 carry a static title and 30 run captions only, so the text hook is not
a requirement even for him.

Where it exists it is a different sentence from anything he says out loud, abridged to three of 30:
"the lonely chapter when chasing your dreams", "steal my hook strategy to get ur next 1M view
video", "'FACELESS' CONTENT WILL NEVER MAKE YOU RICH." **The pattern is the useful part, not the
lines**: the title carries the promise and the number, the spoken line walks in from the side and
never restates it, the three-surfaces rule in `SKILL.md` executed rather than described.

**Two limits, and neither is small.** Run on the top 60 only, all winners, so **it carries no band
comparison**: nothing here says a text hook separates his hits from his median, only that half
have one. And the method has a false positive: a video that opens on a static screen recording
(analytics, a profile page, a reply-to-comment sticker) returns that screen's text as though it
were a title. Six of the 30 are that case.

## What to import, and what to leave

**Import**: the objection sentence (say the viewer's doubt out loud in sentence two, in their
words, the one move the registry did not already carry, costing nothing and making a piece more
honest, with `conversion` holding the doubts verbatim); the three forms of specificity (niche
keyword over category word, a number, a named person, the ultra-specific rule in `SKILL.md` broken
into three checkable parts); concision as a measured fault (three to five seconds to the point
rather than twenty); his calibration trick (after filming, scroll the feed for five minutes, then
watch your own take, which restores the viewer's tolerance to the level the video will actually
meet, beside the eyes-closed pacing test in `video-script`); and reading the first two sentences of
a competitor and stopping, which sharpens the remix rule in `idea-mining`.

**Leave**: every promise about the video's own value ("it will change your life", unfalsifiable,
the truth rule bans them); the intensifier layer, whole, which `humanizer` and the slop list in
`packages/lint/data/slop-words.js` reject on sight; the hooks themselves, which are house style
per the measurement above, arriving with none of the reason his videos worked; and his volume
advice, for the same reason `shorts-script`, `shorts-structures.md` rejects Kallaway's, cadence is a floor, not a
strategy.

## Where he corroborates something we already measured

Independent arrival at a rule already in the registry is worth more than a new claim.

| He says | Already ours |
| --- | --- |
| "Stop obsessing over hooks and retention-hacking, obsess over value per second" (Oct 2025). Months of heavy hook effort lost him followers; months at 20 minutes a video gained 100k | The subject is the reach lever and the hook is the retention lever, `idea-mining`. His own bands say the same thing louder than he does |
| Always "you", never rambling about yourself | "On camera, every I is a you", `humanizer` |
| Spend the scripting time on the hook, bullet the rest | "Every script ships as bullets", with the open verbatim, `video-script` |
| The spoken line is the title, the on-screen text is the thumbnail text, the frame is the thumbnail | "Three surfaces, and the failure is that they disagree", `SKILL.md` |
| State the viewer's problem in their own words | `conversion`, measured from 367 calls rather than imagined from a persona |

His self-correction is the important row: he sells the hook course, and in Oct 2025 told his
audience the hooks were not the thing. The 475 openings behind this file agree with him.
