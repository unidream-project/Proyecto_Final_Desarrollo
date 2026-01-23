import scrapy
import re
import os
from .base_university import BaseUniversitySpider

class UideSpider(BaseUniversitySpider):
    name = "uide"
    allowed_domains = ["uide.edu.ec"]

    path_html = os.path.abspath("uide.html")
    start_urls = [f"file://{path_html}"]
    
    university_name = "Universidad Internacional del Ecuador"
    university_type = "Privada"
    university_contact = "admisiones@uide.edu.ec"

    def parse(self, response):
        rows = response.css("table#table-uide-data tbody tr")
        for row in rows:
            td_carrera = row.css("td:nth-child(1)")
            nombre_facultad = row.css("td:nth-child(2)::text").get()
            
            script = td_carrera.attrib.get("onclick", "")
            match = re.search(r'https?://[^"\']+', script)
            
            if match:
                url_carrera = match.group(0).replace('&quot;', '').replace(';', '')
                yield scrapy.Request(
                    url_carrera, 
                    callback=self.parse_career,
                    meta={'facultad_tabla': nombre_facultad}
                )

    def parse_career(self, response):
        item = self.create_base_item(response)
        facultad_tabla = response.meta.get('facultad_tabla')
        current_url = response.url.lower() # Obtenemos la URL para validar modalidad
        
        raw_name = response.css("h1::text").get() or response.css("h2::text").get()
        item["career_name"] = self.clean_text(raw_name)
        item["faculty_name"] = self.clean_text(facultad_tabla) or "General"

        # Extraemos párrafos informativos
        raw_parts = response.css(".elementor-widget-container p::text").getall()
        parts = [self.clean_text(p) for p in raw_parts if self.clean_text(p)]

        if not parts:
            yield item
            return

        # =========================
        # ASIGNACIÓN DE MODALIDAD Y SEDES (Basado en URL)
        # =========================
        # Verificamos si la URL indica modalidad no presencial
        keywords_online = ["en-linea", "virtual", "distancia", "online"]
        is_online_url = any(x in current_url for x in keywords_online)

        if is_online_url:
            item["modality"] = "En línea"
            item["locations"] = ["Virtual"]
        else:
            item["modality"] = "Presencial"
            # Lógica de sedes por contador de precios (solo para presenciales)
            costos_encontrados = [p for p in parts if "$" in p]
            num_precios = len(costos_encontrados)
            
            if num_precios == 1:
                item["locations"] = ["Quito"]
            elif num_precios == 2:
                item["locations"] = ["Quito", "Guayaquil"]
            else:
                item["locations"] = ["Quito", "Guayaquil", "Loja"]

        # =========================
        # DISTRIBUCIÓN CORRECTA DE DATOS
        # =========================
        # Según la estructura: Título -> Duración -> Modalidad -> Inicio -> Costo
        item["degree_title"] = parts[0] if len(parts) > 0 else "Desconocido"
        item["semesters"] = parts[1] if len(parts) > 1 else "Desconocido"
        
        # El costo lo extraemos de la lista de precios encontrados
        precios = [p for p in parts if "$" in p]
        item["cost"] = " | ".join(precios) if precios else "Consultar universidad"

        # =========================
        # CONSTRUCCIÓN DE DESCRIPCIÓN LIMPÍA
        # =========================
        # Filtramos para que la descripción no repita datos ya extraídos
        indices_a_ignorar = {0, 1, 2, 3} # Título, Duración, Modalidad, Inicio
        desc_parts = []
        
        for idx, text in enumerate(parts):
            if idx in indices_a_ignorar or "$" in text:
                continue
            if len(text.split()) > 5: # Solo párrafos con contenido real
                desc_parts.append(text)

        item["description"] = " ".join(desc_parts)

        # Otros campos
        item["university_contact"] = self.clean_text(
            response.css('a[href^="mailto:"]::text').get()
        ) or self.university_contact
        
        item["study_plan_pdf"] = response.css("a[href$='.pdf']::attr(href)").get()

        yield item