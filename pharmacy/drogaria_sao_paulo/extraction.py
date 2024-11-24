import scrapy
from scrapy_splash import SplashRequest
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

import sys, os
sys.path.append(os.path.abspath('../../'))
from server.database_pharmacy import PharmacyDatabase


# settings.py

from shutil import which

SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('chromedriver')
SELENIUM_DRIVER_ARGUMENTS = ['--headless']  # Opcional: rodar o navegador em modo headless

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
}


class DrogariaSaoPauloScrapper(scrapy.Spider):
    name = 'drogaria_sao_paulo_scrapper'
    domain = 'https://www.drogariasaopaulo.com.br'
    start_urls = ['https://www.drogariasaopaulo.com.br/']

    def parse(self, response):
        db = PharmacyDatabase()
        medicines = db.select_referece_table()

        yield SeleniumRequest(url="https://www.drogariasaopaulo.com.br/pesquisa?q=abatacepte", callback=self.parse_search_medicine, wait_time=40)
        # for medicine in medicines:
        #     link = self.domain + '/pesquisa?q=' + medicine['name']
        #     print(link)
        #     yield scrapy.Request(link, callback=self.parse_search_medicine)
            
    def parse_search_medicine(self, response):
        # self.log(response.text)
        # results = response.css('.view_item_list_success').get() 
        
        # yield { 'href': results }

        self.driver = response.meta['driver'] 
        WebDriverWait(self.driver, 40).until( 
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.collection-image-link'))
        )

        results = response.css('a.collection-image-link::attr(href)').getall() 
        for result in results: 
            full_url = response.urljoin(result) 
            yield {'href': full_url}