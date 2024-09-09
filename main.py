from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json

# Configurer les options et le service de ChromeDriver
chrome_options = Options()
service = Service(ChromeDriverManager().install())

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Accéder à la page
    driver.get("https://www.fnacpro.com/TV-OLED-Evo-LG-OLED55G4-139-cm-4K-UHD-Smart-TV-2024-Noir-et-Argent/a20267281/w-4")
    
    # Utiliser WebDriverWait pour attendre que l'élément du titre soit visible
    wait = WebDriverWait(driver, 10)  # Attendre jusqu'à 10 secondes

    # Extraire les informations
    try:
        title = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    except (NoSuchElementException, TimeoutException):
        title = "Title not found"
    
    try:
        # Attendre que la description soit présente
        descriptions = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "f-productDesc__raw")))
        if len(descriptions) == 4:
            description = descriptions[1].text
        elif len(descriptions) == 3:
            description = descriptions[1].text
        elif len(descriptions) == 2:
            description = descriptions[1].text
        elif len(descriptions) == 1:
            description = descriptions[0].text
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

    print(data)

except TimeoutException:
    print("Timeout occurred while trying to load the page.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Quitter le driver
    driver.quit()
