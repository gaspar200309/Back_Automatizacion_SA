from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

def scrape_data(email, password):
    # Instalar ChromeDriver y obtener la ruta
    chrome_driver_path = ChromeDriverManager().install()
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        login_url = "https://centers.additioapp.com/access/login"
        data_url = "https://centers.additioapp.com/groupsbase/list"

        driver.get(login_url)

        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )
        password_field = driver.find_element(By.NAME, 'password')

        username.send_keys(email)
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
        login_button.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        driver.get(data_url)

        html = driver.page_source
        return html

    finally:
        driver.quit()

# Ejemplo de uso
email = "tu_email@example.com"
password = "tu_contraseña_secreta"
html_data = scrape_data(email, password)
print(html_data)
