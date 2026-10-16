#!/bin/bash
# Post: title-card overlay (0.5-5s) + subtle ambience bed + loudnorm voice + faststart
set -e
cd ~/workspace/youtube-otomatis/empires-en/2026-10-16
FQ=~/workspace/youtube-otomatis/ffmpeg-queue.sh
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
BASE=video/lost-empires-roman-concrete-base.mp4
OUT=video/lost-empires-roman-concrete.mp4
DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$BASE")

# 1) ambience bed: shaped brown noise, very low (-32 dB), fades at ends
FADEOUT=$(awk "BEGIN{print $DUR-3}")
$FQ -y -f lavfi -i "anoisesrc=d=$DUR:c=brown:r=44100:a=0.5" \
   -af "lowpass=f=400,volume=-32dB,afade=t=in:st=0:d=2,afade=t=out:st=$FADEOUT:d=3" \
   -c:a pcm_s16le _tmp_amb.wav 2>/dev/null

# 2) title card text overlay + mix voice (loudnorm) with ambience
$FQ -y -i "$BASE" -i _tmp_amb.wav -filter_complex \
 "[0:v]drawbox=y=ih/2-90:c=black@0.55:w=iw:h=180:t=fill:enable='between(t,0.5,5)',drawtext=fontfile=$FONT:text='THE ROMAN SECRET':fontsize=64:fontcolor=white:borderw=2:bordercolor=black@0.6:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,0.5,5)'[v];[0:a]loudnorm=I=-16:TP=-1.5:LRA=11[vox];[1:a]volume=1.0[amb];[vox][amb]amix=inputs=2:duration=first:dropout_transition=0[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -preset veryfast -pix_fmt yuv420p -r 30 \
 -c:a aac -b:a 128k -movflags +faststart -shortest "$OUT" 2>/dev/null

rm -f _tmp_amb.wav
SIZE=$(stat -c%s "$OUT")
echo "OK: $OUT ($(awk "BEGIN{printf \"%.1f\", $SIZE/1048576}") MB)"
if [ "$SIZE" -gt 104857600 ]; then echo "TERLALU BESAR - perlu kompresi"; fi
