#!/usr/bin/env python3
"""Delete typed text (no media) via the CDP key path.

`orca keypress` and `orca computer press-key` both need an on-screen Orca
window and fail silently without one. `orca exec --command "key Delete"` goes
through CDP and works headless. Law 6 guard still gates every keystroke.
"""

"""Usage:  python3 delcdp.py <targets.json>   # one {page,selector} per entry"""
import json, os, subprocess, sys, time
PAGE = os.environ["DESCRIPT_PAGE"]
def run(a): return subprocess.run(a, capture_output=True, text=True, timeout=120).stdout.strip()
def ev(e):
    o = run(["orca","eval","--page",PAGE,"--expression",e,"--json"])
    try: return json.loads(o[o.index("{"):])["result"]["result"]
    except Exception: return None
def ab(c): return run(["orca","exec","--command",c,"--page",PAGE,"--json"])
def norm(s): return " ".join(s.split())
def find(n, hint):
    t = ev("JSON.stringify(window.__blocks().map(b=>window.__map(b).text))")
    if not t: return None
    ts = json.loads(t); hits = [i for i,x in enumerate(ts) if n in x]
    if not hits: return None
    b = min(hits, key=lambda i: abs(i-hint))
    r = ev("JSON.stringify(window.__find(%s,%d))" % (json.dumps(n), b))
    return json.loads(r) if r else None

for item in json.load(open(sys.argv[1])):
    n, hint = item["t"], item["b"]
    ok = False
    for nudge, wp, rev in ((8,5,False),(8,5,True),(8,1,False),(2,10,False),(12,8,False)):
        r = find(n, hint)
        if r is None: print(json.dumps({"t": n[:45], "status": "gone"})); ok = True; break
        if not (r.get("ok") and r.get("onscreen")):
            print(json.dumps({"t": n[:45], "status": "no-rect"})); break
        sx, sy, ex, ey = r["sx"]+nudge, r["sy"], r["ex"], r["ey"]
        if rev: sx, sy, ex, ey = ex, ey, r["sx"]+nudge, r["sy"]
        ab("mouse up"); time.sleep(0.2); ab(f"mouse move {sx} {sy}"); time.sleep(0.3)
        ab("mouse down"); time.sleep(0.3)
        for k in range(1, wp+1):
            ab(f"mouse move {round(sx+(ex-sx)*k/wp)} {round(sy+(ey-sy)*k/wp)}"); time.sleep(0.12)
        time.sleep(0.3); ab("mouse up"); time.sleep(0.9)
        sel = ev("window.getSelection().toString()") or ""
        if norm(sel) != norm(n):
            print(json.dumps({"t": n[:45], "try": f"n{nudge}w{wp}r{int(rev)}",
                              "status": "refused", "gotLen": len(sel), "got": sel[:50]}), flush=True)
            ab("mouse up"); ev("(window.getSelection().removeAllRanges(),1)")
            continue
        ab("key Delete"); time.sleep(2.0)
        gone = find(n, hint) is None
        print(json.dumps({"t": n[:45], "status": "deleted" if gone else "still-present"}), flush=True)
        ab("mouse up"); ev("(window.getSelection().removeAllRanges(),1)")
        if gone: ok = True; break
    if not ok: print(json.dumps({"t": n[:45], "status": "FAILED"}), flush=True)
