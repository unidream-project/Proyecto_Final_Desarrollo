import scrapy


class CareerItem(scrapy.Item):
    # =========================
    # IDENTIFICACIÓN
    # =========================
    university = scrapy.Field()
    city = scrapy.Field()
    url = scrapy.Field()

    # =========================
    # DATOS PRINCIPALES
    # =========================
    career_name = scrapy.Field()
    faculty = scrapy.Field()
    degree_title = scrapy.Field()
    description = scrapy.Field()

    # =========================
    # INFORMACIÓN ACADÉMICA
    # =========================
    duration = scrapy.Field()
    modality = scrapy.Field()

    # =========================
    # FUTURAS EXTENSIONES
    # =========================
    mission = scrapy.Field()
    vision = scrapy.Field()
    objectives = scrapy.Field()
    career_profile = scrapy.Field()
    study_plan_pdf = scrapy.Field()

    # =========================
    # PARA IA / NLP (FUTURO)
    # =========================
    embedding = scrapy.Field()
    skills = scrapy.Field()
    related_careers = scrapy.Field()
