# The clipboard is a write path, and it needs no credits and no browser

Descript's rich clipboard carries the **edit**, not the text. Copy any selection and the macOS `«class HTML»` flavor holds

```html
<span data-descript-pasteboard="<base64 JSON>">…</span>
```

851 KB for a 325-character selection. Decoded, one payload holds the whole model:

| field | what it is |
|---|---|
| `copiedTaus[]` | `text.string` + `audioSegment {mediaRefId, offset, duration}` |
| `mediaRefsCopyData[].mediaRef.voiceover.metadata.alignment` | every word with `startTime` / `endTime` |
| `sequenceTracks[]`, `copiedComponents[]` | video track, layers, effects, card boundaries |
| `projectId`, `sourceTrack.id` | which composition the payload is addressed to |

**A cut is not a text edit.** Each surviving run of words becomes its own TAU whose `audioSegment`
slices the same media at that run's word timings: select all and copy, a script rewrites
`copiedTaus`, the payload goes back on the clipboard, select all and paste. One paste replaces
forty guarded drags. Verified 2026-08-20: **1036.95s -> 270.15s**, video intact, against a
predicted 278.2s.

`scripts/dclip.py` reads and writes the flavor; `scripts/recut2.py` rebuilds the payload from a cut
list of word indices, the **token** indices `dscript words` prints, not alignment indices - the two
drift apart (alignment carries words falling in gaps between TAUs), so a list read in the wrong
space lands on the wrong sentences without erroring.

## Ignore, not delete - this is the mode to use

**Ignore is `isBlocked` on the TAU, not a text attribute.** The `attributes` array stays empty. An
ignored TAU keeps its text *and* its `audioSegment` and sets `isBlocked: true`, its segment staying
contiguous with its neighbours (tau 1 ending at 169.812 is followed by tau 2 starting at 169.812);
nothing is removed, the region is only skipped on render. So a cut list can ship two ways, and the
second is better - not cosmetically: on the same 12 cuts,
delete gave 2:22 and ignore gave 2:46, 24 seconds of the speaker's own pauses delete silently ate.

| | delete | ignore |
|---|---|---|
| cut words | gone from the script | struck through, still there |
| reversible | undo only | un-ignore any word, any time |
| text integrity | must re-capitalise, orphan commas | text preserved byte-identical |
| pauses | butt-splices word end to word start | contiguous, keeps natural rhythm |

`build_ignore()` in `scripts/recut2.py` emits it: walk each TAU's tokens, split where the blocked
flag changes, give each segment `offset` = its first word's `startTime` and `duration` running to
the *next* segment's first word so the timeline stays gapless, asserting the concatenated text
equals the original before writing the clipboard. Verified 2026-08-20 on `Export Descript files`:
pasted, copied back, and Descript returned exactly what was built - 31 TAUs, 15 blocked, 166.5s playing of 260.1s.

**With ignores present, `composition.duration` is not the render length**: that project reported
279.4s against a 261.8s original, since an ignored region still occupies the timeline. Read the
render length from the clipboard instead - sum the durations of the TAUs whose `isBlocked` is
false.

## Fillers and typos come free

`is_filler()` catches the hesitation set (`uh um uhh umm uhm er erm ah mm hmm mhm`) and truncated
fragments ending in a hyphen (`e-`, `aud-`), cut automatically. `candidates.py` also finds three
harder classes, each its own matcher:

- **Digression MARKERS** (`DIGRESSIONS`) - The author, 2 Sep 2026: "when I say 'you could potentially'
  it's often the digression, this needs to be cut." The marker is bounded filler, but the
  digression it opens runs to a truncation or the sentence end with no closing marker of its own,
  so the span is proposed, not enumerated, and `--check` exits 1 while uncovered.
- **`phrase_cuts()`** - whole phrases that announce a point instead of making it. The author, 2 Sep
  2026: "make sure we cut this off every time I say this." No single token is filler alone, so
  `FILLER_PHRASES` is GENERATED from independent subject/verb/leading-and/trailing-that slots (24
  members) rather than listed, and runs longest match first, before `opener_cuts`, or a shared
  "and" gets cut twice.
- **`opener_cuts()`** - The author, 2 Sep 2026: "you always forget to remove 'now' and 'so'." These are
  filler in ONE position only ("So I built it" opening a sentence vs. "it costs more, so I built
  it"), needing the capitalisation repair a mid-paragraph opener strips (66 of EC49's 226 sentences
  open with one, 29%). `so that` / `now that` keeps its opener, ZERO false positives in 300 tries.

Two classes of typo, and only one is safe to fix. Where the transcriber was wrong and the audio is
right, correcting the text makes them agree - a glued stutter (`th-them` -> `them`) and a mangled
product name, the house glossary in [`what-to-cut.md`](what-to-cut.md). Where the **speaker**
misspoke - "explain you how to export" - correcting the text disagrees with what is heard; leave
those unless the user asks. **In delete mode, removing a filler strands its comma** ("pre-edited,
uh, timeline" becomes "pre-edited, timeline"); ignore mode does not have this problem.

## The four things that will bite

**Pasting plain text does nothing.** Plain text has no `audioSegment`, so Descript treats it as
typed text with no media - the same fault the logs record as *typed text is deleted, never
ignored*. Only the reconstructed pasteboard edits the video. **`osascript -e` blows up on a real
payload**: a 1 MB payload is a 3 MB hex script and argv dies with `Argument list too long`. Pipe
the AppleScript through **stdin** (`osascript -`).

**Never map words onto the alignment with `difflib`.** This is the one that shipped a wrong edit. A
select-all gives one TAU per paragraph, and the copied token stream can differ from the export, so
global indices drift by one. Worse, when a sentence is spoken twelve times, `SequenceMatcher` cannot
tell the repetitions apart and pairs tokens with the **wrong take**, silently: identical token
count, plausible output, and the finished video keeps the take you meant to cut. It flipped all
five contested choices on this run, including reinstating the abandoned opener.

Map by **time** instead: each TAU's `offset`/`duration` claims the alignment words overlapping its
window, trimmed to the token count from whichever end overlaps least. The check that catches the
difflib bug is **word agreement**, not count: difflib scored 2013/2013 on count while pairing wrong
takes; the time-based mapper scores 2013/2013 on the words themselves.

**Paragraph breaks live in the text, never in the TAU boundaries.** 68 TAUs rendered 55 paragraphs.
Appending `"\n"` to every emitted TAU looks harmless and shreds the script: a TAU split merely to
drop a filler starts a new paragraph mid-sentence, and a per-TAU capitalise pass upper-cases the
continuation. Slice the separator out of the source text instead, and only capitalise a run whose
separator actually contains a newline.

**TAUs do not tile the media.** 68 TAUs left 36 gaps totalling 186.04s (`850.91 + 186.04 =
1036.95` exactly) - dead air between takes that a rebuilt payload drops for free, so runtime falls
further than the word count predicts: 56.8% of words here, 74% of runtime.

## Housekeeping the paste needs

- Mint a real `uuid4` for every new TAU.
- `copiedComponents[].tauAnchor.tauId` points at TAUs that no longer exist. Remap each one to the
  **segment that still holds its character position** - `reanchor()` in `recut2.py`. Pointing them
  all at `new[0]` keeps the video framing and silently destroys the structure (a 65-TAU take once
  piled 11 scene boundaries and a marker at the top). A blocked anchor slides to the next live TAU.
- Markers are `markerComponent` with a `text` field on the same `tauAnchor`: a section legend is
  `--markers markers.json`, `[{"phrase": "...", "text": "Why the move"}]`, matched against the
  **surviving** TAU text so a marker never lands on an ignored restart.
- Cutting a connector can strand a lowercase opener: capitalise the first TAU's first letter after
  cutting.
- Keep the pre-edit payload as the restore path, and warn the user not to copy anything else while
  the rebuilt payload is on the clipboard.

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
phrase straddling a TAU boundary is styled once per TAU, and every highlight id must be registered
in `highlighters` (alpha 64; `PALETTE` in `scripts/recut2.py` holds the thirteen valid ids).

A highlight is a **cue to the editor** that survives into the script they work from. The legend,
one colour to one instruction, in `CUES`:

| colour | means | who executes it |
|---|---|---|
| blue | B-ROLL - replace the picture with a full-frame clip | `motion-design`, full-frame register |
| purple | FIGURE - draw this as a diagram or an analogy | `motion-design`, figure register, transparent alpha layer |
| green | ON-SCREEN TEXT - caption or list keyed over the face | `motion-design`, caption register |
| orange | CTA - subscribe / like / book-a-call overlay | `motion-design`, YouTube CTA kit |
| coral | BRAND ASSET - product box, logo, shelf asset | Design Assets shelf |
| yellow | EMPHASIS - punch in, this line carries the point | editor |
| red | PROBLEM - needs a retake or a fix before publish | the speaker |

One paste can hand the editor a script already cut, de-filled, and marked up with where every
b-roll, diagram, caption and CTA goes: `scripts/styles.example.json`,
`[{"phrase": "...", "highlight": "blue", "bold": true}]`. **Verify a style before shipping it**:
read each attribute back and slice the TAU string with its own range - silently wrong, never an
error.

## Run it with `scripts/dscript.py`, not by hand

`grab` / `words` / `apply` / `check` / `history` / `restore`. It archives every payload it sees or
writes to `~/.descript-clip/history`, the only undo that survives the clipboard being overwritten -
and it will be, since the user keeps copying mid-run (Raycast's own history cannot stand in: its
store is encrypted and sqlite refuses it outright). `apply` refuses a clipboard that does not
round-trip, or that carries a style range past the end of its TAU - both faults are silent
otherwise, the paste simply lands wrong. Tell the user not to copy anything else between `apply`
and their paste; they will anyway, which is what `restore` is for.

## The cut list, and everything `apply` does unasked

**Write the cut list in words, never in indices**: indices written by hand are unauditable and
drift by one the moment an earlier needle changes. `scripts/resolve.py` turns a phrase into the
token range `apply` wants, prints five words of context on each side of every needle, and refuses
the whole list when a phrase matches nothing, matches twice with no `nth`, or overlaps another
needle - `"pre"` and `"post"` disambiguate a short needle by what sits beside it. `grab` works on a
**partial selection** too: the payload carries its own offsets.

Six things `apply` does without being asked: cuts as **Ignore**, **keeps every Ignore already in
the composition**, removes fillers and truncated fragments, repairs glued stutters and product
names (`--typos`, the house glossary in [`what-to-cut.md`](what-to-cut.md)), carries every scene
boundary and marker onto the TAU that still holds its text, and refuses to write the clipboard
unless the payload round-trips and every style range resolves inside its TAU. A second pass is
safe: an empty cut list is an exact no-op, `build_ignore([])` returning the source `plays` to the
millisecond.

## The order of operations, and it is not negotiable

Two write paths reach one composition and they do not compose. **The clipboard replaces the script
region from a payload built off an older grab; `pnpm descript layout` writes server-side.** So cut,
markers and pins go in first, as pastes, and every `layout` command runs after - reversed, the
paste silently discards every stamp. This is the whole reason the CLI's `edits` pass is preferred:
one commit has no order to get wrong.
