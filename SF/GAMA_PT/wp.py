from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from keepSession import driver
import time
import msjs
import config

web_admin, web_jugador = config.datos_plataforma()


def enviar_mensaje(mensaje):
    # enviar un mensaje si y solo si se esta dentro del chat..
    xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    chatbox = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.XPATH, xpath))
    chatbox.send_keys(mensaje)
    chatbox.send_keys(Keys.ENTER)

def leer_ultimo_mensaje():
    element_box_message = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_elements(By.CLASS_NAME, "_2AOIt"))#"ItfyB"
    posicion = len(element_box_message) - 1
    element_message = element_box_message[posicion].find_elements(
        By.CLASS_NAME, "_21Ahp")
    ultimo_mensaje = element_message[0].text.strip()
    return ultimo_mensaje


def buscar_chat(nombre_chat): #nombre_chat = nombre si esta agendado, o numero de telefono si no lo esta.
    xpath = '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]'
    barraDeBusqueda = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.XPATH, xpath))
    barraDeBusqueda.send_keys(nombre_chat)
    time.sleep(1)
    barraDeBusqueda.send_keys(Keys.ENTER)
    time.sleep(1)
    cancel = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.CLASS_NAME, "-Jnba"))
    cancel.click()

def capturar_numero():
    numero = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.CLASS_NAME, "_3W2ap").text
    )
    return numero



#########################################################
# MENSAJES ESPECIALES #
#########################################################

def enviar_mensaje_menu_acciones(usuario):
    xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    chatbox = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.XPATH, xpath))
    msj, msj0, msj1, msj2, msj3, msj4, msj5, msj6 = msjs.msj_menu_acciones(usuario,web_jugador)
    chatbox.send_keys(msj)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj0)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj1)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj2)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj3)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj4)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj5)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj6)
    chatbox.send_keys(Keys.ENTER)

def enviar_mensaje_no_user():
    xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    chatbox = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.XPATH, xpath))
    msj, msj0, msj1, msj2, msj3, msj4, msj5, msj6 = msjs.msj_no_user()
    chatbox.send_keys(msj)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj0)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj1)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj2)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj3)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj4)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj5)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj6)
    chatbox.send_keys(Keys.ENTER)

def enviar_mensaje_user_creado():
    xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    chatbox = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.XPATH, xpath))
    msj, msj0, msj1, msj2 = msjs.msj_user_creado(web_jugador)
    chatbox.send_keys(msj)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj0)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj1)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj2)
    chatbox.send_keys(Keys.ENTER)

def enviar_mensaje_pasos_transf(cbu,alias,nombre_cuenta):
    xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    chatbox = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.XPATH, xpath))
    msj, msj0, msj1, msj2, msj3, msj4, msj5, msj6, msj7 = msjs.msj_pasos_transf(cbu,alias,nombre_cuenta)
    chatbox.send_keys(msj)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj0)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj1)
    chatbox.send_keys(Keys.ENTER)
    chatbox.send_keys(msj2)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj3)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj4)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj5)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj6)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj7)
    chatbox.send_keys(Keys.ENTER)

def enviar_mensaje_pago_no_confirmado():
    xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    chatbox = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.XPATH, xpath))
    msj, msj0, msj1, msj2 = msjs.msj_pago_no_confirmado()
    chatbox.send_keys(msj)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj0)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj1)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj2)
    chatbox.send_keys(Keys.ENTER)

def enviar_mensaje_err_crear_user():
    xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    chatbox = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.XPATH, xpath))
    msj, msj0, msj1= msjs.msj_err_crear_user()
    chatbox.send_keys(msj)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj0)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(Keys.SHIFT, Keys.RETURN)
    chatbox.send_keys(msj1)
    chatbox.send_keys(Keys.ENTER)
