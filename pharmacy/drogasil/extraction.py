import pandas as pd
import json
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
        self.domain = 'https://www.drogasil.com.br'

        self.service = Service()
        self.options = webdriver.ChromeOptions()  

    
    def extract(self):
        for medicine in self.medicines:
            link = f"{self.domain}/search?w={medicine['name']}"
            self.open_web(link, medicine['name'])

        print("=================! FINISHED !=================")

    
    def open_web(self, url, medicine):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)

            driver.get(url)
            WebDriverWait(driver, 20).until( 
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            showcase = driver.find_element(By.TAG_NAME, "article")
            elements = showcase.find_elements(By.TAG_NAME, "a")
            hrefs = [element.get_attribute('href') for element in elements] 
            # print(hrefs)

            driver.quit()

            [self.storage_info(href, medicine) for href in hrefs]       

        except Exception as ex:
            print(ex)
            self.db.insert_record_rows([f"'Drogasil', '{medicine}', 'None', 'None', 'None', CAST('0.00' AS DECIMAL(10, 2))"])
            driver.quit()

    
    def storage_info(self, url, medicine):
        try:
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get(url)
            WebDriverWait(driver, 30).until( 
                EC.presence_of_element_located((By.CLASS_NAME, 'product-name'))
            )
            
            # name = driver.find_element(By.CLASS_NAME, 'product-name').find_element(By.TAG_NAME, "h1").text
            # print(name)
            script = driver.find_element(By.XPATH, "//script[@type='application/ld+json']")
            json_content = script.get_attribute('innerHTML')
            product_data = json.loads(json_content)
            name = product_data["name"]
            price = product_data["offers"]["price"]
            # print(price)
            brand = driver.find_element(By.CLASS_NAME, 'brand').text
            # print(brand)
            ingredient = driver.find_element(By.CLASS_NAME, 'activePrinciple').text
            # print(ingredient)

            # print(medicine, name, brand, ingredient, price)
            self.db.insert_record_rows([f"'Drogasil', '{medicine}', '{name}', '{brand}', '{ingredient}', CAST('{price}' AS DECIMAL(10, 2))"])

            driver.quit()
            
        except Exception as ex:
            print(ex)
            driver.quit()



scrapper = DrograriaSaoPauloScrapper()
scrapper.extract()
