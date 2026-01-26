from ai_backeng.db.supabase_client import supabase

def apply_filters(career_scores, preferences):
    filtered = {}

    for career_id, score in career_scores.items():
        career = supabase.table("careers") \
            .select("id, modality") \
            .eq("id", career_id) \
            .single().execute().data

        if preferences["modalidad"]:
            if career["modality"] != preferences["modalidad"]:
                continue

        filtered[career_id] = score

    return filtered
