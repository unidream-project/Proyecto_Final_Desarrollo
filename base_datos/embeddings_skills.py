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
    batch_size = 1000
    offset = 0
    total_processed = 0

    while True:
        subjects = supabase.table("subjects") \
            .select("id, name") \
            .is_("embedding", None) \
            .range(offset, offset + batch_size - 1) \
            .execute().data

        if not subjects:
            break

        print(f"📌 Procesando {len(subjects)} subjects (offset {offset})")

        for sub in subjects:
            embedding = get_embedding(sub["name"])

            supabase.table("subjects").update({
                "embedding": embedding,
                "embedding_model": EMBEDDING_MODEL_NAME
            }).eq("id", sub["id"]).execute()

            total_processed += 1
            print(f"✔ Embedded subject: {sub['name']}")

        offset += batch_size

    print(f"🎉 Total subjects embebidos: {total_processed}")


if __name__ == "__main__":
    embed_subjects()
