import scrapy 


class SusScrapper(scrapy.Spider):
    name = 'sus_scrapper'
    start_urls = ['https://www.saude.sp.gov.br/ses/perfil/gestor/assistencia-farmaceutica/medicamentos-dos-componentes-da-assistencia-farmaceutica/links-do-componente-especializado-da-assistencia-farmaceutica/relacao-estadual-de-medicamentos-do-componente-especializado-da-assistencia-farmaceutica/consulta-por-medicamento']

    def parse(self, response):
        medicines = response.css('article > div.publish > p')
        for medicine in medicines:
            raw = medicine.get()
            if ('<strong>' in raw or not raw.strip()):
                continue 

            name = medicine.css('p > a::text').get()
            if not name:
                name = medicine.css('p::text').get()
            
            yield {
                'name': name
            }
