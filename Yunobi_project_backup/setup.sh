#!/usr/bin/env bash
# =====================================================================
# setup.sh — Instalasi OTOMATIS project Yunobi di mesin Linux baru
#            (Ubuntu/Debian). Dijalankan dari repo yunobi_project_backup.
#
# Cara pakai:
#   cd ~/workspace/backup-repo   # (hasil clone repo)
#   chmod +x setup.sh
#   ./setup.sh
#
# Script ini:
#  1. Install dependensi sistem (ffmpeg, python3, nodejs, git, curl)
#  2. Buat struktur direktori project
#  3. Install package Python yang dibutuhkan
#  4. Wizard kredensial interaktif (tidak pernah menampilkan nilainya)
#  5. Salin config template + script dari repo ke lokasi aktif
#  6. Cetak panduan langkah MANUAL (OAuth, login browser)
#  7. Pasang cron (dengan konfirmasi dulu)
#  8. Verifikasi akhir per komponen
#
# Yang TIDAK bisa otomatis (harus manual, dipandu di langkah 6):
#  - OAuth Blogger & YouTube (klik di HP / browser)
#  - Login browser (YouTube Studio, Blogger, Shopee, TikTok)
# =====================================================================
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_FILE="$REPO_DIR/setup-cron.txt"
TERLEWAT=()   # daftar kredensial yang di-skip user

# ---------- util ----------
info()  { printf '\033[1;34m[INFO]\033[0m %s\n' "$*"; }
ok()    { printf '\033[1;32m[OK]\033[0m %s\n' "$*"; }
warn()  { printf '\033[1;33m[PERINGATAN]\033[0m %s\n' "$*"; }
err()   { printf '\033[1;31m[GAGAL]\033[0m %s\n' "$*" >&2; }

# tanya_ya_tidak "pertanyaan" -> return 0 jika ya
tanya_ya_tidak() {
  local jawab=""
  while true; do
    printf '%s [y/t]: ' "$1" > /dev/tty
    IFS= read -r jawab < /dev/tty || jawab=""
    case "$jawab" in
      y|Y|ya|YA) return 0 ;;
      t|T|tidak|TIDAK) return 1 ;;
      *) echo "Jawab y atau t." > /dev/tty ;;
    esac
  done
}

# tanya_rahasia "label" nama_var
# Membaca TANPA echo ke layar. Kosong = lewati (dicatat di TERLEWAT).
tanya_rahasia() {
  local label="$1" __var="$2" val=""
  printf '%s\n  (ketik lalu Enter; kosongkan untuk lewati)\n> ' "$label" > /dev/tty
  IFS= read -rs val < /dev/tty || val=""
  echo "" > /dev/tty
  printf -v "$__var" '%s' "$val"
  if [ -z "$val" ]; then
    TERLEWAT+=("$label")
    warn "Dilewati: $label"
  else
    ok "Tersimpan: $label (nilai tidak ditampilkan)"
  fi
}

# simpan_600 "path" "isi" — tulis file dengan izin 600
simpan_600() {
  local path="$1" isi="$2"
  mkdir -p "$(dirname "$path")"
  printf '%s' "$isi" > "$path"
  chmod 600 "$path"
}

# ---------- header ----------
echo "====================================================================="
echo " SETUP OTOMATIS PROJECT YUNOBI"
echo " Repo : $REPO_DIR"
echo " Mesin: $(uname -srm)"
echo "====================================================================="
echo ""

# ---------- LANGKAH 1: dependensi sistem ----------
info "LANGKAH 1/8 — Cek & install dependensi sistem (butuh sudo/apt)..."
if ! command -v apt-get >/dev/null 2>&1; then
  err "apt-get tidak ditemukan. Script ini hanya untuk Ubuntu/Debian."
  exit 1
fi
if ! command -v sudo >/dev/null 2>&1 && [ "$(id -u)" -ne 0 ]; then
  err "Butuh 'sudo' atau jalankan sebagai root untuk install paket sistem."
  exit 1
fi

PAKET_BUTUH=(ffmpeg python3 python3-pip python3-venv nodejs npm git curl)
PAKET_APT=(ffmpeg python3 python3-pip python3-venv nodejs npm git curl)
HILANG=()
for p in "${PAKET_BUTUH[@]}"; do
  command -v "$p" >/dev/null 2>&1 || HILANG+=("$p")
done
if [ "${#HILANG[@]}" -gt 0 ]; then
  info "Menginstall: ${HILANG[*]} ..."
  if [ "$(id -u)" -eq 0 ]; then
    apt-get update -qq && apt-get install -y -qq "${PAKET_APT[@]}"
  else
    sudo apt-get update -qq && sudo apt-get install -y -qq "${PAKET_APT[@]}"
  fi
fi
for p in ffmpeg python3 pip3 node git curl; do
  if command -v "$p" >/dev/null 2>&1; then ok "$p: $(command -v "$p")";
  else err "$p masih hilang setelah install!"; exit 1; fi
done

# ---------- LANGKAH 2: struktur direktori ----------
info "LANGKAH 2/8 — Membuat struktur direktori..."
mkdir -p ~/workspace/{blog-otomatis,youtube-otomatis,skills}
mkdir -p ~/.hermes ~/.hermes/yt-growth/tokens ~/memory
mkdir -p ~/workspace/blog-otomatis/hidden_files
mkdir -p ~/workspace/youtube-otomatis/{hidden_files,retry-queue,yt-growth}
ok "Direktori siap."

# ---------- LANGKAH 3: package Python ----------
info "LANGKAH 3/8 — Install package Python..."
PIP_PAKET=(requests feedparser pillow pyyaml google-api-python-client google-auth-oauthlib)
if ! pip3 install --quiet --user "${PIP_PAKET[@]}" 2>/dev/null; then
  warn "pip --user gagal, coba dengan --break-system-packages..."
  pip3 install --quiet --break-system-packages "${PIP_PAKET[@]}"
fi
for m in requests feedparser PIL yaml; do
  if python3 -c "import $m" 2>/dev/null; then ok "modul python '$m' OK";
  else err "modul python '$m' gagal diimport!"; exit 1; fi
done

# ---------- LANGKAH 4: wizard kredensial ----------
info "LANGKAH 4/8 — WIZARD KREDENSIAL"
echo "Isi satu per satu. Nilai TIDAK PERNAH ditampilkan di layar."
echo "Kosongkan (langsung Enter) bila belum punya — bisa diisi nanti."
echo ""

tanya_rahasia "1) OpenRouter API key(s) — boleh lebih dari 1, pisahkan koma" OR_KEYS
tanya_rahasia "2) COMPOSIO_CONSUMER_KEY (opsional)" COMPOSIO_KEY
tanya_rahasia "3) Google OAuth Client ID (untuk Blogger)" G_CLIENT_ID
tanya_rahasia "4) Google OAuth Client Secret (untuk Blogger)" G_CLIENT_SECRET
tanya_rahasia "5) Password dashboard 9Router (opsional)" DASH_PW

# ~/.hermes/.env
ENV_ISI=""
[ -n "${OR_KEYS:-}" ]      && ENV_ISI+="OPENROUTER_KEYS=\"${OR_KEYS}\""$'\n'
[ -n "${COMPOSIO_KEY:-}" ] && ENV_ISI+="COMPOSIO_CONSUMER_KEY=\"${COMPOSIO_KEY}\""$'\n'
if [ -n "$ENV_ISI" ]; then
  simpan_600 ~/.hermes/.env "$ENV_ISI"
  ok "~/.hermes/.env tersimpan (600)."
else
  warn "~/.hermes/.env tidak dibuat (semua dikosongkan)."
fi

# google-oauth-blogger.env
OAUTH_ISI=""
[ -n "${G_CLIENT_ID:-}" ]     && OAUTH_ISI+="GOOGLE_OAUTH_CLIENT_ID=\"${G_CLIENT_ID}\""$'\n'
[ -n "${G_CLIENT_SECRET:-}" ] && OAUTH_ISI+="GOOGLE_OAUTH_CLIENT_SECRET=\"${G_CLIENT_SECRET}\""$'\n'
if [ -n "$OAUTH_ISI" ]; then
  simpan_600 ~/.hermes/google-oauth-blogger.env "$OAUTH_ISI"
  ok "~/.hermes/google-oauth-blogger.env tersimpan (600)."
else
  warn "google-oauth-blogger.env tidak dibuat (dikosongkan)."
fi

# dashboard pw
if [ -n "${DASH_PW:-}" ]; then
  simpan_600 ~/.hermes/.dashboard-pw "$DASH_PW"
  ok "~/.hermes/.dashboard-pw tersimpan (600)."
fi

# bersihkan variabel dari memori shell
unset OR_KEYS COMPOSIO_KEY G_CLIENT_ID G_CLIENT_SECRET DASH_PW ENV_ISI OAUTH_ISI

# ---------- LANGKAH 5: salin config & script ----------
info "LANGKAH 5/8 — Salin config template & script dari repo..."

# config blog
if [ -f "$REPO_DIR/scripts/blog/config.contoh.json" ] && [ ! -f ~/workspace/blog-otomatis/config.json ]; then
  cp "$REPO_DIR/scripts/blog/config.contoh.json" ~/workspace/blog-otomatis/config.json
  ok "config.json dibuat dari template (SESUAIKAN isinya manual!)."
elif [ -f ~/workspace/blog-otomatis/config.json ]; then
  ok "config.json sudah ada — tidak ditimpa."
else
  warn "Template config.contoh.json tidak ditemukan di repo."
fi

# script blog (jangan timpa yang sudah ada)
if [ -d "$REPO_DIR/scripts/blog" ]; then
  for f in "$REPO_DIR"/scripts/blog/*; do
    [ -f "$f" ] || continue
    bn="$(basename "$f")"
    [ "$bn" = "config.contoh.json" ] && continue
    if [ ! -f ~/workspace/blog-otomatis/"$bn" ]; then
      cp "$f" ~/workspace/blog-otomatis/"$bn"
    fi
  done
  ok "Script blog disalin (file yang sudah ada tidak ditimpa)."
fi

# script youtube
if [ -d "$REPO_DIR/scripts/youtube" ]; then
  for f in "$REPO_DIR"/scripts/youtube/*; do
    [ -e "$f" ] || continue
    bn="$(basename "$f")"
    if [ ! -e ~/workspace/youtube-otomatis/"$bn" ]; then
      cp -r "$f" ~/workspace/youtube-otomatis/"$bn"
    fi
  done
  chmod +x ~/workspace/youtube-otomatis/ffmpeg-queue.sh 2>/dev/null || true
  ok "Script youtube disalin (termasuk yt-growth/, ffmpeg-queue.sh)."
fi

# skills
if [ -d "$REPO_DIR/skills" ]; then
  for d in "$REPO_DIR"/skills/*/; do
    [ -d "$d" ] || continue
    bn="$(basename "$d")"
    if [ ! -d ~/workspace/skills/"$bn" ]; then
      cp -r "$d" ~/workspace/skills/"$bn"
    fi
  done
  ok "Skills disalin ke ~/workspace/skills/."
fi

# /etc/9router-proxy.env — template tanpa nilai rahasia
if [ ! -f /etc/9router-proxy.env ]; then
  info "Membuat template /etc/9router-proxy.env (butuh sudo)..."
  if [ "$(id -u)" -eq 0 ]; then
    printf 'NODE_USE_ENV_PROXY=1\nNODE_EXTRA_CA_CERTS=/run/hatch/egress-tls/ca-bundle.pem\n# Tambahkan http_proxy/https_proxy bila mesin baru di balik proxy\n' > /etc/9router-proxy.env
    chmod 600 /etc/9router-proxy.env
  else
    sudo sh -c 'printf "NODE_USE_ENV_PROXY=1\nNODE_EXTRA_CA_CERTS=/run/hatch/egress-tls/ca-bundle.pem\n" > /etc/9router-proxy.env && chmod 600 /etc/9router-proxy.env' \
      && ok "/etc/9router-proxy.env dibuat." \
      || warn "Gagal membuat /etc/9router-proxy.env — buat manual bila perlu."
  fi
else
  ok "/etc/9router-proxy.env sudah ada."
fi

# ---------- LANGKAH 6: panduan manual ----------
info "LANGKAH 6/8 — PANDUAN LANGKAH MANUAL (tidak bisa otomatis)"
cat << 'PANDUAN'

  === A. OAuth Blogger (sekali saja) ===
  1. Pastikan google-oauth-blogger.env sudah terisi (langkah 4).
  2. Di Google Cloud Console, tambah redirect URI: http://127.0.0.1:8080/
     dan daftarkan akun Google kamu sebagai test user.
  3. Jalankan flow otorisasi (ikuti docs/07-kredensial.md) hingga dapat
     ~/.hermes/blogger-tokens.json (otomatis refresh setelah ini).

  === B. OAuth YouTube per channel — yt-growth (17 channel) ===
  1. Download client_secret.json (Desktop app) dari Google Cloud Console
     project YouTube-mu, simpan ke:
       ~/.hermes/yt-growth/client_secret.json   (chmod 600)
  2. Per channel, jalankan DUA perintah ini (klik link di HP):
       cd ~/workspace/youtube-otomatis/yt-growth
       python3 auth.py auth-url "NAMA CHANNEL"
       # -> buka URL di HP, login, KLIK AKUN UTAMA DULU, baru pilih channel,
       #    salin kode dari URL localhost yang error
       python3 auth.py exchange "NAMA CHANNEL" "KODE_DARI_URL"
     Token tersimpan di ~/.hermes/yt-growth/tokens/ (1 token = 1 channel).
  3. Cek: python3 auth.py status   (target: 17/17)

  === C. Login browser (tidak bisa via script) ===
  - YouTube Studio + Blogger : login khususstokyunobi@gmail.com di browser
  - Shopee Affiliate         : login via Google OAuth (stokakunwebyunobi@gmail.com)
  - TikTok @ngeweb.yuk       : login manual di aplikasi HP
  - IG/Threads/FB            : hubungkan via CLI masing-masing (lihat docs)

  === D. Sesuaikan config ===
  - ~/workspace/blog-otomatis/config.json  (ID 10 blog — lihat docs/02-blog-otomatis.md)
  - Pastikan timezone mesin Asia/Jakarta: sudo timedatectl set-timezone Asia/Jakarta

PANDUAN

# ---------- LANGKAH 7: pasang cron ----------
info "LANGKAH 7/8 — Pemasangan cron dari setup-cron.txt"
if [ ! -f "$CRON_FILE" ]; then
  err "File $CRON_FILE tidak ditemukan!"
  exit 1
fi

SHELL_CRONS=()
AGEN_CRONS=()
while IFS= read -r line || [ -n "$line" ]; do
  case "$line" in \#*|"") continue ;; esac
  jadwal="$(echo "$line" | cut -d'|' -f1 | xargs)"
  perintah="$(echo "$line" | cut -d'|' -f2 | xargs)"
  deskripsi="$(echo "$line" | cut -d'|' -f3 | xargs)"
  tipe="$(echo "$line" | cut -d'|' -f4 | xargs)"
  if [ "$tipe" = "shell" ]; then
    SHELL_CRONS+=("$jadwal $perintah  # $deskripsi")
  else
    AGEN_CRONS+=("$jadwal | $deskripsi")
  fi
done < "$CRON_FILE"

echo ""
echo "Cron tipe SHELL yang akan dipasang (${#SHELL_CRONS[@]}):"
for c in "${SHELL_CRONS[@]}"; do echo "  - $c"; done
echo ""
if tanya_ya_tidak "Pasang ${#SHELL_CRONS[@]} cron di atas ke crontab?"; then
  TMP_CRON="$(mktemp)"
  crontab -l 2>/dev/null | grep -v "YUNOBI-AUTO" > "$TMP_CRON" || true
  {
    echo "TZ=Asia/Jakarta"
    echo "# YUNOBI-AUTO: dipasang oleh setup.sh pada $(date '+%F %T')"
    for c in "${SHELL_CRONS[@]}"; do echo "$c"; done
  } >> "$TMP_CRON"
  crontab "$TMP_CRON"
  rm -f "$TMP_CRON"
  ok "Cron terpasang. Cek dengan: crontab -l"
else
  warn "Pemasangan cron dibatalkan user."
fi

echo ""
echo "Cron tipe AGEN (${#AGEN_CRONS[@]}) — TIDAK dipasang otomatis."
echo "Ini butuh runtime agen (Muse) + browser task. Daftarkan manual:"
for c in "${AGEN_CRONS[@]}"; do echo "  - $c"; done

# ---------- LANGKAH 8: verifikasi ----------
info "LANGKAH 8/8 — VERIFIKASI AKHIR"
echo ""
printf '%-42s %s\n' "KOMPONEN" "STATUS"
printf '%-42s %s\n' "------------------------------------------" "------"
cek() { # cek "label" "kondisi(0/1)"
  if [ "$2" -eq 0 ]; then printf '%-42s \033[1;32m%s\033[0m\n' "$1" "OK";
  else printf '%-42s \033[1;33m%s\033[0m\n' "$1" "PERLU AKSI MANUAL"; fi
}
command -v ffmpeg >/dev/null 2>&1;            cek "ffmpeg" $?
command -v python3 >/dev/null 2>&1;           cek "python3" $?
python3 -c "import requests,feedparser,PIL,yaml" 2>/dev/null; cek "modul python (requests/feedparser/pillow/yaml)" $?
[ -f ~/.hermes/.env ];                        cek "~/.hermes/.env (OpenRouter key)" $?
[ -f ~/.hermes/google-oauth-blogger.env ];    cek "~/.hermes/google-oauth-blogger.env" $?
[ -f ~/.hermes/blogger-tokens.json ];         cek "~/.hermes/blogger-tokens.json (OAuth Blogger)" $?
[ -f ~/.hermes/yt-growth/client_secret.json ]; cek "yt-growth client_secret.json" $?
[ "$(ls -1 ~/.hermes/yt-growth/tokens/ 2>/dev/null | wc -l)" -gt 0 ]; cek "token OAuth channel yt-growth" $?
[ -f ~/workspace/blog-otomatis/config.json ]; cek "blog-otomatis/config.json" $?
[ -f ~/workspace/blog-otomatis/jalan.sh ];    cek "blog-otomatis/jalan.sh" $?
[ -f ~/workspace/youtube-otomatis/ffmpeg-queue.sh ]; cek "youtube-otomatis/ffmpeg-queue.sh" $?
crontab -l 2>/dev/null | grep -q "YUNOBI-AUTO"; cek "cron terpasang" $?
[ "$(timedatectl show 2>/dev/null | grep -c 'Timezone=Asia/Jakarta')" -gt 0 ]; cek "timezone Asia/Jakarta" $?

echo ""
if [ "${#TERLEWAT[@]}" -gt 0 ]; then
  warn "Kredensial yang dilewati (isi nanti lalu jalankan ulang langkah 4 manual):"
  for t in "${TERLEWAT[@]}"; do echo "  - $t"; done
  echo ""
fi
echo "====================================================================="
echo " SELESAI. Yang masih PERLU AKSI MANUAL ada di daftar di atas +"
echo " panduan langkah 6. Dokumentasi lengkap: docs/ di repo ini."
echo "====================================================================="
