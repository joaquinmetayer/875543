from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

s = Service('./driver/chromedriver.exe')
options = Options()
driver = webdriver.Chrome(service=s, options=options)

driver.get("https://web.whatsapp.com/")
input("Escanee el codigo QR y presione ENTER")
