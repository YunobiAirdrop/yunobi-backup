# Renaming a composition, and inserting markers

Two operations with no API, driven the way a cut is and guarded the way a cut is.

## Renaming a composition

There is no rename API - `prompt_project_agent` could do it, but on an empty credit balance the browser is the only route. `scripts/rename.py` does one composition end to end:

```bash
PAGE=$P python3 scripts/rename.py <project> <short> "<old name>" "<new name>"
```

Four things it encodes, each of which cost a repair to learn:

- **The title is its own DraftEditor**, separate from the script. `__ed` deliberately picks the editor with >500 characters, so the title never shows up in `__blocks()`. Find it by matching an `isContentEditable` leaf whose text is the current name.
- **Drag it right-to-left.** The same floating button that eats a cut's leading-whitespace anchor covers the title's left edge, so a left-to-right drag selects nothing.
- **A wrapped title needs `getClientRects()`, not `getBoundingClientRect()`.** The bounding box's vertical middle falls *between* the two lines, and a horizontal drag there grabs only the tail - one attempt selected just `Framework`. Drag from the end of the last line box to the start of the first.
- **Commit by blurring, never with Enter.** Enter typed at the title lands a paragraph in the **script**: it added a live space to an otherwise fully-ignored opening block, which rendered as a blank first line and cost 5 seconds on a 77-second short. Undo would not remove it - 12 clicks changed nothing. The repair was to select that whole opening block (reverse drag, guarded) and press Delete, which is the right tool anyway since the block was entirely unwanted. Click into the script to commit instead.

Guard the rename the same way you guard a cut: the selection must equal the old name before you type. A refusal is a free retry; a wrong selection renames over the wrong text.

## Markers and scenes

`help.descript.com` returns 403 to WebFetch. Read it through the browser you already have open instead - a second tab and `document.body.innerText` gets the whole article. `navigate` needs a good 10 seconds before the text is the new page's, so check `location.href` before trusting what you read.

`#` inserts a marker, `/` inserts a scene, `@` inserts a speaker label - all three are documented insert shortcuts. Both need a caret on an **empty line**, and getting one there is the whole difficulty:

- Typing `#` mid-paragraph inserts a literal `#` character into the transcript. It is text, not a marker.
- Clicking an empty line does not put a caret in it. Focus lands on the editor container, `getSelection().anchorNode` comes back null, and anything typed goes nowhere.
- `orca exec --command "type #"` types nothing at all - the command parser eats the `#`. Use `orca type --input "#" --page "$PAGE"`, which reports `"typed": true`.
- **`orca type` ignores `--page` and types into whichever tab is focused.** Mouse commands honour the page; keystrokes do not. On 2026-08-15 a `#` addressed at the marketing tab landed in the sales tab, splitting a paragraph mid-run and stalling the driver that was working there. Before any keystroke, `orca tab switch --page "$PAGE" --focus`, and never type while another lesson is being cut.

The sequence that does work: click the **last word** of the paragraph above (`__find` gives reliable coordinates for a word, never for the gap after it), `key End`, `key Enter`, then `orca type --input "#"`. That produces a real marker card - it shows as a `card-boundary` span in the DOM and, being unnamed, stays out of `export_transcript`. Naming it is unsolved: text typed straight afterwards lands nowhere at all. Solve the label before scripting a marker pass, and verify with `export_transcript(include_markers: true)`, which is the only honest read.
