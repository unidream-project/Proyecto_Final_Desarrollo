import json
import os
import time
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv
from unidecode import unidecode

# ======================
# CONFIG
# ======================

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# ======================
# UTILIDADES
# ======================

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def normalize_skill(skill: str) -> str:
    skill = skill.lower()
    skill = unidecode(skill)
    skill = skill.replace(" y ", " ")
    skill = skill.replace("/", " ")
    skill = " ".join(skill.split())
    return skill.strip()

def infer_category(skill: str) -> str:
    s = skill.lower()

    if any(k in s for k in ["analisis", "calculo", "modelado", "simulacion"]):
        return "analitica"
    if any(k in s for k in ["comunicacion", "presentacion", "expresar"]):
        return "comunicacion"
    if any(k in s for k in ["equipo", "colabor"]):
        return "blanda"
    if any(k in s for k in ["creativ", "diseno", "innov"]):
        return "creativa"
    if any(k in s for k in ["gestionar", "proyecto", "planificar"]):
        return "gestion"
    return "tecnica"

# ======================
# CARRERAS (solo lookup)
# ======================

def get_career_db_id(career_id):
    res = supabase.table("careers") \
        .select("id") \
        .eq("career_id", career_id) \
        .execute()

    if not res.data:
        return None

    return res.data[0]["id"]

# ======================
# SKILLS
# ======================

def get_or_create_skill(skill_name: str):
    normalized = normalize_skill(skill_name)

    res = supabase.table("skills") \
        .select("id") \
        .eq("normalized_name", normalized) \
        .execute()

    if res.data:
        return res.data[0]["id"]

    res = supabase.table("skills").insert({
        "name": skill_name,
        "normalized_name": normalized,
        "category": infer_category(skill_name)
    }).execute()

    time.sleep(0.05)
    return res.data[0]["id"]

def insert_career_skills(career_db_id, skills):
    for skill_name in skills:
        skill_id = get_or_create_skill(skill_name)

        supabase.table("career_skills").upsert({
            "career_id": career_db_id,
            "skill_id": skill_id,
            "weight": 1.0,
            "source": "career_general_skills"
        }, on_conflict="career_id,skill_id").execute()

        time.sleep(0.05)

# ======================
# MAIN
# ======================

def process_file(path):
    careers = load_json(path)

    for c in careers:
        career_db_id = get_career_db_id(c["career_id"])

        if not career_db_id:
            print(f"⚠ Carrera no encontrada: {c['career_name']}")
            continue

        insert_career_skills(
            career_db_id,
            c.get("career_general_skills", [])
        )

        print(f"✔ Skills cargadas: {c['career_name']}")

# ======================
# ENTRYPOINT
# ======================

if __name__ == "__main__":
    INPUT_DIR = Path("../data_skills_final/")

    for archivo in INPUT_DIR.glob("*.json"):
        process_file(archivo)

#UARTES
#EPN
#UCUENCA
#UTC
#UDLA