#!/usr/bin/env python3
"""Move a file row onto a folder row in Descript's Project panel.

Drag-and-drop is the only route: the media context menu has no "move to folder"
and there is no API for it. Two things make the drop land:
  - a short pause after mouse down, then several waypoints, then a hover on the
    target before mouse up (a fast drag reports "Dragging was cancelled.")
  - coordinates re-read immediately before the drag: every drop re-renders the
    tree and shifts every row below it.
Verification is the tree's aria live region, which announces
  Item "<name>" was dropped in Group "<folder>"
"""

"""Usage:  python3 movefile.py <page-file> <file-row-label> <folder-row-label>"""
import json, subprocess, sys, time

PAGE = open(sys.argv[1]).read().strip()
SRC, DST = sys.argv[2], sys.argv[3]

def ev(expr):
    out = subprocess.run(["orca","eval","--page",PAGE,"--expression",expr,"--json"],
                         capture_output=True, text=True).stdout
    try: return json.loads(json.loads(out)["result"]["result"])
    except Exception: return None

def ab(cmd):
    subprocess.run(["orca","exec","--page",PAGE,"--command",cmd,"--json"],
                   capture_output=True, text=True)

COORD = '''(function(names){
 var s=document.querySelector('[data-testid="sidebar-content"]');
 return JSON.stringify(names.map(function(n){
  var el=[].slice.call(s.querySelectorAll('*')).filter(function(e){return e.children.length===0 && (e.textContent||'').trim()===n});
  if(!el.length) return {n:n,found:0};
  var r=el[0].getBoundingClientRect();
  return {n:n,x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)};
 }));
})(%s)'''

def coords(names):
    return ev(COORD % json.dumps(names))

def live():
    return ev("JSON.stringify(document.querySelector('[data-testid=\"sidebar-content\"]').innerText.split('\\n').filter(function(x){return x.trim()}).slice(-1)[0])")

a, b = coords([SRC, DST])
if a.get("found") == 0 or b.get("found") == 0:
    sys.exit(json.dumps({"error":"row not found","a":a,"b":b}))

ab("mouse up")
ab(f"mouse move {a['x']} {a['y']}")
ab("mouse down")
time.sleep(0.4)
ab(f"mouse move {a['x']} {a['y']-6}")
time.sleep(0.4)
for k in range(1, 11):
    ab(f"mouse move {round(a['x']+(b['x']-a['x'])*k/10)} {round(a['y']+(b['y']-a['y'])*k/10)}")
    time.sleep(0.25)
time.sleep(1.5)
ab(f"mouse move {b['x']} {b['y']}")
time.sleep(1.5)
ab("mouse up")
time.sleep(2.5)
print(json.dumps({"src":SRC, "dst":DST, "live":live()}))
