import time
import json
import os
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def clean_text(text):
    if not text: return ""
    return " ".join(text.strip().split())

def scrape_utn_final_discovery():
    print("--- Iniciando Scraping UTN (Descubrimiento y Validación de Contenido) ---")
    
    # Manejo de ruta como pediste
    if not os.path.exists('data'):
        os.makedirs('data')

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1280,720")
    # Agregamos un User-Agent para evitar bloqueos
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # URL base de la UTN
    url_base = "https://www.utn.edu.ec/web/utn/academia/oferta-de-grado"
    careers_data = []

    try:
        print(f"🌍 Accediendo a: {url_base}")
        driver.get(url_base)
        time.sleep(7) # Espera generosa para carga dinámica
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Buscamos todos los links que lleven a /academia/carreras/
        all_links = soup.find_all('a', href=True)
        candidates = set()

        for link in all_links:
            href = link['href']
            if "/academia/carreras/" in href:
                # Asegurar URL completa
                full_url = href if href.startswith("http") else "https://www.utn.edu.ec" + href
                candidates.add(full_url)

        print(f"🔍 Enlaces de carreras detectados: {len(candidates)}. Analizando fichas...")

        for url in candidates:
            try:
                driver.get(url)
                time.sleep(3) # Espera para que renderice la tabla
                c_soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # --- LÓGICA DE EXTRACCIÓN POR TABLA (Basada en tus imágenes) ---
                def get_table_val(label):
                    # Busca la celda que contiene el texto de la etiqueta y toma la siguiente
                    cell = c_soup.find('td', string=re.compile(label, re.I))
                    if cell:
                        sibling = cell.find_next_sibling('td')
                        return clean_text(sibling.get_text()) if sibling else "N/A"
                    return "N/A"

                nombre_carrera = get_table_val("Nombre de la Carrera")
                
                # Solo guardamos si realmente encontramos el nombre en la tabla
                if nombre_carrera != "N/A":
                    item = {
                        "nombre_carrera": nombre_carrera,
                        "nombre_facultad": "Universidad Técnica del Norte", # Se puede refinar
                        "nombre_universidad": "Universidad Técnica del Norte (UTN)",
                        "titulo_egreso": get_table_val("Título que otorga"),
                        "numero_semestres": get_table_val("Número de períodos"),
                        "malla_url": url, 
                        "descripcion": f"Campo Amplio: {get_table_val('Campo amplio')}",
                        "ubicacion": "Ibarra, Campus El Olivo",
                        "publica_privada": "Pública",
                        "costo": "Gratuidad",
                        "modalidad": get_table_val("Modalidad de aprendizaje"),
                        "enlace_carrera": url,
                        "fecha_recoleccion": datetime.now().strftime("%Y-%m-%d"),
                        "contacto": "info@utn.edu.ec"
                    }
                    careers_data.append(item)
                    print(f"✅ Extraída: {nombre_carrera}")
                
            except Exception as e:
                print(f"⚠️ Error analizando {url}: {e}")
                continue

    finally:
        driver.quit()

    # Guardar en JSON
    if careers_data:
        file_path = os.path.join("data", "UTN_carreras_validadas.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(careers_data, f, ensure_ascii=False, indent=4)
        print(f"\n💾 ÉXITO: {len(careers_data)} carreras reales guardadas en la carpeta 'data'.")
    else:
        print("\n❌ No se pudo extraer información. Verifica la conexión o los selectores.")

if __name__ == "__main__":
    scrape_utn_final_discovery()