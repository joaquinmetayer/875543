from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import time
import re

from bp04init import driverPlataforma
import db
import track_procesos
import reporte_errores
import config

admin, clave_admin = config.cuenta_logeo()
user_config = config.usuario_config()

def actividad_panel():
    try:
        xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[1]/div[3]/div/div/button[2]'
        btnNuevoJugador = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath)).click()
        time.sleep(1)
        xpath = "/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/create-agent-modal/div/div/div/form/div[3]/button[1]"
        btnCancelar = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath)).click()
    except:
        xpath = "/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[1]/td[4]/div/div/button"
        btnMenu = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath)).click()
        btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "tgAll")).click()

#################### cambio_de_pagina(). Listo ####################
def cambio_de_pagina(num):
    proceso = f"Cambiando a página número: {num}. Funcion cambio_de_pagina(). Linea 23. Archivo bp04.py"
    print(f"Cambiando a página número: {num}")

    tablaUsuarios = driverPlataforma.execute_script(
        "return document.getElementsByClassName('player-row ng-star-inserted');")
    length = driverPlataforma.execute_script("return arguments[0].length;", tablaUsuarios)

    if length >= 1:
        #hay usuarios retorno true
        xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/div/p-paginator/div/a[3]'
        btn_pasar_pag = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath)).click()
        return True
    else:
        return False
######################################################################

########################## volver_pag_1() integrada ###################

def volver_pag_1():
    btn_principio = driverPlataforma.execute_script(
                "return document.getElementsByClassName('ui-paginator-first')[0];")
    driverPlataforma.execute_script("arguments[0].click();", btn_principio)
    time.sleep(2)

#######################################################################

######################### fichas_administrador() integrada#############

def fichas_administrador():
    proceso = "Chequeando cantidad de fichas del administrador. Funcion fichas_administrador(). Linea 41. Archivo bp04.py"
    print("Chequeando cantidad de fichas del administrador")
    track_procesos.agregar_proceso(proceso)
    try:
        fichas = WebDriverWait(driverPlataforma, timeout=15).until(
		    lambda d: d.find_element(By.CLASS_NAME, 'MainAgentBalance')).text
        return fichas
    except Exception as err:
        return "error al consultar fichas en panel"

#########################################################################

######## fichas_usuario() integrada ###########################

def fichas_usuario(usuario):
    proceso = f"Chequeando cantidad de fichas del usuario: {usuario}. Funcion fichas_usuario(). Linea 54. Archivo bp04.py"
    print(f"Buscando al usuario {usuario} para chequeo de fichas")
    track_procesos.agregar_proceso(proceso)
    try:
        # busco el usuario por barra de busqueda
        xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[1]/div[1]/div[1]/input'
        barraDeBusqueda = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath))
        barraDeBusqueda.send_keys(usuario)
        time.sleep(1)

        xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[1]/div[1]/div[2]/button'
        barraDebusquedaClick = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).click()
        time.sleep(5)

        try:
            xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr'
            tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_elements(By.XPATH, xpath))
        except Exception as err:
            volver_pag_1()
            informe = f"Error chequeando cantidad de fichas del usuario: {usuario}. Chequear que el usuario no este bloqueado."
            print(f"Error chequeando cantidad de fichas del usuario: {usuario}. Chequear que el usuario no este bloqueado.")
            # Seteo visualizacion de usuarios
            xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
            btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()
            return True, informe

        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
			    str(x) + ']/td[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                fichas = WebDriverWait(driverPlataforma, timeout=15).until(
                    lambda d: d.find_element(By.ID, "itemBlc__"+usuario)).text
                fichas_sin_coma = fichas.split(",")
                fichas = fichas_sin_coma[0]
                # chequeo si existe un "." en la cantidad de fichas. Si existe, significa que tiene mas de 999 fichas. ej: 1.000 fichas
                punto = fichas.count(".")
                if punto == 1:
                    fichas = fichas.split(".")
                    fichas_del_usuario = fichas[0] + fichas[1]
                    print(f"Chequeo de fichas al usuario {usuario} exitoso")
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
                    btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    return True, fichas_del_usuario
                elif punto == 2:
                    fichas = fichas.split(".")
                    fichas_del_usuario = fichas[0] + fichas[1] + fichas[2]
                    print(f"Chequeo de fichas al usuario {usuario}: exitoso")
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
                    btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    return True, fichas_del_usuario
                elif punto == 3:
                    fichas = fichas.split(".")
                    fichas_del_usuario = fichas[0] + fichas[1] + fichas[2] + fichas[3]
                    print(f"Chequeo de fichas al usuario {usuario}: exitoso")
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
                    btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()                    
                    return True, fichas_del_usuario
                else:
                    print(f"Chequeo de fichas al usuario {usuario} exitoso")
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
                    btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    return True, fichas
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
            x = x + 1
    except Exception as err:
        volver_pag_1()
        informe = f"Error chequeando cantidad de fichas del usuario: {usuario}. Funcion fichas_usuario(). Linea 91. Archivo bp04.py"
        print(f"Error chequeando cantidad de fichas del usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)

##########################################################################

############### botCarga() integrado ###################################

def botCarga(usuario, monto):
    proceso = f"Cargando {monto} fichas al usuario: {usuario}. Funcion botCarga(). Linea 97. Archivo bp04.py"
    print(f"Buscando al usuario {usuario} para carga de {monto} fichas")
    track_procesos.agregar_proceso(proceso)
    try:
        # Chequeo cantidad defichas en panel, con cantidad de fichas solicitadas para cargar
        fichas = WebDriverWait(driverPlataforma, timeout=15).until(
		    lambda d: d.find_element(By.CLASS_NAME, 'MainAgentBalance')).text
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
        elif punto == 2:
            fichas_split2 = fichas.split(".")
            fichas_en_panel = fichas_split2[0] + fichas_split2[1] + fichas_split2[2]
            # luego de hacer toda la manipulacion de datos, eliminar "." ahora puedo pasar el string a INT sin problemas..
            if int(monto) > int(fichas_en_panel):
                informe = f"*ERROR.* Cantidad de fichas en panel insuficientes.\n *Fichas en panel*: {fichas} \n *Monto a cargar:* {monto} al usuario {usuario}\n Solicite más fichas a su superior, y vuelva a ejectuar el comando.\n"
                return True, informe
        elif punto == 3:
            fichas_split2 = fichas.split(".")
            fichas_en_panel = fichas_split2[0] + fichas_split2[1] + fichas_split2[2] + fichas_split2[3]
            # luego de hacer toda la manipulacion de datos, eliminar "." ahora puedo pasar el string a INT sin problemas..
            if int(monto) > int(fichas_en_panel):
                informe = f"*ERROR.* Cantidad de fichas en panel insuficientes.\n *Fichas en panel*: {fichas} \n *Monto a cargar:* {monto} al usuario {usuario}\n Solicite más fichas a su superior, y vuelva a ejectuar el comando.\n"
                return True, informe
        else:
            print(f"Entrando a comparar monto: {monto} con fichas: {fichas}")
            if int(monto) > int(fichas):
                informe = f"*ERROR.* Cantidad de fichas en panel insuficientes.\n *Fichas en panel*: {fichas} \n *Monto a cargar:* {monto} al usuario {usuario}\n Solicite más fichas a su superior, y vuelva a ejectuar el comando.\n"
                return True, informe
        # busco el usuario por barra de busqueda
        xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[1]/div[1]/div[1]/input'
        barraDeBusqueda = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath))
        barraDeBusqueda.send_keys(usuario)
        time.sleep(1)
        xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[1]/div[1]/div[2]/button'
        barraDebusquedaClick = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).click()
        time.sleep(5)

        # encuentra todos los elementos de la tabla usuarios
        try:
            xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr'
            tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_elements(By.XPATH, xpath))
        except Exception as err:
            volver_pag_1()
            informe = f"Error cargando fichas del usuario: {usuario}. Chequear que el usuario no este bloqueado."
            print(f"Error cargando fichas del usuario: {usuario}. Chequear que el usuario no este bloqueado.")
            # Seteo visualizacion de usuarios
            xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
            btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()
            return True, informe
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
			    str(x) + ']/td[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                try:
                    print(f"Usuario {usuario} encontrado. Cargando fichas")
                    xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
					    str(x) + ']/td[3]/div/div[1]/div'
                    botonCarga = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    time.sleep(2)
                    inputCarga = WebDriverWait(driverPlataforma, timeout=15).until(
					    lambda d: d.find_element(By.ID, "txt_monto")).send_keys(monto)
                    time.sleep(2)
					# boton depositar por javascript executor
                    btn_depositar = driverPlataforma.execute_script(
					    "return document.getElementsByClassName('btn btn-primary')[2];")
                    driverPlataforma.execute_script("arguments[0].click();", btn_depositar)
                    time.sleep(2)
                    botonConfirmacion = WebDriverWait(driverPlataforma, timeout=15).until(
					    lambda d: d.find_element(By.CLASS_NAME, "swal2-confirm"))
                    botonConfirmacion.click()
                    print(f"Carga exitosa de {monto} fichas al usuario {usuario}")
                    informe = "*Carga exitosa.* " + \
                        str(monto) + " al usuario " + nombreUsuario + "\n"
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
                    btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    return True, informe
                    break
                except Exception as err:
                    volver_pag_1()
                    informe1 = f"Error cargando fichas al usuario: {usuario}. Posiblemente usuario bloqueado. Funcion botCarga(). Linea 149. Archivo bp04.py"
                    print(f"Error cargando fichas al usuario: {usuario}. Chequear que el usuario no este bloqueado")
                    reporte_errores.reportar_error(informe1, err)
                    informe = f"Error carga no realizada. Chequear que el usuario {usuario} no este bloqueado. Y volver a ejectuar comando de carga."
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
                    btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    return True, informe
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
            x = x+1
    except Exception as err:
        volver_pag_1()
        informe = f"Error cargando fichas al usuario: {usuario}. Funcion botCarga(). Linea 162. Archivo bp04.py"
        print(f"Error cargando fichas al usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)
        return informe

##############################################################################

####################  botDescarga() listo ################################

def botDescarga(usuario, monto):
    leer = f"""botDescarga esta desabhilitado debido a como esta programada la paginas de gama planeta. Al ingresar
                al cuadro de descarga, automaticamente se carga en el txt_input, la cantidad de fichas totales del usuario
                y no puedo acceder al elemento para modificar el monto. Por esta razon, la descarga debe hacerse manualmente. {usuario},{monto}"""

##############################################################################

#################### botNuevoJugador() listo #################################
def botNuevoJugador(admin, clave_admin, nombreNuevoUsuario, contrasenaNuevoUsuario):
    proceso = f"Creando nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}. Funcion botNuevoJugador(). Linea 226. Archivo bp04.py"
    print(f"Creando nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}")
    track_procesos.agregar_proceso(proceso)
    global driverPlataforma
    try:
        xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[1]/div[3]/div/div/button[2]'
        btnNuevoJugador = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath)).click()
        time.sleep(1)
        inputNombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "txt_createusr_name")).send_keys(nombreNuevoUsuario)
        time.sleep(1)
        inputPassUsuario = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "txt_createusr_pass")).send_keys(contrasenaNuevoUsuario)
        time.sleep(1)
        submit = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "btn_submit")).click()
        time.sleep(2)
        xpath = '//*[@id="swal2-content"]/span'
        errormsj = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_elements(By.XPATH, xpath))
        print(errormsj[0].text)
        if errormsj[0].text == "The username is already in use." or errormsj[0].text == "El nombre de usuario ya esta en uso.":
            xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/create-agent-modal/div/div/div/form/div[1]/button'
            btn_close = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath)).click()
            return False
        else:
            return True
        time.sleep(1)
    except Exception as err:
        informe = f"Error al crear un nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}. Funcion botNuevoJugador(). Linea 276. Archivo bp04.py"
        print(
            f"Error al crear un nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}")
        reporte_errores.reportar_error(informe, err)
        return False

#######################################################################################

################################## botCambiarPw() listo.  V##############

def botCambiarPw(usuario):
    proceso = f"Cambiando contraseña del usuario: {usuario}. Funcion botCambiarPw(). Linea 284. Archivo bp04.py"
    print(f"Buscando usuario: {usuario} para cambio de contraseña")
    track_procesos.agregar_proceso(proceso)
    try:
        # busco el usuario por barra de busqueda
        xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[1]/div[1]/div[1]/input'
        barraDeBusqueda = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath))
        barraDeBusqueda.send_keys(usuario)
        time.sleep(1)
        xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[1]/div[1]/div[2]/button'
        barraDebusquedaClick = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).click()
        time.sleep(5)

        # encuentra todos los elementos de la tabla usuarios
        try:
            xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr'
            tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_elements(By.XPATH, xpath))
        except Exception as err:
            volver_pag_1()
            informe = f"Error cambiando contraseña del usuario: {usuario}. Chequear que el usuario no este bloqueado."
            print(f"Error cambiando contraseña del usuario: {usuario}. Chequear que el usuario no este bloqueado.")
            # Seteo visualizacion de usuarios
            xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
            btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()
            return True, informe

        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
			    str(x) + ']/td[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                try:
                    print("Usuario " + usuario +
                          " encontrado.. Cambiando password..")
                    xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
			    str(x) + ']/td[4]/div/div/button'
                    btn_acciones = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/bs-dropdown-container/div/ul/li[4]/a'
                    botonCambiarPw = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    time.sleep(2)
                    if usuario == user_config:
                        inputNewPw1 = WebDriverWait((driverPlataforma), timeout=15).until(
                            lambda d: d.find_element(By.ID, 'txt_changepassword_newPass')).send_keys("Hola123")
                        time.sleep(1)
                    xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/changepassword-modal/div/div/div/form/div[3]/button[2]'
                    btn_submit = WebDriverWait((driverPlataforma), timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()                    
                    informe = f"Contraseña del usuario {usuario} cambiada"
                    print(informe)
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
                    btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    return True, informe
                    break
                except Exception as err:
                    volver_pag_1()
                    informe1 = f"Error al cambiar contraseña del usuario {usuario}, posiblemente usuario bloqueado. Funcion botCambiarPw(). Linea 324. Archivo bp04.py"
                    print(f"Error cambiando password al usuario: {usuario}. Posiblemente usuario bloqueado. El usuario ya fue notificado.")
                    informe = "*ERROR.* Tu usuario esta bloqueado. Entra en la opcion 4 del menu. Y luego volve a la opcion 2."
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
                    btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    return True, informe
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
                x = x+1
    except Exception as err:
        volver_pag_1()
        informe = f"Error al cambiar contraseña del usuario {usuario}. Funcion botCambiarPw(). Linea 337. Archivo bp04.py"
        print(f"Error al cambiar contraseña del usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)
        return True, informe

#######################################################################################################

################################

def botDesbloquearUser(usuario):
    proceso = f"Buscando usuario: {usuario} para desbloqueo. Funcion botDesbloquearUser(). Linea 344. Archivo bp04.py"
    print(f"Buscando usuario: {usuario} para desbloqueo")
    track_procesos.agregar_proceso(proceso)
    try:
        xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr'
        tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_elements(By.XPATH, xpath))
        time.sleep(2)
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
			    str(x) + ']/td[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                xpath = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
			    str(x) + ']/td[4]/div/div/button'
                btn_acciones = WebDriverWait(driverPlataforma, timeout=15).until(
                    lambda d: d.find_element(By.XPATH, xpath)).click()
                xpath = '/html/body/bs-dropdown-container/div/ul/li[1]/a'
                btnDesbloquear = WebDriverWait(driverPlataforma, timeout=15).until(
                    lambda d: d.find_element(By.XPATH, xpath))
                if btnDesbloquear.text == "Habilitar":
                    btnDesbloquear.click()
                    time.sleep(1)
                    xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/enabledisable-modal/div/div/div/form/div[3]/button[2]'
                    btn_submit = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    time.sleep(1)
                    xpath = '/html/body/div/div/div[3]/button[1]'
                    btn_confirmar = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
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
        volver_pag_1()
        informe = f"Error al desbloquear cuenta del usuario: {usuario}. Funcion botDesbloquearUser(). Linea 376. Archivo bp04.py"
        print(f"Error al desbloquear cuenta del usuario: {usuario}", err)
        reporte_errores.reportar_error(informe, err)
        return True, informe


def cd_bot_plataforma(accion, admin, clave_admin, usuario, monto):
    global driverPlataforma
    if accion == "CARGA":
        proceso = "Llamando bot de carga. Funcion cd_bot_plataforma(). Linea 385. Archivo bp04.py"
        print("Llamando bot de carga")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botCarga(usuario, monto)
    elif accion == "DESCARGA":
        proceso = "Llamando bot de descarga. Funcion cd_bot_plataforma(). Linea 390. Archivo bp04.py"
        print("Llamando bot de descarga")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botDescarga(usuario, monto)
    elif accion == "PASSW":
        proceso = "Llamando bot de cambio de contraseña. Funcion cd_bot_plataforma(). Linea 395. Archivo bp04.py"
        print("Llamando bot de cambio de contraseña")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botCambiarPw(usuario)
    elif accion == "DESBLOQ":
        proceso = "Llamando bot de desbloqueo. Funcion cd_bot_plataforma(). Linea 400. Archivo bp04.py"
        print("Llamando bot de desbloqueo")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botDesbloquearUser(usuario)
    elif accion == "FICHAS":
        proceso = "Llamando bot de consulta de fichas. Funcion cd_bot_plataforma(). Linea 405. Archivo bp04.py"
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
        try:
            volver_pag_1()
        except:
            pass
    except Exception as err:
        informe = f"Error inesperado. Funcion cd_bot_plataforma(). Linea 432. Archivo bp04.py"
        print("Error inesperado")
        reporte_errores.reportar_error(informe, err)
    return informe
