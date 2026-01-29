import google.generativeai as genai
import json
import re

# Configura tu API KEY aquí o en variables de entorno
# genai.configure(api_key="TU_API_KEY")

def extract_profile_updates(user_message: str, current_profile: dict):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # NO le pasamos el perfil completo. Solo queremos extraer datos nuevos.
    prompt = f"""
    Actúa como un extractor de entidades para un sistema de orientación vocacional.
    
    MENSAJE DEL USUARIO: "{user_message}"
    
    TU TAREA:
    Analiza el mensaje y extrae SOLO la información nueva explícita en formato JSON.
    
    CAMPOS A BUSCAR:
    - nombre: (str) Solo si el usuario se presenta.
    - ciudad: (str) Ciudad de residencia.
    - habilidades: (list) Habilidades técnicas o blandas (ej: "sé python", "liderazgo").
    - intereses: (list) Temas que le gustan (ej: "inteligencia artificial", "mecánica").
    - materias_fuertes: (list) Materias donde le va bien.
    - materias_debiles: (list) Materias que no le gustan o le cuestan.
    - has_career_intent: (bool) TRUE si el mensaje implica una preferencia vocacional, búsqueda de carrera o habilidad. FALSE si es solo saludo o charla casual.
    
    REGLAS:
    1. Si no hay info para un campo, NO lo incluyas en el JSON.
    2. Responde SOLO con el JSON válido, sin bloques de código ```json.
    """
    
    try:
        response = model.generate_content(prompt)
        
        # Limpieza robusta de JSON (a veces los modelos meten texto extra)
        clean_text = response.text.strip()
        # Eliminar posibles bloques de código markdown
        clean_text = re.sub(r"```json|```", "", clean_text).strip()
        
        updates = json.loads(clean_text)
        
        # --- AQUÍ SUCEDE LA MAGIA EN PYTHON (Merge Seguro) ---
        
        # 1. Copiamos el perfil actual para no mutar el original por error
        updated_profile = current_profile.copy()
        
        # 2. Actualizamos campos simples (sobre-escritura)
        for field in ["nombre", "ciudad"]:
            if field in updates and updates[field]:
                updated_profile[field] = updates[field]
                
        # 3. Actualizamos listas (append sin duplicados)
        list_fields = ["habilidades", "intereses", "materias_fuertes", "materias_debiles"]
        for field in list_fields:
            if field in updates and isinstance(updates[field], list):
                # Aseguramos que exista la lista en el perfil original
                if field not in updated_profile:
                    updated_profile[field] = []
                
                # Agregamos solo lo que no existía (evita duplicados exactos)
                current_set = set(updated_profile[field])
                for item in updates[field]:
                    if item not in current_set:
                        updated_profile[field].append(item)

        # 4. Devolvemos el perfil completo + el flag de intención para el embedding
        return {
            "profile_data": updated_profile,
            "has_career_intent": updates.get("has_career_intent", False)
        }

    except Exception as e:
        print(f"Error en extractor: {e}")
        # En caso de error, devolvemos el perfil sin cambios y false
        return {
            "profile_data": current_profile,
            "has_career_intent": False
        }