from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.chrome.options import Options

import time
import config

web_admin, web_jugador =  config.datos_plataforma()
admin, clave_admin = config.cuenta_logeo()

s = Service('./driver/chromedriver.exe')
options = Options()
driverPlataforma = webdriver.Chrome(service=s, options=options)
driverPlataforma.get(web_admin)
driverPlataforma.maximize_window()

userLogin = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_element(By.ID, "user"))
userLogin.send_keys(admin)

password = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_element(By.ID, "passwd"))
password.send_keys(clave_admin)

submit = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_element(By.ID, "dologin")).click()

time.sleep(2)

xpath = '//*[@id="sidemenu_global_ul"]/li[2]/a'
usuarios = WebDriverWait(driverPlataforma, timeout=10).until(lambda d: d.find_element(By.XPATH, xpath)).click()

time.sleep(1)

dp50 = driverPlataforma.execute_script("return document.getElementsByClassName('filtrable')[2];")
driverPlataforma.execute_script("arguments[0].click();", dp50)

input("Haga ZOOM OUT al 33%, scrolee hasta arriba del todo y aprete ENTER")



    

