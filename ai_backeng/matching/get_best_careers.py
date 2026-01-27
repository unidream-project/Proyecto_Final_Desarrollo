from ai_backeng.db.vector import to_pgvector
import asyncpg


async def get_best_careers(pool, user_embedding, preferences, top_k=5):
    async with pool.acquire() as conn:

        user_vec = to_pgvector(user_embedding)

        matches = await conn.fetch(
            """
            select *
            from match_careers_by_embedding($1::vector, $2)
            """,
            user_vec,
            top_k
        )

        careers = []

        for row in matches:
            c = await conn.fetchrow(
                """
                select career_name, description, modality, duration
                from careers
                where id = $1
                """,
                row["career_id"]
            )

            if not c:
                continue

            if preferences.get("modalidad"):
                if c["modality"] != preferences["modalidad"]:
                    continue

            careers.append({
                "career_name": c["career_name"],
                "description": c["description"],
                "modality": c["modality"],
                "duration": c["duration"],
                "score": round(row["score"], 3)
            })

        return careers
