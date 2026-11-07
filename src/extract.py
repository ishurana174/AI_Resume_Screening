import docx
import PyPDF2
import os


# =========================================================
# EXTRACT TEXT FROM PDF
# =========================================================

def extract_text_from_pdf(path):

    text = ""

    with open(path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# =========================================================
# EXTRACT TEXT FROM DOCX
# =========================================================

def extract_text_from_docx(path):

    document = docx.Document(path)

    text = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text.append(paragraph.text)

    return "\n".join(text)


# =========================================================
# MAIN RESUME EXTRACTOR
# =========================================================

def extract_resume(path):

    if not os.path.exists(path):

        return ""


    extension = os.path.splitext(path)[1].lower()


    if extension == ".pdf":

        return extract_text_from_pdf(path)


    elif extension == ".docx":

        return extract_text_from_docx(path)


    else:

        return ""