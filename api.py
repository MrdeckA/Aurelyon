from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

app = Flask(__name__)

# Function to perform web scraping
def scrape_fnacpro():
    # Configure ChromeDriver options and service
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless if necessary (no UI)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service(ChromeDriverManager().install())

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Access the page
        driver.get("https://www.fnacpro.com/TV-OLED-Evo-LG-OLED55G4-139-cm-4K-UHD-Smart-TV-2024-Noir-et-Argent/a20267281/w-4")
        
        # Use WebDriverWait to wait for the title element to be visible
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds

        # Extract the information
        try:
            title = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        except (NoSuchElementException, TimeoutException):
            title = "Title not found"
        
        try:
            # Wait for the description to be present
            descriptions = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "f-productDesc__raw")))
            if len(descriptions) > 0:
                description = descriptions[-1].text
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

        # Prepare the data
        data = {
            'title': title,
            'description': description,
            'image': image,
            'ean': ean,
            'price': price,
            'status': status
        }

    except TimeoutException:
        return {"error": "Timeout occurred while trying to load the page."}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
    finally:
        # Quit the driver
        driver.quit()

    return data

# Route to trigger the scraping
@app.route('/scrape', methods=['GET'])
def scrape():
    # Call the scrape function and return its result as JSON
    data = scrape_fnacpro()
    return jsonify(data)



@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
