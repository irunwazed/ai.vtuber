
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore
from libs import pdf, helpers, clustering, database
import json

import os

# directory_path = "datasets/jdih"

def create_datasets_rag(path_dir, save_as):
  datasets = []
  id = 1
  for filename in os.listdir(path_dir):
    file_path = os.path.join(path_dir, filename)

    if os.path.isfile(file_path) and filename.endswith(".pdf"):
      text_pdf = pdf.pdf_to_text(file_path)
      datasets.append({
        "id": id,
        "name": filename.replace(".pdf", ""),
        "desc": text_pdf.strip()
      })
      id += 1

  helpers.save_file(save_as, json.dumps(datasets))


def add_datasets_rag(path_dir, save_as):
  tableAturan = database.tableAturan
  query = database.query
  for filename in os.listdir(path_dir):
    file_path = os.path.join(path_dir, filename)
    name = filename.replace(".pdf", "")
    check = tableAturan.search(query.name == name)

    idx = 1
    if os.path.isfile(file_path) and filename.endswith(".pdf") and len(check) == 0:
      text_pdf = pdf.pdf_to_text(file_path)
      text_pdf = helpers.clean_double_space(text_pdf)
      text_pdf = helpers.clean_page_number(text_pdf)
      tableAturan.insert({
        "name": name,
        "desc": text_pdf.strip()
      })
      print(f"Berhasil simpan {save_as} dengan file {idx}. {filename}")
      idx += 1
    else:
      print(f"sudah ada {name}")

def set_label(path_json):
  data = helpers.load_json(path_json)

  documents = []
  for doc in data:
    documents.append(doc["desc"])

  labels = clustering.get_labels(documents, 20)

  dataLabels = []
  for i, doc in enumerate(data):
    dataLabels.append({
      "id": doc["id"],
      "name": doc["name"],
      "desc": doc["desc"],
      "label": int(labels[i])
    })

  helpers.save_file(path_json, json.dumps(dataLabels))

def search_documents(query, top_k=3):
  tableAturan = database.tableAturan
  all_docs = tableAturan.all()
  docs_text = [doc['desc'] for doc in all_docs]
   
  # Gunakan TF-IDF untuk mengubah dokumen dan query menjadi vektor
  vectorizer = TfidfVectorizer(stop_words='english')
  tfidf_matrix = vectorizer.fit_transform(docs_text + [query])
  
  # Hitung kesamaan kosinus antara query dan dokumen
  cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
  
  # Ambil dokumen dengan kesamaan tertinggi
  similar_indices = cosine_similarities.argsort()[0][-top_k:][::-1]
  
  # Ambil judul dan konten dokumen yang relevan
  relevant_docs = [all_docs[i] for i in similar_indices]
  
  return relevant_docs