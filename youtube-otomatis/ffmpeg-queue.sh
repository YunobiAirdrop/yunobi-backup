#!/bin/bash
# ffmpeg-queue.sh — Batasi render ffmpeg maksimal 2 proses bareng, sisanya ANTRE OTOMATIS.
# Dipakai sebagai pengganti "ffmpeg" di semua script produksi video (youtube-otomatis,
# video-weirdworld, blog-otomatis) agar RAM 7.7GB tidak jebol saat 11 channel produksi
# bareng. Sepenuhnya otomatis: tidak butuh persetujuan/ketukan user.
#
# Cara kerja: semaphore via mkdir atomik di $FFMPEG_SLOTDIR (default /tmp/ffmpeg-slots).
# Slot yang pemiliknya mati (PID tidak hidup) dibersihkan otomatis oleh penunggu berikutnya.
# Semua argumen diteruskan apa adanya ke /usr/bin/ffmpeg.

MAX_SLOTS=2
SLOTDIR="${FFMPEG_SLOTDIR:-/tmp/ffmpeg-slots}"
mkdir -p "$SLOTDIR" 2>/dev/null

grab_slot() {
    local i d pid
    for i in $(seq 1 "$MAX_SLOTS"); do
        d="$SLOTDIR/slot$i"
        if mkdir "$d" 2>/dev/null; then
            echo "$$" > "$d/pid" 2>/dev/null
            printf '%s' "$d"
            return 0
        fi
        # Slot terisi — cek apakah pemiliknya masih hidup; kalau mati, rebut slotnya.
        pid=$(cat "$d/pid" 2>/dev/null)
        if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null; then
            rm -rf "$d" 2>/dev/null
            if mkdir "$d" 2>/dev/null; then
                echo "$$" > "$d/pid" 2>/dev/null
                printf '%s' "$d"
                return 0
            fi
        fi
    done
    return 1
}

slot=""
while [ -z "$slot" ]; do
    slot=$(grab_slot) || sleep 10
done

# Bersihkan slot saat proses ini selesai (normal maupun dibunuh).
# shellcheck disable=SC2064
trap "rm -rf \"$slot\"" EXIT INT TERM

exec /usr/bin/ffmpeg "$@"
