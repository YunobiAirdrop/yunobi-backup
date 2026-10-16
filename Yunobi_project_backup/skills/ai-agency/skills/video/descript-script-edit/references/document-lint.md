# The document lint, and the day a finished edit locked

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling. The gate itself,
the command and the three invariants stay in the skill.

**One dangling id makes the whole project unopenable.** Not one bad card - Descript refuses the
entire document and the editor shows *"Oh no! Something's not working"* with no route back in, so
the repair cannot be done from the app either. On EC49, 2026-08-31, three of them locked the owner out
of a finished 23:57 edit: two `compositions>N>timeline>pins>components>M>sceneId` left pointing at
pin tracks a restore had moved past, and one `roomtoneRefId` on a CTA media ref registered without
its companion.

**Three invariants, and any one of them refuses the whole document:**

1. every `*Id` resolves to an object that exists;
2. every pin a card layer draws is **registered** in that composition's `timeline.pins.components` -
   sitting in the top-level `pinScenes` list is not enough, and "pinTrack" in the client's error
   text means the registration, not the scene;
3. both the cards track and the pins track are in **script order** - appending a component is never
   enough, it has to be sorted in.

**A count is not a validation, and this is the lesson that cost the most.** Cards 122, markers 48,
pin scenes 71, words 6981 - every number matched the known-good state exactly, and the document
would not load. Counting proves nothing was deleted. It says nothing about whether what remains
still refers to things that exist, in the form the client recognises. A first linter that checked
only invariant 1 passed a document that was still refused for 46 unregistered pins, so it bought
one more round trip and nothing else.

**The gate is wired into `commit()` in `CLIs/descript/client.ts`, not just documented here.**
`danglingReferences()` runs on the way out of every write this CLI makes and throws before the push,
so an invalid document cannot leave the machine whoever is driving. `scripts/lint_document.py` is
the same three checks against a `doc.json` on disk. Both were proven on the exact document that
locked EC49 away: 47 faults caught, 0 on the repair.

The console is the other half of the evidence. `DocumentInvalidError` names the exact JSON path of
every dangling reference, so a locked-out project is a five-minute fix rather than a restore - ask
for the browser console before reaching for a snapshot.
