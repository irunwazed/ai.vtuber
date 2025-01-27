
from libs import pdf, helpers, clustering
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