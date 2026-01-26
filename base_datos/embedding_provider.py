from sentence_transformers import SentenceTransformer
import os

PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local-e5")

if PROVIDER == "local-e5":
    model = SentenceTransformer("intfloat/multilingual-e5-large")

    def get_embedding(text: str) -> list[float]:
        # E5 requiere prefijo
        text = f"passage: {text}"
        embedding = model.encode(
            text,
            normalize_embeddings=True
        )
        return embedding.tolist()

    EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large"
