# Shorts script

One reference for the whole job, because the job used to be spread over four. The structure sat in
`video-hooks`, the corpus of hooks that actually ran sat in `social`'s `references/tiktok.md`, and
the note shape sat in `social`'s `references/shorts-production.md`.
 So
this file holds the pieces specific to a whole Short, and it's the one to load when somebody says
"create a short". The truth rule and the voice pass are the trunk's, in `SKILL.md`, and outrank
everything here.

## What you're making

A script he can shoot straight off his phone and that sounds like him talking, not reading. That
means **the ends are written out and the middle is bullets.** He says the first and last lines word
for word and the middle his own way, so a fully scripted middle comes out read aloud and flat. Say
every written line out loud before filing it. If you run out of breath or it sounds like a slide,
rewrite it.

## The order of work

1. **Mine the raw transcript for an action, never the wiki note for an insight.** The nugget is
   something a viewer can do tonight with tools named out loud: a site, a command, a line to paste.
   "Install shadcn, then add one line to CLAUDE.md", never "a component library plus a rule". A
   summary note has already turned his words into categories, so the names are gone before the
   script starts. Three tests: could a stranger do it from the Short alone, repeat it to a friend
   in one sentence, and want to send it to someone (`idea-mining`'s `references/share-test.md`)?
   Weigh the topic before the first line too, with `idea-mining`'s `scripts/topic-demand.mjs`:
   a weak topic gets archived, never rewritten.
   Keep the analogy he reached for live, because that's usually the angle nobody else has. Then the truth rule, which is the trunk's and outranks everything here: every
   name, command and "I did" is checked today, or the re-check block says what to do before shooting.
1b. **Pick the anchor before you write** (`SKILL.md`, the trunk). `node scripts/top-band.mjs <niche words> --n 8`
   prints the best-ranked competitor Shorts on the subject. Choose one and write beside it, beat
   for beat. Copy its moves, never its words: they name the tool in its own sentence, count out
   loud and show each step working.
2. **Pick an opening shape by number** from [hook-library.md](hook-library.md),
   the 30 shapes reverse-engineered from 475 banded openings plus our own posts. Then write 3
   variants on different mechanisms and rate each one for drop-off, per [video-hooks.md](video-hooks.md).
   Write the 2nd beat too: the doubt the viewer already has, said out loud.
3. **Build the body on the skeleton** in [shorts-structures.md](shorts-structures.md):
   outcome hook, named method (only a name you'd say anyway, like "money first": "I call my fix
   the one library rule" is a label made up for a checker), 2 or 3 steps each carrying an example, a flip at about 25 seconds
   that still leaves a fact standing when you delete it, then a reply-trigger CTA whose artefact
   exists before the post goes out.
4. **Shape the note** per [note-shape.md](note-shape.md): title
   `CODE · name`, `CLEAN READ` on top, then `---`, the metadata row, `INTRO` / `MEAT` / `OUTRO`
   with timings, the text hook, the first frame, `RE-CHECK BEFORE SHOOTING`, the TikTok cut,
   description, first comment, hashtags. Read the newest note in the live batch first, because
   its re-check block is where corrections pile up.
5. **Run the gate**: `npx heyramzi-slop <file> --register=shorts` on the clean read, then the
   `humanizer` read by eye. Fix a rate by rewriting the sentence, never by gluing 2 together with
   "and". Two hits stay when you'd defend them out loud, because the top band runs on both: a
   "here's how" opener and a two-beat slogan ("one library, one rule"). Count steps the way the
   top band does, "step 1, step 2, step 3" out loud. **CutKit's `check_script` is a hint, never a
   bar to file.** On 4 Oct 2026 it gave 19 of 20 competitor Shorts an F, a 2,097x breakout among
   them, with a rank correlation of -0.06 against breakout, while S12, the script the author called
   unreadable, got a B-. Editing toward its checks is how a script ends up written for the grader.
   The last test is yours: read it out loud to someone who's never heard of the subject.
6. **Take the code** off `social`'s `scripts/ledger.json` plus the closed Socials tasks,
   never off memory. Then file it in CutKit, never Apple Notes (The author, 1 Oct 2026: the script
   library is CutKit from now on, so it's on his phone's teleprompter):
   `node ~/Studio/cutkit/ios/cli/cutkit-scripts.mjs push <clean-read-file> --title "CODE · name" --label "<pillar>"`
   The body is the clean read only, because the phone reads the whole body out loud. Everything
   below the `---` in the note shape (metadata row, re-check block, TikTok cut, description, first
   comment, hashtags) goes in the Socials task description instead. The pillar label comes from
   the code's letter: `S` Skills, `C` ClickUp, `A` AI and agents, `L` Lifestyle, `P` Product, `M`
   Mindset. A push with a title that exists updates that script, never adds a copy. Open a `to do`
   task on the Socials list whose description says `Script: CutKit > CODE`.
7. **The reasoning goes in the batch brief**:
   variants, ratings, surfaces. The spoken text never goes there. It lives in the CutKit script.

Once it's recorded, everything else (the coding, the edit, scheduling) is `social`'s `references/shorts-production.md`.

## What each reference holds

| File | Read it when |
| --- | --- |
| [hook-library.md](hook-library.md) | Picking the opening, the 2nd beat, the flip or the text hook |
| [hook-diagnosis.md](hook-diagnosis.md) | A hook that fails, or tightening the script after it |
| [shorts-structures.md](shorts-structures.md) | Building the body, and for the skeleton's template |
| [note-shape.md](note-shape.md) | Writing the note, before it's filed |
| [shorts-playbook.md](shorts-playbook.md) | Platform specs, the algorithm, what counts as a view |

## Checklist

- [ ] The opening names a shape from the hook library, and 3 rated variants sit in the brief
- [ ] The 3 surfaces (frame, burned text, spoken line) make one claim
- [ ] The clean read works out loud, the middle is bullets, and the ends are written word for word
- [ ] The anchor Short is named in the brief, with its breakout and URL
- [ ] The cold read named the action with its tools, and its hardest sentence got rewritten
- [ ] The gate ran on `--register=shorts`, and every hit left in is one you'd defend out loud
- [ ] The CTA's artefact exists, or the re-check block says it gets made before publishing
- [ ] The clean read is in CutKit under its pillar label, the rest is on the Socials task, and the task says `Script: CutKit > CODE`
