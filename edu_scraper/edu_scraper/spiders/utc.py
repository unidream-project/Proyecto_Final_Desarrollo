import scrapy
import re
from .base_university import BaseUniversitySpider

class UtcSpider(BaseUniversitySpider):
    name = "utc"
    allowed_domains = ["utc.edu.ec"]
    start_urls = ["https://www.utc.edu.ec/PLANEAMIENTO2/PREGRADO-prueba"]

    university_name = "Universidad Técnica de Cotopaxi"
    university_type = "Pública"

    def parse(self, response):
        # Captura desde el listado principal (Imagen 1639ee)
        career_nodes = response.css("ul.list1.list_padbot li a.button")

        for node in career_nodes:
            link = node.attrib.get('href')
            name = node.css("::text").get()

            if link:
                yield response.follow(
                    link, 
                    callback=self.parse_career,
                    meta={'career_name_list': name}
                )

    def parse_career(self, response):
        item = self.create_base_item(response)
        
        # =========================
        # IDENTIDAD
        # =========================
        item["career_name"] = self.clean_text(response.meta.get('career_name_list'))

        # Facultad: Buscamos el segundo enlace del breadcrumb (Imagen fcb56d)
        all_breadcrumbs = response.xpath("//span[@id='dnn_dnnBREADCRUMB_lblBreadCrumb']//a[@class='breadcrumb']")
        faculty_name = None
        if len(all_breadcrumbs) >= 2:
            # En extensiones, la facultad suele ser el penúltimo elemento
            faculty_name = all_breadcrumbs[-2].xpath("text()").get()

        if faculty_name:
            item["faculty_name"] = self.clean_text(faculty_name)
        else:
            item["faculty_name"] = "Desconocida"

        # =========================
        # INFORMACIÓN ACADÉMICA
        # =========================

        # TÍTULO (Imágenes fbef15, fbe318, fbe2f4, fbd0ad, fbdf33)
        # 1. Buscamos texto que contenga palabras clave de títulos (Licenciado, Ingeniero)
        # 2. Evitamos nodos que solo contengan el encabezado "Título a otorgarse"
        degree_raw = response.xpath("""
            //span[contains(@style, 'justify')]//text()[normalize-space()] |
            //font//span/text()[normalize-space()] |
            //font/text()[normalize-space()] |
            //strong/following-sibling::span/text() |
            //strong/text()[normalize-space()]
        """).getall()

        # Filtrado inteligente para limpiar "Título a otorgarse" y ruidos
        degree_title = ""
        keywords = ["Licenciado", "Ingeniero", "Médico", "Veterinario", "Arquitecto", "Pedagogía", "Economista", "Abogado", "Contador", "Administrador", "Técnico Superior"]
        
        for text in degree_raw:
            clean = text.replace("Título a otorgarse", "").replace(":", "").replace("\xa0", " ").strip()
            # Si el texto contiene una de nuestras palabras clave y no es solo el encabezado
            if any(key.lower() in clean.lower() for key in keywords) and len(clean) > 5:
                degree_title = clean
                break
        
        item["degree_title"] = self.clean_text(degree_title)

        # SEMESTRES (Imágenes 163271, 163212)
        # El número suele estar entre etiquetas <b>Duración</b> y <b>Semestres</b>
        sem_raw_nodes = response.xpath("""
            //*[contains(text(), 'Duración')]/parent::*//text() | 
            //*[contains(text(), 'Duración')]/following-sibling::*//text() |
            //span[contains(@style, 'justify') and contains(., 'Duración')]//text()
        """).getall()
        
        joined_text = " ".join(sem_raw_nodes).replace("\xa0", " ") # Limpiamos &nbsp;
        
        import re
        # Buscamos el primer grupo de dígitos (8, 9, 10, etc.)
        numbers = re.findall(r'\d+', joined_text)
        
        if numbers:
            item["semesters"] = f"{numbers[0]} Semestres"
        else:
            # Búsqueda de último recurso: buscar el número que precede a la palabra 'Semestre'
            fallback_text = response.xpath("//*[contains(text(), 'Semestre')]//text()").getall()
            joined_fallback = " ".join(fallback_text)
            fallback_numbers = re.findall(r'\d+', joined_fallback)
            
            if fallback_numbers:
                item["semesters"] = f"{fallback_numbers[0]} Semestres"
            else:
                item["semesters"] = "Consultar universidad"

        # =========================
        # INFORMACIÓN GENERAL
        # =========================
        
        narrative_parts = response.xpath("""
            //*[contains(., 'OBJETO DE ESTUDIO') or contains(., 'PERFIL PROFESIONAL')]/following::p[contains(@style, 'justify')][1]//text() |
            //*[contains(., 'OBJETO DE ESTUDIO') or contains(., 'PERFIL PROFESIONAL')]/following::text()[normalize-space()][1] |
            //div[contains(@id, 'ContentPane')]//p[contains(@style, 'justify')]//text() |
            //td[@colspan='4']//text()[not(parent::b) and not(parent::strong) and normalize-space()]
        """).getall()

        # Unimos fragmentos y limpiamos metadatos repetitivos
        full_text = " ".join(narrative_parts).replace("\xa0", " ").strip()
        
        # Filtro para eliminar información que ya tenemos en otros campos (Título, Contacto, etc.)
        # Esto asegura que la descripción sea puramente académica para la IA
        clean_description = re.sub(r'(Título a otorgarse:|Duración:|Resolución:|Correo Electrónico:|Teléfonos:).*', '', full_text, flags=re.DOTALL | re.IGNORECASE).strip()

        if len(clean_description) > 30:
            item["description"] = self.clean_text(clean_description)
        else:
            item["description"] = "Descripción académica disponible en el portal oficial de la UTC."




        item["locations"] = ["Latacunga", "La Maná", "Pujilí"]
        item["cost"] = "Gratuita (Pública)"
        item["modality"] = "Presencial"
        
        # Malla PDF (Imagen 162ecf)
        item["study_plan_pdf"] = response.xpath(
            "//a[contains(@href, '.pdf') and not(contains(@href, '.png'))]/@href"
        ).get() or response.xpath(
            "//td[b[contains(.,'Malla Curricular')]]/preceding-sibling::td//a[contains(@href, '.pdf')]/@href"
        ).get()

        # Validación extra para asegurar que la URL sea absoluta
        if item["study_plan_pdf"] and not item["study_plan_pdf"].startswith("http"):
            item["study_plan_pdf"] = response.urljoin(item["study_plan_pdf"])

        contact_raw = response.xpath("""
            //span[contains(text(), '@utc.edu.ec')]/text() |
            //a[contains(@href, 'mailto:')]/text() |
            //p[strong[contains(., 'Correo')]]/following-sibling::p//span/text() |
            //span[contains(@style, 'justify') and contains(., '@')]/text()
        """).getall()

        university_contact = None
        for text in contact_raw:
            clean_email = text.replace("&nbsp;", "").strip()
            # Validamos que parezca un correo real (cite: image_163212)
            if "@utc.edu.ec" in clean_email.lower():
                university_contact = clean_email
                break
        
        item["university_contact"] = self.clean_text(university_contact) if university_contact else "Contactar vía web oficial"

        yield item