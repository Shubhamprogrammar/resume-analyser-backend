from fastapi import FastAPI, UploadFile, File, Form
from parser import extract_text_from_pdf
from ats import find_missing_sections, ats_keyword_match
from scoring import calculate_resume_score
from gpt_analysis import gpt_resume_feedback, gpt_jd_match
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PART 1 ----------------
@app.post("/resume/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)

    missing_sections = find_missing_sections(text)
    found, missing_keywords = ats_keyword_match(text)
    score = calculate_resume_score(found, missing_sections)
    gpt_feedback = gpt_resume_feedback(text)

    return {
        "resume_text": text[:500],
        "missing_sections": missing_sections,
        "ats_keywords_found": found,
        "ats_keywords_missing": missing_keywords,
        "resume_score": score,
        "gpt_feedback": gpt_feedback
    }

# ---------------- PART 2 ----------------
@app.post("/resume/jd-match")
async def resume_job_match(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_text_from_pdf(file.file)
    found, missing = ats_keyword_match(resume_text, job_description.lower().split())
    match_percent = int((len(found) / max(len(found)+len(missing),1)) * 100)

    gpt_analysis = gpt_jd_match(resume_text, job_description)

    return {
        "match_percentage": match_percent,
        "matched_keywords": found,
        "missing_keywords": missing,
        "gpt_analysis": gpt_analysis
    }
# To run the app, use the command:
# uvicorn main:app --reload