#!/bin/bash
# Orkestrator harian multi-blog:
# fetch -> tulis_ulang (berita) -> evergreen (panduan) -> digest (rekap)
# -> baca_juga (internal link) -> trending (riset) -> posting
set -e
cd "$(dirname "$0")"
PY=./venv/bin/python
ALL_BLOGS=$(./venv/bin/python -c "import json; print(' '.join(b['nama'] for b in json.load(open('config.json'))['blogs']))")
# ROTASI HEMAT KUOTA (aturan user 2026-10-05): 6 artikel/hari. KabarViral selalu dapat,
# 5 lainnya rotasi dari sisa blog. File rotasi-blog.txt menyimpan index terakhir.
ROTFILE="rotasi-blog.txt"
BLOG_UTAMA="kabarviral"
SISA_BLOGS=$(echo "$ALL_BLOGS" | tr ' ' '\n' | grep -v "^${BLOG_UTAMA}$" | tr '\n' ' ')
N_SISA=$(echo "$SISA_BLOGS" | wc -w)
IDX=0
[ -f "$ROTFILE" ] && IDX=$(cat "$ROTFILE")
# Ambil 5 blog mulai dari IDX (wrap around)
BLOGS_ROTASI=""
for i in 0 1 2 3 4; do
  POS=$(( (IDX + i) % N_SISA ))
  B=$(echo "$SISA_BLOGS" | cut -d' ' -f$((POS+1)))
  BLOGS_ROTASI="$BLOGS_ROTASI $B"
done
BLOGS="$BLOG_UTAMA $BLOGS_ROTASI"
echo "[$(date '+%F %T')] rotasi blog hari ini:$BLOGS"
# Simpan index berikutnya
echo $(( (IDX + 5) % N_SISA )) > "$ROTFILE"
echo "[$(date '+%F %T')] mulai multi-blog (6 blog rotasi): $BLOGS"

# 1. Fetch semua blog dulu (cepat, tanpa AI)
for BLOG in $BLOGS; do
  echo "===== FETCH: $BLOG ====="
  $PY -u fetch_berita.py --blog "$BLOG" || echo "fetch $BLOG gagal, lanjut"
done

# 2. Riset trending (pakai headline fresh dari fetch)
echo "===== TRENDING ====="
$PY -u trending.py || echo "trending gagal, lanjut"

# 3. Tulis ulang + evergreen + digest + posting PER BLOG
# (posting per blog supaya artikel terbit bertahap, tidak nunggu semua blog selesai)
for BLOG in $BLOGS; do
  echo "===== TULIS: $BLOG ====="
  $PY -u tulis_ulang.py --blog "$BLOG" || echo "tulis $BLOG gagal, lanjut"
  # 2026-10-04: evergreen & digest DINONAKTIFKAN sementara (hemat kuota OpenRouter).
  # 2026-10-05: aturan baru user — 6 artikel/hari rotasi (KabarViral + 5 blog rotasi), 1 artikel/blog.
  # echo "===== EVERGREEN: $BLOG ====="
  # $PY -u evergreen.py --blog "$BLOG" --jumlah 2 || echo "evergreen $BLOG gagal, lanjut"
  # echo "===== DIGEST: $BLOG ====="
  # $PY -u digest.py --blog "$BLOG" || echo "digest $BLOG gagal, lanjut"
  echo "===== BACA-JUGA: $BLOG ====="
  $PY -u baca_juga.py --blog "$BLOG" || echo "baca_juga $BLOG gagal, lanjut"
  echo "===== POSTING: $BLOG (via web UI, API diblokir 2026-10-03) ====="
  $PY -u posting_web.py --blog "$BLOG" || echo "posting $BLOG gagal, lanjut"
done

echo "[$(date '+%F %T')] selesai semua blog"
