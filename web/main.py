from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
import pdfplumber
import requests
from ics import Calendar, Event
from datetime import datetime
import uuid
import os
import io
import json
import redis

app = FastAPI()

# Connect to Redis
r = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
    <body>
        <h1>📄 Upload PDF</h1>
        <form action="/upload" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input type="submit" value="Upload">
        </form>
        <div id="loading" style="display:none;">
            <p>⏳ Datei wird verarbeitet... bitte warten...</p>
        </div>
        <script>
            const form = document.querySelector('form');
            form.addEventListener('submit', () => {
                document.getElementById('loading').style.display = 'block';
            });
        </script>
    </body>
    </html>
    """

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    prompt = f"""
    Extrahiere aus diesem Text eine Liste von Events im Format:
    [{{"date": "YYYY-MM-DD", "start": "HH:MM", "end": "HH:MM", "title": "...", "description": "..."}}]

    Hier ist der Text:
    \"\"\"
    {text}
    \"\"\"
    """

    response = requests.post(
        "http://ollama:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )

    if response.status_code != 200:
        return {"error": f"Ollama API returned {response.status_code}", "details": response.text}

    result = response.json()
    raw_response = result.get("response", "")

    # Try to extract JSON array
    try:
        # Find the first [ and last ] to isolate the array
        start = raw_response.find('[')
        end = raw_response.rfind(']') + 1
        clean_json = raw_response[start:end]
        events = json.loads(clean_json)
    except Exception as e:
        return {"error": "Failed to decode events from Ollama response", "raw": raw_response, "exception": str(e)}

    # Create ICS file
    calendar = Calendar()
    event_list_html = "<ul>"
    for item in events:
        e = Event()
        start_dt = f"{item['date']} {item['start']}"
        end_dt = f"{item['date']} {item['end']}"
        e.name = item['title']
        e.begin = datetime.strptime(start_dt, "%Y-%m-%d %H:%M")
        e.end = datetime.strptime(end_dt, "%Y-%m-%d %H:%M")
        e.description = item.get('description', '')
        calendar.events.add(e)
        event_list_html += f"<li><strong>{e.name}</strong> am {e.begin} - {e.description}</li>"
    event_list_html += "</ul>"

    filename = f"{uuid.uuid4()}.ics"
    with open(filename, 'w') as f:
        f.writelines(calendar)

    # Increment Redis counter
    upload_count = r.incr("upload_count")

    # Build response page
    response_html = f"""
    <html>
    <body>
        <h1>✅ ICS-Datei erstellt</h1>
        <p><a href="/download/{filename}">📥 ICS herunterladen</a></p>
        <p><strong>🚀 Uploads bisher: {upload_count}</strong></p>
        <h2>Gefundene Termine:</h2>
        {event_list_html}
        <p><a href="/">⬅ Zurück</a></p>
    </body>
    </html>
    """

    return HTMLResponse(content=response_html)

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"./{filename}"

    async def cleanup():
        os.remove(file_path)

    return FileResponse(file_path, media_type='text/calendar', filename='events.ics', background=cleanup)
