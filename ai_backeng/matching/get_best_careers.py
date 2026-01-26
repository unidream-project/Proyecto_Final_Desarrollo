# ai_backeng/matching/get_best_careers.py

from ai_backeng.matching.skill_matching import get_similar_skills
from ai_backeng.matching.career_scoring import score_careers_from_skills
from ai_backeng.matching.subject_scoring import score_careers_from_subjects
from ai_backeng.matching.merge_scores import merge_scores
from ai_backeng.matching.filters import apply_filters
from ai_backeng.db.supabase_client import supabase

def get_best_careers(user_embedding, preferences, top_k=5):
    skill_matches = get_similar_skills(user_embedding)
    skill_scores = score_careers_from_skills(skill_matches)

    subject_scores = score_careers_from_subjects(user_embedding)

    career_scores = merge_scores(skill_scores, subject_scores)
    career_scores = apply_filters(career_scores, preferences)

    ranked = sorted(
        career_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    careers = []
    for cid, score in ranked:
        c = supabase.table("careers") \
            .select("career_name, description, modality, duration") \
            .eq("id", cid) \
            .single().execute().data

        c["score"] = round(score, 3)
        careers.append(c)

    return careers
