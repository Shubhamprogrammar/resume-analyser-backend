def calculate_resume_score(found_keywords, missing_sections):
    score = 100
    score -= len(missing_sections) * 10
    score -= (10 - len(found_keywords)) * 3

    return max(score, 0)
