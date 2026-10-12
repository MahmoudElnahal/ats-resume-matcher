# vector_utils.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# تحميل نموذج تضمين جاهز
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """
    تحويل نص إلى Embedding باستخدام نموذج transformer
    """
    return model.encode(text, show_progress_bar=False)

def similarity_score(text1: str, text2: str) -> float:
    """
    حساب Cosine Similarity بين نصين
    """
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    return float(cosine_similarity([emb1], [emb2])[0][0]) * 100
