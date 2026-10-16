#!/usr/bin/env python3
"""Tulis ulang berita antrean jadi artikel orisinal Bahasa Indonesia + SEO.
Memakai model gratis via 9Router. Output: data/artikel.json"""
import json, os, re, sys, time, argparse
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

def get_blog(nama):
    with open(os.path.join(BASE, "config.json")) as f:
        cfg = json.load(f)
    for b in cfg["blogs"]:
        if b["nama"] == nama:
            return b
    print("Blog tidak ada di config.json: " + nama)
    sys.exit(1)

_ap = argparse.ArgumentParser()
_ap.add_argument("--blog", default="kabarviral")
_blog = get_blog(_ap.parse_args().blog)
BLOG_NAMA = _blog["nama"]
NICHE = _blog.get("niche", "campuran")

ROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# langsung ke OpenRouter (bukan via 9Router) supaya tiap API key pakai kuota
# akunnya sendiri-sendiri. 9Router hanya kenal 1 key upstream.
def _load_proxy_env():
    try:
        with open("/etc/9router-proxy.env") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    except FileNotFoundError:
        pass
_load_proxy_env()
MODELS = [
    # 2026-10-04: reasoning model dinonaktifkan — nemotron reasoning pernah
    # membocorkan "Here's a thinking process" ke isi artikel (lihat AGENTS.md).
    # 2026-10-06: qwen3.8-27b:free DIHAPUS (404 — model dipensiunkan OpenRouter),
    # inkling:free DIHAPUS (403 Forbidden konsisten). Sisa 5 model.
    # 2026-10-08: gemma-4-26b dipindah ke depan — nemotron-3.5-lightning konsisten
    # return non-JSON dan menghabiskan budget 24 percobaan (2 blog gagal 8 Okt).
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3.5-lightning:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "inclusionai/ling-3.0-flash-sante:free",
    "google/gemma-4-31b-it:free",
]

def get_api_keys():
    """Ambil semua OpenRouter key: OPENROUTER_KEYS (koma-pisah) atau fallback NINEROUTER_API_KEY."""
    env_path = os.path.expanduser("~/.hermes/.env")
    keys = []
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("OPENROUTER_KEYS="):
                keys = [k.strip().strip('"').strip("'") for k in line.split("=", 1)[1].split(",") if k.strip()]
            elif line.startswith("NINEROUTER_API_KEY=") and not keys:
                keys = [line.split("=", 1)[1].strip('"').strip("'")]
    if not keys:
        raise RuntimeError("Tidak ada API key ditemukan (OPENROUTER_KEYS / NINEROUTER_API_KEY)")
    return keys

def get_api_key():
    return get_api_keys()[0]

_PROMPT_INTRO = {
"keuangan": """Kamu jurnalis keuangan Indonesia yang menulis untuk blog finansial. Tulis ulang berita di bawah menjadi artikel ORISINAL Bahasa Indonesia (jangan salin kalimat sumber), 400-600 kata, gaya santai tapi informatif seperti ditulis manusia — hindari pola tulisan AI yang kaku.

Fokus pada sudut yang berguna bagi pembaca: tips investasi, perbandingan produk keuangan, penjelasan dampak bagi keuangan pribadi/bisnis, atau panduan praktis. Selipkan kata kunci bernilai komersial secara natural (contoh: investasi, saham, reksa dana, asuransi, KPR, kartu kredit, pinjaman, tabungan, deposito, teknologi finansial).""",
"teknologi": """Kamu jurnalis teknologi Indonesia yang menulis untuk blog tekno. Tulis ulang berita di bawah menjadi artikel ORISINAL Bahasa Indonesia (jangan salin kalimat sumber), 400-600 kata, gaya santai tapi informatif seperti ditulis manusia — hindari pola tulisan AI yang kaku.

Fokus pada sudut yang berguna bagi pembaca: review singkat, perbandingan gadget, tips memilih produk teknologi, penjelasan tren AI/digital, atau panduan praktis. Selipkan kata kunci bernilai komersial secara natural (contoh: smartphone, laptop, gadget, AI, aplikasi, software, internet, hosting, VPN).""",
"kesehatan": """Kamu jurnalis kesehatan Indonesia yang menulis untuk blog gaya hidup sehat. Tulis ulang berita di bawah menjadi artikel ORISINAL Bahasa Indonesia (jangan salin kalimat sumber), 400-600 kata, gaya santai tapi informatif seperti ditulis manusia — hindari pola tulisan AI yang kaku.

Fokus pada sudut yang berguna bagi pembaca: tips kesehatan praktis, penjelasan medis dengan bahasa awam, pola hidup sehat, nutrisi, atau olahraga. Selipkan kata kunci bernilai komersial secara natural (contoh: kesehatan, suplemen, vitamin, diet, olahraga, asuransi kesehatan, rumah sakit, obat).""",
"campuran": """Kamu jurnalis Indonesia yang menulis untuk blog berita campuran (keuangan, teknologi, dan umum). Tulis ulang berita di bawah menjadi artikel ORISINAL Bahasa Indonesia (jangan salin kalimat sumber), 400-600 kata, gaya santai tapi informatif seperti ditulis manusia — hindari pola tulisan AI yang kaku.

Untuk berita keuangan/teknologi, fokus pada sudut yang berguna: tips investasi, perbandingan produk keuangan, dampak bagi keuangan pribadi/bisnis, atau panduan praktis — selipkan kata kunci bernilai komersial secara natural (investasi, saham, reksa dana, asuransi, KPR, kartu kredit, pinjaman, tabungan, deposito). Untuk berita umum, tulis dengan gaya jurnalistik yang menarik dan informatif.""",
"hiburan": """Kamu jurnalis hiburan Indonesia yang menulis untuk blog gaya hidup kekinian. Tulis ulang berita di bawah menjadi artikel ORISINAL Bahasa Indonesia (jangan salin kalimat sumber), 400-600 kata, gaya santai, seru, dan kekinian seperti ditulis manusia — hindari pola tulisan AI yang kaku.

Fokus pada sudut yang menarik bagi pembaca: kabar artis, tren viral, film/musik, tips gaya hidup, atau rekomendasi hiburan. Selipkan kata kunci populer secara natural (contoh: artis, viral, film, musik, drama korea, fashion, traveling, kuliner).""",
"olahraga": """Kamu jurnalis olahraga Indonesia yang menulis untuk blog berita olahraga. Tulis ulang berita di bawah menjadi artikel ORISINAL Bahasa Indonesia (jangan salin kalimat sumber), 400-600 kata, gaya semangat dan informatif seperti ditulis manusia — hindari pola tulisan AI yang kaku.

Fokus pada sudut yang menarik bagi pembaca: hasil pertandingan, profil atlet, analisis taktik, jadwal pertandingan, atau tips olahraga. Selipkan kata kunci populer secara natural (contoh: sepak bola, liga indonesia, timnas, motogp, bulutangkis, skor, transfer pemain).""",
"wisata": """Kamu penulis travel Indonesia yang menulis untuk blog wisata. Tulis ulang berita di bawah menjadi artikel ORISINAL Bahasa Indonesia (jangan salin kalimat sumber), 400-600 kata, gaya santai dan inspiratif seperti ditulis manusia — hindari pola tulisan AI yang kaku.

Fokus pada sudut yang berguna bagi pembaca: rekomendasi destinasi, tips traveling hemat, itinerary, kuliner khas daerah, atau info tiket/penginapan. Selipkan kata kunci populer secara natural (contoh: wisata, liburan, pantai, gunung, hotel, tiket pesawat, itinerary).""",
"kuliner": """Kamu food blogger Indonesia yang menulis untuk blog kuliner. Tulis ulang berita di bawah menjadi artikel ORISINAL Bahasa Indonesia (jangan salin kalimat sumber), 400-600 kata, gaya santai dan menggugah selera seperti ditulis manusia — hindari pola tulisan AI yang kaku.

Fokus pada sudut yang menarik bagi pembaca: review makanan, resep, rekomendasi tempat makan, kuliner viral, atau tips masak. Selipkan kata kunci populer secara natural (contoh: kuliner, resep, makanan viral, restoran, street food, masakan padang).""",
"otomotif": """Kamu jurnalis otomotif Indonesia yang menulis untuk blog otomotif. Tulis ulang berita di bawah menjadi artikel ORISINAL Bahasa Indonesia (jangan salin kalimat sumber), 400-600 kata, gaya informatif dan antusias seperti ditulis manusia — hindari pola tulisan AI yang kaku.

Fokus pada sudut yang berguna bagi pembaca: review kendaraan, perbandingan mobil/motor, tips perawatan, info harga, atau teknologi otomotif. Selipkan kata kunci populer secara natural (contoh: mobil, motor, harga mobil, review, modifikasi, servis, oli).""",
"pendidikan": """Kamu penulis pendidikan Indonesia yang menulis untuk blog edukasi. Tulis ulang berita di bawah menjadi artikel ORISINAL Bahasa Indonesia (jangan salin kalimat sumber), 400-600 kata, gaya jelas dan memotivasi seperti ditulis manusia — hindari pola tulisan AI yang kaku.

Fokus pada sudut yang berguna bagi pembaca: tips belajar, info beasiswa, panduan kuliah/sekolah, atau perkembangan dunia pendidikan. Selipkan kata kunci populer secara natural (contoh: beasiswa, kuliah, sekolah, SNBP, CPNS, tips belajar).""",
}
PROMPT = _PROMPT_INTRO.get(NICHE, _PROMPT_INTRO["campuran"]) + """

Berita sumber:
JUDUL: {judul}
SUMBER: {sumber}
ISI: {ringkasan}

Balas HANYA dengan JSON valid (tanpa markdown):
{{
  "judul": "judul SEO menarik, maks 60 karakter, tanpa clickbait murahan",
  "slug": "slug-url-tanpa-spasi",
  "meta_deskripsi": "deskripsi maks 160 karakter yang mengundang klik",
  "label": ["label1", "label2"],
  "artikel_html": "<p>paragraf pembuka...</p><h2>Subjudul</h2><p>isi...</p><p>Sumber: {sumber}</p>",
  "varian_judul": ["3 alternatif judul SEO lain, gaya berbeda, maks 60 karakter"],
  "faq_html": "<h2>Pertanyaan Umum</h2><p><strong>Q1?</strong><br>Jawaban singkat 1-2 kalimat.</p><p><strong>Q2?</strong><br>Jawaban.</p><p><strong>Q3?</strong><br>Jawaban.</p>",
  "alt_gambar": "teks alt SEO untuk gambar utama, deskriptif, maks 125 karakter"
}}
Gunakan minimal 3 subjudul <h2>. Akhiri dengan baris 'Sumber: {sumber}'.
FAQ berisi 3 pertanyaan yang PALING sering dicari pembaca soal topik ini + jawaban singkat faktual.

ATURAN GAYA (wajib, dari skill humanize & seo-optimize):
- Kata kunci utama topik HARUS muncul di judul, minimal satu <h2>, dan di paragraf pertama.
- Setiap <h2> deskriptif, menjawab pertanyaan yang dicari pembaca (bukan judul generik).
- Variasi panjang kalimat dan awalan kalimat; jangan mulai 3 kalimat berurutan dengan kata yang sama.
- DILARANG: pola "bukan X, melainkan Y"; pertanyaan yang dijawab sendiri ("Hasilnya? Mengejutkan."); kalimat klise AI ("di era digital ini", "sebagai kesimpulan", "penting untuk dicatat").
- DILARANG pola triad paksa (tiga hal sejajar yang dipaksakan: "efektif, efisien, dan elegan"); triad hanya bila isinya memang 3 hal berbeda yang penting.
- DILARANG pembuka staged ("Mari kita bahas", "Tanpa berlama-lama", "Inilah yang perlu kamu tahu") — langsung ke isi.
- DILARANG one-liner penutup dramatis ("Itulah yang terpenting.", "Hal ini patut direnungkan.").
- DILARANG inflasi signifikansi ("momen bersejarah", "tonggak penting", "babak baru") — tulis faktanya saja, biar pembaca yang menilai.
- Maksimal 2 tanda — (em dash) per artikel. Bahasa lugas, tanpa kata sifat berlebihan.
- Pertahankan detail konkret (angka, nama, contoh) agar terasa ditulis manusia.
- Satu artikel = satu topik utama; jangan mengulang ide yang sama di paragraf berbeda.

STRUKTUR AI-SEO (wajib, dari marketingskills/ai-seo — supaya dikutip AI search):
- Paragraf pertama = blok jawaban langsung 40-60 kata yang menjawab pertanyaan utama topik (definisi/inti berita). Jangan berputar-putar.
- Setiap angka/data WAJIB disertai sumbernya ("menurut data BPS...", "laporan ... menyebut..."). Tanpa sumber = jangan tulis angkanya.
- Tulis 1-2 kalimat "Catatan redaksi" berisi opini/konteks unik (sudah diwajibkan di NILAI ORISINAL) — ini pembeda dari agregator lain.

NILAI ORISINAL (wajib — ini yang bikin Google menilai konten berkualitas):
- Jangan HANYA menulis ulang fakta berita. Tambahkan minimal 2 dari ini:
  (a) KONTEKS: latar belakang atau penjelasan kenapa berita ini penting
  (b) ANALISIS: apa dampak/implikasinya bagi pembaca Indonesia
  (c) TIPS PRAKTIS: 2-3 saran konkret yang bisa pembaca lakukan terkait topik
  (d) PERBANDINGAN: hubungkan dengan kejadian/tren serupa sebelumnya
- Tulis 1 paragraf opini redaksi yang jelas ditandai ("Menurut redaksi..." atau "Catatan redaksi:") — sudut pandang unik yang tidak ada di sumber berita.
- Jika berita menyebut angka/data, jelaskan artinya dengan bahasa sederhana (jangan cuma kutip angka)."""

def parse_router_response(r):
    """Parse respons 9Router yang kadang ditempeli junk SSE ('data: [DONE]')."""
    dec = json.JSONDecoder()
    obj, _ = dec.raw_decode(r.text.strip())
    return obj

def extract_json(text):
    """Ambil objek JSON pertama yang seimbang dari teks."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    start = text.find("{")
    if start < 0:
        raise ValueError("tidak ada JSON")
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[start:i + 1])
    raise ValueError("JSON tidak seimbang")

def tulis_ulang(item, api_key=None):
    msg = PROMPT.format(judul=item["judul_asli"], sumber=item["sumber"], ringkasan=item["ringkasan"] or item["judul_asli"])
    keys = [api_key] if api_key else get_api_keys()
    last_err = None
    keys_kena_limit = 0
    # 2026-10-04: budget percobaan per artikel. Tiap request 429/503 TETAP
    # memakan jatah harian OpenRouter (50/akun); tanpa batas, 1 artikel macet
    # bisa membakar seluruh kuota 9 akun (±450 req) seperti kejadian hari ini.
    budget = 24
    for key in keys:
        pindah_key = False
        for model in MODELS:
            if pindah_key:
                break
            for attempt in range(2):
                if budget <= 0:
                    raise RuntimeError(f"budget percobaan habis, terakhir: {last_err}")
                try:
                    budget -= 1
                    r = requests.post(ROUTER_URL, headers={
                        "Authorization": f"Bearer {key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://kabarviralterkiniterbaru.blogspot.com/",
                        "X-Title": "Blog Otomatis",
                    }, json={
                        "model": model,
                        "messages": [{"role": "user", "content": msg}],
                        "temperature": 0.7,
                        "max_tokens": 2000,
                    }, timeout=120)
                    if r.status_code in (429, 503):
                        last_err = f"{model} {r.status_code}"
                        # limit harian = per AKUN -> model lain di akun sama pasti kena juga,
                        # langsung pindah key (akun) berikutnya; kalau SEMUA key kena,
                        # berarti kuota habis total -> berhenti
                        if "per-day" in r.text or "free-models" in r.text:
                            keys_kena_limit += 1
                            if keys_kena_limit >= len(keys):
                                raise RuntimeError("QUOTA_HABIS: limit harian model gratis habis di semua akun")
                            pindah_key = True
                            break
                        # 429 provider (bukan jatah harian): backoff lebih lama agar
                        # provider pulih, hemat jatah harian
                        time.sleep(20 * (attempt + 1))
                        continue
                    r.raise_for_status()
                    obj = parse_router_response(r)
                    ch = obj.get("choices") or []
                    _content = (ch[0].get("message", {}).get("content") if ch else None) or ""
                    if not _content.strip():
                        raise ValueError(f"respons tanpa konten (keys: {list(obj.keys())})")
                    text = _content
                    art = extract_json(str(text))
                    art["link_sumber"] = item["link"]
                    art["model"] = model
                    art["gambar"] = item.get("gambar", "")
                    return art
                except (requests.RequestException, ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
                    last_err = f"{model}: {str(e)[:80]}"
                    time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"semua model/key gagal, terakhir: {last_err}")

def main():
    antrean_path = os.path.join(DATA, "antrean-" + BLOG_NAMA + ".json")
    if not os.path.exists(antrean_path):
        print("antrean.json tidak ada, jalankan fetch_berita.py dulu")
        sys.exit(1)
    with open(antrean_path) as f:
        antrean = json.load(f)
    n_keys = len(get_api_keys())
    print(f"mulai tulis ulang {len(antrean)} artikel ({n_keys} API key)")
    hasil = []
    for i, item in enumerate(antrean, 1):
        try:
            art = tulis_ulang(item)
            hasil.append(art)
            print(f"[{i}/{len(antrean)}] OK: {art['judul'][:60]}")
        except Exception as e:
            print(f"[{i}/{len(antrean)}] GAGAL: {str(e)[:100]}")
        time.sleep(2)
    with open(os.path.join(DATA, "artikel-" + BLOG_NAMA + ".json"), "w") as f:
        json.dump(hasil, f, ensure_ascii=False, indent=1)
    print(f"Selesai: {len(hasil)} artikel siap posting")

if __name__ == "__main__":
    main()
