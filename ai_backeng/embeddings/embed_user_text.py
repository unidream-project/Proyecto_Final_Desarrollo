# ai_backeng/embeddings/user_embedding.py

from ai_backeng.embeddings.embedding_provider import get_embedding

def build_user_embedding(profile: dict, new_message: str) -> list[float]:
    text = f"""
    Intereses: {profile.get("intereses", [])}
    Habilidades: {profile.get("habilidades_percibidas", [])}
    Descripción: {profile.get("descripcion_libre", "")}
    Nuevo mensaje: {new_message}
    """
    return get_embedding(text)
