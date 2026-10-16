# 03 — YouTube (18 Channel)

Semua channel di akun khususstokyunobi@gmail.com. Avatar 18/18 custom (terverifikasi 2026-10-08).

## Daftar channel

| # | Nama | Handle | Niche / Bahasa | Pola upload |
|---|---|---|---|---|
| 1 | Kisah Horor | @KisahPOV | horor ID, voice Mudiwa | long/shorts bergantian |
| 2 | Cerita Rakyat (POV Sejarah) | @ceritarakyat862 | sejarah ID, voice Mudiwa | long/shorts bergantian |
| 3 | Lima Misteri | @LimaMisteri | countdown misteri ID, voice Mudiwa | long/shorts bergantian |
| 4 | Kisah Dharma | @KisahDharma | Hindu, footage Pexels | long/shorts bergantian |
| 5 | Jejak Islami | @JejakIslami-h3d | Islam, footage Pexels | long/shorts bergantian |
| 6 | Kisah Alkitab | @KisahAlkitab-k9j | Kristen, footage Pexels | long/shorts bergantian |
| 7 | Jejak Buddha | @JejakBuddha | Buddha, footage Pexels | long/shorts bergantian |
| 8 | Tiny Builders | @tinybuilders-d5z | miniatur AI (satu-satunya full-AI video) | long/shorts bergantian |
| 9 | InkTime | @InkTime-d3t | explainer whiteboard EN | harian (mulai 9 Okt) |
| 10 | Strange Tales | @StrangeTales-g6n | shorts EN, voice Miles, target USA | 3 shorts/hari (21:00/03:00/07:00 WIB) |
| 11 | Ancient Empires | @AncientEmpiresTV | sejarah EN | harian |
| 12 | Echoes of the Past | @EchoesOfThePast-e9n | history EN | harian |
| 13 | Tales of Dread | @TalesOfDreadTV | horror EN | harian |
| 14 | The Dark Mind Files | @TheDarkMindFiles-s6n | psikologi/mind EN | harian |
| 15 | Mystery Shadows | @MysteryShadowsTV | misteri EN | harian |
| 16 | Cosmos Unknown | @CosmosUnknownTV | luar angkasa EN | harian |
| 17 | True Case Files | @TrueCaseFilesTV | true crime EN | harian |
| 18 | Bizarre World Daily | @BizarreWorldDaily | weird EN | harian |

Jadwal tayang umum: **19:00 WIB** (prime time ID); Strange Tales ikut jam USA.

## Aturan ANTI-MOGOK upload (user: "atur saja asal jangan sampe mogok upload")

- Upload gagal karena **batas harian** → worker WAJIB tulis antrean JSON ke
  `youtube-otomatis/retry-queue/{channel}-YYYY-MM-DD.json` (bukan retry langsung).
- **Watchdog** `watchdog-retry-upload-youtube` (daily 20:00) mengerjakan antrean
  yang umurnya **≥23 jam** via browser task + ketukan user.
- Gagal sebab lain → retry segera saat itu juga.
- **Batas 24 jam channel baru & limit harian adalah server-side YouTube —
  tidak ada tool/skill yang bisa bypass.** Satu-satunya jalan: verifikasi HP
  (user menolak) atau tunggu 24 jam + retry otomatis.
- Upload via browser task butuh **ketukan persetujuan user 20:00–23:00 WIB**.
  Jangan biarkan ketukan terbuang untuk upload yang pasti gagal.

## Aturan produksi

- **Render**: SEMUA script video WAJIB via `youtube-otomatis/ffmpeg-queue.sh`
  (bukan bare `ffmpeg`) — semaphore maks 2 konkuren, VM 7.7GB RAM rawan OOM.
  Build berat: scale 1280x720 + `-preset veryfast` (pelajaran OOM 2026-10-05).
- **Gambar literal**: tiap gambar WAJIB menunjukkan objek/aksi yang disebut narasi.
- **Channel rohani**: WAJIB verifikasi frame per klip Pexels SEBELUM assembly —
  search "church"/"bible" sering mengembalikan kuil Hindu/Buddha. Keyword aman:
  alam/gurun/langit/lilin. 1 klip boleh dipakai 2× bila klip bersih <18.
- **Anti full-AI look** (monetisasi): film grain halus, SFX rekaman ASLI tersinkron,
  title card, chapter/beat orisinal, pacing variatif. AI disclosure WAJIB dicentang.
- Voice: Indonesia = **Mudiwa** (wajib fasih natural); Inggris = voice EN.
- Hook: 3 varian A/B/C per script; delegasi penuh ke asisten ("pake yang bakal rame").
- Packaging: `packaging-formulas.md` + `protokol-viral.md` dibaca 17 cron tiap hari.
- Shorts: hashtag maks 3 di AKHIR JUDUL. Long: hashtag di deskripsi.
- File >~100MB ditolak upload via browser task → kompres dulu (target <100MB).

## yt-growth toolkit (gratis, buatan sendiri)

`youtube-otomatis/yt-growth/`: `auth.py` (OAuth per channel), `analytics.py`
(views/retensi — CTR/impresi TIDAK didukung API), `yt_push.py` (update metadata,
default dry-run), `channels.yaml` (17 channel). **17/17 token OAuth aktif**
(user klik manual via HP). Cron `yt-seo-refresh-mingguan`: Senin 09:00 WIB
(run perdana 12 Okt).

## Komentar

Cron `balas-komentar-youtube-pagi` (09:11) & `-malam` (21:11): cek 12 channel,
seed diskusi bila 0 komentar. Pin komentar butuh verifikasi HP (2 channel) —
user menolak, jangan tawarkan lagi.
