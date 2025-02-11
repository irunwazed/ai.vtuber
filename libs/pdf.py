from PyPDF2 import PdfReader # type: ignore
import fitz  # type: ignore # PyMuPDF
from fastapi import FastAPI, File, UploadFile # type: ignore
from io import BytesIO
from pdf2image import convert_from_path # type: ignore
import pytesseract # type: ignore
from PIL import Image # type: ignore
from libs import const, clear

def pdf_to_text(file_path):
  try:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
  except Exception as e:
    return f"An error occurred: {e}"

def upload_pdf_to_text(file: UploadFile):
  try:
    pdf_file = BytesIO(file.file.read()) 
    pdf_reader = PdfReader(pdf_file) 
    
    full_text = []
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        full_text.append(page.extract_text())
    
    return '\n'.join(full_text)
  except Exception as e:
    return f"An error occurred: {e}"
  
def pdf_ocr_to_text(file_location):

    pages = convert_from_path(file_location, 300) 
    # file_location.unlink()

    custom_config = r'--oem 3 --psm 6'
    custom_config = ""
    text = ""
    for page in pages:
        page_text = pytesseract.image_to_string(page, config=custom_config)
        text += page_text + "\n"
    
    return text
