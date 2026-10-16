#!/usr/bin/env python3
"""The edit's run ledger: which of the passes are done, and what proved each one.

The passes, in order, are `../schemas/passes.json`, and RUN.json is checked against
`../schemas/run.schema.json` on every read and write. A bad ledger exits 2 naming the field.

WHY THIS EXISTS: the passes are timed against each other, so a pass done out of order is
work thrown away - motion built before layouts is motion built for a frame about to change. Held
only in a session's head, the order survives until the first interruption. The author, 8 Sep 2026:
"make sure the agent orchestration is state of the art and methodical and sequential by doing
things in steps otherwise we will lose track."

WHY EVIDENCE IS MANDATORY: a tool reporting success is not evidence. Every `done` names one of
the pass's commands as a whole phrase AND hands over something checkable: `--file` is that
command's saved output, which has to exist and not be empty, or `--run` runs the command here,
refuses a non-zero exit, and keeps the output under `proof/`. Either way the ledger records the
file and its sha256. Matching a bare word was the old gate, and "the shortcut is fine" proved
`descript cut`. That is what stops "layouts applied" meaning "layout apply exited 0".

WHY IT REFUSES OUT OF ORDER: `start` on pass N with N-1 not done is the mistake, not a warning.
Override with --anyway, which is recorded in the ledger as an override and shows in the table.

WHY THE BOARD MIRRORS IT: the author, 7 Sep 2026: "create a todo. always do that on a descript
production." `board` writes the same rows as a ClickUp checklist on the video's task, one
item per pass with its state in the text, and every later `start`/`done`/`block` rewrites it. The
ledger on disk is the record; the checklist is the view he opens.

    run.py init <dir> --code EC51 --project <id> --comp <id>
    run.py init <dir> --code EC51 --route local --cut <path/to/cut.json>
    run.py show <dir>                       # the table, and rewrite RUN.md
    run.py next <dir>                       # the one pass to do now
    run.py start <dir> 3
    run.py done <dir> 3 --evidence "layout cards: 47/47 stamped" --file cards.txt
    run.py done <dir> 0 --evidence "descript tracks clean" --run "pnpm descript tracks <id>"
    run.py block <dir> 7 --why "publish dies at 57s on a CLI-stamped composition"
    run.py board <dir> --task 86cb8wak7     # mirror the table to the task's checklist, and keep it so
"""
import json, os, re, subprocess, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import schema

# The order and its gate live in `../schemas/passes.json`, the one home the studio reads too.
# Each row is (key, what it proves, the commands whose output proves it).
PASSES = [(p["key"], p["proves"], p["commands"]) for p in schema.passes()]

STATE_WORD = {"done": "DONE", "started": "IN PROGRESS", "blocked": "BLOCKED", "": "OPEN"}


ROUTES = ("descript", "local")


def sync_board(run):
    """Rewrite the task's checklist from the ledger. Delete-and-recreate: `cu` returns no item ids."""
    task = run.get("task")
    if not task:
        return
    if run.get("checklist"):
        subprocess.run(["cu", "task", "checklist", "delete", run["checklist"], "--yes"],
                       capture_output=True, text=True)
    items = []
    for i, (name, what, _) in enumerate(PASSES):
        s = run["passes"][i]
        ev = f" ({s['evidence']})" if s.get("evidence") else ""
        items.append(f"{STATE_WORD.get(s['state'], 'OPEN')} · {i} {name} - {what}{ev}")
    out = subprocess.run(["cu", "task", "checklist", "create", task, "--name",
                          f"Edit - the {len(PASSES)} passes ({run['code']})", "--items-json", json.dumps(items)],
                         capture_output=True, text=True)
    for line in out.stdout.splitlines():
        if line.startswith("checklistId:"):
            run["checklist"] = line.split(":", 1)[1].strip()
    if out.returncode != 0:
        print(f"board: cu refused: {out.stderr.strip() or out.stdout.strip()}", file=sys.stderr)


def path(d):
    return os.path.join(d, "RUN.json")


def load(d):
    p = path(d)
    if not os.path.exists(p):
        sys.exit(f"no ledger at {p} - run `run.py init {d}` first")
    run = schema.load(p, "run")
    # WHY: every ledger written before 9 Sep 2026 is a Descript one. See the studio spec.
    run.setdefault("route", "descript")
    # A ledger written when there were fewer passes gets the new ones as open rows.
    run["passes"] += [{"state": "", "evidence": ""} for _ in range(len(PASSES) - len(run["passes"]))]
    return run


def save(d, run):
    schema.dump(path(d), "run", run)
    open(os.path.join(d, "RUN.md"), "w").write(table(run))


def refuse(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)


def names_command(text, commands):
    """The first command named in `text` as a whole phrase, never as part of a longer word."""
    for c in commands:
        if re.search(r"(?<![\w.-])" + re.escape(c) + r"(?![\w-])", text):
            return c
    return None


def proof_of(d, n, ev, file, cmd):
    """What makes `done` checkable: a saved output that exists, or a command run and kept here."""
    key, _, commands = PASSES[n]
    if file is None and cmd is None:
        refuse(f"done needs --file <saved output> or --run \"<command>\", so the proof is checkable.\n"
               f"commands for pass {n} ({key}): {', '.join(commands)}")
    if cmd is not None:
        if not names_command(cmd, commands):
            refuse(f"--run must run one of pass {n}'s commands: {', '.join(commands)}\ngot: {cmd!r}")
        done = subprocess.run(cmd, shell=True, cwd=d, capture_output=True, text=True, timeout=900)
        if done.returncode != 0:
            refuse(f"--run exited {done.returncode}, so it proves nothing:\n"
                   f"{(done.stdout + done.stderr)[-2000:]}")
        os.makedirs(os.path.join(d, "proof"), exist_ok=True)
        file = os.path.join(d, "proof", f"{n}-{key}.txt")
        open(file, "w").write(f"$ {cmd}\n{done.stdout}{done.stderr}")
    else:
        if not names_command(ev, commands):
            refuse(f"evidence must name, as a whole phrase, a command whose output you read back: "
                   f"{', '.join(commands)}\ngot: {ev!r}. --anyway if the proof was something else, "
                   f"and say what.")
        file = os.path.abspath(file)
        if not os.path.isfile(file) or os.path.getsize(file) == 0:
            refuse(f"--file {file} does not exist or is empty: save the command's output there first")
    proof = {"file": file, "sha256": schema.sha256(file)}
    if cmd is not None:
        proof["run"] = cmd
    return proof


def idx(arg):
    try:
        n = int(arg)
    except ValueError:
        n = next((i for i, p in enumerate(PASSES) if p[0] == arg), -1)
    if not 0 <= n < len(PASSES):
        sys.exit(f"pass must be 0-{len(PASSES)-1} or one of: " + ", ".join(p[0] for p in PASSES))
    return n


def table(run):
    where = (f"Descript project `{run['project']}`, composition `{run['comp']}`."
             if run.get("route", "descript") == "descript"
             else f"Local route. The cut is `{run.get('cut', '')}`.")
    head = (f"# {run['code']} - run ledger\n\n{where}\n"
            "Written by `video-edit/scripts/run.py`. Do not edit by hand: `show` rewrites it.\n\n"
            "| # | Pass | State | Evidence |\n|---|---|---|---|\n")
    rows = []
    for i, (name, what, _) in enumerate(PASSES):
        s = run["passes"][i]
        mark = {"done": "done", "started": "started", "blocked": "BLOCKED"}.get(s["state"], "")
        if s.get("override"):
            mark += " (out of order)"
        rows.append(f"| {i} | {name} - {what} | {mark} | {s.get('evidence', '')} |")
    return head + "\n".join(rows) + "\n"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, d = sys.argv[1], sys.argv[2]
    # A flag in the directory slot used to be taken as the name: `run.py init --help` wrote a
    # ledger into a directory called `--help` in the repo root, found there 10 September 2026.
    if d.startswith("-"):
        sys.exit(__doc__)
    arg = lambda k, dflt=None: (sys.argv[sys.argv.index(k) + 1] if k in sys.argv else dflt)

    if cmd == "init":
        route = arg("--route", "descript")
        if route not in ROUTES:
            sys.exit(f"route must be one of: {', '.join(ROUTES)}")
        run = {"code": arg("--code", os.path.basename(d.rstrip("/"))),
               "route": route,
               "project": arg("--project", ""), "comp": arg("--comp", ""),
               "cut": arg("--cut", ""),
               "passes": [{"state": "", "evidence": ""} for _ in PASSES]}
        os.makedirs(d, exist_ok=True)
        save(d, run)
        print(table(run))
        return

    run = load(d)

    if cmd == "show":
        save(d, run)
        print(table(run))
    elif cmd == "next":
        n = next((i for i, s in enumerate(run["passes"]) if s["state"] not in ("done", "blocked")), None)
        if n is None:
            print("every pass done")
            return
        name, what, proof = PASSES[n]
        state = run["passes"][n]["state"]
        print(f"{n} {name}: {what}")
        if state == "blocked":
            print(f"  BLOCKED: {run['passes'][n]['evidence']}")
        print("  proves it: " + ", ".join(proof))
    elif cmd == "start":
        n = idx(sys.argv[3])
        behind = [i for i in range(n) if run["passes"][i]["state"] not in ("done", "blocked")]
        if behind and "--anyway" not in sys.argv:
            sys.exit(f"pass {behind[0]} ({PASSES[behind[0]][0]}) is not done. "
                     f"Each pass is timed against the one before it. --anyway to override.")
        run["passes"][n] = {"state": "started", "evidence": "",
                            "override": bool(behind), "at": datetime.date.today().isoformat()}
        sync_board(run)
        save(d, run)
        print(table(run))
    elif cmd == "done":
        n = idx(sys.argv[3])
        ev = arg("--evidence", "")
        entry = dict(run["passes"][n], state="done", evidence=ev,
                     at=datetime.date.today().isoformat())
        if "--anyway" in sys.argv:
            if not ev.strip():
                refuse("--anyway still needs --evidence saying what the proof was")
            entry["override"] = True
        else:
            entry["proof"] = proof_of(d, n, ev, arg("--file"), arg("--run"))
        run["passes"][n] = entry
        sync_board(run)
        save(d, run)
        print(table(run))
    elif cmd == "block":
        n = idx(sys.argv[3])
        run["passes"][n] = dict(run["passes"][n], state="blocked", evidence=arg("--why", ""))
        sync_board(run)
        save(d, run)
        print(table(run))
    elif cmd == "board":
        run["task"] = arg("--task", run.get("task", ""))
        if not run["task"]:
            sys.exit("board needs --task <ClickUp task id>")
        sync_board(run)
        save(d, run)
        print(f"checklist {run.get('checklist', '?')} on {run['task']} mirrors the table")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
