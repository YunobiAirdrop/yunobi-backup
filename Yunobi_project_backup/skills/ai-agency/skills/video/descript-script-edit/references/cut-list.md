## Build the cut list from the live DOM, not the export

Law 5 says the two disagree. Dump the blocks once, with their indices, and write the needles against *that* text - every needle then resolves first time, and the index gives you the block scope for free. Dry-run the whole list through `__find` before any drag: 30 of 30 resolving on screen is the signal to start.

**A needle must lie inside ONE contiguous run of live text.** `__find` matches against
`__map(block).text`, which interleaves the ignored words with the live ones, so a needle written
against the live-only text of a block stops resolving the moment a previous edit left struck
words in the middle of it. Measured 2026-08-19: 16 of 57 needles reported not-found on the dry
run for exactly this reason, every one of them on a block that had already been half cut. Dump the
runs, not the text:

```js
// per block, the text split into [{ig:false,t:"..."},{ig:true,t:"..."},...]
var w = document.createTreeWalker(b, NodeFilter.SHOW_TEXT), runs = [], n;
while ((n = w.nextNode())) {
  var ig = window.__ignored(n);
  if (runs.length && runs[runs.length-1].ig === ig) runs[runs.length-1].t += n.data;
  else runs.push({ig: ig, t: n.data});
}
```

Write the cut as a span in live coordinates, then emit **one needle per live run it crosses**. A
span that covers three live runs is three needles and three drags, which is correct: the ignored
text between them is already out of the video.

**Start every needle at a word boundary.** Ignore works on whole words, so a needle that opens mid-token - typically on the comma in `, and you probably have...` - snaps left and swallows the word before it. That is how `adapt this to your own agency` came out as `adapt this to your own` on 2026-08-15. Begin the needle at the space instead: ` and you probably have...`. The selection guard cannot catch this, because the selection Descript reports is the one you asked for.

**Not when the space next to it is already ignored.** `__find` refuses a match whose first character
sits in struck-through text, so a needle opened on the space after an ignored duplicate take reports
not-found forever. That rule is for live text on both sides; against an ignored run, open at the word
and carry the trailing space instead.

**A lost space is repairable, and Ignore is the only edit here that is.** When two live runs end
up adjacent with the space between them inside the ignored region, the transcript reads
`views.The best part`. Select the ignored span that holds the space, restore it, then re-ignore the
span **without** its leading space:

```
[data-testid="selection-toolbar-restore-ignored-button"]   // and -delete-ignored-button
```

That toolbar mounts on a drag over struck-through text, the same way the Ignore toolbar mounts over
live text, and `__find` will not locate the span for you because it refuses ignored matches - build
the range from `__map(block)` directly and guard the click on `getSelection()` exactly as law 6
requires. Used on 2026-08-19 to put back the space in `right views. The best part`.

**Carry at most one of the two boundary spaces, never both.** A needle written as `" the most And, and most importantly, "` took the space on each side with it, and the surviving words stitched together as `importantly,we're`. The guard has no opinion on the seam - it only checks that the selection matches what you asked for. So does the duration. Only reading the exported transcript catches it, which is why that read is not optional.
