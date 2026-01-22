import scrapy
import json
import os

class MallaExtractorSpider(scrapy.Spider):
    name = "malla_extractor"
    
    # Configuramos la salida a un único archivo JSON para mallas
    custom_settings = {
        'FEEDS': {
            '../data_malla/udla_mallas.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
                'overwrite': True,
            }
        }
    }

    def start_requests(self):
        # 1. Cargamos el JSON de carreras generado por el spider anterior
        path_carreras = '../data/udla_careers.json'
        
        if os.path.exists(path_carreras):
            with open(path_carreras, 'r', encoding='utf-8') as f:
                carreras = json.load(f)
                
                for carrera in carreras:
                    url_malla = carrera.get("study_plan_url")
                    # Solo procesamos si existe un enlace a la malla
                    if url_malla and "http" in url_malla:
                        yield scrapy.Request(
                            url=url_malla,
                            callback=self.parse_malla,
                            # Pasamos datos clave para "conectar" los JSONs
                            meta={
                                'university_name': carrera.get('university_name'),
                                'career_name': carrera.get('career_name'),
                                'career_url': carrera.get('career_url') # ID de conexión
                            }
                        )

    def parse_malla(self, response):
        # Recuperamos la metadata para mantener la conexión
        universidad = response.meta.get('university_name')
        carrera_nombre = response.meta.get('career_name')
        career_url = response.meta.get('career_url')

        resultado = {
            "universidad": universidad,
            "carrera": carrera_nombre,
            "career_url_ref": career_url, # Este campo conecta con el JSON de carreras
            "pensum": "Vigente",
            "materias": [],
            "totales": {
                "total_creditos": 0.0,
                "total_horas": 0
            }
        }

        total_creditos_acumulados = 0.0
        periodos = response.xpath("//div[contains(@class, 'col-md-6') and .//table]")

        for bloque in periodos:
            header_semestre = bloque.xpath(".//h2[contains(@class, 'tituloPeriodo')]/text()").get()
            semestre_num = None
            if header_semestre:
                digits = ''.join(filter(str.isdigit, header_semestre))
                if digits:
                    semestre_num = int(digits)

            if semestre_num is None:
                continue

            filas = bloque.xpath(".//table//tr")

            for fila in filas:
                nombre_raw = fila.xpath("./td[1]//text()").getall()
                nombre = " ".join([t.strip() for t in nombre_raw if t.strip()])
                creditos_raw = fila.xpath("./td[2]//text()").get()
                codigo_raw = fila.xpath("./td[3]//text()").get()
                codigo = codigo_raw.strip() if codigo_raw else ""
                
                if not codigo or "Código" in codigo or "Asignatura" in nombre or not nombre:
                    continue

                try:
                    val_creditos = float(str(creditos_raw).strip())
                except (ValueError, TypeError):
                    val_creditos = 0.0

                materia = {
                    "codigo": codigo,
                    "nombre": nombre.replace("\n", " ").strip(),
                    "creditos": val_creditos,
                    "horas": int(val_creditos * 48), # Cálculo estándar horas/créditos
                    "semestre": semestre_num
                }
                
                resultado["materias"].append(materia)
                total_creditos_acumulados += val_creditos

        resultado["totales"]["total_creditos"] = round(total_creditos_acumulados, 2)
        resultado["totales"]["total_horas"] = int(total_creditos_acumulados * 48)
        
        yield resultado