from nltk.stem import PorterStemmer
ps = PorterStemmer()

def calculate_match_score(resume_skills, jd_keywords):
    resume_map = {ps.stem(skill.lower().strip()): skill for skill in resume_skills}
    jd_map = {ps.stem(kw.lower().strip()): kw for kw in jd_keywords}

    resume_stemmed = set(resume_map.keys())
    jd_stemmed = set(jd_map.keys())

    matched_stemmed = resume_stemmed & jd_stemmed
    missing_stemmed = jd_stemmed - resume_stemmed

    matched = [resume_map[stem] for stem in matched_stemmed]
    missing = [jd_map[stem] for stem in missing_stemmed]

    score = int(len(matched_stemmed) / max(len(jd_keywords), 1) * 100)
    return score, matched, missing
