import scrapy
from edu_scraper.items import CareerItem


class BaseUniversitySpider(scrapy.Spider):
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "ROBOTSTXT_OBEY": True
    }

    university_name = ""
    city = ""

    def create_base_item(self, response):
        """
        Crea un item base con la información común a todas las universidades.
        Los spiders específicos completan el resto.
        """
        item = CareerItem()

        item["university"] = self.university_name
        item["city"] = self.city
        item["url"] = response.url

        return item

    def clean_text(self, text):
        """
        Normaliza texto: elimina saltos de línea, espacios múltiples, etc.
        """
        if not text:
            return None
        return " ".join(text.split())
