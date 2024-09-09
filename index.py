import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuration de Selenium avec Chrome
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')  # Pour éviter d'être détecté comme bot
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Votre clé API 2Captcha
API_KEY = '74e45fd36ec22e506bfcc05ec1f2695c'

# Liste des pages à scraper
url = 'https://www.cultura.com/p-la-doublure-9782253244585.html'
   


# Boucle pour scraper chaque page

# Ouvrir la page avec Selenium
driver.get(url)


title = driver.find_element(By.TAG_NAME, "h1").text
description = driver.find_element(By.CLASS_NAME, "paragraph").text
price = driver.find_elements(By.CLASS_NAME, "span_price")


print(title)
print(description)
print(price[1].text)




for pri in price:
    print(pri.text)
   
time.sleep(10)

# Fermer le navigateur après avoir terminé
driver.quit()
