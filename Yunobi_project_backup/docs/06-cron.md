# 06 — Daftar Cron Aktif

Semua cron timezone **Asia/Jakarta**. File definisi: `~/workspace/goals/*/crons/`.
Ketukan persetujuan user: **20:00–23:00 WIB** tiap malam (upload/posting).

## Blog & konten (goal: kabarviral-automated-news-blog)

| Cron | Jadwal | Tugas |
|---|---|---|
| blog-otomatis-harian | daily 15:11 | Pipeline 6 artikel/hari → instruksi webpost → browser task posting |
| verifikasi-pagi-blog | daily 17:11 | Verifikasi artikel via feed publik + cek bounce Gmail |
| share-ig-harian | daily 20:11 | IG reel → video_script → thread_gen → FB → Threads |
| trend-radar-youtube | daily 13:11 | Riset demand YouTube per 10 niche (silent jika sukses) |
| yt-seo-refresh-mingguan | weekly Senin 09:00 | Refresh metadata via yt-growth (mulai 12 Okt) |
| monitor-token-mingguan | weekly Senin 09:11 | Cek kesehatan token |
| refresh-mingguan | weekly Minggu 18:00 | Refresh rutin |
| ekspansi-blog-2mingguan | tiap 336 jam (mulai 17 Okt) | Buat 10 blog baru via browser + tema + config |

## YouTube — 18 channel (daily 16:11, kecuali disebut)

| Cron | Channel |
|---|---|
| horor-harian | Kisah Horor @KisahPOV |
| youtube-pov-harian | @ceritarakyat862 |
| lima-misteri-harian | @LimaMisteri |
| kisahdharma-harian | @KisahDharma |
| jejakislami-harian | @JejakIslami-h3d |
| kisahalkitab-harian | @KisahAlkitab-k9j |
| jejakbuddha-harian | @JejakBuddha |
| tinybuilders-shorts-harian | @tinybuilders-d5z (goal: channel-youtube-internasional…) |
| inktime-harian | @InkTime-d3t (mulai 9 Okt) |
| strangetales-shorts-harian | @StrangeTales-g6n (3 shorts/hari) |
| empires-en-harian | @AncientEmpiresTV |
| history-en-harian | @EchoesOfThePast-e9n |
| horror-en-harian | @TalesOfDreadTV |
| mind-en-harian | @TheDarkMindFiles-s6n |
| mystery-en-harian | @MysteryShadowsTV |
| space-en-harian | @CosmosUnknownTV |
| truecrime-en-harian | @TrueCaseFilesTV |
| weird-en-harian | @BizarreWorldDaily |

Pola tiap cron channel: baca `protokol-viral.md` + `packaging-formulas.md` →
produksi video (ffmpeg via `ffmpeg-queue.sh`) → upload via browser task
(ketukan user) → status "Terjadwal" besok 19:00 WIB (Strange Tales: 21:00/03:00/07:00).
Gagal karena limit → tulis `retry-queue/{channel}-YYYY-MM-DD.json`.

## Pendukung YouTube

| Cron | Jadwal | Tugas |
|---|---|---|
| watchdog-retry-upload-youtube | daily 20:00 | Eksekusi antrean retry umur ≥23 jam via browser task |
| balas-komentar-youtube-pagi | daily 09:11 | Cek 12 channel, balas + seed diskusi |
| balas-komentar-youtube-malam | daily 21:11 | Sama, shift malam |

## Afiliasi & sosmed

| Cron | Jadwal | Tugas |
|---|---|---|
| promo-afiliasi-harian | daily 17:11 | 5 produk/hari: gambar + video AI + caption → 4 akun (approval) |
| shopee-video-harian | daily 19:11 | Paket 5 video `_wa.mp4` + caption + link (upload manual) |
| tiktok-fyp-harian | daily 10:11 | Konten hiburan FYP @ngeweb.yuk via Taisly (otomatis) |
| tiktok-shop-review-harian | daily 09:11 | DISABLED — aktif lagi setelah 600 followers |
| tiktok-affiliate-harian | daily 10:11 | (lama, diganti fyp-harian) |
| tiktok-shop-ganti-produk | tiap 336 jam | Ingatkan kirim produk baru |

## Lainnya

| Cron | Jadwal | Tugas |
|---|---|---|
| harga-harian | daily 15:11 | Infografis harga harian |
| loker-harian | daily 15:11 | Listing loker → blog loker |
| resep-harian | daily 15:11 | Resep harian → IG |
| pantau-loker-fb | daily 08:11 | Pantau loker FB (goal: cv-dan-lamaran-kerja…) |

## Catatan

- Subagent TIDAK bisa `cron.update` dari konteksnya — perubahan cron harus dari
  side chat yang mengikat cron tersebut (cron yang deliver ke WhatsApp hanya bisa
  diubah dari chat itu).
- Jangan edit MEMORY.md dari cron; observasi ke `~/memory/YYYY-MM-DD.md`.
