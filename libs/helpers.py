import re
import json
import os



def clean_html(raw_html):
  CLEANR = re.compile('<.*?>') 
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext.strip()

def find_all(text, search):
  return [m.start() for m in re.finditer(search.lower(), text.lower())]

def load_json(path_json):
  # Membaca file JSON
  datasets = None
  try:
    with open(path_json, 'r') as file:
      datasets = json.load(file)
  except FileNotFoundError:
    print(f"File {path_json} tidak ditemukan.")
  except json.JSONDecodeError:
    print("File JSON tidak valid.")
  return datasets

def save_file(file_path, text):
  folder_path = os.path.dirname(file_path)
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder {folder_path} telah dibuat.")

  with open(file_path, "w", encoding="utf-8") as file:
      file.write(text)

  print(f"Teks berhasil disimpan ke {file_path}")

def load_file(file_path):
  content = None
  with open(file_path, "r") as file:
    content = file.read()
  return content
