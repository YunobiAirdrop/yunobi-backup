#!/usr/bin/env python3
"""Generate VO tambahan untuk LONG Jejak Buddha (beat 29-58) — perluasan agar 8-9 menit."""
import subprocess, os, sys

ROOT = "/home/hatch/workspace/youtube-otomatis/jejak-buddha/2026-10-16-fix"
TTS = "/opt/hatch/bin/tts"
VOICE = "avocado_v2:mudiwa"

EXTRA = [
# Perluasan: kehidupan istana & ramalan
"Kapilavastu adalah kerajaan makmur di kaki pegunungan Himalaya. Istananya dikelilingi taman-taman yang bunganya mekar sepanjang tahun.",
"Ratu Mahamaya, ibunda Siddhartha, bermimpi seekor gajah putih masuk ke rahimnya. Para brahmana berkata: anak ini akan menjadi manusia luar biasa.",
"Namun ratu wafat tujuh hari setelah melahirkan. Siddhartha dibesarkan oleh bibinya, Mahapajapati, dengan penuh kasih sayang.",
"Delapan brahmana dipanggil untuk meramal nasib bayi itu. Tujuh berkata ia akan menjadi raja besar. Satu, yang termuda, berkata berbeda.",
"Brahmana Kondanna meramalkan: jika pangeran melihat penderitaan dunia, ia akan meninggalkan segalanya dan menjadi Buddha.",
"Mendengar itu, Raja Suddhodana gemetar. Ia bersumpah akan melindungi putranya dari segala penderitaan, berapa pun harganya.",
"Istana pun diubah menjadi surga buatan. Tiga istana untuk tiga musim. Penari, musisi, dan wewangian terbaik dikumpulkan.",
# Perluasan: empat penglihatan (detail)
"Pangeran tumbuh menjadi pemuda tampan dan cerdas. Ia menikahi Yasodhara, putri bangsawan yang cantik jelita.",
"Tapi di usia dua puluh sembilan tahun, kegelisahan mulai menggerogotinya. Ada pertanyaan yang tak bisa dijawab kemewahan.",
"Suatu pagi yang cerah, ia memerintahkan kusirnya, Channa, menyiapkan kereta. Ia ingin melihat kota di luar tembok istana.",
"Raja sudah memerintahkan: bersihkan jalan dari orang tua dan orang sakit. Tapi satu orang tua lolos dari pengawasan.",
"Siddhartha menatap pria renta itu dengan ngeri. Inikah masa depan semua manusia? Inikah masa depanku juga?",
"Keesokan harinya ia keluar lagi. Kali ini ia melihat seorang pria sakit, tubuhnya kurus, napasnya tersengal menahan nyeri.",
"Channa menjelaskan: penyakit bisa menimpa siapa saja, Tuan. Bahkan pangeran sekalipun tak kebal terhadapnya.",
"Hari ketiga, ia menyaksikan iring-iringan duka. Sebuah jenazah diusung menuju tempat pembakaran, diiringi tangis keluarga.",
"Kematian, kata Channa pelan. Ujung dari setiap kehidupan. Tak ada yang bisa menghindarinya, Tuan.",
"Tiga hari, tiga pukulan. Dunia Siddhartha yang selama ini indah runtuh berkeping-keping.",
"Namun di hari keempat, ia melihat sesuatu yang berbeda: seorang pertapa berjubah kuning, berjalan tenang dengan mangkuk sedekah.",
"Wajah pertapa itu damai, seolah ia telah menemukan sesuatu yang tak dimiliki raja mana pun di dunia.",
"Siapa dia, tanya Siddhartha. Dia orang yang meninggalkan dunia untuk mencari kebebasan dari penderitaan, jawab Channa.",
# Perluasan: malam kepergian (detail)
"Malam itu Siddhartha tak bisa tidur. Bayangan orang tua, orang sakit, dan jenazah terus berputar di kepalanya.",
"Ia memandang Yasodhara yang tertidur pulas di samping bayinya. Hatinya tercabik antara cinta dan panggilan yang lebih besar.",
"Jika aku tetap di sini, pikirnya, aku akan menua, sakit, dan mati seperti semua orang. Dan tak ada yang bisa kutolong.",
"Tapi jika aku pergi dan menemukan obat bagi penderitaan, aku bisa menolong semua makhluk, termasuk istri dan anakku.",
"Tekadnya bulat. Ia membangunkan Channa dan memerintahkannya menyiapkan kuda terbaiknya, Kanthaka, yang putih bersih.",
"Sebelum pergi, ia menatap sekali lagi wajah istri dan anaknya dalam cahaya lampu minyak yang temaram.",
"Selamat tinggal, bisiknya. Suatu hari aku akan kembali, bukan sebagai pangeran, tapi sebagai pembawa kabar gembira.",
"Mereka keluar melalui gerbang timur. Langit malam bertabur bintang menjadi saksi kepergian agung itu.",
"Legenda menceritakan para dewa turun membantu: mereka menahan bunyi tapak kuda dan membuka gerbang yang terkunci.",
"Perjalanan malam itu jauh. Menjelang fajar, mereka tiba di tepi sungai Anoma yang airnya berkilau keperakan.",
# Perluasan: menjadi pertapa (detail, sudah ada sebagian — tambah)
"Di tepi sungai, Siddhartha memotong rambutnya yang panjang dan indah dengan pedangnya sendiri.",
"Ia menanggalkan pakaian sutra pangeran dan mengenakannya pada Channa. Ambillah ini, dan kembalilah ke istana.",
"Katakan pada ayahku: jangan berduka. Aku pergi bukan karena benci, tapi karena cinta yang lebih besar.",
"Channa bersimpuh menangis. Ia memohon ikut, tapi Siddhartha menolak dengan lembut namun tegas.",
"Kuda Kanthaka meringkik pilu, seolah mengerti perpisahan ini. Konon ia mati tak lama setelah kembali ke istana.",
"Siddhartha menyeberangi sungai dan melangkah masuk ke hutan. Di belakangnya, kehidupan pangeran berakhir selamanya.",
"Ia bertukar pakaian dengan seorang pemburu, dan sejak hari itu penampilannya tak berbeda dari pertapa mana pun.",
"Bertahun-tahun ia belajar pada guru-guru terkenal. Tapi ajaran mereka tak menjawab pertanyaannya tentang penderitaan.",
"Ia pun memilih jalan ekstrem: bertapa menyiksa diri di hutan Uruvela, berharap penderitaan badan membuka pintu kebenaran.",
"Tubuhnya menyusut tinggal tulang. Teman-temannya sampai mengira ia telah meninggal.",
"Namun di titik terendah itu, ia teringat masa kecilnya: duduk di bawah pohon jambu, bernapas tenang, hatinya damai.",
"Kedamaian itu datang bukan dari menyiksa diri, tapi dari ketenangan batin. Ia pun meninggalkan penyiksaan diri.",
"Lima temannya kecewa dan meninggalkannya. Ia sendirian, tapi untuk pertama kalinya dalam enam tahun, hatinya jernih.",
# Penutup
"Inilah kisah kepergian agung Siddhartha. Dari istana emas menuju hutan belantara, dari pangeran menuju Buddha.",
"Pertanyaannya kini untuk kita: istana emas apa yang menahanmu? Dan beranikah kau melangkah keluar mencarinya?",
]

def main():
    outdir = f"{ROOT}/audio_long"
    start = 29
    for i, t in enumerate(EXTRA, start):
        out = f"{outdir}/beat-{i:03d}.mp3"
        if os.path.exists(out) and os.path.getsize(out) > 5000:
            print(f"skip beat-{i:03d}"); continue
        r = subprocess.run([TTS, "speak", "--voice", VOICE, "--language", "id",
                            "--output", out, "--text-stdin"],
                           input=t.encode(), capture_output=True, timeout=180)
        if r.returncode != 0 or not os.path.exists(out):
            print(f"GAGAL beat-{i:03d}: {r.stderr.decode()[-300:]}"); sys.exit(1)
        print(f"OK beat-{i:03d} {os.path.getsize(out)}b")
    print("SELESAI EXTRA")

if __name__ == "__main__":
    main()
