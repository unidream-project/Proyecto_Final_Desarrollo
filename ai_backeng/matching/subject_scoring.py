# ai_backeng/matching/subject_scoring.py

import numpy as np
import json
from ai_backeng.db.supabase_client import supabase

def score_careers_from_subjects(user_embedding):
    career_scores = {}

    subjects = supabase.table("subjects") \
        .select("career_id, embedding") \
        .execute().data

    # Convertir user_embedding a np.array (si aún no lo estaba)
    user_vec = np.array(user_embedding, dtype=float)

    for s in subjects:
        # Convertir embedding guardado como string a lista de floats
        emb = np.array(json.loads(s["embedding"]), dtype=float)  # Usamos json.loads para convertir el string en lista

        # Calcular el score con np.dot
        score = float(np.dot(emb, user_vec))

        cid = s["career_id"]
        career_scores[cid] = career_scores.get(cid, 0) + score

    return career_scores
