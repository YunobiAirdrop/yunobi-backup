#!/bin/bash
# Caption pass v2 untuk tinybuilders-shorts-2026-10-16:
# caption per-baris (tanpa \n), safe zone 9:16, + title card "TINY BUILDERS".
# Semua render via ffmpeg-queue.sh
set -e
D=~/workspace/youtube-otomatis/miniatur-ai/2026-10-16
FQ=~/workspace/youtube-otomatis/ffmpeg-queue.sh
F=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
FS=40; BW=3; LH=50   # fontsize, border, line-height

# cap <t0> <t1> <y0> "baris1|baris2|baris3"
cap() {
  local t0=$1 t1=$2 y0=$3 IFS='|'
  local i=0
  for line in $4; do
    line=${line//,/\\,}
    VF="${VF}drawtext=fontfile=${F}:text='${line}':fontsize=${FS}:fontcolor=white:borderw=${BW}:bordercolor=black:x=(w-text_w)/2:y=$((y0 + i*LH)):enable='between(t\\,${t0}\\,${t1})',"
    i=$((i+1))
  done
}
VF=""
cap 0  6  848 "This lighthouse is|smaller than your thumb —|its light really turns on."
cap 6  12 848 "Every brick,|every wave...|built by hand."
cap 12 17 873 "The lamp room holds|a real, working light."
cap 17 23 873 "When the storm comes,|the beam keeps turning."
cap 23 29 848 "Someone lives here —|the light never|goes out."
cap 29 35 873 "Tiny builders.|Impossible details."
# title card kecil di beat terakhir (tidak merusak loop)
VF="${VF}drawtext=fontfile=${F}:text='TINY BUILDERS':fontsize=30:fontcolor=white@0.85:borderw=2:bordercolor=black@0.6:x=(w-text_w)/2:y=90:enable='gte(t\\,29)',"
VF=${VF%,}

"$FQ" -y -loglevel error -i "$D/video_raw.mp4" -vf "$VF" \
  -c:v libx264 -preset veryfast -pix_fmt yuv420p -r 30 \
  -c:a copy -movflags +faststart "$D/tinybuilders-shorts-2026-10-16.mp4"
echo CAPTION_OK
ffprobe -v error -show_entries format=duration,size \
  -of default=noprint_wrappers=1:nokey=1 "$D/tinybuilders-shorts-2026-10-16.mp4"
