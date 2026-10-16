#!/bin/bash
# rename_folder.sh <page-file> <current-row-label> <new-name>
# Right-click -> Rename leaves the field's text pre-selected: type straight over
# it. Meta+a closes the field instead of selecting (learned 2026-08-15), and the
# name only commits on Enter.
set -e
SP="$(dirname "$0")"; PGF="$1"; ROW="$2"; NEW="$3"; PG=$(cat "$PGF")
python3 "$SP/menu.py" "$PGF" "$ROW" "Rename" >/dev/null
orca tab switch --page "$PG" --focus --json >/dev/null
orca type --input "$NEW" --page "$PG" --json >/dev/null
sleep 1
orca exec --page "$PG" --command "press Enter" --json >/dev/null
sleep 2
orca eval --page "$PG" --expression "JSON.stringify(document.querySelector('[data-testid=\"sidebar-content\"]').innerText.split('\n').filter(function(x){return x.trim()}))" --json | jq -r '.result.result' | python3 -c "import sys,json;a=json.load(sys.stdin);i=a.index('Files');print(a[i:i+22])"
