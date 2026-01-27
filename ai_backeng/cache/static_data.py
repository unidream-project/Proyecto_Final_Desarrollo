# ai_backeng/cache/static_data.py

from ai_backeng.db.supabase_client import supabase

SKILLS = supabase.table("skills").select("id, embedding").execute().data
SUBJECTS = supabase.table("subjects").select("career_id, embedding").execute().data
