#!/usr/bin/env python3
"""Rename Descript compositions through Orca's browser.

Usage: PAGE=<browserPageId> python3 rename.py <project> <short> "<old name>" "<new name>"

Descript has no rename API, so this drives the title editor - which is a
SEPARATE DraftEditor from the script, hence its own element lookup.

Two things it must not do:
  - drag left-to-right from the title's left edge: a floating button sits over
    the leading whitespace and swallows the mouse down. Drag right-to-left.
  - press Enter to commit: that lands a paragraph in the SCRIPT. Blur instead.
"""
import json
import os
import subprocess
import sys
import time

PAGE = os.environ["PAGE"]


def orca(args, timeout=90):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout).stdout


def ev(expr):
    out = orca(["orca", "eval", "--page", PAGE, "--expression", expr, "--json"])
    try:
        return json.loads(out).get("result", {}).get("result")
    except Exception:
        return None


def ab(cmd):
    orca(["orca", "exec", "--command", cmd, "--page", PAGE, "--json"])


def rename(project, short, old, new):
    orca(["orca", "exec", "--page", PAGE, "--command",
          f"navigate https://web.descript.com/{project}/{short}", "--json"])
    time.sleep(16)

    url = json.loads(ev("JSON.stringify({u:location.href})"))["u"]
    if not url.endswith(short):
        return {"short": short, "status": "wrong-composition", "url": url}

    box = ev(
        "(function(){var n=%s;var el=null;"
        "document.querySelectorAll('*').forEach(function(e){"
        "if(e.children.length===0&&(e.textContent||'').trim()===n&&e.isContentEditable)el=e;});"
        "if(!el)return null;var r=el.getBoundingClientRect();"
        "return JSON.stringify({l:Math.round(r.left),rt:Math.round(r.right),"
        "y:Math.round(r.top+r.height/2)});})()" % json.dumps(old)
    )
    if not box or box == "null":
        return {"short": short, "status": "title-not-found"}
    b = json.loads(box)

    # Right-to-left: the left edge is covered by a floating button.
    ab("mouse up")
    ab(f"mouse move {b['rt'] - 2} {b['y']}")
    ab("mouse down")
    ab(f"mouse move {(b['l'] + b['rt']) // 2} {b['y']}")
    ab(f"mouse move {b['l'] + 2} {b['y']}")
    ab("mouse up")
    time.sleep(1)

    sel = json.loads(ev("JSON.stringify({s:getSelection().toString()})"))["s"]
    if sel.strip() != old.strip():
        ab("mouse up")
        ev("(window.getSelection().removeAllRanges(),1)")
        return {"short": short, "status": "guard-refused", "got": sel[:60]}

    orca(["orca", "type", "--input", new, "--page", PAGE, "--json"])
    time.sleep(2)

    # Commit by blurring into the script. NEVER Enter.
    ab("mouse move 300 300")
    ab("mouse down")
    ab("mouse up")
    time.sleep(3)
    ev("(window.getSelection().removeAllRanges(),1)")
    return {"short": short, "status": "renamed", "new": new}


if __name__ == "__main__":
    print(json.dumps(rename(*sys.argv[1:5])))
