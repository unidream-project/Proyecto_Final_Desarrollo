import json
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_or_create_university(name, utype, contact):
    res = supabase.table("universities").select("*").eq("name", name).execute()
    if res.data:
        return res.data[0]["id"]

    res = supabase.table("universities").insert({
        "name": name,
        "type": utype,
        "contact": contact
    }).execute()

    return res.data[0]["id"]

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def insert_career(career, university_id):
    res = supabase.table("careers").upsert({
        "career_id": career["career_id"],
        "university_id": university_id,
        "career_name": career["career_name"],
        "faculty_name": career.get("faculty_name"),
        "degree_title": career.get("degree_title"),
        "description": career.get("description"),
        "modality": career.get("modality"),
        "duration": career.get("duration"),
        "cost": str(career.get("cost")),
        "career_url": career.get("career_url"),
        "study_plan_name": career.get("study_plan_name"),
        "study_plan_pdf": career.get("study_plan_pdf"),
        "data_collection_date": career.get("data_collection_date")
    }, on_conflict="career_id").execute()

    return res.data[0]["id"]

def insert_subjects(career_id, subjects):
    for s in subjects:
        supabase.table("subjects").insert({
            "career_id": career_id,
            "code": s.get("code"),
            "name": s["name"],
            "semester": s.get("semester")
        }).execute()

def insert_locations(career_id, locations):
    for loc in locations:
        supabase.table("career_locations").insert({
            "career_id": career_id,
            "location": loc
        }).execute()

def process_file(path):
    careers = load_json(path)

    for c in careers:
        university_id = get_or_create_university(
            c["university_name"],
            c.get("university_type"),
            c.get("university_contact")
        )

        career_db_id = insert_career(c, university_id)

        insert_locations(career_db_id, c.get("locations", []))
        insert_subjects(career_db_id, c.get("subjects", []))

        print(f"✔ {c['career_name']}")

if __name__ == "__main__":
    process_file("../data_unificada/UTC.json")   # cambia por tus archivos
