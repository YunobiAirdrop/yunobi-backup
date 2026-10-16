<img src="assets/banner.png" alt="ai-agency" width="100%">

# ai-agency

You get 26 agent skills with 6 slash commands and 1 agent for the 3 parts of an
agency that repeat each week: search, video production and client delivery. Another 2
tools keep a skills registry from rotting, because everything here has to
survive being added to.

Everything in it is the working version of something taught in **[AI Agency][skool]**,
a free Skool room where each classroom teaches 1 column of an agency. The course is
the mental model you read. The folder here is the same system your own Claude runs.

[**Join the room**][skool]. It is free, the 5 built classrooms are open, and the
commands below run their courses on your own business.

[skool]: https://go.upsys-consulting.com/skool

## Start here

Fork it. This repo is a base for your own kit. Add your skills under `skills/`, keep the 2 that ship with it, and they
keep the rest honest as the registry grows.

```
/plugin marketplace add heyramzi/ai-agency
/plugin install ai-agency@ai-agency
```

Or clone it and point Claude Code at the directory.

**Working through an agent with no terminal?** A single fetch answers what is here:

> Read https://raw.githubusercontent.com/heyramzi/ai-agency/main/index.json and tell me which skill fits.

[`index.json`](index.json) is generated beside the zips and carries every skill's
name, area and description with the raw URL of its `SKILL.md`, plus the 6
commands and the agent. No agent lists a directory over HTTP and guessing raw
URLs off a README table is where a run goes wrong, so they are written out. Point any
Claude at a `skill_md` URL and it runs that skill without installing anything.

**Not in a terminal?** Claude Cowork and claude.ai take 1 skill at a time as a
zip. You get every skill prebuilt as a zip in [`zips/`](zips): download the zip you
want, then go to Customize, Skills, the plus button, Create skill, Upload a
skill, and pick it. About a minute per skill, and it is the same skill either
way.

## A folder per role

Skills sit in `skills/<area>/<skill>/`, and the areas are the same 12 the
[AI Agency](https://go.upsys-consulting.com/skool) classroom is built from. An
area is 1 column of an agency, and the course named beside it teaches a person to run
that column, so the shelf you read and the folder you install out of say the same thing.

| Folder | The role it adds up to | Skills |
| --- | --- | --- |
| [`skills/search`](skills/search) | The SEO Copywriter | 4 |
| [`skills/video`](skills/video) | The Video Producer | 11 |
| [`skills/delivery`](skills/delivery) | The Project Manager | 8 |
| [`skills/design`](skills/design) | The Art Director | 1 |
| [`skills/content`](skills/content) | The Ghostwriter | 1 |
| [`skills/operations`](skills/operations) | The Chief of Staff | 1 |

The other 6 areas (strategy, demand, sales, engineering, finance and quality) are rows
on the classroom shelf with no public skills yet, and they get a folder the day 1 lands.

**A kit is a workflow.** The SEO kit is `skills/search` from start to finish, but the
YouTube kit crosses 3 areas. The thumbnail is art direction and the posts cut out of a video
are ghostwriting, so they file under `design` and `content` and still run in the video
order below. File each skill by whose job it is.

**A nested folder stays invisible until its path is listed.** `.claude-plugin/plugin.json` names each
skill path, and `./scripts/build-zips.sh` regenerates that list, so adding a skill to a
fork is 1 folder plus 1 run of the script.

## The SEO kit

4 skills that take a site from a blank keyword file to published pages
that rank, plus the read of the scoreboard afterwards. They are the ones behind
[The SEO Copywriter](https://go.upsys-consulting.com/skool), and they run in this order.

| Skill | Does |
| --- | --- |
| [programmatic-seo](skills/search/programmatic-seo) | ① The whole pipeline: what page to write next, keyword and prompt research, the draft, and the off-site mentions that decide whether an assistant names you. Serper scripts at each step |
| [seo-content-strategy](skills/search/seo-content-strategy) | ② That research to an ordered plan, pillars and clusters |
| [seo-schema-markup](skills/search/seo-schema-markup) | ③ JSON-LD on the page once it is written, and the rich results it buys |
| [search-console](skills/search/search-console) | ④ Real GSC data: pages stuck on page 2, dead click rates and pages competing with each other |

It was 14 skills until [`ca64ef2`](https://github.com/heyramzi/ai-agency/commit/ca64ef2)
retired the 10 that were never invoked and folded what they knew into `programmatic-seo`. A
skill that never fires is a skill the model picks between, and that is a cost with no return.

Once a skill is installed you do not summon it with a magic phrase. Describe the
job and Claude picks it up:

> Do keyword research for Mac dictation apps. Save it to a file.

> Look at that keyword file and tell me the first 10 articles to write, best intent first.

> Write the comparison page for us against VoiceInk. Here are my numbers.

`programmatic-seo` wants a key from
[serper.dev](https://serper.dev), free for 2,500 queries. `search-console` uses
your own Google account through `gcloud`, and reads only.

## The YouTube kit

13 skills that take a video from the first line of the hook to the posts cut out of
it afterwards. They are the ones behind [The Video
Producer](https://go.upsys-consulting.com/skool), and they run in this order.

| Skill | Does |
| --- | --- |
| [video-hooks](skills/video/video-hooks) | ① The opening. Variants by named mechanism, each rated for drop-off risk |
| [video-script](skills/video/video-script) | ② The body. 8 blocks, a beat budget, and 1 commercial ask at the end |
| [video-coach](skills/video/video-coach) | ③ The take reviewed against its plan, before a single cut, returning 1 habit to change |
| [descript-script-edit](skills/video/descript-script-edit) | ④ The cut happens in Descript's rich clipboard with a rewrite. You then measure the rhythm of that cut and place the shots against it |
| [youtube-thumbnail](skills/design/youtube-thumbnail) | ⑤ The frame, designed off a measurement you run yourself |
| [descript-projects](skills/video/descript-projects) | Footage into Descript, named and foldered so the media browser is the shot list |
| [dji-sync](skills/video/dji-sync) | The lav take waveform-matched to the camera clip and swapped in losslessly |
| [motion-design](skills/video/motion-design) · [youtube-ctas](skills/video/youtube-ctas) | Motion graphics cut against the read, and the transparent overlays an edit is dressed with |
| [whiteboard](skills/video/whiteboard) | Concept boards written as code and drawn onto the tablet live, on camera. Ships the engine and 1 worked board |
| [ai-video-prompting](skills/video/ai-video-prompting) | Prompts for Veo, Kling, Seedance and the rest, and when a model should not render a beat at all |
| [shorts-production](skills/video/shorts-production) | A finished Short taken to a scheduled task with its pillar code, and the rule that an export ships untouched |
| [generate-social](skills/content/generate-social) | The transcript turned back into LinkedIn and X posts |

Nothing in it is summoned with a magic phrase either. Describe the job:

> Write me 3 hooks for a video about why agency retainers stall. Rate each one.

> Here is the raw transcript of the take. Coach me before I cut it.

> Cut this Descript script. I copied it, it is on the clipboard.

> The cut is fine and it still feels long. Where does the frame sit still?

Of these, 3 need more than a terminal. `descript-script-edit` drives the macOS clipboard,
`motion-design` and `youtube-ctas` render through [Remotion](https://remotion.dev), and `whiteboard`
ships a small TypeScript project in [`skills/video/whiteboard/tool`](skills/video/whiteboard/tool),
which is the one thing here with an install step: `cd tool && pnpm install`. It is the exception to
the dependency-free rule below, because speaking Excalidraw's collaboration protocol means speaking
socket.io.

### The thumbnail, in more detail

[youtube-thumbnail](skills/design/youtube-thumbnail) treats a thumbnail as a
measurement problem before it treats it as a design problem.

Most thumbnail advice is a style opinion repeated until it sounded like a rule. The way
past that is banding: for each channel you learn from, build a winner band and a control
band from that same channel and period, so brand, photographer and budget are held
constant. **A trait present in both bands is house style.** Copy only the traits that
separate the bands.

Run it on a real niche and the usual advice starts falling over. A face tends to appear in
both bands, so its presence counts as house style and a close-up filling the frame often
marks a control. Somebody else's revenue is a control marker. Adjectives with no object are
control markers. A bounded promise in 2 to 4 words is the one reliable difference.

The skill carries the method from start to finish: how to build the bands, how to choose between the
face and faceless variants, 6 copy formulas with the ban list, and the composite rules
for rendering with an image model. [`scripts/render.mjs`](skills/design/youtube-thumbnail/scripts/render.mjs)
is a dependency-free renderer that takes your own photographs as reference images, so the
model composites around a real face you supply. Bring a Gemini API key, or
point it at a gateway.

It ships without an evidence file on purpose. The bands are yours to build, on your own
niche, and the skill is the method for building them. The whole kit is written that way:
each measured claim in it names what produced the number, and each one of them is worth
re-running on your own channel before you trust it.

## The ClickUp kit

Delivery on ClickUp runs on 2 free skills and 1 agent. They're the ones behind
[The Project Manager](https://go.upsys-consulting.com/skool), and they both talk to the
same `cu` command line.

| Skill | Does |
| --- | --- |
| [clickup](skills/delivery/clickup) | Every read and write: tasks, lists, docs, views, fields and time, bulk cleanup, and the browser path for templates, automations and dashboards |
| [board](skills/delivery/board) | A task specced into a brief, built in its own worktree, shipped through the merge gate, or just moved to a new status |

Planning the week in batches with points and a per-person cap, and turning a call into
tasks, come with [Agency Master](https://www.upsys-consulting.com/en/agency-master).

The agent on top is [project-manager](agents/delivery/project-manager.md). It reads the
board, names what is late, names what is waiting on a client, and proposes 1 move
per problem. It never presses the button itself.

> What is late on the delivery board, and what is waiting on a client?

> Write the brief for the oldest open task, then start it.

**These need the `cu` command line.** Its install line is handed out in The Project
Manager, lesson 2. The skills read as documentation without it, and run with it.

## The agent runs the courses

The Classroom shelf in [AI Agency](https://go.upsys-consulting.com/skool) is 13
cards with 1 per column of an agency plus Start Here, and 5 of them are built. All 5
are free, and each one ships a second copy of itself written for the agent.
The course is the mental model you read. The command is the same system as
instructions your own Claude can execute, so the reading and the building happen at once.

| Command | Course | Runs |
| --- | --- | --- |
| `/start-here` | Start Here | Scores your agency out of 12, then builds the intake from start to finish |
| `/clickup-foundations` | ClickUp Foundations | Your own ClickUp, from the 5 decisions to the template and the 3 automations |
| `/seo-engine` | The SEO Copywriter | Your rows, your keyword file, 1 page shape, then the console queue |
| `/marketing-department` | The Media Buyer | The 5 files, built on your own calls and your own numbers |
| `/youtube-engine` | The Video Producer | The 4 numbers off your own channel, from the runtime table to the ledger |
| `/the-project-manager` | The Project Manager | Your board, your capacity number, and the 4 gates the work passes |

Install the plugin and type the command. It runs a module a sitting, asks you the
decisions that are yours, stops at the checkpoint, and names the lesson you read next.
It runs beside the course and it will send you back to it.

Start Here opens the day you join. The other 4 sit on the room's level ladder and
open as you post and reply, which takes a few days of turning up.
The 8 unbuilt cards are locked above each rung anyone has reached, because an
empty course that opens is a worse promise than a padlock.

**No terminal?** Each command is a single markdown file. Paste this into any Claude and it
does the same thing:

> Read https://raw.githubusercontent.com/heyramzi/ai-agency/main/commands/seo-engine.md and run it with me.

None of them touch a live account without showing you first, none of them invent a number
you have not measured, and every one of them stops when the module ends.

## The 2 failure modes

Agent configuration rots in a specific way. It fails without noise. A broken skill
drops out of the offer list with no error. A duplicated name collapses to 1 side.
The skill below makes silent failures visible and repairs the parts with exactly
1 correct answer.

A registry decays in 2 directions at once, and 1 skill owns both, because
both are judged against the same quality floor. 2 files holding 1 standard
become 2 standards inside a quarter.

| Path | Direction | Cadence | Use when |
| --- | --- | --- | --- |
| [ai-architecture](skills/operations/ai-architecture) `new` / `heal` | Additive | Per session | A skill needs writing or its description fires on the wrong prompts, a session taught you something a file should have known, or a skill keeps repeating a mistake it already made |
| [ai-architecture](skills/operations/ai-architecture) `clean` | Subtractive | Scheduled | Duplicates and overlapping skills compete for the same task, a skill works some days and not others, skills are scattered across projects and home directories, or links are dead |

**It accumulates.** Each skill you add competes with the others for the same
triggers. Past a certain size the model picks between 4 skills that all look right,
and you cannot tell which skill it
picked. The clean path merges those down to 1 survivor each, behind a git
guard so a bad merge is 1 command to undo.

**It goes stale.** A file keeps giving an instruction that stopped being true,
and every session pays again for the same wrong turn. The heal path writes the
lesson into the file that should have known it, in the session that learned it,
and deletes what the lesson contradicts.

Run them on the same cadence and they fight: 1 pass adding caveats while
another removes them. Heal continuously, clean on a schedule, and let the clean
pass fold in what the heal passes accumulated.

## Layout

```
.claude-plugin/
  marketplace.json      this repo as a marketplace
  plugin.json           this repo as a plugin
commands/
  <course>.md           1 slash command per Skool course
agents/
  <area>/<agent>.md     1 folder per area, same 12 as the skills
skills/
  <area>/
    <skill-name>/
      SKILL.md          frontmatter and instructions
      references/       detail loaded only when needed
      scripts/          executables, committed, no install step
zips/
  <skill-name>.zip      1 zip per skill, for Cowork and claude.ai
assets/                 the banner above and the social card, generated
index.json              every skill, command and agent with its raw URL
```

`zips/`, `index.json` and the `skills` array in `plugin.json` are all generated. After changing
anything under `skills/`, run `./scripts/build-zips.sh` and commit what it writes. The
zip is flat inside, `<skill>/SKILL.md`. The area describes this repo, while the skill
stands alone.

A skill is self-contained, carries its own reference material, and ships a
dependency-free script so it works on a fresh clone. Node 20 or later, nothing
installed. `whiteboard` is the one exception and says so: its `tool/` wants
`pnpm install` once, because the collaboration protocol it speaks is socket.io.

## Checking your own fork

The tools run against this repo, and against each other. That is the intended
way to use them on your own:

```bash
node skills/operations/ai-architecture/scripts/heal.cjs check skills
python3 skills/operations/ai-architecture/scripts/review_skill.py skills
python3 skills/operations/ai-architecture/scripts/context_cost.py skills
```

They exit non-zero when something is wrong, so they drop into CI as-is.

## The classrooms and the room

The classrooms these skills came out of, the builds run in a real workspace 1 a
week, and the room where you can ask about your own setup:

**[go.upsys-consulting.com/skool][skool]**. The room is free, and each request is read by hand.
