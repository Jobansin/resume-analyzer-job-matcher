from fastapi import FastAPI, File, UploadFile
import pdfplumber
import docx
import re  # 🔹 Import regex for text cleaning

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is working!"}

# ✅ Function to clean text
def clean_text(text):
    text = text.replace("\n", " ")  # 🔹 Replace newlines with spaces
    text = re.sub(r'\s+', ' ', text).strip()  # 🔹 Remove extra spaces
    return text

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    extracted_text = ""  # Store extracted text

    # ✅ If the uploaded file is a PDF, extract text
    if file.content_type == "application/pdf":
        with pdfplumber.open(file.file) as pdf:
            extracted_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    # ✅ If the uploaded file is a DOCX, extract text
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file.file)
        extracted_text = "\n".join([para.text for para in doc.paragraphs if para.text])

    # ✅ Clean extracted text
    cleaned_text = clean_text(extracted_text)

    return {"filename": file.filename, "content_type": file.content_type, "text": cleaned_text}


