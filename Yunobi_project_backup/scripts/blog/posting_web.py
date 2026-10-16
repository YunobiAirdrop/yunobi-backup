#!/usr/bin/env python3
"""Posting artikel via web UI Blogger (pengganti posting_api.py yang diblokir 403).

Cara kerja:
1. Baca data/artikel-{blog}.json, rakit body HTML (reuse rakit_body dari posting_api)
2. Tulis data/webpost/{blog}.json berisi [{judul, html}]
3. Tulis instruksi ke data/webpost/instruksi-{blog}.txt + cetak "SPAWN_BROWSER_TASK:{blog}:{n}"
4. AGEN (bukan script ini) membaca webpost/{blog}.json lalu spawn browser task
   dengan isi artikel ditempel langsung di deskripsi task (browser tidak bisa
   akses localhost VM ini)
5. Setelah browser task lapor TERPOSTING, agen pindahkan artikel ke terkirim

Pakai: posting_web.py --blog <nama>
"""
import json, os, sys, time, glob, argparse, subprocess, socket

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
WEBDIR = os.path.join(DATA, "webpost")
os.makedirs(WEBDIR, exist_ok=True)
sys.path.insert(0, BASE)

# reuse rakit_body dari posting_api (tanpa API call)
import importlib.util
spec = importlib.util.spec_from_file_location("papi", os.path.join(BASE, "posting_api.py"))
papi = importlib.util.module_from_spec(spec)
# cegah argparse di posting_api jalan saat import: patch sys.argv
_sav = sys.argv
sys.argv = ["posting_api.py", "--blog", "kabarviral"]
try:
    spec.loader.exec_module(papi)
finally:
    sys.argv = _sav

def get_blog(nama):
    cfg = json.load(open(os.path.join(BASE, "config.json")))
    for b in cfg["blogs"]:
        if b["nama"] == nama:
            return b
    print("Blog tidak ada: " + nama)
    sys.exit(1)

def server_jalan():
    s = socket.socket()
    try:
        s.connect(("127.0.0.1", 8899))
        s.close()
        return True
    except Exception:
        return False

def pastikan_server():
    if server_jalan():
        print("webpost server sudah jalan")
        return
    subprocess.Popen([sys.executable, os.path.join(BASE, "webpost_server.py")],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)
    for _ in range(10):
        time.sleep(1)
        if server_jalan():
            print("webpost server dimulai")
            return
    print("GAGAL start webpost server")
    sys.exit(1)

TASK_TEMPLATE = """Posting {n} artikel ke blog Blogger "{tampil}" ({blog_id}) via web UI.

Konteks: Login sebagai khususstokyunobi@gmail.com di blogger.com (sesi sudah ada).

DATA ARTIKEL (dari agen, ditempel langsung):
{artikel_data}

Untuk SETIAP artikel di atas (urutan sesuai):
1. Buka https://www.blogger.com/blog/posts/{blog_id}
2. Klik "POSTINGAN BARU" / "Buat Entri Baru".
3. Isi judul dengan "Judul" artikel (teks biasa).
4. Klik "Tampilan HTML" (ikon pensil/HTML di editor), tempel SELURUH "HTML" artikel.
5. Klik "Publikasikan", konfirmasi "KONFIRMASI" jika diminta.
6. Tunggu notifikasi "Pos dipublikasikan", lalu lanjut ke artikel berikutnya.
7. Jeda ~20 detik antar postingan agar tidak terdeteksi spam.

PENTING:
- Jangan ubah isi HTML, tempel apa adanya.
- Jika ada artikel yang gagal (error/timeout), catat judulnya dan lanjut ke berikutnya.
- Jangan posting artikel yang sama 2x.

LAPORAN AKHIR:
Tulis daftar: [judul] → TERPOSTING / GAGAL (alasan)."""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--blog", required=True)
    a = ap.parse_args()

    blog = get_blog(a.blog)
    nama = blog["nama"]

    # 1. baca artikel
    art_path = os.path.join(DATA, f"artikel-{nama}.json")
    artikels = []
    if os.path.exists(art_path):
        artikels = json.load(open(art_path))
    # tambah pending
    for pf in sorted(glob.glob(os.path.join(DATA, f"artikel_pending_{nama}_*.json"))):
        try:
            d = json.load(open(pf))
            if isinstance(d, list):
                artikels = d + artikels
        except Exception:
            pass
    # filter yang gagal (judul "...")
    artikels = [x for x in artikels if x.get("judul", "").strip() not in ("", "...")]
    if not artikels:
        print(f"Tidak ada artikel untuk {nama}")
        return
    print(f"Siapkan {len(artikels)} artikel untuk {nama}")

    # 2. rakit body
    out = []
    for art in artikels:
        try:
            _judul, html = papi.rakit_body(art)
        except Exception as e:
            print(f"rakit_body gagal untuk {art.get('judul','')[:40]}: {e}")
            continue
        out.append({"judul": art.get("judul", ""), "html": html})
    if not out:
        print("Tidak ada artikel yang bisa dirakit")
        return

    # 3. tulis webpost JSON
    wp = os.path.join(WEBDIR, f"{nama}.json")
    json.dump(out, open(wp, "w"), ensure_ascii=False)
    print(f"Tulis {wp} ({len(out)} artikel)")

    # 4. tulis instruksi dengan data artikel embedded
    artikel_data = ""
    for i, a in enumerate(out, 1):
        artikel_data += f"\nARTIKEL {i}:\nJudul: {a['judul']}\nHTML:\n{a['html']}\n"
    task = TASK_TEMPLATE.format(n=len(out), tampil=blog["tampil"],
                                blog_id=blog["blog_id"], artikel_data=artikel_data)
    instr_path = os.path.join(WEBDIR, f"instruksi-{nama}.txt")
    open(instr_path, "w").write(task)
    print(f"Instruksi browser task: {instr_path} ({len(task)} karakter)")
    print(f"SPAWN_BROWSER_TASK:{nama}:{len(out)}")

if __name__ == "__main__":
    main()
