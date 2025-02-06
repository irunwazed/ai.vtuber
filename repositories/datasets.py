
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore
from libs import pdf, helpers, clustering, database
import json
import nltk # type: ignore
from nltk.corpus import stopwords # type: ignore

import os


nltk.download('stopwords')

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


def add_datasets_rag(path_dir):
  # tableAturan = database.tableAturan
  # query = database.query
  idx = 1
  for filename in os.listdir(path_dir):
    file_path = os.path.join(path_dir, filename)
    name = filename.replace(".pdf", "")
    check = database.get_by_name(name)

    if os.path.isfile(file_path) and filename.endswith(".pdf") and not check:
      text_pdf = pdf.pdf_to_text(file_path)
      text_pdf = helpers.clean_double_space(text_pdf)
      text_pdf = helpers.clean_page_number(text_pdf)
      database.insert_document(name, f"nama dokumen: {name} \n isi dokumen: {text_pdf.strip()}")
      print(f"{idx}. Berhasil simpan dengan file  {filename}")
    else:
      print(f"{idx}. sudah ada {name}")
    
    idx += 1

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

# def search_documents(query, top_k=3):
#   tableAturan = database.tableAturan
#   all_docs = tableAturan.all()
#   docs_text = [doc['desc'] for doc in all_docs]
   
#   # Gunakan TF-IDF untuk mengubah dokumen dan query menjadi vektor
#   vectorizer = TfidfVectorizer(stop_words='english')
#   tfidf_matrix = vectorizer.fit_transform(docs_text + [query])
  
#   # Hitung kesamaan kosinus antara query dan dokumen
#   cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
  
#   # Ambil dokumen dengan kesamaan tertinggi
#   similar_indices = cosine_similarities.argsort()[0][-top_k:][::-1]
  
#   # Ambil judul dan konten dokumen yang relevan
#   relevant_docs = [all_docs[i] for i in similar_indices]
  
#   return relevant_docs


def search_documents(query, top_k=3):
  all_docs = database.fetch_all_documents()

  # if doc["name"] and len(doc["desc"]) > 100:
  docs_text = [doc[2] for doc in all_docs if doc[1] and len(doc[2]) > 1000]
  docs_judul_text = [doc[1] for doc in all_docs if doc[1] and len(doc[2]) > 1000]
  print("panjang", len(docs_judul_text))

  stop_words_indonesian = stopwords.words('indonesian')
   
  # Gunakan TF-IDF untuk mengubah dokumen dan query menjadi vektor
  vectorizer = TfidfVectorizer(stop_words=stop_words_indonesian)
  tfidf_matrix = vectorizer.fit_transform(docs_text + [query])
  tfidf_matrix_judul = vectorizer.fit_transform(docs_judul_text + [query])
  
  # Hitung kesamaan kosinus antara query dan dokumen
  cosine_similarities = cosine_similarity(tfidf_matrix_judul[-1], tfidf_matrix_judul[:-1])
  isJudul = False
  for i in cosine_similarities:
    for j in i:
      if float(j) > 0.4:
        isJudul = True

  if not isJudul:
    print("not judul")
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
  else:
    print("judul")

  
  # Ambil dokumen dengan kesamaan tertinggi
  similar_indices = cosine_similarities.argsort()[0][-top_k:][::-1]
  
  # Ambil judul dan konten dokumen yang relevan
  relevant_docs = [{
    "id": all_docs[i][0],
    "name": all_docs[i][1],
    "context": all_docs[i][2],
  } for i in similar_indices]
  
  
  return relevant_docs