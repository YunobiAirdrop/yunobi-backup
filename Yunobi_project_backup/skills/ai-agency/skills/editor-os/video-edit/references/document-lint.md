# The document lint, the schemas, and the day a finished edit locked

Read this when a project refuses to open, and before writing anything that touches pins or cards.

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

**The gate is wired into `commit()` in `CLIs/descript/history.ts`, not just documented here.**
`inspectDocument()`, from `CLIs/descript/gate.ts`, runs on the way out of every write this CLI
makes and throws before the push, so an invalid document cannot leave the machine whoever is
driving. `pnpm descript lint <project>` runs the same three checks without writing. Both were proven on the exact document that
locked EC49 away: 47 faults caught, 0 on the repair.

The console is the other half of the evidence. `DocumentInvalidError` names the exact JSON path of
every dangling reference, so a locked-out project is a five-minute fix rather than a restore - ask
for the browser console before reaching for a snapshot.

## Five things that broke, and the invariants that now hold

Every one of these is a gate in `inspectDocument`, which `commit()` runs. **Linting beats prose:**
if you learn a new invariant, add it there with a test rather than a warning in a markdown file.

1. **`DocumentInvalidError: Components are in incorrect order` is about ORDER, not duplicate
   slots.** Diagnosing it as duplicates and blocking on them refuses Descript's own data: a
   "Copy of" composition has sixteen cards all at `sortTiebreaker: 0`. Measured on two
   app-authored documents (91 cards + 105 pins, and 102 + 23): in every track, array order agrees
   with `sortTiebreaker` order and with script order. The value is arbitrary; only the order
   blocks.
2. **A pin's `sortTiebreaker` is derived from a card index (`index + 0.5`).** Cutting a card
   shifts every later card and invalidates every pin after it. `realign()` renumbers cards in
   reading order and re-derives every pin, at the end of every write touching either track. This
   is why one clip out of nine survived a lost pass: the survivor cut no card.
3. **A text layer names its font.** `applyLayout` remapped every pin's media and never
   `textProperties.fontMediaRefId`, so stamping a text layout carried the pack's id across and
   the editor died on load. The font is usually already in the project - the pack names it by
   **asset key** and the project holds the same asset under a mediaRef id of its own, so
   `rehomeFonts()` matches on `assetKey` and imports nothing.
4. **`fontMediaRefId` was missing from `REFERENCE_FIELDS`**, which is why the gate passed the
   document that crashed the editor. **When a `DocumentInvalidError` names a JSON path, put the
   last segment of that path on that list before fixing anything else.**
5. **Test a candidate invariant against a document the app AUTHORED before blocking on it.** Two
   rules were falsified in one command each: "duplicate tiebreakers are the fault" (the Copy-of
   composition has sixteen) and "a pin must sit inside its card's gap" (a healthy document
   violates it 105 times out of 105).

**Reading a document back is not verification.** The API returned eight placed clips correctly,
twice, and the editor discarded all of them the moment it opened. Two whole passes of work were
lost that way. Prove it draws instead:

```bash
pnpm descript verify <project> --expect "the words the edit put on screen"
```

## Two `merge` traps on a re-seed

`merge()` decides what a re-seed may change on a library entry it already holds.

- It could enrich a **name** and nothing else, so adding a new field to `Template` left all 100
  held entries without one: a re-seed reported "renamed: 0, library: 100" and changed nothing.
  **Any new field needs its own line in the keep branch.**
- `named()` only asked whether the string had a slash, so a generated `Text/c5d195ba` counted as
  a real name and the published name could never take. A pack card is unnamed in the pack's
  **document** and named in its published **template**, so `layout seed` passes the
  `cardId -> Group/Name` map from `layouts(pack)` into `seedPack`.

## The files one stage hands the next

Agents only choose. A script makes every change to a project, and every file an agent or a script
hands to the next stage is checked against one schema on the write and again on every read.
So the same approved plan always replays the same edit. A bad file stops the stage that reads it,
naming the file, the field and what was expected (`pins.json: [3].media must be a string`), and
it never gets cast, guessed or skipped.

| File | Written by | Read by | Schema |
|---|---|---|---|
| `RUN.json` | `run.py` (the studio sets only `route`) | `run.py`, studio `shelf.ts`, `project.ts` | `schemas/run.schema.json` |
| `passes.json` | by hand, it's the pass order | `run.py`, studio `shelf.ts` | `schemas/passes.schema.json` |
| `pins.json` | `sequence.py plan`, then an agent picks media and fills `FILL ME` | `pins.py`, `dscript.py`, `arrange.py`, `visuals.py --plan`, studio `projectPlan` | `schemas/pins.schema.json` |
| `*.phrases.json` | `sequence.py plan` (the jump cuts), an agent | `resolve.py` | `schemas/phrases.schema.json` |
| `needles.json` | an agent (the cut list as words) | `candidates.py`, `restate.py`, `prove_cuts.py` | `schemas/needles.schema.json` |
| `briefs.json` | an agent, off `visuals.py brief` | `visuals.py check` | `schemas/briefs.schema.json` |
| `cut.json` | the local cut builder | studio `planEdit` | `schemas/cut.schema.json` |
| `plan.json` | the planner (read only for the studio; motion draft props) | the studio | `schemas/plan.schema.json` |
| `plan.notes.json` | the studio, `studio notes --done` | the studio | `schemas/plan-notes.schema.json` |

2 validators read the same schema files and print the same message: `scripts/schema.py` for the
Python scripts, which exit 2 on a bad file, and the studio's `schema.ts`, which answers 400.
Check one file by hand with `python3 scripts/schema.py pins path/to/pins.json`.

Both know only the keywords the schemas use: `type`, `required`, `properties`,
`additionalProperties`, `items`, `prefixItems`, `minItems`, `maxItems`, `enum`, `const`, `pattern`,
`minimum`, `minLength` and `anyOf`. A schema with any other keyword is refused, so a rule can't
look enforced while nothing checks it. Add the keyword to both validators first.

A few rules JSON Schema can't say live in code, next to the read:

- `plan.json`: a slot id names one slot (`plan.ts` `oneSlotPerId`).
- A `cell` pick needs `pick.props` the template takes. The studio reads the template list from
  the motion kit's `scripts/templates.mjs` and won't queue a draft `fill` would refuse; the slot shows
  why instead.
- `run.py done` needs a checkable proof: `--file` (a saved output that exists) or `--run` (run
  here, exit 0, output kept under `proof/`). The ledger records the file and its sha256.
