# The clock a clip is cut against

A b-roll clip's length is the span between two phrases in the cut. Getting that span from a
subtitle export is how the Glance set ended up timed **203.8 seconds wrong**: a cut took the
composition from 2038.3s to 1834.5s, and the plan written afterwards still carried the old clock.
Nothing failed. Twelve clips were designed against timings out by up to 196 seconds, and the error
surfaced only because somebody re-derived them from the document.

## Derive it

```bash
pnpm descript doc <project> --out doc.json
python3 scripts/beatclock.py doc.json                      # every surviving tau, with its start
python3 scripts/beatclock.py doc.json --find "a phrase"    # the taus holding it
python3 scripts/beatclock.py doc.json --beat "first words" "last words"   # start, end, duration
```

It walks the composition's superTau, skips every blocked tau — an Ignore draws no time — and
returns the cumulative play clock. **Its total equals what `get_project` reports as the composition
duration**, and that equality is the check that says this clock is the render's clock. Print it once
before writing a single timing.

A position inside a tau is interpolated across the tau's characters, which is the same
approximation the subtitle export makes and is exact enough: a `tauAnchor` is `{tauId, location}`
where `location` is a character offset, so a pin already starts mid-tau.

## What it shows that an export does not

**A beat is its own sentence.** Several Glance beats had been timed past the line they serve — one
ran to 37s when its sentence ends at 27.8, another held 27 seconds for a 2.6-second line — because
the pre-cut script had material after them that nobody was timing against. Measure each beat from
its first word to its last, then decide whether it has the runtime for the design.

**A beat's neighbours are a constraint, not context.** Two beats 2.6 seconds apart cannot both be
clips: `motion-design/planning.md` calls that a montage, and the read underneath goes unheard. So the
GAP between measured spans decides the plan as much as the spans do. In the Glance cut that turned
two planned beats into one clip and demoted a third to face, and it is invisible from a list of
in-points.

**A cut is not a uniform shift.** The Glance drift was 0.85s at the start, 6s at 2:30 and 196s at
29:00. A plan "adjusted by the difference in total duration" is wrong everywhere except the end.

## When to re-run it

After any cut, any reorder, any paste. The composition autosaves, so the document is current within
seconds of the editor. A clip already rendered against an old clock does not need rebuilding unless
its DURATION changed — only its placement moves — but check both, because a shortened beat whose
component was choreographed for the old length silently loses its last movement. That happened to
the Glance payoff beat: its resolve sat at frame 344 of a 318-frame clip, so the movement the whole
beat existed for never played.

## Why the derived clock is the only true one

Moved out of SKILL.md on 31 Aug 2026 to hold it under the 250-line ceiling.

The play clock, derived: superTau walked, blocked taus skipped, each duration divided by its
`speed` because `duration` is source time - ES02 is 476.83s undivided and 454.54s divided, and
454.54 is the truth. Reading a beat off an SRT is how one video's clips were timed 203.8s wrong.
**Read [`references/the-clock.md`](the-clock.md) before writing a timing.**
