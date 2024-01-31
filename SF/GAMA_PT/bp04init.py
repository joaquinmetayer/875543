from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
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
time.sleep(2)

xpath = '//*[@id="kt_login"]/div/div[2]/div[2]/ng-component/div/form/div[1]/input'
userLogin = WebDriverWait(driverPlataforma, timeout=20).until(lambda d: d.find_element(By.XPATH, xpath))
userLogin.send_keys(admin)

time.sleep(2)

xpath = '//*[@id="kt_login"]/div/div[2]/div[2]/ng-component/div/form/div[2]/input'
password = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath))
password.send_keys(clave_admin)

time.sleep(2)

xpath = '//*[@id="kt_login"]/div/div[2]/div[2]/ng-component/div/form/div[3]/button'
submit = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath))
submit.click()

time.sleep(5)

dp = WebDriverWait(driverPlataforma, timeout=30).until(lambda d: d.find_element(
	By.XPATH, '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/div/p-paginator/div/p-dropdown/div')).click()
time.sleep(2)
dp50 = driverPlataforma.execute_script(
	"return document.getElementsByClassName('ui-dropdown-item')[2];")
driverPlataforma.execute_script("arguments[0].click();", dp50)

time.sleep(1)
## Observacion en documentacion. Solucion duplicado de contraseñas en pw. Alambre por error de codigo fuente enplataforma##
def configuracion_contrasena(usuario):
    try:
        xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr'
        tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_elements(By.XPATH, xpath))
        time.sleep(1)
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
			    str(x) + ']/td[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                try:
                    xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
			    str(x) + ']/td[4]/div/div/button'
                    btn_acciones = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/bs-dropdown-container/div/ul/li[4]/a'
                    botonCambiarPw = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    time.sleep(2)
                    inputNewPw1 = WebDriverWait((driverPlataforma), timeout=15).until(
                            lambda d: d.find_element(By.ID, 'txt_changepassword_newPass')).send_keys("Hola123")
                    time.sleep(1)
                    xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/changepassword-modal/div/div/div/form/div[3]/button[2]'
                    btn_submit = WebDriverWait((driverPlataforma), timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()                    
                    informe = f"Configuracion inicial de cambio de contrasena exitoso"
                    print(informe)
                    break
                except Exception as err:
                    print("Error. Configuracion inicial de cambio de contrasena. Posible problema con opc 2 de menu. Contactar soporte.")
                    break
    except Exception as err:
                    print("Error. Configuracion inicial de cambio de contrasena. Posible problema con opc 2 de menu. Contactar soporte.")
                    pass

input("Haga ZOOM OUT al 33%, scrolee hasta arriba del todo y aprete ENTER")
configuracion_contrasena(config.usuario_config())
##fin alambreado##
