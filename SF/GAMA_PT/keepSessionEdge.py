from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# Servicio del webdriver
s = Service('./driver/edgedriver.exe')
options = Options()
driver = webdriver.Edge(service=s, options=options)

driver.get("https://web.whatsapp.com/")
input("Escanee el codigo QR y presione ENTER")
