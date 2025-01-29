import pandas as pd
import matplotlib.pyplot as plt
from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
import os
from libs import database
import nltk # type: ignore
from nltk.corpus import stopwords # type: ignore

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def clustering_bertopic(docs):
    
    stopwords_indonesia = [
        "dan", "atau", "yang", "di", "ke", "dari", "pada", "dengan", "untuk", "dalam", "adalah",
        "ini", "itu", "sebagai", "oleh", "karena", "dapat", "juga", "akan", "mereka", "kami",
        "kita", "anda", "saya", "dia", "telah", "sebelum", "sesudah", "bisa", "harus", "agar",
        "lebih", "kurang", "banyak", "sedikit", "setelah", "bahwa", "namun", "tetapi", "walaupun",
        "misalnya", "seperti", "maupun", "meskipun", "saat", "jadi", "sekarang", "kemudian", "begitu", 
        "tidak", "paling", "serta", "kepada", "pemerintahan", "bagi"
    ]
    stopwords_tambahan = [
         "pasal", "undang", "jelas", "cukup", "ayat",  "dimaksud",
         "pemerintah", "sebagaimana",  "negara", "indonesia", "perumahan", "huruf", 
         "tahun", "masyarakat", "pembangunan", "daerah", "republik", "peraturan", "kawasan",
         "lingkungan", "nomor", "uu", "undangundang", "atas", "tentang", "perubahan",
         "perpu", "pemberantasan", "pelaksanaan", "tahun", "pertanggungjawaban", "agung", "desa", "ketentuan", 
         "sesuai", "dilakukan", "permukiman", "rumah", "hukum", "badan", "umum", "danatau", "kepala", "kabupatenkota", 
         "penyelenggaraan", "partai", "angka", "ketua", "sarana", "prasarana"
    ]

    stopwords_number = []
    for i in range(3000):
      stopwords_number.append(str(i))

    stopwords_number += ["satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan", "puluh", "ratus", "ribu"]

    # Cara 1: Menggunakan operator `+`
    stopwords_indonesia += stopwords_number
    stopwords_indonesia += stopwords_tambahan


    # # 🔹 1. Konfigurasi UMAP untuk reduksi dimensi
    # umap_model = UMAP(n_components=5, n_neighbors=2000, min_dist=0.1, metric="cosine")

    # # 🔹 2. Konfigurasi HDBSCAN untuk clustering
    # hdbscan_model = HDBSCAN(min_cluster_size=5, metric="euclidean", cluster_selection_method="eom")

    # leaf / eom
    umap_model = UMAP(n_components=2, n_neighbors=100, min_dist=0.3, metric="cosine")
    hdbscan_model = HDBSCAN(min_cluster_size=2, min_samples=1, metric="euclidean", cluster_selection_method="leaf")


    ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)    

    # 🔹 3. Konfigurasi CountVectorizer dengan stopwords yang diperbaiki
    vectorizer = CountVectorizer(stop_words=stopwords_indonesia)

    # 🔹 4. Buat model BERTopic dengan konfigurasi yang diperbaiki
    topic_model = BERTopic(
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer,
        ctfidf_model=ctfidf_model,
        min_topic_size=2  # Menyesuaikan ukuran minimum topik agar lebih fleksibel
    )

    # 🔹 5. Jalankan model untuk menemukan topik
    topics, probs = topic_model.fit_transform(docs)

    print("probs", probs)

    # 🔹 6. Tampilkan daftar topik yang ditemukan
    topic_info = topic_model.get_topic_info()
    print("\n📝 Daftar Topik yang Ditemukan:")
    print(topic_info)

    # 🔹 7. Tampilkan setiap dokumen beserta label topiknya
    print("\n📌 Label Topik untuk Setiap Dokumen:")
    for i, (doc, topic) in enumerate(zip(docs, topics)):
        topic_name = topic_model.get_topic(topic)  # Ambil kata kunci dari topik
        topic_words = ", ".join([word for word, _ in topic_name]) if topic_name else "Tidak ada topik"
        print(f"📄 Dokumen {i+1}:")
        print(f"   🔹 Topik {topic}: {topic_words}\n")

    # 🔹 8. Visualisasi jika ada topik yang valid
    if len(topic_info) > 1:  # Pastikan ada topik selain outlier (-1)
        topic_model.visualize_barchart().show()
    else:
        print("❌ Tidak ada topik yang valid untuk divisualisasikan.")

# datas = database.tableAturan.all()

# docs = []
# for data in datas:
#   docs.append(data["desc"])
# clustering_bertopic(docs)

