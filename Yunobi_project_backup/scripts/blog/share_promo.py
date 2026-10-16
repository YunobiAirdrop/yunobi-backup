#!/usr/bin/env python3
"""Promo afiliasi harian ke sosmed: 5 produk/hari/akun, rotasi tiap hari.
Akun: IG @falcon_esport537, Threads @beritaviraldotcom + @ngewebyuk, FB Page BeritaViraldotcom.
Konten: gambar promo profesional + video 9:16 + caption + link afiliasi.
Pakai: share_promo.py [--dry-run] [--produk N (1-5, default 5)]
CATATAN: posting IG/FB/Threads butuh approval user (aturan runtime).
"""
import json, os, sys, time, subprocess, random, uuid
from datetime import datetime, timezone, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from promo_produk import bikin_promo
from video_gen import bikin_video

WIB = timezone(timedelta(hours=7))
IMG_DIR = os.path.join(BASE, "promo_img")
OUT_DIR = os.path.join(BASE, "promo_out")
os.makedirs(OUT_DIR, exist_ok=True)

# --- akun ---
IG_ID = "17841462795414201"          # falcon_esport537
THREADS_1 = "17841423460796922"      # beritaviraldotcom
THREADS_2 = "17841442711837842"      # ngewebyuk
FB_PAGE = "1347201611814398"         # BeritaViraldotcom

# --- katalog produk: (file_gambar, nama, harga, warna, link, hashtag) ---
PRODUK = [
    ("skincare-jrg.jpg", "Cream JRG Original BPOM 30gr", "Rp28.000", "#E91E63",
     "https://s.shopee.co.id/9V1w99dZY0", ["skincare", "pemutihwajah", "glowing", "skincareviral"]),
    ("skincare-paket.jpg", "Paket Cream JRG Glowing BPOM", "Rp76.000", "#E91E63",
     "https://s.shopee.co.id/4fwgOHU4Q8", ["skincare", "paketskincare", "glowing", "perawatanwajah"]),
    ("tws-gen4.jpg", "ThePods Gen 4 TWS Bluetooth ANC", "Rp339.520", "#2196F3",
     "https://s.shopee.co.id/8AWYYltgKB", ["tws", "earphone", "gadget", "bluetooth"]),
    ("tws-pro3.jpg", "ThePods Pro 3 TWS ANC Original", "Rp339.520", "#2196F3",
     "https://s.shopee.co.id/8AWYYmXYQW", ["tws", "headset", "gadgetviral", "earbuds"]),
    ("panci-castiron.jpg", "Panci Wajan Cast Iron Pancaguna", "Rp364.100", "#FF6B35",
     "https://s.shopee.co.id/7faHxkFSgS", ["alatmasak", "dapur", "masak", "perabotdapur"]),
    ("rebus-telur.jpg", "Alat Rebus Telur Elektrik", "Rp155.100", "#FF6B35",
     "https://s.shopee.co.id/40gzb1K9Fi", ["dapur", "alatdapur", "masakpraktis", "perabotrumah"]),
    ("nb-freshfoam.jpg", "New Balance Fresh Foam X 2025", "Rp850.000", "#FF9800",
     "https://s.shopee.co.id/1gJ4onHvca", ["sepatu", "sepatulari", "newbalance", "running"]),
    ("nb-rebel.jpg", "New Balance Fuelcell Rebel V5", "Rp850.000", "#FF9800",
     "https://s.shopee.co.id/6VOKZgYrb7", ["sepatu", "sepatuolahraga", "lari", "sneakers"]),
    ("spion-koso.jpg", "Spion Koso Lipat Universal Motor", "Rp59.999", "#607D8B",
     "https://s.shopee.co.id/3qNZOxWSZe", ["aksesorismotor", "spion", "modifikasi", "otomotif"]),
    ("knalpot.jpg", "Knalpot Racing All Motor", "Rp1.500.000", "#607D8B",
     "https://s.shopee.co.id/9zyCkJDjgO", ["knalpot", "racing", "modifikasimotor", "otomotif"]),
    ("buku-medical.jpg", "English for Health Professionals", "Rp46.400", "#9C27B0",
     "https://s.shopee.co.id/6L4uNaqnMe", ["buku", "bukukesehatan", "belajar", "mahasiswa"]),
    ("buku-kesling.jpg", "Ilmu Kesehatan Lingkungan 2026", "Rp58.400", "#9C27B0",
     "https://s.shopee.co.id/7ptiAMGV9s", ["buku", "kesehatanlingkungan", "kuliah", "literasi"]),
    ("kantong-sepatu.jpg", "Kantong Sepatu Travelling Serut", "Rp8.800", "#009688",
     "https://s.shopee.co.id/8AWYYqwPC8", ["travel", "traveling", "perlengkapantravel", "liburan"]),
    ("pouch-travel.jpg", "Pouch Travel Organizer Serut", "Rp2.550", "#009688",
     "https://s.shopee.co.id/113O1h9k26", ["travel", "organizer", "pouch", "jalanjalan"]),
    ("vitamin-kucing.jpg", "Vitamin Minyak Ikan Kucing Omega 3&6", "Rp32.305", "#4CAF50",
     "https://s.shopee.co.id/7Ae1MyngRM", ["kucing", "pecintakucing", "vitaminkucing", "petshop"]),
    ("vitamin-cerna.jpg", "Vitamin Pencernaan Kucing", "Rp65.339", "#4CAF50",
     "https://s.shopee.co.id/50ZWn0PyQm", ["kucing", "kesehatanhewan", "petlovers", "catlover"]),
    # --- batch 2 (2026-10-03): 20 produk tambahan ---
    ("sabun-piring.jpg", "Sabun Cuci Piring 5 Liter Premium", "Rp12.000", "#00BCD4",
     "https://s.shopee.co.id/2gBc2APRvk", ["rumahtangga", "sabun", "dapur", "hemat"]),
    ("impact-wrench.jpg", "Impact Wrench Cordless Brushless 700NM", "Rp459.000", "#607D8B",
     "https://s.shopee.co.id/2LYldbPmWS", ["perkakas", "otomotif", "bengkel", "tools"]),
    ("tumbler.jpg", "Tumbler 900ml Stainless Steel", "Rp63.990", "#009688",
     "https://s.shopee.co.id/3LRIpS3LxT", ["tumbler", "botolminum", "stainless", "travel"]),
    ("gamis-karina.jpg", "Gamis Mewah Karina Dress Ceruty", "Rp125.000", "#E91E63",
     "https://s.shopee.co.id/5LCND9LjY8", ["gamis", "fashionmuslim", "dress", "ootd"]),
    ("gamis-kayla.jpg", "Gamis Kondangan Kayla Dress Viral", "Rp80.000", "#E91E63",
     "https://s.shopee.co.id/5LCND9vTuL", ["gamis", "kondangan", "dressviral", "fashion"]),
    ("dress-midi.jpg", "Aura Midi Dress Jumbo Busui Friendly", "Rp66.644", "#E91E63",
     "https://s.shopee.co.id/gQXeagX5M", ["dress", "fashion", "bajuwanita", "ootdhijab"]),
    ("mainan-sains.jpg", "Mainan Edukasi Sains Kayu Anak", "Rp98.000", "#FF9800",
     "https://s.shopee.co.id/9AP5mEEVt2", ["mainan", "edukasi", "anakkreatif", "montessori"]),
    ("puzzle-kayu.jpg", "Puzzle Kayu Edukasi Montessori", "Rp21.890", "#FF9800",
     "https://s.shopee.co.id/9pemZScr45", ["mainan", "puzzle", "anakpintar", "edukasianak"]),
    ("lcd-tablet.jpg", "LCD Drawing Tablet 8.5 inci Anak", "Rp17.575", "#FF9800",
     "https://s.shopee.co.id/6q1AzxJlFm", ["mainan", "gambaranak", "edukasi", "tablet"]),
    ("lcd-taiyo.jpg", "Taiyo LCD Drawing Tablet Anak", "Rp21.900", "#FF9800",
     "https://s.shopee.co.id/2LYldh5grV", ["mainan", "drawingtablet", "anak", "kreatif"]),
    ("armrest.jpg", "Armrest Pad USB Tisu Mobil Premium", "Rp117.900", "#607D8B",
     "https://s.shopee.co.id/4B0Pp5Rw85", ["aksesorismobil", "interiormobil", "otomotif", "nyetir"]),
    ("tongkat-tol.jpg", "Tongkat Tol Telescopic Portable", "Rp10.659", "#607D8B",
     "https://s.shopee.co.id/1qcV2o5cKQ", ["aksesorismobil", "tol", "praktis", "otomotif"]),
    ("toneup.jpg", "Perface Tone Up Cream BPOM Halal", "Rp38.800", "#E91E63",
     "https://s.shopee.co.id/4VdGDiznxx", ["skincare", "toneup", "bpom", "cerah"]),
    ("serum-hanasui.jpg", "HANASUI Power Bright Expert Serum", "Rp36.429", "#E91E63",
     "https://s.shopee.co.id/20vvF8eG2l", ["serum", "skincare", "brightening", "hanasui"]),
    ("keyboard-rk.jpg", "Royal Kludge RK R65 Gaming Keyboard", "Rp632.900", "#2196F3",
     "https://s.shopee.co.id/W77SOnHCS", ["keyboard", "gaming", "setup", "aksesorispc"]),
    ("keyboard-rexus.jpg", "Rexus SH600 Keyboard Gaming Mechanical", "Rp229.000", "#2196F3",
     "https://s.shopee.co.id/5q8doCxlr9", ["keyboard", "gaming", "mechanical", "pcgaming"]),
    ("kue-wijen.jpg", "Kue Wijen Renyah 500g", "Rp34.999", "#FF6B35",
     "https://s.shopee.co.id/5fpDbv3qSA", ["camilan", "kue", "jajanan", "oleholeh"]),
    ("kentang-mustofa.jpg", "Kentang Mustofa Renyah Gurih", "Rp33.740", "#FF6B35",
     "https://s.shopee.co.id/7KxRazSZaC", ["camilan", "kentang", "gurih", "jajananviral"]),
    ("cutter-mini.jpg", "Cutter Mini Portable Pastel Lucu", "Rp5.678", "#9C27B0",
     "https://s.shopee.co.id/1gJ4qaqd3A", ["stationery", "alattulis", "lucu", "sekolah"]),
    ("kalender-meja.jpg", "Kalender Abadi Meja + Tempat Pensil", "Rp30.000", "#9C27B0",
     "https://s.shopee.co.id/2BFLRWOP8E", ["stationery", "kantor", "kalender", "organizer"]),
]

# --- Manfaat spesifik per produk (Affitor viral-post-writer: spesifik > generik) ---
# Dipakai template caption framework; key = nama file gambar di PRODUK.
MANFAAT = {
    "skincare-jrg.jpg": "bantu cerahkan wajah kusam",
    "skincare-paket.jpg": "rangkaian lengkap buat glowing",
    "tws-gen4.jpg": "ANC peredam bising, baterai awet",
    "tws-pro3.jpg": "ANC + suara jernih buat daily",
    "panci-castiron.jpg": "panas merata, awet puluhan tahun",
    "rebus-telur.jpg": "telur matang sempurna tanpa ditunggu",
    "nb-freshfoam.jpg": "empuk banget buat lari harian",
    "nb-rebel.jpg": "ringan dan responsif buat speed",
    "spion-koso.jpg": "bisa dilipat, anti mentok",
    "knalpot.jpg": "suara gahar, tarikan enteng",
    "buku-medical.jpg": "bekal bahasa Inggris buat nakes",
    "buku-kesling.jpg": "referensi kuliah kesehatan lingkungan",
    "kantong-sepatu.jpg": "sepatu tetap rapi di koper",
    "pouch-travel.jpg": "barang kecil nggak tercecer",
    "vitamin-kucing.jpg": "bulu kucing lebih lebat",
    "vitamin-cerna.jpg": "pencernaan kucing lancar",
    "sabun-piring.jpg": "5 liter, awet berbulan-bulan",
    "impact-wrench.jpg": "buka baut 700NM tanpa effort",
    "tumbler.jpg": "900ml, dingin tahan lama",
    "gamis-karina.jpg": "bahan ceruty premium, jatuh anggun",
    "gamis-kayla.jpg": "model viral buat kondangan",
    "dress-midi.jpg": "ukuran jumbo dan busui friendly",
    "mainan-sains.jpg": "belajar sains sambil main",
    "puzzle-kayu.jpg": "asah logika anak ala montessori",
    "lcd-tablet.jpg": "gambar sepuasnya tanpa kertas berantakan",
    "lcd-taiyo.jpg": "coret-coret hemat kertas",
    "armrest.jpg": "sandaran tangan + USB + tempat tisu",
    "tongkat-tol.jpg": "bayar tol tanpa buka kaca lebar-lebar",
    "toneup.jpg": "wajah cerah instan, sudah BPOM halal",
    "serum-hanasui.jpg": "brightening dengan niacinamide",
    "keyboard-rk.jpg": "mechanical compact buat setup rapi",
    "keyboard-rexus.jpg": "mechanical murah meriah",
    "kue-wijen.jpg": "renyah 500 gram buat stok di rumah",
    "kentang-mustofa.jpg": "gurih renyah, nagih",
    "cutter-mini.jpg": "mini pastel, muat di pouch",
    "kalender-meja.jpg": "kalender abadi + tempat pensil",
}

# --- Template caption framework (Affitor/affiliate-skills: viral-post-writer) ---
# Aturan: hook di baris pertama | spesifik > generik | story > pitch | 1 CTA saja.
# DILARANG frasa kosong: "game-changer", "revolusioner", "terbaik sedunia".
def _cap_cerita(nama, harga, manfaat):
    return (f"Awalnya skeptis sama {nama}...\n\n"
            f"Ternyata {manfaat}, dan cuma {harga} aja. Nggak nyesel checkout 😭\n\n"
            f"Link-nya di sini 👇")

def _cap_before_after(nama, harga, manfaat):
    return (f"Sebelum kenal {nama}: ribet.\n"
            f"Sesudah: {manfaat}.\n\n"
            f"Harganya {harga} doang. Kenapa nggak dari dulu coba?! 😅\n\n"
            f"Checkout 👇")

def _cap_masalah(nama, harga, manfaat, kategori):
    return (f"Capek sama {kategori} yang gitu-gitu aja?\n\n"
            f"{nama}: {manfaat}. Harganya {harga} aja.\n\n"
            f"Solusinya ternyata segampang ini 👇")

def _cap_hottake(nama, harga, manfaat):
    return (f"Unpopular opinion: {nama} seharga {harga} ini lebih worth it\n"
            f"dari yang mahal-mahal.\n\n"
            f"Soalnya {manfaat}. Setuju nggak? 👀\n\n"
            f"Link 👇")

def _cap_listicle(nama, harga, manfaat):
    return (f"3 alasan {nama} laris manis:\n\n"
            f"1. {manfaat.capitalize()}\n"
            f"2. Harganya cuma {harga}\n"
            f"3. Rating pembelinya bagus-bagus\n\n"
            f"Nomor 1 sih yang bikin aku checkout 👇")

def _cap_rekomendasi(nama, harga, manfaat):
    return (f"Rekomendasi jujur (bukan iklan lebay):\n\n"
            f"{nama} — {manfaat}.\n"
            f"Harga {harga}.\n\n"
            f"Kekurangannya? Sejauh ini belum nemu yang fatal 😄\n\n"
            f"Buat yang butuh, link-nya 👇")

CAPTION_BUILDERS = [_cap_cerita, _cap_before_after, _cap_masalah,
                    _cap_hottake, _cap_listicle, _cap_rekomendasi]

HOOKS = [  # dipertahankan untuk kompatibilitas; caption baru pakai framework di atas
    "Jangan sampai kehabisan! 🔥",
    "Ini yang lagi viral diburu orang! 👀",
    "Harga segini, kualitas premium! ✨",
    "Stok terbatas, siapa cepat dia dapat! ⚡",
    "Racun Shopee hari ini! 🛒",
    "Wajib punya sih ini! 💯",
]

def pilih_produk(n=5):
    """Pilih n produk yang paling lama tidak dipromosikan (riwayat di promo_history.json).
    Menjamin produk tidak berulang dalam beberapa hari."""
    hist_path = os.path.join(BASE, "promo_history.json")
    hist = {}
    if os.path.exists(hist_path):
        try:
            hist = json.load(open(hist_path))
        except Exception:
            pass
    # urutkan produk berdasar kapan terakhir diposting (paling lama dulu)
    def terakhir(i):
        return hist.get(str(i), "2000-01-01")
    urutan = sorted(range(len(PRODUK)), key=terakhir)
    pilih = urutan[:n]
    # catat hari ini
    hari_ini = datetime.now(WIB).date().isoformat()
    for i in pilih:
        hist[str(i)] = hari_ini
    json.dump(hist, open(hist_path, "w"))
    return [PRODUK[i] for i in pilih]

def bikin_caption(p):
    fimg, nama, harga, _, link, tags = p
    manfaat = MANFAAT.get(fimg, "praktis dipakai sehari-hari")
    builder = random.choice(CAPTION_BUILDERS)
    if builder is _cap_masalah:
        body = builder(nama, harga, manfaat, tags[0] if tags else "produk")
    else:
        body = builder(nama, harga, manfaat)
    tag_str = " ".join(f"#{t}" for t in tags[:4])
    return (f"{body}\n🛒 {link}\n\n"
            f"#racunshopee #shopeehaul {tag_str}")

def siapkan_konten(p):
    """Generate gambar promo + video Ken Burns. Return (img_path, vid_path).
    Video presenter AI dibuat terpisah oleh agent via media.generate_video."""
    fimg, nama, harga, warna, _, _ = p
    src = os.path.join(IMG_DIR, fimg)
    ts = int(time.time() * 1000) % 100000000
    img_out = os.path.join(OUT_DIR, f"promo_{ts}.jpg")
    if not os.path.exists(src):
        # fallback: gambar polos
        from PIL import Image
        Image.new("RGB", (800, 800), (230, 230, 235)).save(src)
    bikin_promo(src, nama, harga, img_out, warna=warna)
    vid_out = os.path.join(OUT_DIR, f"promo_{ts}.mp4")
    try:
        bikin_video(img_out, vid_out)
    except Exception as e:
        print(f"  video gagal: {str(e)[:60]}")
        vid_out = None
    return img_out, vid_out

def post_ig(img, vid, caption):
    cmd = ["instagram-cli", "post-feed", "--account-id", IG_ID,
           "--file", vid or img, "--caption", caption]
    if vid:
        cmd += ["--cover", img]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return r.returncode == 0, r.stderr[:200]

def post_threads(account_id, img, vid, caption):
    teks = caption[:480]
    cmd = ["threads-cli", "publish-post", "--account-id", account_id, "--text", teks]
    media = {"file": vid or img}
    if vid:
        media["cover"] = img
    cmd += ["--media-item", json.dumps(media)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return r.returncode == 0, r.stderr[:200]

def post_fb(img, vid, caption):
    cmd = ["facebook-cli", "pages", "posts", "create",
           "--page-id", FB_PAGE, "--text", caption[:900],
           "--request-id", str(uuid.uuid4()),
           "--privacy", "PUBLIC", "--file", vid or img]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return r.returncode == 0, r.stderr[:200]

def main():
    dry = "--dry-run" in sys.argv
    n = 5
    for a in sys.argv:
        if a.startswith("--produk"):
            n = int(a.split("=")[-1]) if "=" in a else 5
    produk = pilih_produk(n)
    print(f"Produk hari ini ({len(produk)}):")
    for p in produk:
        print(f" - {p[1]} ({p[2]})")
    if dry:
        print("DRY RUN - konten tidak dibuat, tidak posting")
        return
    akun = [("IG", "ig"), ("Threads-1", "t1"), ("Threads-2", "t2"), ("FB", "fb")]
    for p in produk:
        print(f"\n>> {p[1]}")
        img, vid = siapkan_konten(p)
        caption = bikin_caption(p)
        for nama_akun, kode in akun:
            if kode == "ig":
                ok, err = post_ig(img, vid, caption)
            elif kode == "t1":
                ok, err = post_threads(THREADS_1, img, vid, caption)
            elif kode == "t2":
                ok, err = post_threads(THREADS_2, img, vid, caption)
            else:
                ok, err = post_fb(img, vid, caption)
            print(f"  [{nama_akun}] {'OK' if ok else 'GAGAL: ' + err[:80]}")
            time.sleep(90)  # jeda antar posting

if __name__ == "__main__":
    main()
