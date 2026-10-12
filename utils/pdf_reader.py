# pdf_reader.py
import fitz  # PyMuPDF

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extracts text from a PDF byte stream using PyMuPDF.
    """
    try:
        text = ""
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""
