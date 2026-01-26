from ai_backeng.db.supabase_client import supabase
import numpy as np
import json

def get_similar_skills(user_embedding, limit=20):
    response = supabase.table("skills") \
        .select("id, name, embedding") \
        .execute()

    skills = response.data
    user_embedding = np.array(user_embedding, dtype=float)

    for s in skills:
        skill_emb = s["embedding"]

        # Convertir a lista de floats de forma segura
        if isinstance(skill_emb, list):
            skill_embedding = np.array([float(x) for x in skill_emb], dtype=float)
        else:
            skill_embedding = np.array([float(x) for x in json.loads(skill_emb)], dtype=float)

        score = float(np.dot(skill_embedding, user_embedding))
        s["score"] = score
        s["distance"] = 1 - score  # agregamos la distancia

    skills.sort(key=lambda x: x["score"], reverse=True)
    return skills[:limit]
