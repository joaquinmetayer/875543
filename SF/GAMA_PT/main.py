from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from keepSession import driver
import time
import db
import fun
import wp
import wpEdge
import msjs
import bpConfirmar
import track_procesos
import config
from bp04 import actividad_panel

def mantenimiento():
    print("BOT EN MANTENIMIENTO ..")
    while True:
        #print("BUSCANDO CHATS..")
        chats = WebDriverWait(driver, timeout=15).until(
            lambda d: d.find_elements(By.CLASS_NAME, "_8nE1Y"))
        for i in range(len(chats)):
            #print("DETECTANDO MENSAJES SIN LEER..")
            chats = driver.find_elements(By.CLASS_NAME, "_8nE1Y") # Buscar chats de nuevo cada vez
            chat = chats[i]
            chats_nuevos = chat.find_elements(By.CLASS_NAME, "_2H6nH")
            if len(chats_nuevos) == 0:
                #print("NO HAY MENSAJES SIN LEER")
                continue
            chat_numero = chat.find_element(By.CLASS_NAME, "_21S-L")
            numero = chat_numero.text.strip()
            chat.click()
            time.sleep(1)
            with open("./resource/contactos_autorizados.txt", mode='r', encoding='utf-8') as archivo:
                contactos = [linea.strip() for linea in archivo]
                if numero in contactos:
                    wp.enviar_mensaje("*BOT EN MANTENIMIENTO.* Corrobora que la plataforma este ONLINE o Comunicate con soporte.")
                    continue
            wp.enviar_mensaje("*BOT o PLATAFORMA EN MANTENIMIENTO.* Vuelvo en unos minutos.")
            wp.buscar_chat("Leem")

def buscar_chats():
    #print("BUSCANDO CHATS..")
    chats = WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_elements(By.CLASS_NAME, "_8nE1Y"))
    for i in range(len(chats)):
        #print("DETECTANDO MENSAJES SIN LEER..")
        chats = driver.find_elements(By.CLASS_NAME, "_8nE1Y") # Buscar chats de nuevo cada vez
        chat = chats[i]
        chats_nuevos = chat.find_elements(By.CLASS_NAME, "_2H6nH")
        if len(chats_nuevos) == 0:
            #print("NO HAY MENSAJES SIN LEER")
            continue
        print("Mensaje sin leer")
        chat_numero = chat.find_element(By.CLASS_NAME, "_21S-L")
        numero = chat_numero.text.strip()
        chat.click()
        time.sleep(1)
        with open("./resource/contactos_autorizados.txt", mode='r', encoding='utf-8') as archivo:
            contactos = [linea.strip() for linea in archivo]
            if numero in contactos:
                print(f"Contacto autorizado: {numero}")
                if fun.detectar_comando():
                    print("@@@@@@@@ BOT CORRIENDO... @@@@@@@@@@")
                    track_procesos.eliminar_archivo()
                    continue
        consultar_estado(numero)
        time.sleep(1)
        wp.buscar_chat("Leem")
        return True
    return False

def consultar_estado(numero):
    print("Número:", numero)
    estado, usuario = db.chequear_usuario(numero)
    if estado == "En bienvenida":
        wp.enviar_mensaje(msjs.msj_bienvenida(config.nombre_robot()))
        wp.enviar_mensaje_no_user()
    elif estado == "En creacion de usuario":
        fun.crear_usuario(numero)
    elif estado == "En menu de acciones":
        fun.menu_acciones(numero, usuario)
    elif estado == "En pasos de transferencia":
        fun.pasos_transf(numero, usuario)
    elif estado == "En confirmacion de pago":
        fun.confirmacion_pago(numero, usuario)
    elif estado == "En confirmacion de pw":
        fun.confirmacion_pw(numero, usuario)
    elif estado == "En datos de retiro":
        fun.datos_retiro(numero,usuario)
    elif estado == "En confirmacion de retiro":
        fun.confirmacion_retiro(numero,usuario)
    else:
        print("Error. Salto el Else de funcion consultar_estado(). Linea 93. Archivo main.py")

def whatsapp_bot_init():
    global driver

    print("@@@@@@@@ BOT CORRIENDO... @@@@@@@@@@")
    last_activity_time = time.time()
    error_counter = 0
    last_error_time = time.time()

    while True:
        try:
            if not buscar_chats():
                current_time = time.time()
                if current_time - last_activity_time >= 900:  # 900 segundos = 15 minutos
                    print("Realizando activad en el panel..")
                    actividad_panel()
                    last_activity_time = current_time
                time.sleep(1)
                continue
            print("@@@@@@@@ BOT CORRIENDO... @@@@@@@@@")
            track_procesos.eliminar_archivo()
        except Exception as err:
            try:
                wp.buscar_chat("Leem")
                track_procesos.agregar_proceso(f"Error en consola: {err}")
                reporte = track_procesos.leer_archivo()
                track_procesos.eliminar_archivo()
                msj = f"Error inesperado en main.py : \n {reporte} \n | *Bot corriendo normalmente*"
                print("Error inesperado en main.py. Reporte enviado. Levantando bot nuevamente..")
                wpEdge.buscar_chat("BOT REPORTES")
                time.sleep(1)
                wpEdge.enviar_mensaje(msj)
                time.sleep(1)
            except:
                wpEdge.btnNoMic()
            finally:
                # Incrementar contador de errores
                    error_counter += 1
                    current_time = time.time()

                    # Verificar si se ha alcanzado el límite de errores y el tiempo transcurrido
                    if error_counter >= 5 and (last_error_time is None or current_time - last_error_time <= 180):  # 180 segundos = 3 minutos
                        error_counter = 0  # Reiniciar el contador
                        mantenimiento()
                    elif current_time - last_error_time > 180:
                        error_counter = 0  # Reiniciar el contador

                    last_error_time = current_time
                    print("@@@@@@@@ BOT CORRIENDO... @@@@@@@@@")

whatsapp_bot_init()
        
    
