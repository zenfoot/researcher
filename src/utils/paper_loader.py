# This utility loads and processes papers in PDF format.


import os
from PyPDF2 import PdfReader
import fitz  # PyMuPDF

class PaperLoader:
    def __init__(self):
        pass

    def load_paper(self, pdf_path, num_pages=None, min_size=100):
        text = ""
        try:
            doc = fitz.open(pdf_path)
            if num_pages:
                pages = doc[:num_pages]
            else:
                pages = doc
            text = ""
            for page in pages:
                text += page.get_text()
            if len(text) < min_size:
                raise Exception("Text too short")
        except Exception as e:
            print(f"Error loading PDF: {e}")
            # Fallback to PyPDF2
            try:
                reader = PdfReader(pdf_path)
                if num_pages:
                    pages = reader.pages[:num_pages]
                else:
                    pages = reader.pages
                text = "".join(page.extract_text() for page in pages)
                if len(text) < min_size:
                    raise Exception("Text too short")
            except Exception as e:
                print(f"Error with PyPDF2: {e}")
                text = ""
        return text