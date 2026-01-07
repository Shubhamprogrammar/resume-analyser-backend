import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
print("Gemini API Key Loaded",os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def gpt_resume_feedback(resume_text):
    prompt = f"""
    Analyze this resume and provide:
    1. Strengths
    2. Weaknesses
    3. Improvement suggestions

    Resume:
    {resume_text[:2000]}
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    # except ResourceExhausted:
    #     return "AI quota exceeded. Try again later."

    except Exception as e:
        return f"AI error: {str(e)}"


def gpt_jd_match(resume_text, jd_text):
    prompt = f"""
    Compare the resume with the job description.
    Provide:
    - Match summary
    - Skill gaps
    - Hiring recommendation

    Resume:
    {resume_text[:1500]}

    Job Description:
    {jd_text[:1500]}
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except ResourceExhausted:
        return "AI quota exceeded. Try again later."
    except Exception as e:
        return f"AI error: {str(e)}"
