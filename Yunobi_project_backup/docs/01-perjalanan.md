# 01 — Perjalanan 2026-09-30 → 2026-10-08

Kronologi pivot dan keputusan besar. Detail harian ada di `~/memory/2026-10-*.md`.

## 2026-09-30 — Fondasi
- Yunobi memperkenalkan diri via WhatsApp. Nama asisten: "Yunobi bot agent".
- Hermes Agent v0.21.5 + 9Router terinstal di VM; OpenRouter API key Yunobi divalidasi.
- Diagnosis: akun OpenRouter ~$0 (402 insufficient credits) — blocker utama tooling AI.
- 922 skill terinventaris di `~/.hermes/skills/`.

## 2026-10-01 — Pipeline blog lahir
- Pipeline konten blog dibangun: `tulis_ulang.py` (bloggingskills: humanize + SEO),
  OpenRouter free-tier 50 req/hari/akun, rotasi 9 key ≈ 450 req/hari.
- Growth: FAQ, 3 varian judul, alt gambar, caption_viral, trending, baca_juga,
  digest, evergreen, video_script, thread_gen, meme_gen.
- Push notification ditunda total (OneSignal tolak akses; PushEngage "ribet").

## 2026-10-02 — Koreksi user
- User koreksi: artikel harus **round-robin** antar blog (bukan satu blog dihabiskan dulu).

## 2026-10-03 — PIVOT BESAR: 1 Gmail + 5 blog baru
- User: stop 4 blog lama (CuanPintar, TeknoGebrakan, SehatBugar — KabarViral tetap),
  fokus ke 1 Gmail (akuntyunobi17@gmail.com) + 5 blog BARU.
- OAuth Blogger API berhasil (token di `~/.hermes/blogger-tokens.json`).
- Blogger API v3 **tidak bisa buat blog baru** → user buat manual 5 blog.
- **Google batasi posting via Blogger API** (pelanggaran kebijakan, global sejak 2 Okt).
  Jalur aktif diganti: **posting via web UI** (`posting_web.py` → instruksi →
  browser task login khususstokyunobi@gmail.com).
- Tema v1.19 (5 varian warna) terpasang di semua blog via browser.
- Ekspansi: +4 blog (WisataIndo, KulinerNusantara, OtomotifInfo, PendidikanCerdas).
  Total **10 blog aktif**.
- Shopee Affiliate terisi: 16 link afiliasi, komisi tertinggi buku 81,5%.
- Promo sosmed afiliasi: `promo_produk.py` + `share_promo.py`, 5 produk/hari ke
  4 akun (IG @beritaviraldotcom, Threads ×2, FB Page BeritaViraldotcom).
- Cron `blog-otomatis-harian` 15:11 WIB.

## 2026-10-04 — Verifikasi pagi
- Cron `verifikasi-pagi-blog` 17:11: verifikasi artikel via feed publik + cek bounce Gmail.

## 2026-10-05 — Channel baru + aturan main
- **Strange Tales** (@StrangeTales-g6n): channel shorts Bahasa Inggris, voice Miles,
  3 shorts/hari, target USA. Acuan gaya: Denis Shofiandi.
- **Lima Misteri** (@LimaMisteri): countdown "5 kejadian aneh" Bahasa Indonesia,
  ilustrasi AI orisinal, voice Mudiwa. Pola: bergantian long/shorts.
- 3 varian hook A/B/C per script (persiapan uji A/B YouTube).
- Trend radar YouTube (`trend_radar.py`, cron 13:11).
- Volume blog: user setuju **6 artikel/hari** (turun dari 13) — KabarViral selalu
  dapat 1, 5 lainnya rotasi.
- Voiceover Indonesia wajib **Mudiwa** (fasih natural, bukan dubbing).
- Aturan: tiap gambar WAJIB literal sesuai narasi.

## 2026-10-06 — Delegasi penuh + Tiny Builders
- User: "oke atur saja yang terbaik untuk saya" → **delegasi penuh operasional**.
- **Tiny Builders**: channel miniatur AI (satu-satunya channel boleh full AI video).
- Verifikasi HP YouTube **DITOLAK user** → pola upload bergantian jadi permanen;
  aturan **anti-mogok upload**: gagal karena limit → antrean JSON di `retry-queue/`,
  watchdog 20:00 eksekusi yang umurnya ≥23 jam.
- Klip video AI DITOLAK user ("biar awet token") → 11 channel non-agama kembali
  ke gambar AI; 4 channel agama tetap footage Pexels.
- VPS backup ditunda ("nanti aja").

## 2026-10-07 — Anti full-AI look + job-hunt
- Aturan **anti "full-AI look"** untuk monetisasi: film grain, SFX asli tersinkron,
  title card, pacing variatif, AI disclosure wajib.
- Format meme roasting ala @caveine DITOLAK user ("yaudah jangan di buat").
- User buka front personal: **job-hunt operator pabrik** (nama, TTL, HP, riwayat
  kerja asli diserahkan; lamaran dikirim dari Gmail-nya).

## 2026-10-08 — Puncak & kegagalan
- **7 skill GitHub terpasang** (marketingskills, last30days, humanizer, OpenMontage,
  affiliate-skills, youtube-marketing-skills, ai-agency) + diterapkan ke pipeline.
- **4 paket skill YouTube** terpasang (yutu, youtube-mcp, youtube-agent-skill,
  youtube-skills). Hasil pencarian: **tidak ada skill yang bisa bypass limit 24 jam**
  (server-side YouTube).
- **Toolkit yt-growth** selesai: OAuth 17/17 channel aktif, cron SEO mingguan.
- **PIVOT TikTok**: tempel produk butuh 600 followers (akun baru 5) → mode review
  DIHENTIKAN, ganti konten hiburan FYP (cron `tiktok-fyp-harian` 10:11).
- **Channel ke-18: InkTime** (@InkTime-d3t): explainer whiteboard, cron 16:11,
  video pertama 9 Okt.
- Avatar 18/18 channel terverifikasi custom (2 dibuat & dipasang hari ini).
- Blog gagal 4 hari (5–8 Okt): 3× restart drain, 1× kuota; run manual 8 Okt malam
  **6 artikel akhirnya tayang** (KabarViral 3, Otomotif 1, Pendidikan 1, Teknopedia 1).
- Promo afiliasi: 20 slot GAGAL total (Meta 403 semua — imbas penangguhan FB).
- Upload Kisah Dharma kena limit harian → antrean retry (total 16 video antre).
- Formula packaging judul/hook (`packaging-formulas.md`) live di 17 cron.
