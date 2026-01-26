
def empty_profile():
    return {
        # Lo que el usuario DICE explícitamente
        "intereses": [],
        "habilidades_percibidas": [],

        # Preferencias duras (filtros)
        "preferencias": {
            "modalidad": None,
            "ciudad": None,
            "universidad_publica": None
        },

        # Texto libre acumulado (resumen conversacional)
        "descripcion_libre": "",

        # Embedding acumulado del usuario (CLAVE)
        "user_embedding": None
    }