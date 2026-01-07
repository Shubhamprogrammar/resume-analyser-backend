SECTIONS = {
    "skills": ["skills", "technologies", "tools"],
    "projects": ["projects", "work samples"],
    "experience": ["experience", "employment", "internship"],
    "education": ["education", "qualification"],
    "certifications": ["certification", "certificate"]
}

COMMON_KEYWORDS = [
    "python", "react", "node","data structures","github","mysql",
    "sql", "mongodb", "api", "git"
]

def find_missing_sections(text):
    missing = []
    text_lower = text.lower()

    for section, keywords in SECTIONS.items():
        if not any(k in text_lower for k in keywords):
            missing.append(section)

    return missing

def ats_keyword_match(text, keywords=COMMON_KEYWORDS):
    found = []
    missing = []

    text_lower = text.lower()
    for kw in keywords:
        if kw in text_lower:
            found.append(kw)
        else:
            missing.append(kw)

    return found, missing
