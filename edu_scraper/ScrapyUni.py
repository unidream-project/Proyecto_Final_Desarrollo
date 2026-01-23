import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import pdfplumber
import io
import pandas as pd
import os
import sys
import warnings
from urllib.parse import urljoin
import urllib3
import time

# --- CONFIGURACIÓN ---
sys.stdout.reconfigure(encoding='utf-8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
}

INFO_UNIVERSIDADES = {
    'UISEK':  {'city': 'Quito', 'type': 'Privada', 'contact': 'admisiones@uisek.edu.ec'},
    'UG':     {'city': 'Guayaquil', 'type': 'Pública', 'contact': 'info@ug.edu.ec'},
    'ESPOCH': {'city': 'Riobamba', 'type': 'Pública', 'contact': 'rectorado@espoch.edu.ec'}
}

class AcademicScraper:
    def __init__(self):
        self.dataset = [] 
        if not os.path.exists('data'):
            os.makedirs('data')

    def safe_get(self, url):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30, verify=False)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"      ❌ Error conectando: {e}")
            return None

    def extract_text_from_pdf(self, pdf_url):
        try:
            print(f"      ⬇️ Bajando PDF: {pdf_url}...")
            response = requests.get(pdf_url, headers=HEADERS, timeout=30, verify=False)
            with pdfplumber.open(io.BytesIO(response.content)) as pdf:
                text = "".join([p.extract_text() or "" for p in pdf.pages])
            return " ".join(text.replace('\n', ' ').split())
        except: return None

    def _guardar(self, uni_key, career_name, career_url, study_plan_url, raw_text):
        if not career_name or len(career_name) < 4: return
        
        # Filtros anti-basura
        name_low = career_name.lower()
        if any(x in name_low for x in ['maestría', 'doctorado', 'posgrado', 'diplomado', 'educación continua']): return
        if "noticia" in career_url or "evento" in career_url: return

        meta = INFO_UNIVERSIDADES.get(uni_key, {'city': 'Ec', 'type': 'N/A', 'contact': ''})
        clean_text = " ".join(raw_text.split())

        item = {
            "university_name": uni_key,
            "university_type": meta['type'],
            "university_contact": meta['contact'],
            "career_name": career_name,
            "career_url": career_url,
            "description": clean_text[:3000], 
            "degree_title": "Pendiente IA",
            "faculty": "Pendiente IA",
            "duration": "Pendiente IA",
            "modality": "Presencial",
            "locations": [meta['city']],
            "cost": "Consultar",
            "study_plan_url": study_plan_url,
            "full_raw_text": clean_text[:45000]
        }
        self.dataset.append(item)
        print(f"      ✅ GUARDADO: {career_name[:40]}")

    def finalizar(self, nombre_archivo):
        if not self.dataset:
            print(f"⚠️ {nombre_archivo}: No se extrajeron datos.")
            return
        df = pd.DataFrame(self.dataset)
        ruta = os.path.join("data", f"{nombre_archivo}.json")
        df.to_json(ruta, orient='records', indent=4, force_ascii=False)
        print(f"\n💾 ÉXITO: {ruta} ({len(df)} carreras)")
        self.dataset = []

    def _visitar_pagina(self, url, uni_key, nombre_override=None):
        html = self.safe_get(url)
        if not html: return
        soup = BeautifulSoup(html, 'html.parser')

        # Limpieza
        for tag in soup.select('header, footer, nav, script, style, .menu, .sidebar, #top-bar'): tag.decompose()

        h1 = soup.find('h1')
        nombre = nombre_override if nombre_override else (h1.text.strip() if h1 else "Carrera")
        nombre = nombre.replace("Carrera de", "").replace("Licenciatura en", "").replace("Ingeniería en", "").strip()

        content = ""
        malla_url = url

        # Buscar PDF
        for a in soup.find_all('a', href=True):
            href = a['href'].lower()
            if href.endswith('.pdf') and ("malla" in href or "plan" in href or "curricu" in href):
                malla_url = urljoin(url, a['href'])
                content = self.extract_text_from_pdf(malla_url)
                if content: break
        
        # Texto Web
        if not content:
            body = soup.find('body')
            if body: content = body.get_text(separator=' ')

        self._guardar(uni_key, nombre, url, malla_url, content)

    # ==========================================
    # --- ESTRATEGIAS ESPECIALES ---
    # ==========================================

    def scrape_uisek(self):
        print("\n--- Scrapeando UISEK (Lista Directa) ---")
        # UISEK suele tener una página de "Programas" limpia
        start_urls = [
            "https://uisek.edu.ec/oferta-academica/",
            "https://uisek.edu.ec/pregrado/"
        ]
        visited = set()
        
        for url in start_urls:
            html = self.safe_get(url)
            if not html: continue
            soup = BeautifulSoup(html, 'html.parser')
            
            # Buscamos enlaces a carreras
            for a in soup.find_all('a', href=True):
                href = a['href']
                full = urljoin(url, href)
                txt = a.text.strip()
                
                # Filtro: URL que contenga "carrera" o "ingenieria" o esté en el path de oferta
                if "uisek.edu.ec" in full:
                    if "/carrera/" in full or "/programa/" in full or "ingenieria" in full:
                        if full not in visited and len(txt) > 5:
                            print(f"   🎯 Candidata: {txt[:30]}")
                            self._visitar_pagina(full, "UISEK", nombre_override=txt)
                            visited.add(full)
        self.finalizar("UISEK")

    def scrape_espoch(self):
        print("\n--- Scrapeando ESPOCH (Facultades) ---")
        # ESPOCH organiza por facultades. Vamos a la lista raíz.
        url_base = "https://www.espoch.edu.ec/"
        html = self.safe_get(url_base)
        visited = set()
        
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # Buscamos en el menú "Oferta Académica" o "Facultades"
            for a in soup.find_all('a', href=True):
                txt = a.text.strip().lower()
                href = a['href']
                full = urljoin(url_base, href)
                
                # Buscamos palabras clave de carrera directamente en el menú
                keywords = ['ingeniería', 'licenciatura', 'escuela de', 'carrera de']
                if any(k in txt for k in keywords):
                    if "posgrado" not in full and "maestria" not in full:
                        if full not in visited:
                            print(f"   🎯 Detectada: {txt[:30]}")
                            self._visitar_pagina(full, "ESPOCH", nombre_override=a.text.strip())
                            visited.add(full)
        self.finalizar("ESPOCH")

    def scrape_ug(self):
        print("\n--- Scrapeando UG (Fuerza Bruta por Facultades) ---")
        # UG es muy difícil. Vamos a intentar acceder a las facultades comunes.
        # Estas son URLs probables de facultades de la UG.
        facultades_posibles = [
            "http://www.ug.edu.ec/oferta-academica-grado/",
            "http://www.ug.edu.ec/facultad-ciencias-administrativas/",
            "http://www.ug.edu.ec/facultad-ciencias-agrarias/",
            "http://www.ug.edu.ec/facultad-ciencias-medicas/",
            "http://www.ug.edu.ec/facultad-ingenieria-industrial/",
            "http://www.ug.edu.ec/facultad-ingenieria-quimica/",
            "http://www.ug.edu.ec/facultad-ciencias-matematicas-fisicas/"
        ]
        
        visited = set()
        
        for fac in facultades_posibles:
            print(f"   🏛️ Probando: {fac}...")
            html = self.safe_get(fac)
            if not html: continue
            
            soup = BeautifulSoup(html, 'html.parser')
            # Buscar enlaces que digan "Carrera" o "Malla"
            for a in soup.find_all('a', href=True):
                txt = a.text.strip().lower()
                href = a['href']
                full = urljoin(fac, href)
                
                if "carrera" in txt or "ingeniería" in txt or "licenciatura" in txt:
                    if "ug.edu.ec" in full and full not in visited:
                         print(f"      🎯 Carrera UG: {txt[:30]}")
                         self._visitar_pagina(full, "UG")
                         visited.add(full)
                
                # Si encontramos un PDF directo de malla
                if "malla" in txt and href.endswith('.pdf'):
                    if full not in visited:
                        print(f"      📄 Malla PDF: {txt[:30]}")
                        content = self.extract_text_from_pdf(full)
                        self._guardar("UG", txt.title(), fac, full, content)
                        visited.add(full)

        self.finalizar("UG")

if __name__ == "__main__":
    bot = AcademicScraper()
    
    bot.scrape_uisek()
    bot.scrape_espoch()
    bot.scrape_ug()