import google.generativeai as genai
import json
import os
import requests
import PIL.Image
from pathlib import Path
from dotenv import load_dotenv
from pdf2image import convert_from_path

# =========================
# 1. CARGA DE VARIABLES DE ENTORNO
# =========================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la GEMINI_API_KEY en el archivo .env")

genai.configure(api_key=API_KEY)

# =========================
# 2. CONFIGURACIÓN DE RUTAS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
universidad = "epn"  # Ajusta según la universidad (utc, epn, etc.)

INPUT_JSON = os.path.abspath(
    os.path.join(BASE_DIR, "..", "data", f"{universidad}_careers.json")
)

OUTPUT_DIR = Path(os.path.join(BASE_DIR, "..", "data_malla"))
TEMP_PDF_DIR = Path(os.path.join(BASE_DIR, "temp_pdfs"))

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_PDF_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# 3. FUNCIONES DE PROCESAMIENTO
# =========================

def descargar_pdf(url, nombre_archivo):
    ruta_local = TEMP_PDF_DIR / nombre_archivo
    try:
        # verify=False para evitar problemas de SSL
        response = requests.get(url, stream=True, timeout=25, verify=False)
        response.raise_for_status()
        with open(ruta_local, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return str(ruta_local)
    except Exception as e:
        print(f"   ❌ Error descargando {url}: {e}")
        return None

def procesar_malla_con_vision_ia(ruta_pdf):
    """Convierte PDF a imagen y procesa con Gemini Vision"""
    try:
        # Convertimos PDF a imágenes (una por página)
        paginas_imagenes = convert_from_path(ruta_pdf)
    except Exception as e:
        return {"error": f"Error al convertir PDF a imagen: {e}"}
    
    # Usamos el modelo flash para visión
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash', # Recomendado para visión masiva y estable
        generation_config={"response_mime_type": "application/json"}
    )

    # El prompt solicitado para análisis visual
    prompt = """
    Analiza visualmente esta imagen de una malla curricular y extrae los datos en formato JSON.
    
    Extrae:
    - universidad (nombre de la institución)
    - carrera (nombre del programa)
    - pensum (año o versión)
    - materias (lista de objetos: codigo, nombre, creditos, horas, semestre)
    - totales (objeto: total_creditos, total_horas)

    Es vital que revises cada semestre visualmente. Si un dato no es legible, pon "null".
    """

    try:
        # Enviamos prompt + lista de imágenes de las páginas
        contenido_para_ia = [prompt] + paginas_imagenes
        response = model.generate_content(contenido_para_ia)
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"Fallo en comunicación con IA: {str(e)}"}

# =========================
# 4. LÓGICA PRINCIPAL (MAIN)
# =========================

def main():
    print(f"🔍 Iniciando proceso para: {universidad}")
    print(f"📂 Leyendo: {INPUT_JSON}")

    if not os.path.exists(INPUT_JSON):
        print(f"❌ Error: No existe el archivo {INPUT_JSON}")
        return

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        carreras_scrapy = json.load(f)

    lista_final_formateada = []
    contador_api = 0

    for item_scrapy in carreras_scrapy:
        url_pdf = item_scrapy.get("study_plan_pdf")
        nombre_carrera = item_scrapy.get("career_name", "sin_nombre")

        # Saltar si no hay URL válida
        if not url_pdf or url_pdf == "null":
            continue

        # Lógica de rotación/cambio de API Key cada 5 elementos
        if contador_api > 0 and contador_api % 5 == 0:
            print("\n" + "!"*40)
            print(f"🔔 Lote de 5 completado.")
            nueva_key = input("🔑 Ingresa una NUEVA API KEY (o presiona Enter para seguir con la misma): ").strip()
            if nueva_key:
                genai.configure(api_key=nueva_key)
            print("!"*40 + "\n")

        print(f"🚀 ({contador_api + 1}) Procesando: {nombre_carrera}")
        
        # Limpiar nombre para el archivo local
        nombre_archivo = nombre_carrera.replace(" ", "_").replace("/", "-")[:50] + ".pdf"
        ruta_pdf = descargar_pdf(url_pdf, nombre_archivo)

        if ruta_pdf:
            # PROCESAR USANDO VISIÓN (PDF -> IMAGEN -> IA)
            datos_ia = procesar_malla_con_vision_ia(ruta_pdf)
            
            # Normalizar respuesta si viene en lista
            if isinstance(datos_ia, list) and len(datos_ia) > 0:
                datos_ia = datos_ia[0]
            if not isinstance(datos_ia, dict):
                datos_ia = {}

            # Construir objeto final manteniendo la estructura anterior
            objeto_formateado = {
                "universidad": datos_ia.get("universidad") or "Universidad Técnica de Cotopaxi",
                "carrera": nombre_carrera,
                "career_url_ref": url_pdf, 
                "pensum": datos_ia.get("pensum") or "Vigente",
                "materias": datos_ia.get("materias") if isinstance(datos_ia.get("materias"), list) else [],
                "totales": datos_ia.get("totales") if isinstance(datos_ia.get("totales"), dict) else {"total_creditos": 0, "total_horas": 0}
            }
            
            lista_final_formateada.append(objeto_formateado)
            
            # Limpiar archivo temporal
            if os.path.exists(ruta_pdf):
                os.remove(ruta_pdf)
            
            contador_api += 1

    # Guardar resultados
    archivo_final = OUTPUT_DIR / f"{universidad}_mallas_vision_total.json"
    with open(archivo_final, "w", encoding="utf-8") as f:
        json.dump(lista_final_formateada, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ ¡Proceso terminado! Datos guardados en: {archivo_final}")

if __name__ == "__main__":
    main()