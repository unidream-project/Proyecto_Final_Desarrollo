import scrapy
import re
from datetime import date
from .base_university import BaseUniversitySpider

class UcuencaSpider(BaseUniversitySpider):
    name = "ucuenca"
    allowed_domains = ["ucuenca.edu.ec"]
    start_urls = ["https://www.ucuenca.edu.ec/oferta-academica/grado/"]

    university_name = "Universidad de Cuenca"
    university_type = "Pública"
    university_contact = "https://www.ucuenca.edu.ec/contacto"

    def parse(self, response):
        # Seleccionamos cada tarjeta de carrera en el listado
        items = response.css("div.filter-item")

        for item in items:
            facultad = item.css("a.etiqueta-medium::text").get()
            career_node = item.css("a[href*='/carreras/']")
            career_url = career_node.css("::attr(href)").get()
            career_name = career_node.css("h3.headline-small::text").get()
            degree_title = item.css("p.filter-item__titulado::text").get()

            if career_url:
                yield response.follow(
                    career_url, 
                    callback=self.parse_career,
                    meta={
                        'facultad': facultad,
                        'carrera': career_name,
                        'titulo': degree_title
                    }
                )

    def parse_career(self, response):
        career_raw = response.meta.get('carrera')
        
        # Estructura de datos completa fusionada
        item = {
            # Identidad y Metadatos
            "career_id": re.sub(r'\W+', '_', career_raw.upper()) if career_raw else None,
            "university_name": self.university_name,
            "career_url": response.url,
            "data_collection_date": date.today().strftime("%Y-%m-%d"),
            "university_type": self.university_type,
            "university_contact": self.university_contact,
            
            # Datos de la Carrera
            "career_name": self.clean_text(career_raw),
            "faculty_name": self.clean_text(response.meta.get('facultad')),
            "degree_title": self.clean_text(response.meta.get('titulo')),
            "description": self.clean_text(" ".join(response.css("#descripcion .vision_content p::text").getall())),
            
            # Ubicación y Costos
            "locations": ["Cuenca"],
            "cost": "Gratuita (Pública)",
            
            # Datos Académicos
            "duration": self.clean_text(response.xpath("//p[contains(text(),'Duración')]/following-sibling::p/text()").get()),
            "modality": self.clean_text(response.xpath("//p[contains(text(),'Modalidad de estudios')]/following-sibling::p/text()").get()),
            
            # Malla (Nombre genérico si no hay PDF)
            "study_plan_name": "Malla Curricular Unificada",
            "study_plan_pdf": response.css("a[href$='.pdf']::attr(href)").get() or "No disponible",
            
            "subjects": []
        }

        # =========================
        # EXTRACCIÓN DE MATERIAS (Evitando duplicados de itinerarios)
        # =========================
        subjects_list = []
        # Filtramos para entrar solo al primer itinerario y evitar ciclos repetidos
        malla_principal = response.css("div.itinerario1")
        if not malla_principal:
            malla_principal = response.css("div.malla_curricular_content")

        ciclos = malla_principal.css("div[class*='ciclo_']")
        vistas = set() # Para asegurar unicidad

        for ciclo in ciclos:
            header = ciclo.css("h3.titulo-large::text").get()
            semester_num = None
            if header:
                match = re.search(r'(\d+)', header)
                semester_num = int(match.group(1)) if match else None

            materias = ciclo.css("ul.lista li p::text").getall()
            for materia in materias:
                nombre_limpio = self.clean_text(materia)
                if nombre_limpio:
                    # Huella única para evitar que después del semestre 8 vuelva al 1
                    huella = f"{semester_num}-{nombre_limpio.lower()}"
                    
                    if huella not in vistas:
                        subjects_list.append({
                            "code": None,
                            "name": nombre_limpio,
                            "semester": semester_num
                        })
                        vistas.add(huella)

        item["subjects"] = subjects_list
        yield item