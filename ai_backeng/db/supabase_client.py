import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_all_careers():
    response = supabase.table("careers").select(
        "career_name, description, modality, duration"
    ).execute()
    return response.data
