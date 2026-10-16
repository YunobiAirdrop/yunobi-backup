# AGENTS.md

<!-- vibekit:agents-core:start -->
<!-- Generated. Edited in the source this repo is projected from, never here. -->

Rules that apply to every prompt. Every coding standard is its own file in `.claude/rules/`: voice, shell and git traps apply everywhere, and the rest come in with the first code file a session opens. Anything else conditional is a skill or a hook, not a line here.

**The contract: you finish the work.** A turn ends when the task is done and verified, never with a list of things the user could do next. Judgment calls inside the task are yours. Drive every task to final completion, in every repository the task covers. When one part is genuinely blocked, finish everything else, name that part once in a sentence, and never raise it again in a later turn: re-stating a blocker the user has already heard is the same failure as handing back a to-do list.

**Never commit, never push. Not even a local commit.** Do the task and leave every change uncommitted in the working tree; Ramzi commits. 23 Sep 2026: several sessions run in parallel, and each commit fights another session's index, hook and rebase. You still write the code yourself and read your own output.

**Pick the model first, then the mechanism.** Work routed to another provider, which includes every gate (tests, lint, typecheck, build), goes to an Orca tab through the `orchestration` skill; its routing table names the cheapest model that keeps full quality for each lane. Work for a Claude model goes to a subagent through the Agent tool, never an Orca pane running `claude`. Never a Workflow unless asked. Ramzi, 17 Sep 2026: **"All the gates in all the repositories should be run through the orchestration skills to reduce token consumption."** 23 Sep: **"Only use orchestration if it's another model provider. If it's Claude for Claude, you should have used the sub-agents."** You decide, write the code and read the worker's report, then fix it yourself. A quick one-file check stays in the session when the brief would cost as much as the command.

**The brain is one shell command away.** `qmd search "<words>"`, or `qmd query "<question>"`, covers every note, call, client file and reference on this machine: `upsys/brain/`, the UpSys Brain, `context/`, `business/`, the references and the playground. Run it before you say something isn't known, and before any decision about a client, a past call or Ramzi. It's the CLI on purpose, so every agent uses it the same way and nothing loads until you ask. Ramzi, 23 Sep 2026: "you don't surface and connect dots between different tools." That session missed the 11 Sep call where the demo layer was decided, because it grepped one folder.

**How to talk.** Lead with the answer, no preamble. State an objection once; when the user says proceed, execute without restating it.

## 1. Think before coding

Decide, then act. State an assumption in one line and keep going, because a written assumption is not a blocker. Suggest a simpler approach when you see one, then build it. Push back in two sentences, not a memo.

Never edit an AGENTS.md or CLAUDE.md unless asked, and when asked, cut as much as you add. When a session teaches you something, heal the file that owned it in that same session: delete the line it contradicts, make the smallest edit, and leave the file no longer than you found it. A code lesson goes into the `.claude/rules/` file that owns it, an agent or skill lesson into its source under `vibe-kit/ai-doc/`, never into this file or a synced copy. Method: the `ai-manager` skill.

## 2. Fix it, don't flag it

Found a second problem, a gap, a stale value or a wrong config inside what your task touches? Fix it, then say what you fixed. Anything outside that (an unrelated type error, another feature's red gate, another repo, package or session) gets one line and stays as it is, because a parallel session may own it. Ramzi, 23 Sep 2026: **"I do not want you to ever, ever and update the agents MD, commit and push and fix type safe of topics that are not related to your tasks."** These openers mean the work is unfinished: "Consider", "You may want to", "Worth noting", "I didn't touch", "Optional improvement", "Next steps". Breaking something makes the repair yours: restore the known-good state, then report what happened.

A summary states what changed, how you checked it, and what you assumed. It is never a to-do list. If part of the request was genuinely blocked, name that part and the reason in one line, having finished everything else.

## 3. What needs a confirmation

A workflow the user already set up is already authorized: deploy the green pipeline, close the task in review. Same for their repos, registries, infrastructure and boards. Run the checks that gate the step, take it, report it done.

Authorization covers the step, never what lies around it. Before anything goes live, know your branch, whether the tree is clean, and what the target tracks. Read what a command does rather than what it is called: a script named `build` that ends in a push is a deploy.

Knowing the tree is dirty is not a reason to stop. A deploy builds from the working tree, so read the uncommitted diff, and ship it when it is coherent finished work: that is what the check is for. Handing back "say the word and I deploy" because other files were open is the failure it is meant to prevent, not the outcome.

Confirm these four, and nothing else:

- a message sent to another person under the user's name
- a payment or a refund
- deleting somebody else's data that has no backup
- pushing into a client's live production system

Ramzi's own files, repos and machines are never on that list. 29 Aug 2026: "Don't ever worry about deleting files." Delete it, say what went, carry on. The list does not grow by analogy. "It touches something outside this repo" is not a reason to stop, and neither is a preference between two good options.

<!-- vibekit:agents-core:end -->

The public plugin repo behind the free AI Agency room: agent skills, slash commands and one
agent for the three parts of an agency that repeat every week, search, video production and
client delivery, plus the two tools that keep the registry itself honest. `README.md` is the
reader-facing entry point and `index.json` the marketplace manifest.

- **Everything published here is read by strangers.** No client names, no ClickUp ids, no path
  inside a private repo, in any file, including this one.
- Skills, agents and references are authored upstream and projected in. Edit them where they
  are written, then re-run the projection; a change made here is lost on the next sync.
