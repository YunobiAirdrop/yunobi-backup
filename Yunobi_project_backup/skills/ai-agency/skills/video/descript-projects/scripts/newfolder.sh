#!/bin/bash
# newfolder.sh <page-file> [name]   creates a ROOT-level media folder in the Project panel
#
# The Files context menu mirrors the current selection: with a folder selected
# "New folder" nests inside that folder, and with a file selected the menu has no
# New folder at all. So clear the selection first - left-click the empty space
# below the last row - then right-click the same spot for the root menu
# (Computer / Media library / Other projects / Zoom / Google Drive / Slides /
# Sequence / Folder) and take "Folder".
#
# The new folder opens STRAIGHT INTO its inline rename field, and the row stays
# reading "Group" (the tree's aria label) for as long as that field is open - it
# never settles to "Untitled Folder" on its own. So the settle signal is the
# focused INPUT whose value is "Untitled Folder", and passing a name here types
# it there. rename_folder.sh is only for renaming a folder later.
set -e
PG=$(cat "$1")
NAME="$2"

# An empty y below the last row, still inside the panel.
Y=$(orca eval --page "$PG" --expression "(function(){var s=document.querySelector('[data-testid=\"sidebar-content\"]');var rows=[].slice.call(s.querySelectorAll('*')).filter(function(e){return e.children.length===0 && (e.textContent||'').trim()});var last=rows[rows.length-1].getBoundingClientRect();var p=s.getBoundingClientRect();return String(Math.round(Math.min(last.bottom+60, p.bottom-40)))})()" --json | jq -r '.result.result')
X=1300

orca exec --page "$PG" --command "press Escape" --json >/dev/null; sleep 1
orca exec --page "$PG" --command "mouse move $X $Y" --json >/dev/null
orca exec --page "$PG" --command "mouse down" --json >/dev/null
orca exec --page "$PG" --command "mouse up" --json >/dev/null
sleep 1
orca exec --page "$PG" --command "mouse down right" --json >/dev/null
orca exec --page "$PG" --command "mouse up right" --json >/dev/null
sleep 2

M=$(orca eval --page "$PG" --expression "JSON.stringify([].slice.call(document.querySelectorAll('[role=\"menuitem\"]')).filter(function(e){return (e.innerText||'').trim()==='Folder'}).map(function(e){var r=e.getBoundingClientRect();return {x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)}}))" --json | jq -r '.result.result')
MX=$(echo "$M" | jq -r '.[0].x'); MY=$(echo "$M" | jq -r '.[0].y')
if [ "$MX" = "null" ]; then
  echo '{"error":"no Folder item - something is still selected, or the click missed the empty area"}'
  exit 1
fi
orca exec --page "$PG" --command "mouse move $MX $MY" --json >/dev/null
orca exec --page "$PG" --command "mouse down" --json >/dev/null
orca exec --page "$PG" --command "mouse up" --json >/dev/null

OK=0
for _ in 1 2 3 4 5 6 7 8; do
  sleep 2
  V=$(orca eval --page "$PG" --expression "JSON.stringify(document.activeElement.value||'')" --json | jq -r '.result.result')
  [ "$V" = '"Untitled Folder"' ] && { OK=1; break; }
done
[ "$OK" = 1 ] || { echo '{"error":"rename field never took focus - the Folder click missed"}'; exit 1; }

if [ -z "$NAME" ]; then
  echo '{"created":"Untitled Folder","renameFieldOpen":true}'
  exit 0
fi

# orca type ignores --page, so focus the tab. Type straight over the pre-selected
# text (Meta+a closes the field), Enter commits.
orca tab switch --page "$PG" --focus --json >/dev/null
orca type --input "$NAME" --page "$PG" --json >/dev/null
sleep 1
orca exec --page "$PG" --command "press Enter" --json >/dev/null
sleep 3
orca eval --page "$PG" --expression "JSON.stringify(document.querySelector('[data-testid=\"sidebar-content\"]').innerText.split('\n').filter(function(x){return x.trim()}))" --json | jq -r '.result.result'
