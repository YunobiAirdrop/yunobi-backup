#!/bin/bash
# run_pipeline.sh — self-driving chain: chunks -> voiceover_full -> bed+mix -> assembly.
# Each step waits its turn on ffmpeg-queue.sh; safe to re-run (idempotent outputs).
set -u
WD=/home/hatch/workspace/youtube-otomatis/mystery-en/2026-10-16/v2/short3
LOG="$WD/pipeline.log"
exec >>"$LOG" 2>&1
echo "=== pipeline start $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
cd "$WD" || { echo "FATAL: work dir missing: $WD"; exit 1; }
for f in build_audio.py mix_audio.py rakit_short3.py manifest.json; do
  [ -e "$f" ] || { echo "FATAL: missing $f (dir may have been wiped)"; exit 1; }
done
python3 build_audio.py || { echo "FATAL: build_audio.py failed"; exit 1; }
python3 mix_audio.py   || { echo "FATAL: mix_audio.py failed"; exit 1; }
python3 rakit_short3.py manifest.json || { echo "FATAL: rakit_short3.py failed"; exit 1; }
echo "=== pipeline done $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
ls -la mystery-en-short3-2026-10-16.mp4 || echo "WARNING: final mp4 missing"
