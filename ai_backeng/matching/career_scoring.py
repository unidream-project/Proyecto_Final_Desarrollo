from ai_backeng.db.supabase_client import supabase

def score_careers_from_skills(skill_matches):
    career_scores = {}

    for s in skill_matches:
        skill_id = s["id"]
        weight = 1 - s["distance"]  # más cerca = mejor

        links = supabase.table("career_skills") \
            .select("career_id") \
            .eq("skill_id", skill_id) \
            .execute().data

        for link in links:
            cid = link["career_id"]
            career_scores[cid] = career_scores.get(cid, 0) + weight

    return career_scores
