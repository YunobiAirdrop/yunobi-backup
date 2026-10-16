# Formula Packaging YouTube (judul + hook) — WAJIB dipakai saat bikin judul/deskripsi/hook

Diadaptasi dari riset packaging 2026 (korpus 214 video). Prinsip inti: **CTR × retensi**.
Judul yang menang klik tapi penonton kabur <30 detik = penalti algoritma. Judul harus
jujur: tidak boleh menjanjikan lebih dari yang dibuka di 30 detik pertama.

## FORMULA JUDUL (pilih 1 yang cocok dengan isi video, buat 3-5 varian)

- **Y1 Curiosity-Gap:** hasil mengejutkan yang mekanismenya disembunyikan.
  Contoh: "Kenapa Piramida Dibangun dengan Presisi Mustahil?" / "Fenomena Ini
  Melanggar Hukum Fisika — Ilmuwan Tak Bisa Menjelaskan"
- **Y2 Number/Listicle:** angka konkret + payoff jelas.
  Contoh: "7 Trik Edit yang Melipatgandakan Retensi (Nomor 4 Cuma 10 Menit)"
- **Y3 How-I Outcome:** hasil nyata orang pertama + angka + timeframe.
  Contoh: "Saya Posting Shorts Tiap Hari 30 Hari. Ini Hasilnya."
- **Y4 Mistake/Negativity:** kesalahan mahal yang penonton lakukan (loss aversion).
  Contoh: "Stop Export 1080p. Kamu Buang Setengah Views-mu."
- **Y5 Transformation:** before → after + timeframe.
  Contoh: "Saya Meditasi 30 Hari. Ini yang Berubah."
- **Y6 Versus:** dua opsi bernama diadu (bagus untuk search).
  Contoh: "Borobudur vs Angkor Wat: Mana yang Lebih Megah?"
- **Y11 Third-Party Success Story:** orang lain + angka besar + dari nol.
  Contoh: "How a 16-Year-Old Built an AI Startup" → versi ID: "Anak 16 Tahun
  Membangun Startup AI"

## ATURAN JUDUL (keras)
- Maks 100 karakter, ideal 40-60 (mobile kepotong ~60 karakter).
- Kata penentu klik di DEPAN, bukan setelah titik dua di karakter 70.
- Judul dan thumbnail DILARANG mengulang kata yang sama — bagi tugas: yang
  ditunjuk thumbnail tidak ditulis di judul, dan sebaliknya.
- 1 angka spesifik menaikkan CTR ("dalam 28 hari" > "dengan cepat").
- Tanpa ALL CAPS, maks 1 emoji, tanpa clickbait yang tidak ditepati video.
- Bahasa Inggris untuk channel EN, Bahasa Indonesia untuk channel ID.

## FORMULA HOOK PEMBUKA (retensi)
- **Long (30 detik pertama):** Y7 Restate-and-Raise (ulangi janji judul dengan
  bahasamu + naikkan taruhan), Y8 Cold-Open (tunjukkan momen puncak 3-8 detik
  dulu, baru kembali ke awal), Y9 Question-and-Contract (jawab cepat sebagian,
  janji bonus kalau nonton sampai habis). DILARANG: "welcome back", intro
  animasi 15 detik, basa-basi.
- **Shorts (3 detik pertama):** langsung kalimat/frame paling menegangkan,
  tanpa greeting tanpa logo. Contoh: "pengaturan ini melipatgandakan views dan
  default-nya mati". Teks on-screen di kalimat hook (penting untuk yang nonton
  tanpa suara). Akhir dibuat nge-loop natural.

## ATURAN DESKRIPSI (SEO)
- 150 karakter pertama = hook + keyword utama (ini yang tampil di hasil search).
- Keyword utama juga dalam 40 karakter pertama JUDUL.
- Long: tambahkan bab/chapter + 1-2 kalimat opini pribadi + link relevan.
- Chapter: minimal 3, format `0:00 Judul` (tanpa kurung/tanda hubung), mulai dari 0:00.
- Tags: 20 tag, urut spesifik → luas, total <500 karakter, 1 kata jangan diulang 8x+.
- Jangan keyword-stuffing. Tulis untuk manusia dulu, mesin kedua.

## ATURAN HOOK LANJUTAN (dari ai-agency/video-hooks — untuk script & Shorts)
- **Ultra-spesifik atau bukan hook.** Bentuk kondisional: "if you <situasi +
  angka/alat/orang>" — penonton harus bisa jawab ya/tidak dari hidupnya
  sendiri. Contoh ID: "kalau kamu upload tiap hari tapi views stuck di 200,
  ini yang salah".
- **Tiga permukaan, satu klaim.** Frame visual pertama + teks on-screen +
  kalimat yang diucapkan = klaim yang SAMA. Penonton yang lihat A, baca B,
  dengar C akan pergi — bukan karena bosan, tapi bingung.
- **Konfirmasi klik 5 detik pertama.** Sebut subjek yang dijanjikan judul
  dengan bahasa penonton (bukan mengulang judul kata per kata).
- **5 mekanisme hook** (tulis 3+ varian per video, beda mekanisme, tiap varian
  dinilai risiko drop-off): kejut/kontradiksi, agitasi masalah, story open,
  curiosity gap, social proof.
- **Hook membuka loop, tidak menutupnya.** Jangan jawab di hook — payoff-nya
  di body. Kalau body cuma mengulang hook = clickbait = penonton kabur.
- **Maks 1 "bukan X, melainkan Y" per script.** Lebih dari itu = bau AI,
  kedengaran di telinga penonton.
- **Angka = digit, dan harus nyata/terukur.** Jangan mengarang angka.

## STRUKTUR SCRIPT (dari youtube-agent-skill/yt-script — wajib untuk long-form)
- **15 detik pertama = segalanya.** 3 tugas: konfirmasi klik yang dijanjikan
  judul, buka pertanyaan yang tak bisa ditutup penonton, buktikan payoff ada.
- **Hook: tulis 5, simpan 2 terbaik** (naik dari 3 varian). Nilai tiap hook:
  spesifisitas, menyapa masalah penonton, taruhan, curiosity, keringkasan.
  Tool: `python3 ~/workspace/skills/youtube-agent-skill/skills/yt-script/hookscore.py --hook "..."`
- **The turn (0:15-0:45):** 1 kalimat apa yang akan dilakukan video, lalu
  LANGSUNG kerjakan. DILARANG: "sebelum mulai", intro channel, minta
  subscribe di awal — ini penyebab tunggal terbesar jurang 0:30.
- **Body:** 1 ide per beat. Tiap beat tulis **[ON SCREEN: ...]** — apa yang
  terlihat, bukan cuma yang diucapkan. Talking head tanpa visual = podcast.
- **Payoff:** deliver janji hook secara eksplisit ("ini settingnya, ada di
  deskripsi").
- **Close:** 1 ajakan saja. Bukan tiga.

## ATURAN THUMBNAIL (dari youtube-agent-skill/yt-package)
- Judul + thumbnail = SATU unit. Thumbnail DILARANG mengulang kata di judul
  (bagi tugas: janji yang sama, kata berbeda).
- Teks thumbnail MAKS 3 kata — kata ke-4 jadi abu-abu tak terbaca di feed.
- Maks 2 kata ALL-CAPS per judul, lebih dari itu terbaca spam.
- Batas potong: 60 karakter (desktop search), 40 karakter (feed HP).
- **Tulis 10 judul, saring 2 terbaik.** Tool lint:
  `python3 ~/workspace/skills/youtube-agent-skill/skills/yt-package/title.py --title "..." --thumb "KATA THUMB"`
  (cek duplikasi judul-thumbnail, angka konkret, batas karakter).

## BANK HOOK SHORTS (dari viral-hooks-skill — 100 formula, 10 trigger)
Referensi: `~/workspace/skills/viral-hooks-skill/hooks-database.md`.
10 kategori: Curiosity Gap, Contrarian/Pattern-Interrupt, Authority & Proof,
Emotional Trigger, Listicle & Value Stack, Question Hooks, Story & Narrative,
Negation/Myth Buster, Specificity & Data, Personal Confession.
Saat bikin 3 varian hook Shorts, ambil dari 3 kategori BERBEDA.

## ATURAN CAPTION & LOOP SHORTS (dari vidmoat-skills)
- **Safe zone 9:16:** caption di atas 22% bawah (UI TikTok/Reels menutup
  ~400-420px) dan di bawah 12% atas. Jangan menutup wajah atau teks lain.
- **Caption:** 3-4 kata per baris (punchy), ikuti kata yang diucapkan —
  jangan mengarang teks.
- **Seamless loop:** frame terakhir harus nyambung ke frame pertama
  (posisi/gerak/suara). Potong keras di seam — JANGAN fade (fade = penanda
  loop). Energi konstan, tanpa teks "awal". Audio ikut loop atau silent;
  musik dipotong per birama utuh, tanpa fade.

## SKOR IDE TOPIK (dari youtube-marketing-skills/ideate — untuk trend-radar)
- Kesenjangan freshness: video topik ini di SERP sudah 2+ tahun = peluang.
- Demand terbukti: keyword punya volume (autocomplete/YouTube search).
- Diferensiasi: angle yang kompetitor belum pakai.
- Prioritas: 🔴 minggu ini / 🟡 bulan ini / 🟢 backlog.
