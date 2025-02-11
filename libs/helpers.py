import re
import json
import os

from fastapi import UploadFile # type: ignore
from libs import const

import numpy as np # type: ignore



def clean_html(raw_html):
  CLEANR = re.compile('<.*?>') 
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext.strip()

def clean_double_space(text):
  cleaned_text = re.sub(r'\s+', ' ', text)
  return cleaned_text.strip()

def clean_page_number(text):
  cleaned_text = re.sub(r'-\s*\d+\s*-', '', text)
  return cleaned_text.strip()

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
  result  = False
  try:
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
      # print(f"Folder {folder_path} telah dibuat.")

    with open(file_path, "w", encoding="utf-8") as file:
      file.write(text)
    result = True
  except Exception as e:
    print("error : ", e)

  # print(f"Teks berhasil disimpan ke {file_path}")
  return result

def load_file(file_path):
  content = None
  with open(file_path, "r") as file:
    content = file.read()
  return content

async def upload(file: UploadFile, filename:str):
    file_location = const.UPLOAD_DIR_DOCUMENT / filename
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    return file_location


def string_to_numpy_array(data_str):
    try:
        data_list = json.loads(data_str)
        numpy_array = np.array(data_list)
        return numpy_array
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return None

def numpy_to_json_string(np_array):
    return json.dumps(np_array.tolist())