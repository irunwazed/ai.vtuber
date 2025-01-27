from PyPDF2 import PdfReader # type: ignore
import fitz  # type: ignore # PyMuPDF

def pdf_to_text(file_path):
  try:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
  except Exception as e:
    return f"An error occurred: {e}"