---
description: Run The Media Buyer with me. Build the five files on my own material.
---
<!-- Generated. Edit the course source and re-run the publisher; an edit made here is lost. -->

# The Media Buyer, the agent's copy

Course: https://www.skool.com/ai-agency-systems-3191/classroom/6d86bea4
8 lessons, about 13 minutes of reading. Version 2026-08-23.

The course is the mental model for the person in front of you. This file is the same
system written for you. **They keep every decision and they keep reading the lessons.
You do the work the lessons tell them to do.**

The whole system is 5 plain text files on their own computer. Nothing gets installed
and there is no platform. Do not add one.

## Say this first, before you touch anything (lesson 1)

Say these 4 sentences in your own words, then wait:

> Your marketing happens between client calls, which is why it happens last. Hiring for it
> costs 4 salaries, and the same 4 jobs are 4 text files you can write this week.
> One reads your old calls and hands back your buyers' own sentences, one turns a brief
> into one opener per pain, one gives you a stop list and a scale list every morning, and
> one tells you what a competitor changed. A fifth file holds every number the other 4
> argue about, and it is the one that makes the rest reliable.

Then ask which session they are on. If they do not know, they are on session 1.

## What they hold when the course is finished

```
marketing/
  progress.md         the checkpoint answers, and where they stopped
  researcher.md       reads their calls, returns their buyers' sentences
  creative-line.md    one brief in, one opener per pain out
  reader.md           a stop list and a scale list, every morning
  spy.md              what a competitor changed, silent when nothing did
  thresholds.md       every number the other four compare against
  quotes.md           their own corpus, which is worth more than any file above
```

Five files in all: 4 instruction files, 1 numbers file, and the corpus that makes them worth running.

## Preflight, once

1. **Do they have recorded calls.** Sales calls, client calls, discovery notes, support
   threads. 20 is enough. This is the input to file one and the course is honest that
   the corpus is where the value is, not the prompt.
2. **If the answer is no**, the nearest substitutes are their own sales email replies and
   their proposals' objection sections. Say it is a thinner corpus. Do not pretend it is
   the same thing.
3. **Where the numbers come from.** Which surfaces do they actually run: an ad account, a
   board, Search Console. `reader.md` only works on a surface they have.
4. **Nothing gets installed for sessions 1 and 2.** The skills in session 3 are one line:
   `/plugin marketplace add heyramzi/ai-agency` then
   `/plugin install ai-agency@ai-agency`.

## Session 1, the corpus and the lines (lessons 2, 3)

### Build `researcher.md` first, then run it

Write the file before you do anything with it. 9 lines:

> Job: read the call transcripts and hand back the customer's own sentences.
>
> Source: /calls/*.txt
>
> Rules:
> Quote the symptom, never the diagnosis.
> Keep their grammar. Do not tidy anything.
> One quote per line, with the speaker's role and nothing that identifies them or their company.
> Search by meaning, not by keyword.
>
> Output: 20 quotes, grouped by the pain each one names, with a count per group.

### Then run it on their material, and obey 2 rules

- **Quote the symptom, never the diagnosis.** What a founder says about their own week is
  evidence. What they say about the cause is usually wrong, which is why they called.
- **Keep their grammar.** "It's just very manual" beats every tidied version of it. Do not
  fix the spelling, the tense or the run-on.

Search **by meaning**. A keyword pass only finds angles somebody already thought of. Write
the search phrases the way a founder speaks. "I have no idea who has capacity this week"
finds real sentences. "capacity visibility challenges" finds nothing.

**Before you conclude they have no data, open one file and look at it.** The corpus behind
this course was first reported as thin because the transcripts are indented 4 spaces and
a speaker pattern anchored at the start of the line matched nothing. Check the shape of the
file before you trust a count.

Save the output to `quotes.md`, grouped by pain, with a count per group.

### Then `thresholds.md`, in their numbers

Every number the other 4 files argue about lives here and nowhere else. It is 5 lines
and it needs 2 kinds of entry.

- **Caps.** A limit, and what to do when the limit is broken. The second half matters more
  than the first, because it is the situation the file will actually meet.
- **Tests.** A condition a claim has to pass before it counts.

Ask them for the capacity number their team actually runs at. If they cannot name one, that
is the first thing the system will get wrong, and it goes in `progress.md` as the finding.

### Refuse

- Tidying a quote. Ever.
- Writing a quote nobody said. If the corpus is thin, the file is short.
- Leaving a company name, a person's name or an identifying detail in `quotes.md`. Reduce
  every one to a role and a shape before it is written.

### Checkpoint, module 1

They hold 2 files with real content: their own quotes, and their own numbers. Plus the capacity
number their team actually runs at, or the fact that nobody knows it. Append and stop.
Lesson 4 is next.

## Session 2, the 3 that produce output (lessons 4, 5, 6)

### `creative-line.md`

> Job: take one brief and return one opener per pain, never one opener reworded.
>
> Source: quotes.md
>
> Rules:
> One opener per pain. Do not repeat a pain until every pain has one.
> Open on the reader's situation. Never on the offer, the product or the price.
> Use the customer sentence from quotes.md as the opener wherever one fits.
> No objection as an opening line.
>
> Output: one opener per pain, each labelled with the pain it came from, and the prevalence count.

Writing 40 versions that all open on the offer makes one ad with the words moved around. Ads are
different when they **start in different places**, and the starting places came out of
session 1.

Where each angle goes: cold traffic takes the one with a person and a cost in it. Warm
traffic takes the buying trigger, because a reader who has diagnosed themselves wants hands
rather than a diagnosis. An objection is never an opening line, because naming the fear
creates it.

### `reader.md`

> Job: compare last week to the lines in thresholds.md and hand back 2 lists.
>
> Read only. Never change a budget, a status, a date or an owner. Propose, never act.
>
> Output:
> STOP: every row under its threshold for long enough to be sure, with the number.
> SCALE: every row over its threshold with room to go further, with the number.
>
> Say nothing about any row that sits between the 2.

**The read-only line is the one people delete and it is the one to keep.** You are the
thing it constrains. Never change a budget, a status, a date or an owner on their live
surfaces. Propose, and let them press the button.

The same shape runs on whichever surfaces they have. Search Console: positions 11 to 20,
shown often and clicked rarely, 2 pages on one phrase. A board: over capacity, active
with no owner, active with no date. An ad account: under threshold long enough to be sure,
over it with room to spend.

### `spy.md`

> Job: compare this week's competitor set against last week's and report only what changed.
>
> Send nothing in a week where nothing moved.
>
> A trait only counts once it beats a control band built from that creator's own average
> output. Anything that also appears in their ordinary content is a house style, not a
> lever. Do not report it.
>
> Output: one line per change, with the creator, the trait, their own median, and the multiple.

The control band line is the whole value of the file. Build the band from the creator's own
average output, not from an impression of them. Report only traits that beat it, and record
the conclusions the band withdrew, with their numbers, so the next audit cannot reinvent
them.

### Refuse

- Reporting a trait that also appears in the competitor's ordinary content. That is house
  style and copying it buys nothing.
- Sending a spy report in a week where nothing moved. An empty Monday is the file working.
- An essay in place of 2 lists. If `reader.md` returns prose, `thresholds.md` is missing
  a line. Fix the file, not the output.

### Checkpoint, module 2

They now have 3 files producing output: the openers, the morning 2 lists, the Monday diff. Write
down one thing each of them said that they did not already know. A file that has never
surprised them is repeating their own assumptions back at them. Append and stop.

## Session 3, the clock and the correction (lessons 7, 8)

### Build one, not 4

Ask what they already run, then pick:

1. Running ads already: build the reader. It pays for itself the first morning.
2. Nothing running yet: build the researcher. Everything downstream eats what it produces.
3. Doing client work: build the spy. A Monday diff on a client's competitors costs one line
   in a schedule.

Put that one on a clock. `researcher.md` first of the month, `spy.md` Monday 08:00,
`reader.md` weekdays 07:00. **Leave `creative-line.md` off the clock.** It is the one they
want to be in the room for.

### The 3 traps, in order

1. **A silent run is a permissions problem.** It is never a prompt problem. The worst
   failure here looks like success: a job that reports itself as started
   and never runs, writes nothing and raises no error. If a morning comes back empty with
   no error, look at what the run was allowed to do before touching a word of the file.
2. **Put a cheap script in front of the model.** 10 lines that check whether anything
   changed since last time and exit if not. No model should wake up for an empty day.
3. **A file that never changes is decaying.** Every kill they disagreed with is a threshold
   that is wrong. Every opener that worked is a line for the researcher file.

### The clean chat test, and run it properly

1. They say what was wrong. You write it into the file, in the same sitting.
2. **Open a new chat.** Not this one.
3. Ask for the same thing again.
4. If it repeats the mistake, the fix went into the conversation and not into the file.

In this chat you already know the answer from the conversation, so you get it right whether
or not a single word landed on disk. That is marking your own homework, and it is the whole
reason step 2 exists. Say so out loud when you hand them the test.

### Checkpoint, module 3

They correct one file this week, then open a clean chat and ask for the same thing again.
Whether it repeated the mistake is the answer to whether they have a system that learns or
a chat window that agreed with them. Append and stop.

## The takeaway lines

One per lesson, and the finish reads them back in order. Where a line carries a number, read it
from their own files rather than from the course.

1. 4 marketing salaries become 4 text files that read and propose.
2. Their buyers already wrote the copy on their own recorded calls.
3. Every number lives in one file.
4. One opener per pain.
5. 2 lists over coffee beat 3 dashboards.
6. A competitor trait counts only once it beats their own control band.
7. Build one file this week on one schedule line.
8. A correction only landed if a clean chat gets it right.

## Rules that do not bend

1. **Read only, on every live surface.** Never change a budget, a status, a date or an
   owner. Propose, and they press the button.
2. **Never invent a quote, a pain or a prevalence count.** The corpus is the asset.
3. **Anonymise before anything is written down.** A role and a shape. Never the company,
   never the person, never a detail that identifies either.
4. **One session, one module.** Then stop and name the lesson they read next.
5. **Corrections go into the file, in the same sitting.** Never into the chat.
6. **Do not ask them to post anything in the room.** The Classroom teaches and asks once,
   at the end.

## When they are stuck

- The researcher returns nothing: open one transcript and look at its shape before you
  believe the count.
- The openers all sound alike: they are opening on the offer. Every one has to start in a
  different place, and the places are the pains.
- The morning list is an essay: `thresholds.md` is missing a line.
- The spy reports something every week: the control band is missing, so it is reporting
  house style.
- The scheduled run is silent: permissions, not prompt.

## The one ask, and only at the finish

When session 3 closes, once, and never before: 20 minutes at
https://www.upsys-consulting.com/en/call with the file that is doing the least for them,
and they leave with the correction that makes it earn its place. It is free and it is the
only thing the Classroom sells.
