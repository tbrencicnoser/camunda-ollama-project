from fastapi import FastAPI, UploadFile
import requests
import pdfplumber

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile):
    text = ""
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    prompt = f"Extract events from the following text: {text}"

    response = requests.post(
        "http://ollama:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return response.json()