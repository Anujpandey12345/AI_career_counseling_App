import PyPDF2
import docx

def extract_text_from_resume(file_path):
    if file_path.endswith('.pdf'):
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        return " ".join([p.text for p in doc.paragraphs])
    
    return ""
