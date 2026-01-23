import scrapy
from .base_university import BaseUniversitySpider

class EpnSpider(BaseUniversitySpider):
    name = "epn"
    allowed_domains = ["epn.edu.ec"]
    start_urls = ["https://www.epn.edu.ec/oferta-de-grado/"]

    university_name = "Escuela Politécnica Nacional"
    university_type = "Pública"
    university_contact = "admision@epn.edu.ec"

    def parse(self, response):
        # Selector para las tarjetas de carreras (imagen a31cd2)
        career_links = response.css(".news-thum a::attr(href)").getall()
        
        for link in list(set(career_links)):
            if "epn.edu.ec" in link:
                yield response.follow(link, callback=self.parse_career)

    def parse_career(self, response):
        item = self.create_base_item(response)

        # Metadatos institucionales
        item["university_name"] = self.university_name
        item["university_type"] = self.university_type
        item["university_contact"] = self.university_contact
        item["career_url"] = response.url
        item["locations"] = ["Quito"]
        item["cost"] = "Gratuita (Pública)"

        # =========================
        # IDENTIDAD Y ACADÉMICO (Imágenes a29d0d, a29ced, a29cce, a29caf)
        # =========================
        
        # Carrera: Usamos el h1 principal o el título en el infobox de 'Título que otorga'
        # Imagen a29ced muestra el título en un <p> dentro de un infobox
        career_raw = response.css("h1::text").get() or \
                     response.xpath("//h3[contains(.,'Título que otorga')]/following-sibling::p/text()").get()
        item["career_name"] = self.clean_text(career_raw)

        # Facultad (Imagen a29d0d)
        item["faculty_name"] = self.clean_text(
            response.xpath("//h3[contains(.,'Unidad Académica')]/following-sibling::p/text()").get()
        )

        # Título otorgado (Imagen a29ced)
        item["degree_title"] = self.clean_text(
            response.xpath("//h3[contains(.,'Título que otorga')]/following-sibling::p/text()").get()
        )

        # Duración / Semestres (Imagen a29cce)
        item["semesters"] = self.clean_text(
            response.xpath("//h3[contains(.,'Duración')]/following-sibling::p/text()").get()
        )

        # Modalidad (Imagen a29caf)
        item["modality"] = self.clean_text(
            response.xpath("//h3[contains(.,'Modalidad')]/following-sibling::p/text()").get()
        )

        # =========================
        # DESCRIPCIÓN
        # =========================
        # Se mantiene el selector de vision_content o párrafos de la sección descripción
        description_parts = response.css(".elementor-element p::text, .elementor-text-editor p::text").getall()
        item["description"] = self.clean_text(" ".join(description_parts))

        # =========================
        # MALLA CURRICULAR (Imagen a291e4, a29204)
        # =========================
        # La imagen muestra que la malla está en un visor de PDF (iframe o visor de documentos)
        # Buscamos el enlace al PDF que se carga en esa sección
        item["study_plan_pdf"] = response.css("iframe.pdf-viewer::attr(src), a[href$='.pdf']::attr(href)").get()

        yield item