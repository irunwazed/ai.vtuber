

from pathlib import Path

# Tentukan direktori tujuan untuk menyimpan file
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

UPLOAD_DIR_DOCUMENT = Path("uploads/documents")
UPLOAD_DIR_DOCUMENT.mkdir(parents=True, exist_ok=True)