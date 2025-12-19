import re
from sklearn.feature_extraction.text import CountVectorizer

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_keywords(text, top_n=10):
    text = clean_text(text)
    vectorizer = CountVectorizer(stop_words="english")
    X = vectorizer.fit_transform([text])
    freqs = zip(vectorizer.get_feature_names_out(), X.toarray()[0])
    sorted_words = sorted(freqs, key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:top_n]]

def extract_skills(text):
    skill_list = ["python", "java", "sql", "excel", "data analysis",
                  "machine learning", "communication", "teamwork"]
    text_clean = clean_text(text)
    return [skill for skill in skill_list if skill.lower() in text_clean]
