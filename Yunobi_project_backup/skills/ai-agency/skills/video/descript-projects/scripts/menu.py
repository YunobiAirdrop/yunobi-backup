#!/usr/bin/env python3
"""Right-click a row in the Project panel and click one menu item by label."""

"""Usage:  python3 menu.py <page-file> <row-label> <menu-item-label>"""
import json, subprocess, sys, time
PAGE=open(sys.argv[1]).read().strip(); ROW=sys.argv[2]; ITEM=sys.argv[3]
def ev(expr):
    out=subprocess.run(["orca","eval","--page",PAGE,"--expression",expr,"--json"],capture_output=True,text=True).stdout
    try: return json.loads(json.loads(out)["result"]["result"])
    except Exception: return None
def ab(cmd): subprocess.run(["orca","exec","--page",PAGE,"--command",cmd,"--json"],capture_output=True,text=True)
c=ev('''(function(n){var s=document.querySelector('[data-testid="sidebar-content"]');
 var el=[].slice.call(s.querySelectorAll('*')).filter(function(e){return e.children.length===0 && (e.textContent||'').trim()===n});
 if(!el.length) return JSON.stringify({found:0});
 var r=el[0].getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)})})(%s)'''%json.dumps(ROW))
if not c or c.get("found")==0: sys.exit(json.dumps({"error":"row not found","row":ROW}))
ab(f"mouse move {c['x']} {c['y']}"); ab("mouse down right"); ab("mouse up right"); time.sleep(2)
m=ev('''JSON.stringify([].slice.call(document.querySelectorAll('[role="menuitem"]')).filter(function(e){return (e.innerText||'').trim().indexOf(%s)===0}).map(function(e){var r=e.getBoundingClientRect();return {x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)}}))'''%json.dumps(ITEM))
if not m: sys.exit(json.dumps({"error":"menu item not found","item":ITEM}))
ab(f"mouse move {m[0]['x']} {m[0]['y']}"); ab("mouse down"); ab("mouse up"); time.sleep(2)
print(json.dumps({"row":ROW,"item":ITEM,"ok":True}))
