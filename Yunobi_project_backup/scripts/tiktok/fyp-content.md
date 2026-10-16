# FYP Content Bible — @ngeweb.yuk (mode kejar followers)

## Misi
600 followers (sekarang: 5). Selama belum 600, upload konten hiburan viral.
Setelah user mengonfirmasi 600 followers → aktifkan kembali cron `tiktok-shop-review-harian` (mode review produk).

## Format rotasi (pilih 1 per hari, jangan ulang format 2 hari beruntun)
1. **Mini drama bersambung** — "Tetangga Kepo" / "Drama Anak Kos": 25-35 dtk, akhiri dengan cliffhanger + teks "Part 2 besok — follow biar nggak ketinggalan". Ini pendorong follow utama.
2. **Komedi skit relatable** — situasi sehari-hari yang bikin ngakak/ngangguk (POV).
3. **Tebak-tebakan** — pertanyaan jebakan di hook, jawaban di akhir video (completion rate tinggi).
4. **Fakta unik** — 3 fakta mengejutkan, tempo cepat.

## Aturan naskah (dari tiktok-skills + viral-hooks)
- Hook 0-3 dtk: kalimat pertama HARUS bikin penasaran/ketawa. Rotasi trigger: curiosity, negation, specificity, confession, contrarian.
- Bahasa Indonesia santai, gaya ngobrol (tanpa pola AI: tanpa "di era digital", tanpa list kaku).
- Drama: 1 konflik kecil per episode, cliffhanger di 3 detik terakhir.
- Durasi total 25-35 detik.

## Produksi
1. Tulis naskah + tentukan episode/series (lanjutkan nomor episode dari fyp-history.json untuk series bersambung).
2. 3 klip via media.generate_video: aktor AI Indonesia natural, setting rumahan/kos, vertical, pencahayaan natural. Prompt Inggris detail per adegan.
3. Voiceover: tts skill, Bahasa Indonesia, suara natural (sesuaikan karakter: narator / dialog).
4. Rakit via ~/workspace/youtube-otomatis/ffmpeg-queue.sh + film grain halus.
5. Simpan: output/fyp-{format}-{YYYYMMDD}.mp4 + caption .txt.
6. Posting via Taisly: `taisly posts:create --video <file> --platforms 6ac71c80572b2159e0a2f190 --description "<caption>"`. Cek status via `taisly posts:status --id <historyId>`.
7. Update fyp-history.json: {tanggal, format, judul, episode}.

## Caption
Hook 1 baris + hashtag: #fyp #dramaindonesia / #komedi / #tebaktebakan (sesuai format) + #viral #tiktokindonesia. Untuk drama bersambung tambah: "Part {n} besok, follow dulu!"

## Laporan ke user
Judul + format + status posting Taisly (ok/gagal + historyId). Tambahkan SELALU di akhir: "Followers sekarang berapa? Kabari saya kalau sudah 600 biar langsung mulai mode review produk."
