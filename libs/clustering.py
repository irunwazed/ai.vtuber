import numpy as np # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.cluster import KMeans # type: ignore
from sklearn.metrics import silhouette_score # type: ignore
import nltk # type: ignore
from nltk.corpus import stopwords # type: ignore

def testing(dokumen):
  # Contoh data: 
  # dokumen = [
  #     "Ini adalah dokumen pertama.",
  #     "Dokumen ini adalah dokumen kedua.",
  #     "Dan ini adalah dokumen ketiga.",
  #     "Apakah ini dokumen pertama?",
  # ]
  # # Pastikan jumlah dokumen adalah 100 (untuk demonstrasi, ulang beberapa dokumen)
  # dokumen = dokumen * (100 // len(dokumen)) + dokumen[: 100 % len(dokumen)]

  # Unduh stopword bahasa Indonesia jika belum tersedia
  nltk.download('stopwords')
  stop_words_indonesian = stopwords.words('indonesian')



  # Langkah 1: Preprocessing teks
  def preprocess_teks(dok):
      return dok.lower()

  dokumen = [preprocess_teks(dok) for dok in dokumen]
  # print("dokumen", dokumen)

  # Langkah 2: Konversi teks ke representasi numerik (TF-IDF)
  tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words_indonesian)

  # print("tfidf_vectorizer", tfidf_vectorizer)
  tfidf_matrix = tfidf_vectorizer.fit_transform(dokumen)
  # print("tfidf_matrix", tfidf_matrix)

  # Langkah 3: Tentukan jumlah cluster terbaik menggunakan silhouette score
  range_n_clusters = range(2, 20)  # Coba beberapa nilai cluster
  best_n_clusters = 2
  best_score = -1

  for n_clusters in range_n_clusters:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(tfidf_matrix)
    silhouette_avg = silhouette_score(tfidf_matrix, cluster_labels)
    print(f"Untuk n_clusters = {n_clusters}, silhouette score adalah {silhouette_avg}")

    if silhouette_avg > best_score:
      best_n_clusters = n_clusters
      best_score = silhouette_avg

  print(f"Jumlah cluster terbaik: {best_n_clusters} dengan silhouette score: {best_score}")

  # Langkah 4: Clustering dengan jumlah cluster terbaik
  final_kmeans = KMeans(n_clusters=best_n_clusters, random_state=42)
  final_clusters = final_kmeans.fit_predict(tfidf_matrix)

  # Langkah 5: Output hasil clustering
  for i, cluster in enumerate(final_clusters):
    print(f"Dokumen {i+1} berada di Cluster {cluster}")


def get_labels(dokumen, max_label):
  # Contoh data: 
  # dokumen = [
  #     "Ini adalah dokumen pertama.",
  #     "Dokumen ini adalah dokumen kedua.",
  #     "Dan ini adalah dokumen ketiga.",
  #     "Apakah ini dokumen pertama?",
  # ]
  # max_label = 20

  # Unduh stopword bahasa Indonesia jika belum tersedia
  nltk.download('stopwords')
  stop_words_indonesian = stopwords.words('indonesian')

  # Langkah 1: Preprocessing teks
  def preprocess_teks(dok):
      return dok.lower()

  dokumen = [preprocess_teks(dok) for dok in dokumen]
  # print("dokumen", dokumen)

  # Langkah 2: Konversi teks ke representasi numerik (TF-IDF)
  tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words_indonesian)
  tfidf_matrix = tfidf_vectorizer.fit_transform(dokumen)

  # Langkah 3: Tentukan jumlah cluster terbaik menggunakan silhouette score
  range_n_clusters = range(2, max_label) 
  best_n_clusters = 2
  best_score = -1

  for n_clusters in range_n_clusters:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(tfidf_matrix)
    silhouette_avg = silhouette_score(tfidf_matrix, cluster_labels)
    print(f"Untuk n_clusters = {n_clusters}, silhouette score adalah {silhouette_avg}")

    if silhouette_avg > best_score:
      best_n_clusters = n_clusters
      best_score = silhouette_avg

  print(f"Jumlah cluster terbaik: {best_n_clusters} dengan silhouette score: {best_score}")

  # Langkah 4: Clustering dengan jumlah cluster terbaik
  final_kmeans = KMeans(n_clusters=best_n_clusters, random_state=42)
  final_clusters = final_kmeans.fit_predict(tfidf_matrix)

  return final_clusters

