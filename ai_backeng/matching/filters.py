from ai_backeng.db.supabase_client import supabase

import unicodedata

def normalize_text(text: str) -> str:
    """
    Convierte a minúsculas y quita tildes/acentos
    """
    if not text:
        return ""
    text = text.lower().strip()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

def apply_filters(career_scores, preferences):
    filtered = {}

    # normalizar modalidad del usuario
    pref_modality = normalize_text(preferences.get("modalidad"))

    for career_id, score in career_scores.items():
        career = supabase.table("careers") \
            .select("id, modality") \
            .eq("id", career_id) \
            .single().execute().data

        career_modality = normalize_text(career.get("modality"))

        # Si el usuario especificó modalidad, filtramos
        if pref_modality and career_modality != pref_modality:
            continue

        filtered[career_id] = score

    return filtered


#def apply_filters(career_scores, preferences):
#    filtered = {}
#
#    for career_id, score in career_scores.items():
#        career = supabase.table("careers") \
#            .select("id, modality") \
#            .eq("id", career_id) \
#            .single().execute().data
#
#        if preferences["modalidad"]:
#            if career["modality"] != preferences["modalidad"]:
#                continue
#
#        filtered[career_id] = score
#
#    return filtered
