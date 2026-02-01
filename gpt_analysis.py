import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_API_KEY,
)

def gpt_resume_feedback(resume_text):
    prompt = f"""
You are an ATS + hiring manager.

Analyze the resume and return ONLY valid JSON in the exact format below.

JSON Schema:
{{
  "resume_score": number (0-100),
  "missing_sections": string[],
  "ats_keywords_missing": string[],
  "strengths": [{{"title": string, "detail": string}}],
  "weaknesses": string[],
  "experience_improvements": [
    {{
      "company": string,
      "role": string,
      "bullets": string[]
    }}
  ],
  "project_improvements": [
    {{
      "project": string,
      "improvements": string[]
    }}
  ],
  "skill_matrix": {{
    "proficient": string[],
    "familiar": string[],
    "learning": string[]
  }},
  "certification_fixes": string[],
  "overall_recommendation": string
}}

Rules:
- Return ONLY JSON
- No markdown
- No explanations
- No extra text

Resume:
{resume_text[:2500]}
"""

    completion = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Instruct-0905",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return completion.choices[0].message.content

def gpt_jd_match(resume_text, jd_text):
    prompt = f"""
You are an ATS + hiring manager.

Compare the resume and job description.
Return ONLY valid JSON.

JSON Schema:
{{
  "match_percentage": number,
  "match_summary": string,
  "matched_skills": string[],
  "missing_skills": string[],
  "experience_gaps": string[],
  "final_hiring_recommendation": string
}}

Rules:
- No markdown
- No extra text
- Only JSON

Resume:
{resume_text[:2000]}

Job Description:
{jd_text[:2000]}
"""

    completion = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Instruct-0905",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return completion.choices[0].message.content
