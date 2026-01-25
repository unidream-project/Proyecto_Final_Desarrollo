import os
from supabase import create_client
from embedding_provider import get_embedding, EMBEDDING_MODEL_NAME
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def embed_skills():
    skills = supabase.table("skills") \
        .select("id, name") \
        .is_("embedding", None) \
        .execute().data

    print(f"📌 Skills sin embedding: {len(skills)}")

    for s in skills:
        embedding = get_embedding(s["name"])

        supabase.table("skills").update({
            "embedding": embedding,
            "embedding_model": EMBEDDING_MODEL_NAME
        }).eq("id", s["id"]).execute()

        print(f"✔ Embedded skill: {s['name']}")

def embed_subjects():
    subjects = supabase.table("subjects") \
        .select("id, name") \
        .is_("embedding", None) \
        .execute().data

    print(f"📌 Subjects sin embedding: {len(subjects)}")

    for sub in subjects:
        embedding = get_embedding(sub["name"])

        supabase.table("subjects").update({
            "embedding": embedding,
            "embedding_model": EMBEDDING_MODEL_NAME
        }).eq("id", sub["id"]).execute()

        print(f"✔ Embedded subject: {sub['name']}")


if __name__ == "__main__":
    embed_skills()
