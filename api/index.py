from fastapi import FastAPI, UploadFile, File, Form
from parser import extract_text_from_pdf
from gpt_analysis import gpt_resume_feedback, gpt_jd_match
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "FastAPI running on Vercel 🚀"}

# ---------------- PART 1 ----------------
@app.post("/resume/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)
    gpt_raw = gpt_resume_feedback(text)

    try:
        gpt_structured = json.loads(gpt_raw)
    except:
        gpt_structured = {"error": "Invalid GPT response"}

    return {
        "resume_text": text[:500],
        "gpt_feedback": gpt_structured
    }

# ---------------- PART 2 ----------------
@app.post("/resume/jd-match")
async def resume_job_match(file: UploadFile = File(...),job_description: str = Form(...)):
    resume_text = extract_text_from_pdf(file.file)
    gpt_raw = gpt_jd_match(resume_text, job_description)

    try:
        gpt_structured = json.loads(gpt_raw)
    except:
        gpt_structured = {"error": "Invalid GPT response"}

    return {
        "gpt_analysis": gpt_structured
    }
# To run the app, use the command:
# venv\Scripts\activate
# uvicorn main:app --reload