# Writing a new skill or agent

Read this when creating something from scratch. The quality bar for the file itself, including
the description contract, is `skill-floor.md`.

## Contents

- Step 1: Recover the run
- Step 2: Turn the run into reusable parts
- Step 3: Initialise
- Step 4: Write the parts, then the body
- Step 5: Package
- Writing an agent instead
- The four kinds, and how each fails

## Step 1: Recover the run

The skill is being written because something was done twice. Recover that run before asking any
questions: the conversation usually holds the tools used, the order, the corrections the user
made, and the input and output shapes that actually occurred. Extract from there first and put the
gaps to the user, rather than interviewing from zero.

What is still missing, asked a couple of questions at a time:

1. What should this let a session do that it currently does badly or slowly?
2. What would a user type when they need it? Ask for the casual phrasing, not the formal one.
3. What does the finished output look like, exactly?
4. What went wrong the first time it was done by hand?

Question 4 is the one that produces the useful content. The correction, the trap and the wasted
hour are what the base model does not know; the happy path it can usually infer.

Stop when the shape is clear enough to name the kind (Procedure, Judgment, Interface, Context).

## Step 2: Turn the run into reusable parts

Walk each concrete example and ask what would have to be rewritten from scratch next time.

- Code rewritten every run is a **script**. Rotating a PDF, rebuilding an index, validating a
  payload. Deterministic, token-free at read time, and a script an agent can drive takes flags and
  prints its own `--help` rather than prompting on stdin.
- A schema, a table of IDs, a long format spec, a vendor's real error codes: a **reference**.
  Loaded only when the condition in its pointer is met.
- Boilerplate that ends up inside the output, a template, a font, a starter directory: an
  **asset**. Never loaded into context.

If nothing comes out of this step, the skill is a body and a description, which is a normal and
good outcome. Directories created empty are dead weight.

## Step 3: Initialise

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

It writes the directory, a `SKILL.md` template with placeholders, and example files under
`scripts/`, `references/` and `assets/`. Delete every example file that the skill does not need.

## Step 4: Write the parts, then the body

Write the scripts, references and assets first. They decide what the body has to say, and a body
written first ends up describing work the reference already carries.

The body is written for another session, not for a person reading documentation. Imperative,
verb first. Give the reason behind a rule in the same sentence as the rule. Then load
`skill-floor.md` and read the file back against it.

## Step 5: Package

Only for a skill leaving this workspace.

```bash
scripts/package_skill.py <path/to/skill-folder> [./dist]
```

It validates frontmatter, naming, structure and file organisation, and writes a zip named after
the skill. Validation failure stops the package.

## Writing an agent instead

### Is it an agent at all

An agent is a persona spawned into its own context with its own tools and its own budget. Three
tests, and it has to pass all three.

1. **Fresh eyes are the point.** The value comes from a reader outside the parent thread's
   attention gravity: a reviewer of finished work, a researcher who reads a hundred files and
   returns four lines, a second opinion. If the parent could do the same work with the same
   context and get the same answer, the agent is overhead.
2. **The body is judgment, not a checklist.** Steps, gates and a fixed output shape are a skill.
   An agent that lists a procedure is a skill wearing a costume, and the registry already carries
   several.
3. **It is distinct from every other agent.** If two agents would write near-identical system
   prompts, they are one agent under the broader name.

The commonest correct answer is that the work is a skill. The second commonest is that it is a
skill the parent invokes, and the agent's only job is to be told to invoke it.

### The frontmatter is a budget

```yaml
---
name: thing-reviewer                        # equals the filename, lowercase and hyphens only
description: "..."                          # quoted; what it does and when to spawn it
skills: [refactor, diagnose]                # the only skills it can load; at least one
model: sonnet                               # sonnet by default, haiku for simple work, never opus
disallowedTools: Write, Edit, NotebookEdit  # a reviewer that cannot edit
maxTurns: 30                                # a ceiling, so a bad run ends instead of grinding
effort: high                                # only where depth is the whole deliverable
---
```

The tool line is the strongest in the file. An agent that reviews should not be able to edit, and
saying so in the frontmatter is worth more than a paragraph asking it not to.

**Reach for `disallowedTools` rather than a `tools` allowlist.** An allowlist replaces the
inherited pool, so it silently drops every MCP tool and every skill the agent already leaned on,
and the failure appears as an agent that quietly stops doing half its job. A denylist removes
exactly the capability that has to go and leaves the rest. Write a `tools` allowlist only for an
agent built around a named handful of tools from the start. Two entries need care either way: an
allowlist with nothing that resolves refuses to launch, and `Skill` belongs in the `skills` field
rather than in `tools`.

**`skills:` is the agent's whole library.** A subagent inherits none of the parent's skills, and
each one listed is preloaded whole, so name every skill the body sends it to and nothing more.
Budgets that held across the 75 agents here: 30 turns for a read-only reviewer, 40 for a builder, 50 for a coordinator running a multi-step pipeline. `effort`
is left inherited unless depth is the deliverable, which came to six agents out of 75.

`claude plugin validate <dir>` parses a whole directory of agents and names any frontmatter that
does not load. Point it at the real path: it does not follow symlinks, so a projected
`.claude/agents` reports every entry as unread.

### The body

**An input contract, named as one.** What the parent passes, what is required, and what the agent
does when a required input is missing. An agent that guesses at a missing input returns confident
fiction.

**A stated turn ceiling and what to do about it.** A ceiling ends a run without warning, and a run
that ends before it wrote its output has returned nothing. Say so, and say when to stop reading and
start writing:

> A hard turn ceiling ends the run without warning. Treat reading as an allowance: take the
> contract, the captures and the primary files first, sample rather than walking the tree, and by
> roughly the tenth turn stop reading and write. Name whatever went unread in one line above the
> output.

**The output shape, exactly.** The parent parses this. Name the sections, name the order, and say
what an empty result looks like.

**What it must not do.** A reviewer edits nothing. A producer does not redesign. An applier owns
source edits and nothing else. One line each, at the top, because these are the failures that cost
a whole run.

### Every agent needs a degraded path

Subagents are not always available or permitted. The skill that spawns the agent says what to do
when it cannot: run the same passes inline, in a stated order, in the parent thread. Impeccable
keeps a mirror of every agent under `reference/degraded/` for exactly this, and its inline
instruction reads "when a sub-agent tool is available and permitted, run these independently;
otherwise run them yourself in this order".

An agent with no degraded path is a skill that silently does nothing on half the machines it
reaches.

### Placement

Naming and file rules are in `contract.md`. Eight agents per area is the ceiling. After adding,
renaming or deleting one, run `ai-doc/scripts/check-agent-readme.py --fix`, then
`node scripts/validate-architecture.mjs`.

## The four kinds, and how each fails

The kind names what the reader of the finished file is doing when they open it. It decides what
the body should contain, and each kind fails differently.

- **Procedure.** A workflow with steps that must happen in order and that can go wrong halfway:
  shipping a release, taking a board task through review, running a migration. The deliverable is
  the sequence, the gates between steps, and the recovery when one fails. Its failure mode is a
  step that quietly does the wrong thing.
- **Judgment.** A craft the model can already attempt and does badly by default: voice, layout,
  copy, hooks, thumbnails. The deliverable is a quality floor and a list of refusals, not steps.
  Its failure mode is a checklist that describes good work without producing any.
- **Interface.** A tool, API or CLI whose behavior cannot be guessed: an auth split, a base URL
  that silently rejects, a boolean that means the opposite of its name. The deliverable is exact
  invocations and the traps. Its failure mode is a copy of the vendor's documentation.
- **Context.** Facts about this workspace that no model can hold: object IDs, entity names, the
  decisions behind a product. The deliverable is the values and where they live. Its failure mode
  is going stale without anyone noticing.

Pick the kind from what the reader needs, not from the topic. A skill that names a CLI can still
be Judgment if the hard part is deciding what to run.

The short form is in `SKILL.md`.
