import scrapy
from .base_university import BaseUniversitySpider

class UdlaSpider(BaseUniversitySpider):
    name = "udla"
    allowed_domains = ["udla.edu.ec"]

    university_name = "Universidad de Las Américas"
    university_type = "Privada"
    university_contact = "https://www.udla.edu.ec/es/contactos"

    api_url = (
        "https://www.udla.edu.ec/api/careers/"
        "?viewDisplay=undergraduates--grid_by_undergraduate"
        "&keys=&modality=&faculty=&page={page}"
    )

    def start_requests(self):
        for page in range(0, 7):
            yield scrapy.Request(
                url=self.api_url.format(page=page),
                callback=self.parse_api
            )

    def parse_api(self, response):
        payload = response.json()
        careers = payload.get("results", [])

        for career in careers:
            item = {}
            item["university_name"] = self.university_name
            item["university_type"] = self.university_type
            item["university_contact"] = self.university_contact
            item["career_name"] = self.clean_text(career.get("title"))

            # URL de la carrera
            slug = career.get("path", {}).get("alias")
            career_url = response.urljoin(slug) if slug else None
            item["career_url"] = career_url

            # Descripción (meta)
            descripcion = None
            for body in career.get("metatag", []):
                if body.get("attributes", {}).get("name") == "description":
                    descripcion = body.get("attributes", {}).get("content")
                    break
            item["description"] = self.clean_text(descripcion)

            # Datos de la tarjeta (Card)
            carrer_card = career.get("carrer_card", {})
            item["degree_title"] = self.clean_text(carrer_card.get("qualification"))
            item["faculty"] = self.clean_text(carrer_card.get("faculty_school", {}).get("name"))
            item["duration"] = self.clean_text(carrer_card.get("duration"))
            
            code_info = carrer_card.get("career_code_info", [])
            item["modality"] = self.clean_text(code_info[0].get("modality", {}).get("name")) if code_info else None
            item["locations"] = ["Quito"]
            item["cost"] = self.clean_text(carrer_card.get("investment"))

            # Si hay URL de carrera, entramos a buscar el link de la malla
            if career_url:
                yield scrapy.Request(
                    url=career_url,
                    callback=self.parse_career_detail,
                    meta={'item': item}
                )
            else:
                item["study_plan_url"] = None
                yield item

    def parse_career_detail(self, response):
        item = response.meta['item']
        
        # Extraemos el link de la malla detallada (el de tu imagen)
        # Buscamos el <a> que contiene el texto "Malla Académica Detallada"
        malla_link = response.xpath("//a[contains(., 'Malla Académica Detallada')]/@href").get()
        
        # Guardamos el enlace (o el PDF si fuera el caso)
        item["study_plan_url"] = response.urljoin(malla_link) if malla_link else None
        
        yield item