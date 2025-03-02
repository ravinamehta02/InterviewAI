import fitz  # PyMuPDF for PDF processing

def extract_text_from_pdf(file_data):
    file_bytes = file_data.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text