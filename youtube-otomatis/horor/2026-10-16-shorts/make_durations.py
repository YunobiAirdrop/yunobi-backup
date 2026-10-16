#!/usr/bin/env python3
"""Hitung durasi per beat proporsional panjang teks, total = durasi audio aktual."""
import json, subprocess, os

BASE = "/home/hatch/workspace/youtube-otomatis/horor/2026-10-16-shorts"

BEATS = {
    "shorts1": [
        "Perawat ini naik lift rumah sakit jam dua pagi. Pintunya terbuka di lantai empat, lantai yang sudah tutup sepuluh tahun.",
        "Namanya Rina, perawat shift malam di rumah sakit tua ini. Malam itu ia buru-buru, jadi ia naik lift sendirian. Ia tekan lantai dua. Tapi liftnya naik terus. Berhenti di lantai empat.",
        "Pintu terbuka perlahan. Lorong gelap. Bau obat menyengat. Dan di ujung lorong, ada sosok berseragam suster, menyeret tubuhnya di lantai. Rina menjerit, menekan tombol tutup pintu berkali-kali. Pintu tidak bergerak. Sosok itu makin dekat. Lalu lampu lift padam.",
        "Sejak malam itu, setiap jam dua pagi, lift ini berhenti sendiri di lantai empat. Dan pintunya terbuka sendiri.",
    ],
    "shorts2": [
        "Anak kos ini cek CCTV kamarnya karena barangnya hilang tiap malam. Yang ia lihat justru dirinya sendiri, sedang tidur.",
        "Namanya Dimas. Tiga malam berturut-turut dompetnya pindah tempat. Ia pasang CCTV kecil di sudut kamar, menghadap kasur. Lalu ia tidur seperti biasa.",
        "Jam tiga pagi, rekaman menunjukkan Dimas tidur pulas. Lalu pintu kamar terbuka sendiri. Masuk sosok tinggi berwajah pucat, duduk di ujung kasur, menatap Dimas lama sekali.",
        "Sosok itu lalu meraih dompet di meja, membukanya, dan mengembalikan uang yang kemarin ia ambil. Selembar demi selembar, ditata rapi.",
        "Dimas pindah kos minggu itu juga. Tapi kata penghuni baru, tiap jam tiga pagi, masih terdengar suara seseorang merapikan barang di kamar itu. Sendirian.",
    ],
    "shorts3": [
        "Ia belanja di pasar ini tiap malam karena murah. Sampai suatu malam ia sadar: tidak satu pun penjualnya punya bayangan.",
        "Namanya Pak Warto. Tiap pulang lembur jam sebelas malam, ia mampir ke pasar kaget di ujung jalan. Sayur segar, harga setengah pasar biasa. Ia langganan tiga bulan.",
        "Malam itu lampu pasar redup. Saat membayar cabai, ia menunduk mengambil kembalian. Dan ia lihat ke lantai: bayangan si penjual tidak ada. Ia lihat sekeliling. Tidak satu pun orang di pasar itu punya bayangan.",
        "Tangannya gemetar. Ia menatap wajah penjual itu. Senyumnya melebar terlalu lebar. Belanja lagi besok ya, Pak, kata penjual itu, dengan suara seperti dua orang bicara bersamaan.",
        "Pak Warto lari. Besoknya ia kembali siang hari. Di ujung jalan itu tidak ada pasar. Hanya tanah kosong dan sebuah papan tua bertuliskan: pasar ini tutup sejak tahun delapan puluh tujuh.",
    ],
}

def audio_dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", p],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

for s, beats in BEATS.items():
    ap = os.path.join(BASE, s, "audio", "narasi.mp3")
    total = audio_dur(ap)
    lens = [len(b) for b in beats]
    ssum = sum(lens)
    # beri beat terakhir (title card) minimal 3 detik
    raw = [total * l / ssum for l in lens]
    if raw[-1] < 3.0:
        need = 3.0 - raw[-1]
        raw[-1] = 3.0
        # ambil dari beat lain proporsional
        others = sum(raw[:-1])
        raw[:-1] = [r - need * r / others for r in raw[:-1]]
    d = {f"beat-{i+1:03d}": round(v, 2) for i, v in enumerate(raw)}
    # koreksi rounding agar jumlah pas
    diff = round(total - sum(d.values()), 2)
    d[f"beat-{len(raw):03d}"] = round(d[f"beat-{len(raw):03d}"] + diff, 2)
    jp = os.path.join(BASE, s, "durasi.json")
    json.dump(d, open(jp, "w"), indent=1)
    print(s, "audio", round(total, 1), "->", d, "sum", round(sum(d.values()), 2))
