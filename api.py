from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json

app = FastAPI()

def scrape_page(url: str):
    # Configurer les options et le service de ChromeDriver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Pour ne pas ouvrir de fenêtre
    service = Service(ChromeDriverManager().install())
    
    # Créer un dictionnaire vide pour stocker les résultats
    data = {}

    try:
        # Démarrer ChromeDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Accéder à la page
        driver.get(url)
        
        # Utiliser WebDriverWait pour attendre que l'élément du titre soit visible
        wait = WebDriverWait(driver, 10)  # Attendre jusqu'à 10 secondes
        
        # Extraire les informations
        try:
            title = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        except (NoSuchElementException, TimeoutException):
            title = "Title not found"
        
        try:
            descriptions = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "f-productDesc__raw")))
            if len(descriptions) > 0:
                description = descriptions[1].text if len(descriptions) > 1 else descriptions[0].text
            else:
                description = "Description not found"
        except (NoSuchElementException, TimeoutException):
            description = "Description not found"
        
        try:
            image = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "f-productMedias__viewItem--main"))).get_attribute('src')
        except (NoSuchElementException, TimeoutException):
            image = "Image not found"
        
        try:
            eans = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "characteristicsDashboard__item")))
            ean = ''
            for ean_element in eans:
                if ean_element.text.startswith("EAN"):
                    ean = ean_element.text.replace('EAN', '').strip()
            if not ean:
                ean = "EAN not found"
        except (NoSuchElementException, TimeoutException):
            ean = "EAN not found"
        
        try:
            price = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "f-faPriceBox__priceLine"))).text
        except (NoSuchElementException, TimeoutException):
            price = "Price not found"
        
        try:
            status = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "js-priceBox"))).text
            if len(status) > 150:
                status = "Status not found"
        except (NoSuchElementException, TimeoutException):
            status = "Status not found"

        # Préparer les données
        data = {
            'title': title,
            'description': description,
            'image': image,
            'ean': ean,
            'price': price,
            'status': status
        }

    except TimeoutException:
        raise HTTPException(status_code=408, detail="Timeout occurred while trying to load the page.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        # Quitter le driver
        driver.quit()

    return data

@app.get("/scrape")
def scrape(url: str):
    return scrape_page(url)
