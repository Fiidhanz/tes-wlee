import numpy as np

GENERIC_WORDS = {

    "tutorial",
    "edukasi",
    "belajar",
    "online",
    "tips",
    "cara",
    "panduan",
    "konten",
    "menarik",
    "viral",
    "trend",
    "video",
    "shorts",
    "fyp",
    "tiktok",
    "youtube",
    "instagram",
    "pemula",
    "dasar",
    "mudah",
    "simple",
    "cepat",
    "lengkap",
    "step",
    "step-by-step",
}

IMPORTANT_KEYWORDS = {

    "python",
    "coding",
    "programming",
    "developer",
    "flask",
    "django",
    "javascript",
    "java",
    "php",
    "react",
    "backend",
    "frontend",
    "machine",
    "learning",
    "ai",
    "data",
}

def cosine_similarity_manual(vec1, vec2):

    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    denominator = (
        np.linalg.norm(vec1)
        * np.linalg.norm(vec2)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(vec1, vec2)
        / denominator
    )

def compute_all(user_vec, vectors):

    return np.array([

        cosine_similarity_manual(
            user_vec,
            v
        )

        for v in vectors
    ])

def extract_keywords(text):

    words = set(
        str(text)
        .lower()
        .split()
    )

    words = words - GENERIC_WORDS

    return words

def keyword_overlap_score(
    user_query,
    text
):

    user_words = extract_keywords(
        user_query
    )

    text_words = extract_keywords(
        text
    )

    if len(user_words) == 0:
        return 0.0

    overlap = user_words.intersection(
        text_words
    )

    return (
        len(overlap)
        / len(user_words)
    )

def strict_keyword_match(
    user_query,
    text,
    threshold=0.5
):

    score = keyword_overlap_score(
        user_query,
        text
    )

    return score >= threshold

def important_keyword_filter(
    user_query,
    text
):

    user_words = extract_keywords(
        user_query
    )

    important = user_words.intersection(
        IMPORTANT_KEYWORDS
    )

    if not important:
        return True

    text_words = extract_keywords(
        text
    )

    return len(
        important.intersection(text_words)
    ) > 0