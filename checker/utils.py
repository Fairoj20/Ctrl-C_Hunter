import io
from PyPDF2 import PdfReader
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def extract_text_from_file(file_obj, filename=None):
    """
    Accepts a Django InMemoryUploadedFile or file-like object.
    Try PDF extraction, otherwise decode bytes as text.
    """
    name = filename or getattr(file_obj, 'name', '') or ''
    if name.lower().endswith('.pdf'):
        try:
            file_obj.seek(0)
            reader = PdfReader(file_obj)
            pages = []
            for p in reader.pages:
                pages.append(p.extract_text() or "")
            return "\n".join(pages)
        except Exception:
            try:
                file_obj.seek(0)
                return file_obj.read().decode('utf-8', errors='ignore')
            except Exception:
                return ""
    else:
        try:
            file_obj.seek(0)
            return file_obj.read().decode('utf-8', errors='ignore')
        except Exception:
            return ""


def normalize_text(text):
    if not text:
        return ""
    # Lowercase, remove repeated whitespace and punctuation
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^0-9a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def compute_similarity(text1, text2):
    """
    Return similarity_score in [0,1] and a human-readable status.
    Uses TF-IDF + cosine similarity with improved handling for short texts.
    """
    t1 = normalize_text(text1 or "")
    t2 = normalize_text(text2 or "")

    if not t1 or not t2:
        return 0.0, 'DIFFERENT'

    if t1 == t2:
        return 1.0, 'IDENTICAL'

    try:
        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words=None,
            ngram_range=(1, 2),
            min_df=1
        )

        tfidf_matrix = vectorizer.fit_transform([t1, t2])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except Exception as e:
        print(f"Error in similarity calculation: {e}")
        return 0.0, 'ERROR'

    similarity_score = float(sim)

    if similarity_score >= 0.85:
        status = 'IDENTICAL'
    elif similarity_score >= 0.6:
        status = 'HIGHLY SIMILAR'
    elif similarity_score >= 0.4:
        status = 'SIMILAR'
    elif similarity_score >= 0.2:
        status = 'SOMEWHAT SIMILAR'
    else:
        status = 'DIFFERENT'

    return similarity_score, status


