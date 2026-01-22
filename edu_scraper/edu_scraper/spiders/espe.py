import scrapy
from .base_university import BaseUniversitySpider


class EspeSpider(BaseUniversitySpider):
    name = "espe"
    allowed_domains = ["espe.edu.ec"]
    start_urls = [
        "https://www.espe.edu.ec/oferta-academica-espe-presencial/"
    ]

    university_name = "Universidad de las Fuerzas Armadas ESPE"
    university_type = "Pública"
    university_contact = "https://www.espe.edu.ec/contactos/"

    def parse(self, response):
        # La ESPE lista las carreras en bloques tipo Elementor
        links = response.css(
            "span.subtext a[href^='https://www.espe.edu.ec/']::attr(href)"
        ).getall()

        for link in links:
            yield response.follow(link, callback=self.parse_career)

    def parse_career(self, response):
        item = self.create_base_item(response)

        # =========================
        # IDENTIDAD DE LA CARRERA
        # =========================

        item["career_name"] = self.clean_text(
            response.css("h1.elementor-heading-title::text").get()
        )

        item["faculty_name"] = self.clean_text(
            response.xpath(
                "//strong[contains(text(),'Departamento') or contains(text(),'Facultad')]/following::text()[1]"
            ).get()
        )

        item["degree_title"] = self.clean_text(
            response.xpath(
                "//strong[contains(text(),'Título que otorga')]/following::text()[1]"
            ).get()
        )

        # =========================
        # INFORMACIÓN GENERAL
        # =========================

        item["description"] = self.clean_text(
            " ".join(
                response.css(
                    "div.elementor-widget-text-editor p::text"
                ).getall()
            )
        )

        item["locations"] = ["Sangolquí"]

        item["cost"] = "Consultar universidad"

        # =========================
        # INFORMACIÓN ACADÉMICA
        # =========================

        item["semesters"] = self.clean_text(
            response.xpath(
                "//strong[contains(text(),'Duración')]/following::text()[1]"
            ).get()
        )

        item["modality"] = self.clean_text(
            response.xpath(
                "//strong[contains(text(),'Modalidad')]/following::text()[1]"
            ).get()
        )

        item["study_plan_pdf"] = response.css(
            "a[href$='.pdf']::attr(href)"
        ).get()

        yield item
