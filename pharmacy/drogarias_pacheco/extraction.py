import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys, os
sys.path.append(os.path.abspath('../../'))
from server.database_pharmacy import PharmacyDatabase


class DrograriaSaoPauloScrapper:
    def __init__(self):
        self.db = PharmacyDatabase()
        self.medicines = self.db.select_referece_table()
        # print(self.medicines)
        self.domain = 'https://www.drogariaspacheco.com.br'

        self.service = Service()
        self.options = webdriver.ChromeOptions()  

    
    def extract(self):
        for medicine in self.medicines:
            link = f"{self.domain}/pesquisa?q={medicine['name']}"
            self.open_web(link, medicine['name'])

        print("=================! FINISHED !=================")

    
    def open_web(self, url, medicine):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)

            driver.get(url)
            WebDriverWait(driver, 30).until( 
                EC.presence_of_element_located((By.CLASS_NAME, 'chaordic-search-list'))
            )
            showcase = driver.find_element(By.CLASS_NAME, "chaordic-search-list")
            elements = showcase.find_elements(By.CLASS_NAME, "collection-image-link")
            hrefs = [element.get_attribute('href') for element in elements] 
            # print(hrefs)

            driver.quit()

            # self.storage_info(hrefs[0], medicine)
            [self.storage_info(href, medicine) for href in hrefs]       

        except Exception as ex:
            print(ex)
            # self.db.insert_record_rows([f"'Drogarias Pacheco', '{medicine}', 'None', 'None', 'None', CAST('0.00' AS DECIMAL(10, 2))"])
            driver.quit()

    
    def storage_info(self, url, medicine):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get(url)
            WebDriverWait(driver, 30).until( 
                EC.presence_of_element_located((By.CLASS_NAME, 'productName'))
            )
            name = driver.find_element(By.CLASS_NAME, 'productName').text
            price = driver.find_element(By.CLASS_NAME, 'skuBestPrice').text
            price = price.replace('R$', '').replace('.', '').replace(',', '.').strip()
            # print(price)
            brand = driver.find_element(By.CLASS_NAME, 'rnk-nome-marca').text
            ingredient = driver.find_element(By.CLASS_NAME, 'rnk-comp-especificacoes').find_element(By.TAG_NAME, 'a').text
            ingredient = ingredient.replace('Com', '').strip()

            # print(medicine, name, brand, ingredient, price)
            self.db.insert_record_rows([f"'Drogarias Pacheco', '{medicine}', '{name}', '{brand}', '{ingredient}', CAST('{price}' AS DECIMAL(10, 2))"])
            
            driver.quit()

        except Exception as ex:
            print(ex)
            driver.quit()



scrapper = DrograriaSaoPauloScrapper()
scrapper.extract()
