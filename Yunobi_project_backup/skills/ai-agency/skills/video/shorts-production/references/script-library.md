# The script library

Extracted from `SKILL.md` on 2026-08-13 to bring that file back under the 250-line limit.
This is the Apple Notes side of production: how the folders are contracted, how a batch is
triaged against ClickUp, and what shape a note has to be in.

## Triage the script library

Apple Notes is the script store; ClickUp is the production record. They drift, because a Short can
be shot without anyone opening the note. Re-triage whenever a batch is recorded.

**Folder contract.** Everything lives under one parent folder, `Shorts`. Inside it, the `Batch N`
folders hold written scripts waiting to be shot, `Unscripted pool` holds ideas with a title and no
script, so they are **not batchable** and must be left out of any rebalance, `Shot` holds anything
recorded whether or not it has published yet, and `Archive` holds the dead. There is no `Done`
folder: `Shot` is the recorded folder, so read the live folder list before writing rather than
trusting a name from this file.

**The batch numbers roll, they are not a fixed set of three.** When a batch is recorded, its folder
empties and a new one is created at the far end, so the live set walks 1/2/3 to 2/3/4 and on. Read
which folders exist and which are empty before planning; the lowest-numbered non-empty folder is the
one being recorded now. Leave the emptied folder in place rather than deleting it.

**Step 1, find what is already recorded.** Cross-reference the codes in note titles against the
video posts that actually exist (Buffer, on both orgs, plus the ClickUp Socials list; TryPost was
retired on 13 Aug 2026 and holds nothing live). Anything with a scheduled or published post is recorded and moves to `Shot`.
Do not trust the date in a note title: those are planned dates and they go stale immediately.

**Step 2, expect scripts that do not exist, and do not read anything into it.** The speaker
improvises to camera and says so plainly:
 "sometimes there is no script I improvise, it's totally normal" (20 Aug
2026). It is the normal mode, not an exception. On 2 Aug four of eight recorded Shorts had no note
(`M10`, `L07`, `M07`, the GSC `S01`); by 20 Aug it was 20 of 40 coded tasks. That is not a missing
file to hunt for and **it is not a kill signal** — see the warning in `social-scheduling`, which only
fires for a note you watched disappear. The ClickUp task is the record. Write
`Script: none in Apple Notes (improvised to camera)` on the task and move on; never ask anybody to
account for a note that never existed, and never invent one.

**Step 3, rebalance the batches by pillar, moving as few notes as possible.** A recording session
should yield a varied publishing week, so aim for one of each pillar per batch rather than equal
totals. **Every move bumps the note's modification date and Notes sorts by it, so a full reshuffle
destroys the existing ordering.** Compute the target assignment first, then emit only the notes whose
batch actually changes. On 2 Aug that was 12 moves out of 23 for a clean A:2 C:2 L:2 M:1 P:1 split
across three batches.

**Moves need the full Core Data id and the store UUID:**

```bash
S=$(python3 -c "import sqlite3,shutil,tempfile,pathlib;\
src=pathlib.Path.home()/'Library/Group Containers/group.com.apple.notes/NoteStore.sqlite';\
t=pathlib.Path(tempfile.mkdtemp());[shutil.copy(str(src)+e,t) for e in ('','-wal','-shm')];\
print(sqlite3.connect(t/'NoteStore.sqlite').execute('select z_uuid from Z_METADATA').fetchone()[0])")
osascript -e "tell application \"Notes\" to move note id \"x-coredata://$S/ICNote/p2681\" to folder \"Batch 1\""
```

`notes.py` has no move command, so this is raw AppleScript. **Never move by walking a folder**, and
do not verify with `container of note id`: it returns -1728 after a move even though the move
succeeded, and sometimes on notes that were never touched. Verify with folder counts plus a
`list --folder` read instead.

**Step 3b, a note that moves batch drags two lines in ClickUp with it.** Every coded task's
description opens with `Scheduled: <date>` and `Script: Apple Notes > … > Batch N > CODE`. Neither is
maintained by anything, so both are stale on almost every task, and the path in them still names
folder trees that no longer exist. Rewrite both lines on every task whose note moved or whose date
changed, and normalise the path to the real tree, `Apple Notes > Shorts > Batch N > CODE`.

**Step 3c, decide which way the calendar and the batches point, and say so.** They drift apart, and
the two repairs are opposite: either sort the scripts into batches by their existing publish dates,
or keep the batches as they are and re-flow the publish dates to follow the recording order. The
second is usually right once the calendar is already slipping, but it moves work by weeks, so it is
the owner's call and not a default.
 Whichever way it goes, publish dates land only on Monday, Tuesday,
Thursday or Friday, and slots already held by recorded or in-progress material are not reused.

**Step 4, report the collisions rather than fixing them silently.** Two live examples: `S01` is used
by both the recorded GSC short and the unrecorded "The Make word that decides your bill", and the
second-brain topic has two leftover idea fragments in a batch even though `M05` is already shot.
Re-coding or killing those is the owner's call.

## The note shape: written at the ends, bullets in the middle

Every script note runs `INTRO`, `MEAT`, `OUTRO` with timings on each. **The MEAT is bullets and
never full prose.** The speaker reads the first and last lines as written and says the middle their own way,
so a scripted middle is read out rather than spoken and it flattens the register `voice-dna`
measures. Bullets keep the beats and let the sentences happen on camera.

The two ends are written out for a reason and each has its own: the opening carries the conditional
that qualifies the audience and the one cited number, and the closing line is usually shared word for
word with the pinned post and the first DM, so rewording it on camera breaks the surfaces that were
deliberately saying one thing.

Under the timings, a note also carries the one-line metadata row, `Lives at:`, the word count against
the target pace, the tags, and a `RE-CHECK BEFORE SHOOTING` block holding whatever would go wrong if
it were said differently. Read the newest note in the live batch before writing a new one, because
that block is where corrections accumulate.

