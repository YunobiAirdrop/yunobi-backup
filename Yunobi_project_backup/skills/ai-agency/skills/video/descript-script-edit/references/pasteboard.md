# The clipboard is a write path, and it needs no credits and no browser

Descript's rich clipboard carries the **edit**, not the text. Copy any selection and the
macOS `«class HTML»` flavor holds

```html
<span data-descript-pasteboard="<base64 JSON>">…</span>
```

851 KB of it for a 325-character selection. Decoded, one payload holds the whole model:

| field | what it is |
|---|---|
| `copiedTaus[]` | `text.string` + `audioSegment {mediaRefId, offset, duration}` |
| `mediaRefsCopyData[].mediaRef.voiceover.metadata.alignment` | every word with `startTime` / `endTime` |
| `sequenceTracks[]`, `copiedComponents[]` | video track, layers, effects, card boundaries |
| `projectId`, `sourceTrack.id` | which composition the payload is addressed to |

**A cut is not a text edit.** Each surviving run of words becomes its own TAU whose
`audioSegment` slices the same media at that run's word timings. So the round trip is:
the user selects all and copies, a script rewrites `copiedTaus`, the payload goes back on
the clipboard, the user selects all and pastes. One paste replaces forty guarded drags,
costs no AI credits, and needs no browser session at all - the user is already logged in.

Verified 2026-08-20 on `Embracing AI for Agency Delivery`: **1036.95s -> 270.15s** in a
single paste, video intact, against a predicted 278.2s.

`scripts/dclip.py` reads and writes the flavor; `scripts/recut2.py` rebuilds the payload
from a cut list of word indices. Those indices are the **token** indices `dscript words` prints,
not alignment indices - the alignment carries words that fall in gaps between TAUs, so the two
drift apart and a cut list read in the wrong space lands on the wrong sentences without erroring.

## Ignore, not delete - this is the mode to use

**Ignore is `isBlocked` on the TAU, not a text attribute.** The `attributes` array stays
empty. An ignored TAU keeps its text *and* its `audioSegment` and sets `isBlocked: true`,
and its segment stays contiguous with its neighbours - tau 1 ending at 169.812 is followed
by tau 2 starting at 169.812. Nothing is removed; the region is skipped on render.

So a cut list can ship two ways, and the second is better:

| | delete | ignore |
|---|---|---|
| cut words | gone from the script | struck through, still there |
| reversible | undo only | un-ignore any word, any time |
| text integrity | must re-capitalise, orphan commas | text preserved byte-identical |
| pauses | butt-splices word end to word start | contiguous, keeps natural rhythm |

The last row is not cosmetic. On the same 12 cuts, delete gave 2:22 and ignore gave 2:46 -
24 seconds of the speaker's own pauses that the delete mode had silently eaten.

`build_ignore()` in `scripts/recut2.py` emits it: walk each TAU's tokens, split where the
blocked flag changes, give each segment `offset` = its first word's `startTime` and
`duration` running to the *next* segment's first word so the timeline stays gapless. Assert
that the concatenated text equals the original before writing the clipboard.

Verified 2026-08-20 on `Export Descript files`: pasted, copied back, and Descript returned
exactly what was built - 31 TAUs, 15 blocked, 166.5s playing of 260.1s.

**With ignores present, `composition.duration` is not the render length.** That project
reported 279.4s against a 261.8s original, because an ignored region still occupies the
timeline. Read the render length from the clipboard - sum the durations of the TAUs whose
`isBlocked` is false - not from `get_project`.

## Fillers and typos come free

`is_filler()` catches the hesitation set (`uh um uhh umm uhm er erm ah mm hmm mhm`) and
truncated fragments ending in a hyphen (`e-`, `aud-`). Cutting them is automatic; on this
video it was 8 words.

Two classes of typo, and only one is safe to fix. Where the transcriber was wrong and the
audio is right, correcting the text makes them agree: a glued stutter (`th-them` -> `them`,
matched by `\b(\w{1,3})-(\1\w*)\b`) and mangled product names (`scripts/typos.example.json`
holds ClickUp, Claude Code, DaVinci, Seedance and the rest). Where the **speaker** misspoke -
"explain you how to export", "it depends on workflow" - correcting the text makes the
captions disagree with what is heard. Leave those unless the user asks.

**In delete mode, removing a filler strands its comma.** "pre-edited, uh, timeline" becomes
"pre-edited, timeline"; the comma existed only to bracket the filler. Ignore mode does not
have this problem at all, which is one more reason to prefer it.

## The four things that will bite

**Pasting plain text does nothing.** Plain text has no `audioSegment`, so Descript treats it
as typed text with no media - the same fault the laws record as *typed text is deleted,
never ignored*. Only the reconstructed pasteboard edits the video.

**`osascript -e` blows up on a real payload.** A 1 MB payload is a 3 MB hex script and argv
dies with `Argument list too long`. Pipe the AppleScript through **stdin** (`osascript -`).

**Never map words onto the alignment with `difflib`.** This is the one that shipped a wrong
edit. A select-all gives one TAU per paragraph (68 here), and the copied token stream can
differ from the export - a word that falls in a gap between TAUs exists in the alignment and
in `export_transcript` but in no TAU, so global indices drift by one. Worse, when a sentence
is spoken twelve times, `SequenceMatcher` cannot tell the repetitions apart and pairs tokens
with the **wrong take**. It fails silently: identical token count, plausible output, and the
finished video keeps the take you meant to cut. On this run it flipped all five contested
choices, including reinstating the abandoned opener.

Map by **time** instead. Each TAU's `offset`/`duration` claims the alignment words
overlapping its window; trim to the token count from whichever end overlaps least. The check
that catches the difflib bug is not the count, it is **word agreement**: assert that every
mapped token equals its alignment word. difflib scored 2013/2013 on count and the time-based
mapper scores 2013/2013 on the words themselves.

**Paragraph breaks live in the text, never in the TAU boundaries.** 68 TAUs rendered 55
paragraphs. Appending `"\n"` to every emitted TAU looks harmless and shreds the script: a TAU
split merely to drop a filler starts a new paragraph mid-sentence, and a per-TAU capitalise
pass then upper-cases the continuation - "export the pre-edited," / "Timeline, because I have
removed repeats,". Slice the separator out of the source text instead, and only capitalise a
run whose separator actually contains a newline.

**TAUs do not tile the media.** 68 TAUs left 36 gaps totalling 186.04s, and
`850.91 + 186.04 = 1036.95` exactly. Those gaps are dead air between takes, and a rebuilt
payload drops them for free, so runtime falls further than the word count predicts: 56.8% of
words here, 74% of runtime.

## Housekeeping the paste needs

- Mint a real `uuid4` for every new TAU.
- `copiedComponents[].tauAnchor.tauId` points at TAUs that no longer exist. Remap each one to
  the **segment that still holds its character position** - `reanchor()` in `recut2.py`. Pointing
  them all at `new[0]` keeps the video framing and silently destroys the structure: on a 65-TAU
  take that was 11 `cardBoundaryComponent` scene boundaries and one `markerComponent`
  ("Why the move") all piled at the top of the script. An anchor that lands on a TAU the cut
  blocked slides forward to the next live one, or the card opens on struck-through text.
- Markers are `markerComponent` with a `text` field, on the same `tauAnchor`. Nothing else
  distinguishes them, so a section legend is `--markers markers.json`:
  `[{"phrase": "...", "text": "Why the move"}]`, matched against the **surviving** TAU text so a
  marker never lands on an ignored restart. Existing markers are kept by text, never duplicated.
- Cutting a connector can strand a lowercase opener. Capitalise the first letter of the
  first TAU's text after cutting.
- Keep the pre-edit payload. It is the restore path: put it back on the clipboard and paste.
- Warn the user not to copy anything else while the rebuilt payload is on the clipboard.

## Bold, highlight, and the cue legend the editor reads

Formatting rides in the same payload:

```json
"attributes": [
  {"attribute": {"name": "bold",      "value": true},                "range": {"location": 18, "length": 4}},
  {"attribute": {"name": "highlight", "value": "0x:highlight:sand"}, "range": {"location": 12, "length": 5}}
]
"highlighters": [{"id": "0x:highlight:sand", "name": "Sand", "color": [250, 152, 5, 64]}]
```

`location` and `length` are characters **inside that TAU's own string**, not the document, so a
phrase straddling a TAU boundary must be styled once per TAU. Every highlight id used has to be
registered in `highlighters` or the reference dangles. Alpha is 64. Descript's palette is Yellow,
Red, Orange, Green, Blue, Purple, Coral, Magenta, Lime, Seafoam, Lavender, Grey and Sand -
`PALETTE` in `scripts/recut2.py` holds them; do not invent ids.

This is the real prize, because a highlight is a **cue to the editor** that survives into the
script they work from. The legend, one colour to one instruction, in `CUES`:

| colour | means | who executes it |
|---|---|---|
| blue | B-ROLL - replace the picture with a full-frame clip | `motion-design`, full-frame register |
| purple | FIGURE - draw this as a diagram or an analogy | `motion-design`, figure register, transparent alpha layer |
| green | ON-SCREEN TEXT - caption or list keyed over the face | `motion-design`, caption register |
| orange | CTA - subscribe / like / book-a-call overlay | `youtube-ctas` |
| coral | BRAND ASSET - product box, logo, shelf asset | Design Assets shelf |
| yellow | EMPHASIS - punch in, this line carries the point | editor |
| red | PROBLEM - needs a retake or a fix before publish | the speaker |

So one paste can hand the editor a script that is already cut, already de-filled, and already
marked up with where every b-roll, diagram, caption and CTA goes. Write the marks as
`scripts/styles.example.json`: `[{"phrase": "...", "highlight": "blue", "bold": true}]`.

**Verify a style before shipping it.** Read each attribute back and slice the TAU string with its
own range - the fragment must be the phrase you meant. A range is silently wrong, never an error.

## Run it with `scripts/dscript.py`, not by hand

`grab` / `words` / `apply` / `check` / `history` / `restore`. It archives every payload it sees or
writes to `~/.descript-clip/history`, which is the only undo that survives the clipboard being
overwritten - and it will be overwritten, because the user keeps copying things mid-run. Raycast's
own clipboard history cannot stand in for this: its store is encrypted and sqlite refuses it
outright (`file is not a database`).

`apply` refuses to hand over a clipboard that does not round-trip, or that carries a style range
running past the end of its TAU. Both faults are silent otherwise - the paste simply lands wrong.

Tell the user not to copy anything else between `apply` and their paste. They will anyway; that is
what `restore` is for.

## The cut list, and everything `apply` does unasked

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling.

**Write the cut list in words, never in indices.** `scripts/resolve.py` turns a phrase into the
token range `apply` wants, prints five words of context on each side of every needle so the landing
can be read back, and refuses the whole list when a phrase matches nothing, matches twice with no
`nth`, or overlaps another needle. `"pre"` and `"post"` disambiguate a short needle by what sits
beside it - a bare `"Then"` with `nth: 1` lands on the first `then` in the whole take, forty
minutes from the one that was meant. Indices written by hand are unauditable and drift by one the
moment an earlier needle changes.

`grab` works on a **partial selection** too - the payload carries its own offsets, so a paste
replaces exactly the region that was selected.

Six things `apply` does without being asked: cuts as **Ignore** (struck through and reversible,
never deleted), **keeps every Ignore already in the composition**, removes fillers and truncated
fragments, repairs glued stutters and product names, carries every scene boundary and marker onto
the TAU that still holds its text, and refuses to write the clipboard unless the payload
round-trips and every style range resolves inside its TAU. So a second pass is safe and an empty
cut list is an exact no-op - verify that way whenever the maths looks wrong: `build_ignore([])`
must return the source `plays` to the millisecond.

`--markers markers.json` names the sections - `[{"phrase": "...", "text": "Why the move"}]` - matched against the surviving text so a marker never lands on an ignored restart.`--typos` is the house glossary and it is what stops a caption saying the wrong product name: 41 entries, and the rule that keeps them safe, in [`references/typos.md`](typos.md).
