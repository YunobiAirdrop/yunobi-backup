#!/usr/bin/env python3
"""Generate VO Mudiwa per beat untuk 3 video Jejak Buddha."""
import subprocess, os, sys

ROOT = "/home/hatch/workspace/youtube-otomatis/jejak-buddha/2026-10-16-fix"
TTS = "/opt/hatch/bin/tts"
VOICE = "avocado_v2:mudiwa"

LONG = [
"Tengah malam, seorang pangeran mencium kening istrinya yang sedang tertidur. Lalu ia pergi, dan tidak pernah kembali sebagai pangeran.",
"Namanya Siddhartha Gautama. Pangeran kerajaan Kapilavastu, hidup dalam kemewahan yang tak terbayangkan.",
"Istana emas, taman-taman indah, pelayan di setiap sudut. Semua keinginan terpenuhi sebelum sempat terucap.",
"Sejak lahir, para peramal meramalkan dua jalan hidupnya: menjadi raja besar penguasa dunia, atau menjadi Buddha, penemu kebenaran.",
"Ayahnya, Raja Suddhodana, memilih jalan pertama. Ia membangun tembok kemewahan agar Siddhartha tak pernah melihat penderitaan.",
"Orang tua, orang sakit, dan kematian dilarang mendekati istana. Sang pangeran hanya mengenal keindahan.",
"Tapi tembok setinggi apa pun tak bisa menahan rasa ingin tahu. Suatu hari, Siddhartha meminta keluar melihat kota.",
"Di jalan ia melihat untuk pertama kalinya: seorang tua renta berjalan tertatih. Rambut putih, tubuh bungkuk.",
"Apakah aku juga akan menjadi seperti itu, tanyanya. Kusirnya menjawab lirih: Ya, Tuan. Semua manusia akan menua.",
"Hari berikutnya: seorang sakit terbaring mengerang. Lalu hari ketiga: iring-iringan jenazah menuju pembakaran.",
"Tiga pemandangan itu menghantamnya seperti petir. Kemewahan istana tiba-tiba terasa seperti sangkar emas.",
"Lalu ia melihat pemandangan keempat: seorang pertapa berjubah sederhana, wajahnya tenang dan damai.",
"Dia telah meninggalkan dunia, tapi wajahnya lebih bahagia dari raja mana pun, pikir Siddhartha.",
"Malam itu kabar gembira datang: istrinya, Yasodhara, melahirkan seorang bayi laki-laki. Namanya Rahula.",
"Tapi Siddhartha justru berbisik: Belenggu telah lahir. Ikatan telah lahir. Kebahagiaan itu terasa seperti rantai baru.",
"Ia tahu waktunya tiba. Tengah malam, saat istana terlelap, ia membangunkan kusir setianya, Channa.",
"Siapkan kuda Kanthaka. Malam ini juga kita pergi. Channa gemetar, tapi ia tak bisa menolak tekad tuannya.",
"Mereka melintasi gerbang istana dalam sunyi. Konon para dewa menahan suara derap kaki kuda agar tak membangunkan penjaga.",
"Di tepi sungai Anoma, Siddhartha turun dari kudanya. Ia memotong rambut panjangnya dengan pedang.",
"Ia menanggalkan pakaian pangeran, memberikannya kepada Channa beserta seluruh perhiasannya. Kembalilah. Katakan pada ayahku, aku pergi mencari obat bagi penderitaan manusia.",
"Channa menangis. Kuda Kanthaka pun konon mati karena patah hati tak lama setelahnya.",
"Siddhartha berjalan masuk ke dalam hutan. Tanpa mahkota, tanpa pelayan, tanpa apa pun, kecuali satu tekad.",
"Enam tahun ia bertapa dengan cara paling ekstrem: hampir tak makan, tubuhnya tinggal tulang berbalut kulit.",
"Sampai suatu hari ia sadar: menyiksa diri sama kelirunya dengan memanjakan diri. Jalan tengah itulah jawabannya.",
"Ia menerima semangkuk nasi susu dari seorang gadis desa bernama Sujata. Tubuhnya kembali kuat.",
"Lalu ia duduk di bawah sebuah pohon beringin besar, dan bertekad: Aku tidak akan bangun sebelum menemukan kebenaran.",
"Malam itu ia menjadi Buddha, yang tercerahkan. Pangeran yang kabur itu kembali sebagai cahaya bagi dunia.",
"Kadang, untuk menemukan dirimu yang sejati, kau harus berani meninggalkan istana emasmu sendiri.",
"Kapilavastu adalah kerajaan makmur di kaki pegunungan Himalaya. Istananya dikelilingi taman-taman yang bunganya mekar sepanjang tahun.",
"Ratu Mahamaya, ibunda Siddhartha, bermimpi seekor gajah putih masuk ke rahimnya. Para brahmana berkata: anak ini akan menjadi manusia luar biasa.",
"Namun ratu wafat tujuh hari setelah melahirkan. Siddhartha dibesarkan oleh bibinya, Mahapajapati, dengan penuh kasih sayang.",
"Delapan brahmana dipanggil untuk meramal nasib bayi itu. Tujuh berkata ia akan menjadi raja besar. Satu, yang termuda, berkata berbeda.",
"Brahmana Kondanna meramalkan: jika pangeran melihat penderitaan dunia, ia akan meninggalkan segalanya dan menjadi Buddha.",
"Mendengar itu, Raja Suddhodana gemetar. Ia bersumpah akan melindungi putranya dari segala penderitaan, berapa pun harganya.",
"Istana pun diubah menjadi surga buatan. Tiga istana untuk tiga musim. Penari, musisi, dan wewangian terbaik dikumpulkan.",
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
"Inilah kisah kepergian agung Siddhartha. Dari istana emas menuju hutan belantara, dari pangeran menuju Buddha.",
"Pertanyaannya kini untuk kita: istana emas apa yang menahanmu? Dan beranikah kau melangkah keluar mencarinya?",
]

S1 = [
"Malam itu, seluruh pasukan iblis menyerang satu orang yang sedang duduk diam.",
"Namanya Siddhartha. Ia bersumpah tak akan bangun dari bawah pohon ini sebelum mencapai pencerahan.",
"Mara, raja kegelapan, tak terima. Ia mengerahkan pasukan iblis bersenjata lengkap.",
"Panah api melesat, tombak beterbangan. Tapi semuanya berubah menjadi bunga sebelum menyentuhnya.",
"Gagal dengan kekerasan, Mara mengirim tiga putrinya yang cantik untuk menggoda. Siddhartha tak bergeming.",
"Mara pun maju sendiri dan menantang: Siapa yang menjadi saksimu, hai pertapa?",
"Siddhartha menyentuhkan tangannya ke bumi. Dan bumi pun bergetar menjadi saksi.",
"Pasukan kegelapan lari tunggang langgang. Fajar menyingsing, dan Siddhartha pun menjadi Buddha.",
"Ketenangan mengalahkan seribu pasukan.",
]

S2 = [
"Ia telah membunuh sembilan ratus sembilan puluh sembilan orang. Kalungnya kurang satu jari lagi.",
"Namanya Angulimala. Dulu ia murid terpandai bernama Ahimsaka, yang berarti tanpa kekerasan.",
"Difitnah, gurunya memerintahkannya membunuh seribu orang sebagai mahar ilmu.",
"Ia menjadi teror. Setiap korbannya dipotong jarinya, dirangkai menjadi kalung.",
"Raja mengerahkan pasukan, tapi tak ada yang berani mendekatinya.",
"Suatu pagi, Buddha berjalan tenang melewati hutan tempatnya bersembunyi.",
"Angulimala mengejar dengan pedang terhunus, tapi secepat apa pun ia berlari, tak pernah bisa menyusul.",
"Berhenti, pertapa! teriaknya. Buddha menjawab: Aku telah berhenti, Angulimala. Berhentilah engkau.",
"Kalimat itu meruntuhkannya. Ia berlutut, membuang pedang, dan menjadi murid Buddha.",
"Tak ada yang terlalu jauh untuk kembali.",
]

def synth(texts, outdir):
    os.makedirs(outdir, exist_ok=True)
    for i, t in enumerate(texts, 1):
        out = f"{outdir}/beat-{i:03d}.mp3"
        if os.path.exists(out) and os.path.getsize(out) > 5000:
            print(f"skip beat-{i:03d}"); continue
        r = subprocess.run([TTS, "speak", "--voice", VOICE, "--language", "id",
                            "--output", out, "--text-stdin"],
                           input=t.encode(), capture_output=True, timeout=180)
        if r.returncode != 0 or not os.path.exists(out):
            print(f"GAGAL beat-{i:03d}: {r.stderr.decode()[-300:]}"); sys.exit(1)
        print(f"OK beat-{i:03d} {os.path.getsize(out)}b")

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "long"): synth(LONG, f"{ROOT}/audio_long")
    if which in ("all", "s1"):   synth(S1, f"{ROOT}/audio_s1")
    if which in ("all", "s2"):   synth(S2, f"{ROOT}/audio_s2")
    print("SELESAI TTS", which)
