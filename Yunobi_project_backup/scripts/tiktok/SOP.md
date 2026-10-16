# SOP — Video Review TikTok Shop Affiliate (@ngeweb.yuk)

## Konsep
Video review pemakaian produk oleh AI presenter (~30 detik, 3 klip @ ~10 dtk).
Alur video TETAP setiap kali (4 beat), tapi isi/hook/angle BERBEDA tiap video.

### 4 beat (urutan tetap)
1. **HOOK (0-3 dtk)** — kalimat pembuka 1 baris. Rotasi formula hook (pilih berdasarkan `varian % 5`):
   - 0 curiosity: "Jujur... aku kaget pas pertama kali coba ini."
   - 1 negation: "Stop beli yang mahal dulu sebelum lihat ini."
   - 2 specificity: "Cuma RpXX ribu, tapi efeknya kayak barang jutaan."
   - 3 confession: "Aku skeptis banget awalnya, ternyata..."
   - 4 contrarian: "Semua orang salah pakai ini selama ini."
2. **DEMO PEMAKAIAN (3-18 dtk)** — presenter memakai/mendemokan produk (lihat field `demo` di produk.json). Sebutkan 2-3 poin keunggulan (field `poin`) dengan bahasa santai natural, bukan bahasa iklan.
3. **KOMENTAR TERBAIK (18-25 dtk)** — "Kata yang udah beli:" + 2 testimoni (field `testimoni`, gaya komentar pembeli asli).
4. **CTA (25-30 dtk)** — "Cek keranjang kuning di bawah, lagi diskon dari RpX jadi RpY."

### Rotasi produk
- `history.json`: `{"posted": [{"id": "...", "tanggal": "YYYY-MM-DD", "varian": N}]}`
- Tiap run: pilih produk yang BELUM pernah diposting. Jika semua sudah diposting 1x → mulai siklus baru dengan `varian+1` (varian = jumlah siklus selesai), dan sertakan di laporan: "Semua produk sudah diposting — siklus baru dengan angle video berbeda."
- `varian` dipakai untuk merotasi hook (varian % 5) dan angle naskah.

### Produksi video
1. Tulis naskah voiceover Indonesia (±30 dtk, ±70 kata) mengikuti 4 beat.
2. Generate 3 klip via media.generate_video (maks 6 klip/pesan — pakai 3):
   - Klip 1 (hook): close-up presenter wanita Indonesia natural, kasual, ekspresi kaget/penasaran, memegang produk. Prompt: "Indonesian woman in her 20s, natural casual home setting, holding [produk], surprised curious expression, close-up, vertical video, natural lighting"
   - Klip 2 (demo): adegan pemakaian sesuai field `demo` produk.
   - Klip 3 (testimoni+CTA): presenter tersenyum memegang produk ke arah kamera, gestur menunjuk ke bawah (keranjang kuning).
3. Voiceover: tts skill, Bahasa Indonesia, suara perempuan natural (Mudiwa bila tersedia).
4. Rakit: gabung 3 klip + voiceover via ffmpeg. WAJIB lewat `~/workspace/youtube-otomatis/ffmpeg-queue.sh` (bukan ffmpeg langsung). Tambah film grain halus (noise filter) + warna natural — hindari look plastik-AI.
5. Simpan: `output/review-{id}-{YYYYMMDD}-v{varian}.mp4` + caption `.txt`.

### Caption
Baris 1: hook. Baris 2-3: 1 keunggulan + testimoni singkat. CTA: "Cek keranjang kuning". Hashtag: #racunbelanja #tiktokshop #racuntiktok #fyp #belanjaditiktok + 1 hashtag kategori produk.

### Batasan jujur (jangan janjikan ke user)
- Upload + tempel produk (keranjang kuning) HARUS user lakukan di aplikasi TikTok (proteksi anti-otomatisasi TikTok memblokir jalur web/API).
- Testimoni ditulis gaya komentar pembeli berdasarkan keunggulan produk (bukan scrape review asli — review TikTok tidak bisa diakses dari browser).
- Komisi yang dipakai = data screenshot user 2026-10-08; bisa berubah sewaktu-waktu.

### Laporan ke user (tiap run)
Kirim: file video + caption + "Produk: {nama} — Komisi Rp{komisi} — Harga Rp{harga}. Upload di aplikasi TikTok dan tempel produk via keranjang kuning."
