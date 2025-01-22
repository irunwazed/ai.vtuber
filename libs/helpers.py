import re
import json



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

