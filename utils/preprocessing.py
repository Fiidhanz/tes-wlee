import re

STOPWORDS = {
    "dan", "di", "ke", "dari", "yang", "untuk", "pada", "dengan",
    "adalah", "itu", "ini", "atau", "karena", "sebagai", "oleh",
    "dalam", "juga", "agar", "lebih", "kurang", "akan", "bisa",
    "jadi", "seperti", "tentang"
}

def is_valid_topic(text):

    text = str(text).lower().strip()

    if len(text) < 5:
        return False

    if len(text.split()) > 8:
        return False

    if re.search(r'(.)\1{4,}', text):
        return False

    spam_words = [
        "slot",
        "gacor",
        "rtp",
        "maxwin",
        "login",
        "apk",
        "cyou",
        "musang",
        "xlme"
    ]

    if any(w in text for w in spam_words):
        return False

    digit_ratio = sum(c.isdigit() for c in text) / max(len(text), 1)

    if digit_ratio > 0.3:
        return False

    return True

def case_folding(text):
    if text is None:
        return ""
    return str(text).lower()

def cleaning(text):
    if text is None:
        return ""
    return re.sub(r'[^a-z0-9 ]', ' ', text)

def tokenizing(text):
    if not text:
        return []
    return [t for t in text.split() if t]

def stopword_removal(tokens):
    if not tokens:
        return []
    return [t for t in tokens if t not in STOPWORDS]

def full_preprocess(text):

    text_cf = case_folding(text)
    text_clean = cleaning(text_cf)
    tokens = tokenizing(text_clean)
    tokens_no_stop = stopword_removal(tokens)

    # 🔥 fallback safety (biar tidak kosong total)
    if not tokens_no_stop:
        tokens_no_stop = tokens

    return {
        "case_folding": text_cf,
        "cleaning": text_clean,
        "tokenization": tokens,
        "tokens": tokens,                  # raw tokens
        "final_tokens": tokens_no_stop,    # after stopword
        "final_text": " ".join(tokens_no_stop)
    }