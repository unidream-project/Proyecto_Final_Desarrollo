from ai_backeng.matching.skill_matching import get_similar_skills
from ai_backeng.matching.career_scoring import score_careers_from_skills
from ai_backeng.matching.filters import apply_filters
from ai_backeng.db.supabase_client import supabase

def get_best_careers(user_embedding, preferences, top_k=5):
    skill_matches = get_similar_skills(user_embedding)
    career_scores = score_careers_from_skills(skill_matches)
    career_scores = apply_filters(career_scores, preferences)

    ranked = sorted(
        career_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    careers = []
    for career_id, score in ranked:
        c = supabase.table("careers") \
            .select("career_name, description, modality, duration") \
            .eq("id", career_id) \
            .single().execute().data

        c["score"] = round(score, 3)
        careers.append(c)

    return careers
