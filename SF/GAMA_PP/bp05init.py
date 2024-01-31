from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time
import config

web_admin, web_jugador = config.datos_plataforma()
admin, clave_admin = config.cuenta_logeo()

s = Service('./driver/chromedriver.exe')
options = Options()
driverPlataforma = webdriver.Chrome(service=s, options=options)
driverPlataforma.get(web_admin)
driverPlataforma.maximize_window()
time.sleep(2)

xpath = '/html/body/app-root/app-login/mat-card/section/app-login-form/app-form-group/form/app-login-username-form-field/mat-form-field/div/div[1]/div/input'
userLogin = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath))
userLogin.send_keys(admin)

xpath = '/html/body/app-root/app-login/mat-card/section/app-login-form/app-form-group/form/app-login-password-form-field/mat-form-field/div/div[1]/div[1]/input'
password = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath))
password.send_keys(clave_admin)

submit = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, "/html/body/app-root/app-login/mat-card/section/button")).click()

time.sleep(2)

xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
usuarios = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath)).click()

time.sleep(1)

btn_bloqueados = driverPlataforma.execute_script(
        "return document.getElementById('mat-slide-toggle-1-input');")
driverPlataforma.execute_script("arguments[0].click();", btn_bloqueados)

input("Haga ZOOM OUT al 33%, seleccione dropdown 50, scrolee hasta arriba del todo y aprete ENTER")

    

