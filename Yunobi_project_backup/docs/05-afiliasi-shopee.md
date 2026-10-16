# 05 — Afiliasi Shopee

## Produk

- **36 produk** di `share_promo.py` + 36 foto di `promo_img/` (blog-otomatis/).
- Rotasi berbasis riwayat (`promo_history.json`): **7 hari tanpa produk berulang**.
- 16 link afiliasi dari dashboard; 17/18 box `afiliasi.json` terisi
  (ekonomibisnis kosong). Komisi tertinggi: buku 81,5%, skincare 80%, vitamin 77%.
- ⚠️ **Komisi tidak cair sampai user lengkapi info pembayaran & pajak**
  di affiliate.shopee.co.id.
- Link di caption IG **tidak bisa diklik** (user sudah tahu; X/Threads lebih baik
  untuk klik tapi user pilih IG).

## Pipeline promo harian

1. `promo_produk.py` — gambar promo profesional.
2. Video presenter AI (gaya manusia, bukan Ken Burns): 5 video/hari, satu/produk.
   Format dikunci: **20 detik, 2 segmen** (review + pakai produk), voiceover WAJIB
   Indonesia. Lip-sync tidak 100% sempurna (keterbatasan tool gratis) — user terima.
   Tool berbayar DITOLAK — HARUS gratis.
3. `share_promo.py` — rotasi 5 produk/hari ke 4 akun:
   IG @beritaviraldotcom, Threads @beritaviraldotcom + @ngewebyuk,
   FB Page BeritaViraldotcom.
   Caption: 6 framework (cerita, before/after, masalah-solusi, hot take,
   listicle, rekomendasi jujur) + manfaat per produk. Hashtag wajib.

## Aturan posting ber-approval

- IG/FB/Threads writes memicu **runtime user-approval** di detached run
  (pending_user_confirmation) → status "menunggu persetujuan", jangan bypass.
  `--dry-run` untuk list judul antrean di laporan.
- Run yang ter-SIGTERM: `posting_promo_*.py` me-retry SEMUA slot non-TERPOSTING
  saat dijalankan ulang → jangan jalankan ulang mentah-mentah (duplikat).
  Pakai skrip `_lanjutan` khusus slot yang belum dicoba + dedupe per (produk, akun).
- **Insiden 2026-10-08**: 20 slot gagal total (15 timeout approval + 5× 403) —
  retry 15 slot: SEMUA ditolak server Meta (HTTP 403, digate server-side).
  Kemungkinan imbas penangguhan FB. Coba lagi besok.

## Cron

- `promo-afiliasi-harian` — daily 17:11 WIB (goal: radar-cuan-affiliate-product-automation)
- `shopee-video-harian` — daily 19:11 WIB: paket video Shopee (5 video `_wa.mp4` +
  caption siap-copy + link afiliasi) untuk upload manual via aplikasi Shopee tab Video.
