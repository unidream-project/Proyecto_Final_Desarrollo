import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime
import urllib3

# Configuración
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def clean_text(text):
    if not text: return ""
    return " ".join(text.strip().replace('\xa0', ' ').split())

def deducir_duracion_por_niveles(texto_completo):
    niveles_encontrados = []
    patrones = [
        r'(?:Nivel|Semestre|Ciclo)\s+(?:No\.\s*)?(\d+)',
        r'(?:Nivel|Semestre|Ciclo)\s+(Uno|Dos|Tres|Cuatro|Cinco|Seis|Siete|Ocho|Nueve|Diez)'
    ]
    mapa_numeros = {
        'Uno': 1, 'Dos': 2, 'Tres': 3, 'Cuatro': 4, 'Cinco': 5, 
        'Seis': 6, 'Siete': 7, 'Ocho': 8, 'Nueve': 9, 'Diez': 10
    }
    for patron in patrones:
        coincidencias = re.findall(patron, texto_completo, re.IGNORECASE)
        for c in coincidencias:
            if c in mapa_numeros:
                niveles_encontrados.append(mapa_numeros[c])
            elif str(c).isdigit():
                niveles_encontrados.append(int(c))
    
    if niveles_encontrados:
        max_nivel = max(niveles_encontrados)
        if 4 <= max_nivel <= 12:
            return f"{max_nivel} Semestres (Deducido)"
    return "No especificado"

def scrape_utn():
    print("--- Iniciando Scraping UTN (Estrategia por Facultades) ---")
    
    if not os.path.exists('data'):
        os.makedirs('data')

    UNI_DATA = {
        "nombre_universidad": "Universidad Técnica del Norte",
        "siglas": "UTN",
        "ubicacion": "Ibarra",
        "tipo": "Pública",
        "contacto": "info@utn.edu.ec",
        "costo": "Gratuita (Sistema Público)"
    }

    # LISTA MAESTRA DE FACULTADES (URLs directas de oferta académica)
    # Estas son las páginas donde viven realmente los enlaces
    seed_urls = [
        ("https://www.utn.edu.ec/fica/oferta-academica/", "FICA"),   # Ingenierías
        ("https://www.utn.edu.ec/fecyt/oferta-academica/", "FECYT"), # Educación
        ("https://www.utn.edu.ec/facae/oferta-academica/", "FACAE"), # Administrativas
        ("https://www.utn.edu.ec/fccss/oferta-academica/", "FCCSS"), # Salud
        ("https://www.utn.edu.ec/ficaya/oferta-academica/", "FICAYA") # Agropecuarias (A veces redirige a FINA)
    ]
    
    careers_data = []
    urls_visitadas = set()
    links_to_scrape = []

    # --- FASE 1: RECOLECCIÓN DE LINKS ---
    print(f"📡 Buscando carreras en {len(seed_urls)} facultades...")

    for url, fac_name in seed_urls:
        try:
            print(f"   --> Explorando Facultad: {fac_name} ({url})")
            response = requests.get(url, headers=headers, verify=False, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar todos los enlaces dentro del área de contenido principal
            # WordPress suele usar 'entry-content', 'elementor-widget-container', etc.
            content_area = soup.find('div', class_='entry-content') or soup.find('body')
            links = content_area.find_all('a', href=True)

            count_local = 0
            for link in links:
                href = link['href']
                text = link.get_text(" ", strip=True).lower()
                
                # FILTROS DE LIMPIEZA
                # 1. Ignorar archivos y anclas
                if href.startswith('#') or any(href.lower().endswith(x) for x in ['.jpg', '.png', '.pdf', '.zip']):
                    continue
                
                # 2. Ignorar páginas administrativas/basura común
                keywords_bad = ["malla", "horario", "docente", "noticia", "evento", "contacto", "login", "campus", "autoridades", "misión"]
                if any(bad in text for bad in keywords_bad) or any(bad in href.lower() for bad in keywords_bad):
                    continue

                # 3. Validar dominio (debe ser subdominio de UTN)
                if "utn.edu.ec" not in href:
                    continue

                # 4. CRITERIO DE ACEPTACIÓN:
                # Si el enlace es largo (probable página interna) y no está visitado
                if href not in urls_visitadas and len(href) > 25:
                    # Filtro extra: Que no sea la misma URL de la facultad
                    if href.rstrip('/') != url.rstrip('/'):
                        links_to_scrape.append((href, fac_name))
                        urls_visitadas.add(href)
                        count_local += 1
            
            print(f"       + Encontrados {count_local} enlaces potenciales.")

        except Exception as e:
            print(f"       ❌ Error conectando a {fac_name}: {e}")

    print(f"\nℹ️ Total de enlaces únicos a analizar: {len(links_to_scrape)}")

    # --- FASE 2: SCRAPING INDIVIDUAL ---
    for full_url, fac_origin in links_to_scrape:
        # Pausa pequeña para no saturar
        # time.sleep(0.5) 
        
        try:
            c_resp = requests.get(full_url, headers=headers, verify=False, timeout=15)
            c_soup = BeautifulSoup(c_resp.text, 'html.parser')

            # Limpieza visual
            for trash in c_soup.select('header, nav, footer, .sidebar, .widget'):
                trash.decompose()

            body_text = c_soup.get_text(" ", strip=True)

            # --- EXTRACCIÓN DE DATOS ---
            
            # 1. NOMBRE
            h1 = c_soup.find('h1', class_='entry-title') or c_soup.find('h1')
            nombre_carrera = clean_text(h1.text) if h1 else "Desconocido"

            # Validación crítica: Si el H1 es "Inicio" o "Oferta Académica", no es una carrera
            if nombre_carrera.lower() in ["inicio", "home", "oferta académica", "facultad", "bienvenidos"]:
                print(f"   ⚠️ Descartado (No es página de carrera): {full_url}")
                continue

            # 2. FACULTAD (Usamos la de origen si no encontramos otra)
            facultad = fac_origin

            # 3. TÍTULO
            titulo = "No especificado"
            match_tit = re.search(r'(?:Título|Profesional)[:\s]*([A-Za-zÁÉÍÓÚáéíóúñÑ\.\s]+?)(?:\.|\n|Duración|Modalidad|$)', body_text, re.IGNORECASE)
            if match_tit: titulo = clean_text(match_tit.group(1))

            # 4. DURACIÓN
            semestres = deducir_duracion_por_niveles(body_text)

            # 5. MODALIDAD
            modalidad = "Presencial"
            if "semipresencial" in body_text.lower(): modalidad = "Semipresencial"
            elif "en línea" in body_text.lower(): modalidad = "En Línea"
            elif "híbrida" in body_text.lower(): modalidad = "Híbrida"

            # 6. MALLA
            malla = "No encontrada"
            # Buscar PDF
            for a in c_soup.find_all('a', href=True):
                if '.pdf' in a['href'].lower() and ('malla' in a.text.lower() or 'curricular' in a.text.lower()):
                    malla = a['href']
                    break
            # Buscar Imagen
            if malla == "No encontrada":
                for img in c_soup.find_all('img', src=True):
                    if 'malla' in img['src'].lower():
                        malla = img['src']
                        break

            # 7. DESCRIPCIÓN
            descripcion = ""
            match_desc = re.search(r'(?:Perfil Profesional|Objetivo|Misión)(.*?)(?:Perfil Ocupacional|Visión|Malla)', body_text, re.IGNORECASE | re.DOTALL)
            if match_desc:
                descripcion = clean_text(match_desc.group(1))[:800]
            else:
                # Intento genérico: Primer párrafo largo
                paras = c_soup.select('div.entry-content p')
                for p in paras:
                    if len(p.text) > 150:
                        descripcion = clean_text(p.text)
                        break

            item = {
                "nombre_carrera": nombre_carrera,
                "nombre_facultad": facultad,
                "nombre_universidad": UNI_DATA["nombre_universidad"],
                "nombre_titulo": titulo,
                "numero_semestres": semestres,
                "malla_url": malla,
                "descripcion_carrera": descripcion,
                "ubicacion_sedes": [UNI_DATA["ubicacion"]],
                "tipo_universidad": UNI_DATA["tipo"],
                "costo": UNI_DATA["costo"],
                "modalidad": modalidad,
                "enlace_carrera": full_url,
                "fecha_recoleccion": datetime.now().strftime("%Y-%m-%d"),
                "contacto_universidad": UNI_DATA["contacto"]
            }

            careers_data.append(item)
            print(f"   ✅ Guardado: {nombre_carrera}")

        except Exception as e:
            print(f"   ❌ Error en {full_url}: {e}")

    # Guardar
    if careers_data:
        file_path = os.path.join("data", "UTN_careers.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(careers_data, f, ensure_ascii=False, indent=4)
        print(f"\n💾 ÉXITO FINAL: {file_path} generado con {len(careers_data)} carreras.")
    else:
        print("\n⚠️ Aún no se encontraron datos. Verifica manualmente las URLs de las facultades.")

if __name__ == "__main__":
    scrape_utn()