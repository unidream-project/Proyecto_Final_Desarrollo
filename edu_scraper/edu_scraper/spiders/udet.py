import scrapy
import re
import unicodedata
from .base_university import BaseUniversitySpider


class UdetSpider(BaseUniversitySpider):
    name = "udet"
    allowed_domains = ["udet.edu.ec"]
    start_urls = ["https://udet.edu.ec/pa-pregrado/"]

    university_name = "Universidad de Especialidades Turísticas"
    university_type = "Privada"
    university_contact = "https://udet.edu.ec/contacto/"

    # =========================
    # UTILIDAD
    # =========================
    def slugify(self, text):
        text = unicodedata.normalize("NFD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")
        text = re.sub(r"[^\w\s-]", "", text.lower())
        return re.sub(r"[\s_-]+", "-", text).strip("-")

    # =========================
    # LISTADO DE CARRERAS
    # =========================
    def parse(self, response):
        career_blocks = response.css(
            "div[class*='et_pb_text'] p"
        )

        for p in career_blocks:
            career_name = self.clean_text(p.css("::text").get())

            if not career_name or len(career_name) < 4:
                continue

            slug = self.slugify(career_name)

            # excepciones reales de UDET
            if slug == "comunicacion":
                slug = "comunicacion-mf"
            if slug == "gastronomia":
                slug = "520-2"

            career_url = f"https://udet.edu.ec/{slug}/"

            yield response.follow(
                career_url,
                callback=self.parse_career,
                meta={"career_name": career_name}
            )

    # =========================
    # DETALLE DE CARRERA
    # =========================
    def parse_career(self, response):
        item = self.create_base_item(response)

        # =========================
        # IDENTIDAD
        # =========================
        item["career_name"] = response.meta.get(
            "career_name",
            self.clean_text(
                response.css("h1::text").get()
            )
        )

        item["faculty_name"] = self.clean_text(
            response.xpath(
                "//strong[contains(text(),'Facultad')]/following::text()[1]"
            ).get()
        )

        item["degree_title"] = self.clean_text(
            response.xpath(
                "//strong[contains(text(),'Título')]/following::text()[1]"
            ).get()
        )

        # =========================
        # DESCRIPCIÓN
        # =========================
        item["description"] = self.clean_text(
            " ".join(
                response.css(
                    ".et_pb_text_inner p::text"
                ).getall()
            )
        )

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

        # =========================
        # METADATOS
        # =========================
        item["locations"] = ["Quito"]
        item["cost"] = "Consultar universidad"

        yield item
