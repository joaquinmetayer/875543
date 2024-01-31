from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support import expected_conditions as EC
import time
import re

from bp03init import driverPlataforma
import db
import track_procesos
import reporte_errores
import config

admin, clave_admin = config.cuenta_logeo()


def actividad_panel():
    try:
        #actividad para contrarestar el problema de deslogeo por inactividad de panel
        btn_actualizar1 = WebDriverWait(driverPlataforma, timeout=5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/section/div/div[2]/div[1]/div/div/div[1]/div[3]/div/label[2]")))
        btn_actualizar1.click()
        time.sleep(2)
        btn_actualizar2 = WebDriverWait(driverPlataforma, timeout=5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/section/div/div[2]/div[1]/div/div/div[1]/div[3]/div/label[1]")))
        btn_actualizar2.click()
        time.sleep(2)
    except:
        btn_actualizar1 = WebDriverWait(driverPlataforma, timeout=5).until(EC.element_to_be_clickable((By.ID, "NewUserButton")))
        btn_actualizar1.click()
        time.sleep(2)
        btn_actualizar2 = WebDriverWait(driverPlataforma, timeout=5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[9]/div/div/div/div/div[1]/div[2]/button[1]")))
        btn_actualizar2.click()
    
def cambio_de_pagina(num):
    proceso = f"Cambiando a página número: {num}. Funcion cambio_de_pagina(). Linea 23. Archivo bp03.py"
    print(f"Cambiando a página número: {num}")

    btn_disable = driverPlataforma.execute_script(
        "return document.getElementsByClassName('paginate_button page-item next disabled');")
    length = driverPlataforma.execute_script("return arguments[0].length;", btn_disable)
    if length == 0:
        btn_avaible = driverPlataforma.execute_script(
                "return document.getElementById('users_next');")
        driverPlataforma.execute_script("arguments[0].click();", btn_avaible)
        return True
    else:
        return False

def volver_pag_1():
    time.sleep(1)
    print(f"Volviendo a página principal")
    #actualizar tabla
    btn_actualizar1 = WebDriverWait(driverPlataforma, timeout=5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/section/div/div[2]/div[1]/div/div/div[1]/div[3]/div/label[2]")))
    btn_actualizar1.click()
    time.sleep(2)
    btn_actualizar2 = WebDriverWait(driverPlataforma, timeout=5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/section/div/div[2]/div[1]/div/div/div[1]/div[3]/div/label[1]")))
    btn_actualizar2.click()
    time.sleep(2)


def fichas_administrador():
    proceso = "Chequeando cantidad de fichas del administrador. Funcion fichas_administrador(). Linea 41. Archivo bp03.py"
    print("Chequeando cantidad de fichas del administrador")
    track_procesos.agregar_proceso(proceso)
    try:
        xpath = '/html/body/header/nav/ul/li[1]/a/span'
        fichas = WebDriverWait(driverPlataforma, timeout=5).until(
            lambda d: d.find_element(By.XPATH, xpath)).text
        return fichas
    except Exception as err:
        return "error al consultar fichas en panel"

def fichas_usuario(usuario):
    proceso = f"Chequeando cantidad de fichas del usuario: {usuario}. Funcion fichas_usuario(). Linea 54. Archivo bp03.py"
    print(f"Buscando al usuario {usuario} para chequeo de fichas")
    track_procesos.agregar_proceso(proceso)
    try:
        time.sleep(1)
        xpath = '//*[@id="users"]/tbody/tr'
        tablaUsuarios = WebDriverWait(driverPlataforma, timeout=5).until(
            lambda d: d.find_elements(By.XPATH, xpath))
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '//*[@id="users"]/tbody/tr[' + str(x) + ']/td[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=5).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                xpath = '//*[@id="users"]/tbody/tr[' + str(x) + ']/td[2]'
                fichas = WebDriverWait(driverPlataforma, timeout=5).until(
                    lambda d: d.find_element(By.XPATH, xpath)).text
                fichas_sin_coma = fichas.split(",")
                fichas = fichas_sin_coma[0]
                # chequeo si existe un "." en la cantidad de fichas. Si existe, significa que tiene mas de 999 fichas. ej: 1.000 fichas
                punto = fichas.count(".")
                if punto == 1:
                    fichas = fichas.split(".")
                    fichas_del_usuario = fichas[0] + fichas[1]
                    print(f"Chequeo de fichas al usuario {usuario} exitoso")
                    return True, fichas_del_usuario
                else:
                    print(f"Chequeo de fichas al usuario {usuario} exitoso")
                    return True, fichas
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
            x = x + 1
    except Exception as err:
        informe = f"Error chequeando cantidad de fichas del usuario: {usuario}. Funcion fichas_usuario(). Linea 91. Archivo bp03.py"
        print(f"Error chequeando cantidad de fichas del usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)

def botCarga(usuario, monto):
    proceso = f"Cargando {monto} fichas al usuario: {usuario}. Funcion botCarga(). Linea 97. Archivo bp03.py"
    print(f"Buscando al usuario {usuario} para carga de {monto} fichas")
    track_procesos.agregar_proceso(proceso)
    try:
        # Chequeo cantidad defichas en panel, con cantidad de fichas solicitadas para cargar
        xpath = '/html/body/header/nav/ul/li[1]/a/span'
        fichas = WebDriverWait(driverPlataforma, timeout=10).until(
            lambda d: d.find_element(By.XPATH, xpath)).text
        # teniendo en cuenta que en juga en vivo siempre va a haber decimales.. no creo un "if" preguntando si existe "," simplemente hago el split
        fichas_split1 = fichas.split(",")
        fichas = fichas_split1[0]
        punto = fichas.count(".")
        if punto == 1:
            fichas_split2 = fichas.split(".")
            fichas_en_panel = fichas_split2[0] + fichas_split2[1]
            # luego de hacer toda la manipulacion de datos, eliminar "." ahora puedo pasar el string a INT sin problemas..
            print(f"Entrando a comparar monto: {monto} con fichas_en_panel: {fichas_en_panel}")
            if int(monto) > int(fichas_en_panel):
                informe = f"*ERROR.* Cantidad de fichas en panel insuficientes.\n *Fichas en panel*: {fichas} \n *Monto a cargar:* {monto} al usuario {usuario}\n Solicite más fichas a su superior, y vuelva a ejectuar el comando.\n"
                return True, informe
        else:
            print(f"Entrando a comparar monto: {monto} con fichas: {fichas}")
            if int(monto) > int(fichas):
                informe = f"*ERROR.* Cantidad de fichas en panel insuficientes.\n *Fichas en panel*: {fichas} \n *Monto a cargar:* {monto} al usuario {usuario}\n Solicite más fichas a su superior, y vuelva a ejectuar el comando.\n"
                return True, informe
        # encuentra todos los elementos de la tabla usuarios
        xpath = '//*[@id="users"]/tbody/tr'
        tablaUsuarios = WebDriverWait(driverPlataforma, timeout=5).until(
            lambda d: d.find_elements(By.XPATH, xpath))
        time.sleep(2)
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '//*[@id="users"]/tbody/tr[' + str(x) + ']/td[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=5).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                try:
                    print(f"Usuario {usuario} encontrado. Cargando fichas")
                    xpath = '//*[@id="users"]/tbody/tr['+ str(x) + ']/td[3]/a[1]'
                    botonCarga = WebDriverWait(driverPlataforma, timeout=5).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    time.sleep(2)
                    inputCarga = WebDriverWait(driverPlataforma, timeout=10).until(
                        lambda d: d.find_element(By.ID, "ModalCreditAmount")).send_keys(monto)
                    submitCarga = WebDriverWait(driverPlataforma, timeout=10).until(
                        lambda d: d.find_element(By.ID, "ModalCreditSubmit")).click()
                    print(f"Carga exitosa de {monto} fichas al usuario {usuario}")
                    informe = "*Carga exitosa.* " + \
                        str(monto) + " al usuario " + nombreUsuario + "\n"
                    return True, informe
                    break
                except Exception as err:
                    informe1 = f"Error cargando fichas al usuario: {usuario}. Posiblemente usuario bloqueado. Funcion botCarga(). Linea 149. Archivo bp03.py"
                    print(f"Error cargando fichas al usuario: {usuario}. Chequear que el usuario no este bloqueado")
                    reporte_errores.reportar_error(informe1, err)
                    informe = f"Error carga no realizada. Chequear que el usuario {usuario} no este bloqueado. Y volver a ejectuar comando de carga."
                    return True, informe
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
            x = x+1
    except Exception as err:
        informe = f"Error cargando fichas al usuario: {usuario}. Funcion botCarga(). Linea 162. Archivo bp03.py"
        print(f"Error cargando fichas al usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)
        return informe

def botDescarga(usuario, monto):
    proceso = f"Descargando {monto} fichas al usuario: {usuario}. Funcion botDescarga(). Linea 169. Archivo bp03.py"
    print(f"Buscando usuario {usuario} para descarga de {monto} fichas")
    track_procesos.agregar_proceso(proceso)
    try:
        # encuentra todos los elementos de la tabla usuarios
        xpath = '//*[@id="users"]/tbody/tr'
        tablaUsuarios = WebDriverWait(driverPlataforma, timeout=5).until(
            lambda d: d.find_elements(By.XPATH, xpath))
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '//*[@id="users"]/tbody/tr[' + str(x) + ']/td[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=5).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                try:
                    print(f"Usuario {usuario} encontrado. Descargando fichas")
                    xpath = '//*[@id="users"]/tbody/tr['+ str(x) + ']/td[3]/a[2]'
                    botonDescarga = WebDriverWait(driverPlataforma, timeout=5).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    time.sleep(2)
                    inputDescarga = WebDriverWait(driverPlataforma, timeout=10).until(
                        lambda d: d.find_element(By.ID, "ModalCreditAmount")).send_keys(monto)
                    submitDescarga = WebDriverWait(driverPlataforma, timeout=10).until(
                        lambda d: d.find_element(By.ID, "ModalCreditSubmit")).click()
                    print(f"Descarga exitosa de {monto} fichas al usuario {usuario}")
                    informe = "*Descarga exitosa.* " + \
                        str(monto) + " al usuario " + nombreUsuario + "\n"
                    return True, informe
                    break
                except Exception as err:
                    #informe1 para reportar error. informe para avisar a jugador.
                    informe1 = f"Error descargando fichas al usuario: {usuario}.Posiblemente usuario bloqueado. Ya fue notificado el jugador. Funcion botDescarga(). Linea 206. Archivo bp03.py"
                    print(f"Error descargando fichas al usuario: {usuario}. Usuario bloqueado. Ya fue notificado el jugador")
                    #reporte_errores.reportar_error(informe1, err)
                    informe = "*ERROR.* Tu usuario esta bloqueado. Entra en la opcion 4 del menu. Y luego volve a la opcion 3."
                    return True, informe
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
            x = x+1
    except Exception as err:
        informe = f"Error descargando fichas al usuario: {usuario}. Funcion botDescarga(). Linea 219. Archivo bp03.py"
        print(f"Error descargando fichas al usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)
        return informe

def botNuevoJugador(admin, clave_admin, nombreNuevoUsuario, contrasenaNuevoUsuario):
    proceso = f"Creando nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}. Funcion botNuevoJugador(). Linea 226. Archivo bp03.py"
    print(f"Creando nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}")
    track_procesos.agregar_proceso(proceso)
    global driverPlataforma
    try:
        btnNuevoJugador = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_element(By.ID, "NewUserButton")).click()
        time.sleep(1)
        inputNombreUsuario = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_element(By.ID, "NewUserPlayerUsername")).send_keys(nombreNuevoUsuario)
        time.sleep(1)
        inputPassUsuario = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_element(By.ID, "NewUserPlayerPassword")).send_keys(contrasenaNuevoUsuario)
        time.sleep(1)
        submit = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_element(By.ID, "ModalNewUserPlayerSubmit")).click()
        time.sleep(2)
        errormsj = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_elements(By.ID, "NewUserPlayerError"))
        print(errormsj[0].text)
        if not errormsj[0].text:
            informe = True
        else:
            btnCancelar = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_element(By.XPATH, '//*[@id="NewUserTabPlayer"]/div[2]/button[1]')).click()
            informe = False
        time.sleep(1)
        return informe
    except Exception as err:
        informe = f"Error al crear un nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}. Funcion botNuevoJugador(). Linea 276. Archivo bp03.py"
        print(
            f"Error al crear un nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}")
        reporte_errores.reportar_error(informe, err)
        return False

def botCambiarPw(usuario):
    proceso = f"Cambiando contraseña del usuario: {usuario}. Funcion botCambiarPw(). Linea 284. Archivo bp03.py"
    print(f"Buscando usuario: {usuario} para cambio de contraseña")
    track_procesos.agregar_proceso(proceso)
    try:
        xpath = '//*[@id="users"]/tbody/tr'
        tablaUsuarios = WebDriverWait(driverPlataforma, timeout=5).until(
            lambda d: d.find_elements(By.XPATH, xpath))
        time.sleep(1)
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '//*[@id="users"]/tbody/tr[' + str(x) + ']/td[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=5).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                try:
                    print("Usuario " + usuario +
                          " encontrado.. Cambiando password..")
                    xpath = '//*[@id="users"]/tbody/tr['+ str(x) + ']/td[4]/a[2]'
                    botonCambiarPw = WebDriverWait(driverPlataforma, timeout=5).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    time.sleep(2)
                    inputNewPw1 = WebDriverWait((driverPlataforma), timeout=5).until(
                        lambda d: d.find_element(By.ID, 'ChangePasswordNew1')).send_keys("Hola123")
                    time.sleep(1)
                    inputNewPw2 = WebDriverWait((driverPlataforma), timeout=5).until(
                        lambda d: d.find_element(By.ID, 'ChangePasswordNew2')).send_keys("Hola123")
                    time.sleep(1)
                    btn_submit = WebDriverWait((driverPlataforma), timeout=5).until(
                        lambda d: d.find_element(By.ID, 'ModalChangePasswordSubmit')).click()
                    time.sleep(1)
                    errormsj = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_elements(By.ID, "ChangePasswordError"))
                    time.sleep(2)
                    print(errormsj[0].text)
                    if not errormsj[0].text:
                        informe = f"CAMBIO DE CONTRASEÑA EXITOSO PARA EL USUARIO {usuario}"
                    else:
                        #Si salta mensaje error, es porque  la contraseña anterior del usuario es "Hola123" en este caso, igualmente informo cambio correcto, y cierro la ventana de cambio de pw de la plat.
                        informe = f"CAMBIO DE CONTRASEÑA EXITOSO PARA EL USUARIO {usuario}"
                        xpath = '//*[@id="ModalChangePassword"]/div/div/div[3]/button[1]'
                        botonCancelar = WebDriverWait(driverPlataforma, timeout=5).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    print(f"Contraseña del usuario {usuario} cambiada")
                    return True, informe
                    break
                except Exception as err:
                    informe1 = f"Error al cambiar contraseña del usuario {usuario}, posiblemente usuario bloqueado. Funcion botCambiarPw(). Linea 324. Archivo bp03.py"
                    print(f"Error cambiando password al usuario: {usuario}. Posiblemente usuario bloqueado.  El usuario ya fue notificado.")
                    informe = "*ERROR.* Tu usuario esta bloqueado. Entra en la opcion 4 del menu. Y luego volve a la opcion 2."
                    return True, informe
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
                x = x+1
    except Exception as err:
        informe = f"Error al cambiar contraseña del usuario {usuario}. Funcion botCambiarPw(). Linea 337. Archivo bp03.py"
        print(f"Error al cambiar contraseña del usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)
        return True, informe

def botDesbloquearUser(usuario):
    proceso = f"Buscando usuario: {usuario} para desbloqueo. Funcion botDesbloquearUser(). Linea 344. Archivo bp03.py"
    print(f"Buscando usuario: {usuario} para desbloqueo")
    track_procesos.agregar_proceso(proceso)
    try:
        xpath = '//*[@id="users"]/tbody/tr'
        tablaUsuarios = WebDriverWait(driverPlataforma, timeout=5).until(
            lambda d: d.find_elements(By.XPATH, xpath))
        time.sleep(2)
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '//*[@id="users"]/tbody/tr[' + str(x) + ']/td[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=5).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                xpath = '//*[@id="users"]/tbody/tr['+ str(x) + ']/td[4]/a[4]'
                btnDesbloquear = WebDriverWait(driverPlataforma, timeout=5).until(
                    lambda d: d.find_element(By.XPATH, xpath)).click()
                time.sleep(1)
                try: #para desbloquear no pide justificacion de pq. entonces nunca va a estar el elemento btnAceptar.
                    btnAceptar = WebDriverWait(driverPlataforma, timeout=5).until(lambda d: d.find_element(By.ID, "ModalLockUserConfirmSubmit")).click()
                except:
                    pass
                informe = "desbloqueado"
                time.sleep(1)
                print(f"Usuario {usuario} desbloqueado")
                return True, informe
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
                x = x+1
    except Exception as err:
        informe = f"Error al desbloquear cuenta del usuario: {usuario}. Funcion botDesbloquearUser(). Linea 376. Archivo bp03.py"
        print(f"Error al desbloquear cuenta del usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)
        return True, informe


def cd_bot_plataforma(accion, admin, clave_admin, usuario, monto):
    global driverPlataforma
    if accion == "CARGA":
        proceso = "Llamando bot de carga. Funcion cd_bot_plataforma(). Linea 385. Archivo bp03.py"
        print("Llamando bot de carga")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botCarga(usuario, monto)
    elif accion == "DESCARGA":
        proceso = "Llamando bot de descarga. Funcion cd_bot_plataforma(). Linea 390. Archivo bp03.py"
        print("Llamando bot de descarga")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botDescarga(usuario, monto)
    elif accion == "PASSW":
        proceso = "Llamando bot de cambio de contraseña. Funcion cd_bot_plataforma(). Linea 395. Archivo bp03.py"
        print("Llamando bot de cambio de contraseña")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botCambiarPw(usuario)
    elif accion == "DESBLOQ":
        proceso = "Llamando bot de desbloqueo. Funcion cd_bot_plataforma(). Linea 400. Archivo bp03.py"
        print("Llamando bot de desbloqueo")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botDesbloquearUser(usuario)
    elif accion == "FICHAS":
        proceso = "Llamando bot de consulta de fichas. Funcion cd_bot_plataforma(). Linea 405. Archivo bp03.py"
        print("Llamando bot de consulta de fichas")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = fichas_usuario(usuario)
    try:
        num = 2
        while bolean == False:
            time.sleep(1)
            k = cambio_de_pagina(num)
            num = num + 1
            if k == True:
                time.sleep(1)
                if accion == "CARGA":
                    bolean, informe = botCarga(usuario, monto)
                elif accion == "DESCARGA":
                    bolean, informe = botDescarga(usuario, monto)
                elif accion == "PASSW":
                    bolean, informe = botCambiarPw(usuario)
                elif accion == "DESBLOQ":
                    bolean, informe = botDesbloquearUser(usuario)
                elif accion == "FICHAS":
                    bolean, informe = fichas_usuario(usuario)
            else:
                informe = f"*Usuario inexistente.*\n El usuario {usuario}, no existe en tu lista."
        # ALAMABRE PARA PODER VOLVER A LA PAGINA NUMERO 1 EN LA TABLA DE USUARIOS DE LA PLATAFORMA.
        time.sleep(2)
        volver_pag_1()
    except Exception as err:
        volver_pag_1()
        informe = f"Error inesperado. Funcion cd_bot_plataforma(). Linea 432. Archivo bp03.py"
        print("Error inesperado")
        reporte_errores.reportar_error(informe, err)
    return informe
