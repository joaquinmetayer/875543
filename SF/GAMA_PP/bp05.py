from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import pyautogui
import time
import re

from bp05init import driverPlataforma
import db
import track_procesos
import reporte_errores
import config

admin, clave_admin = config.cuenta_logeo()

def actividad_panel():
    #funcion para evitar que el panel se cierre por inactividad
    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
        lambda d: d.find_element(By.XPATH, xpath)).click()
    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
        lambda d: d.find_element(By.XPATH, xpath)).click()


def cambio_de_pagina(num):
    try:
        time.sleep(2)
        proceso = f"Cambiando a página número: {num}. Funcion cambio_de_pagina(). Linea 23. Archivo bp05.py"
        print(f"Cambiando a página número: {num}")
        xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-paginator/div/div/div[2]/button[2]'
        elem_paginacion = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).click()
        return True
    except:
        print("Usuario no existe. No hay más paginas, y no se encontro usuario con ese nombre.")
        return False

def volver_pag_1(num):
    time.sleep(1)
    while num > 0:
        xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-paginator/div/div/div[2]/button[1]'
        elem_paginacion = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).click()
        num -= 1
    time.sleep(1)

def fichas_administrador():
    proceso = "Chequeando cantidad de fichas del administrador. Funcion fichas_administrador(). Linea 41. Archivo bp05.py"
    print("Chequeando cantidad de fichas del administrador")
    track_procesos.agregar_proceso(proceso)
    try:
        xpath = '/html/body/app-root/app-default/app-header/mat-toolbar/mat-toolbar-row/ul/li[1]/span/app-credit/span'
        fichas = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).text
        return fichas
    except Exception as err:
        return "error al consultar fichas en panel"


def fichas_usuario(usuario):
    proceso = f"Chequeando cantidad de fichas del usuario: {usuario}. Funcion fichas_usuario(). Linea 54. Archivo bp05.py"
    print(f"Buscando al usuario {usuario} para chequeo de fichas")
    track_procesos.agregar_proceso(proceso)
    try:
         # busco el usuario por barra de busqueda
        xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[1]/app-users-page-search/app-search-user-form-field/mat-form-field/div/div[1]/div[1]/input'
        barraDeBusqueda = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath))
        barraDeBusqueda.send_keys(usuario)
        time.sleep(5)
        
        # Busco elementos tabla de usuarios
        try:
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row'
            tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_elements(By.XPATH, xpath))
        except Exception as err:
            informe = f"Error chequeando cantidad de fichas del usuario: {usuario}. Chequear que el usuario no este bloqueado."
            print(f"Error chequeando cantidad de fichas del usuario: {usuario} Chequear que el usuario no este bloqueado.")
            # Seteo visualizacion de usuarios
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
            dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
            usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()
                    
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row['+str(
                x)+']/mat-cell[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row['+str(
                    x)+']/mat-cell[3]/app-credit/span'
                fichas = WebDriverWait(driverPlataforma, timeout=15).until(
                    lambda d: d.find_element(By.XPATH, xpath)).text
                # chequeo si existe un "." en la cantidad de fichas. Si existe, significa que tiene mas de 999 fichas. ej: 1.000 fichas
                punto = fichas.count(".")
                if punto == 1:
                    fichas = fichas.split(".")
                    fichas_del_usuario = fichas[0] + fichas[1]
                    print(f"Chequeo de fichas al usuario {usuario}: exitoso")
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    return True, fichas_del_usuario
                elif punto == 2:
                    fichas = fichas.split(".")
                    fichas_del_usuario = fichas[0] + fichas[1] + fichas[2]
                    print(f"Chequeo de fichas al usuario {usuario}: exitoso")
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    return True, fichas_del_usuario
                elif punto == 3:
                    fichas = fichas.split(".")
                    fichas_del_usuario = fichas[0] + fichas[1] + fichas[2] + fichas[3]
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    print(f"Chequeo de fichas al usuario {usuario}: exitoso")
                    return True, fichas_del_usuario
                else:
                    print(f"Chequeo de fichas al usuario {usuario}: exitoso")
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    return True, fichas
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
            x = x + 1
    except Exception as err:
        informe = f"Error chequeando cantidad de fichas del usuario: {usuario}. Funcion fichas_usuario(). Linea 91. Archivo bp05.py"
        print(f"Error chequeando cantidad de fichas del usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)


def botCarga(usuario, monto):
    proceso = f"Cargando {monto} fichas al usuario: {usuario}. Funcion botCarga(). Linea 97. Archivo bp05.py"
    print(f"Buscando al usuario {usuario} para carga de {monto} fichas")
    track_procesos.agregar_proceso(proceso)
    try:
        # Chequeo cantidad defichas en panel, con cantidad de fichas solicitadas para cargar
        xpath = '/html/body/app-root/app-default/app-header/mat-toolbar/mat-toolbar-row/ul/li[1]/span/app-credit/span'
        fichas = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).text
        punto = fichas.count(".")
        if punto == 1:
            fichas_split2 = fichas.split(".")
            fichas_en_panel = fichas_split2[0] + fichas_split2[1]
            # luego de hacer toda la manipulacion de datos, eliminar "." ahora puedo pasar el string a INT sin problemas..
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
            if int(monto) > int(fichas):
                informe = f"*ERROR.* Cantidad de fichas en panel insuficientes.\n *Fichas en panel*: {fichas} \n *Monto a cargar:* {monto} al usuario {usuario}\n Solicite más fichas a su superior, y vuelva a ejectuar el comando.\n"
                return True, informe

        # busco el usuario por barra de busqueda
        xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[1]/app-users-page-search/app-search-user-form-field/mat-form-field/div/div[1]/div[1]/input'
        barraDeBusqueda = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath))
        barraDeBusqueda.send_keys(usuario)
        time.sleep(5)
        
        # encuentra todos los elementos de la tabla usuarios
        try:
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row'
            tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_elements(By.XPATH, xpath))
            time.sleep(2)
        except Exception as err:
            print(f"Error cargando fichas al usuario: {usuario}. Chequear que el usuario no este bloqueado")
            informe = f"Error carga no realizada. Chequear que el usuario *{usuario}* no este bloqueado. Y volver a ejectuar comando de carga."
            # Seteo visualizacion de usuarios
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
            dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
            usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()        
            return True, informe
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row['+str(
                x)+']/mat-cell[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                try:
                    print(f"Usuario {usuario} encontrado. Cargando fichas")
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row['+str(
                        x)+']/mat-cell[4]/app-set-credits[1]/button'
                    botonCarga = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    time.sleep(2)
                    xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/app-set-player-credits-dialog/mat-dialog-content/section[2]/app-credits-form-field/mat-form-field/div/div[1]/div/input'
                    inputCarga = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).send_keys(monto)
                    xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/app-set-player-credits-dialog/footer/button[2]'
                    submitCarga = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    print(f"Carga exitosa de {monto} fichas al usuario {usuario}")
                    informe = "*Carga exitosa.* " + \
                        str(monto) + " al usuario " + nombreUsuario + "\n"
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    
                    return True, informe
                    break
                except Exception as err:
                    print(f"Error cargando fichas al usuario: {usuario}. Chequear que el usuario no este bloqueado")
                    informe = f"Error carga no realizada. Chequear que el usuario *{usuario}* no este bloqueado. Y volver a ejectuar comando de carga."
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    
                    return True, informe
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
            x = x+1
    except Exception as err:
        informe = f"Error cargando fichas al usuario: {usuario}. Funcion botCarga(). Linea 162. Archivo bp05.py."
        print(f"Error cargando fichas al usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)
        return informe


def botDescarga(usuario, monto):
    proceso = f"Descargando {monto} fichas al usuario: {usuario}. Funcion botDescarga(). Linea 169. Archivo bp05.py"
    print(f"Buscando usuario {usuario} para descarga de {monto} fichas")
    track_procesos.agregar_proceso(proceso)
    try:
        
        # busco el usuario por barra de busqueda
        xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[1]/app-users-page-search/app-search-user-form-field/mat-form-field/div/div[1]/div[1]/input'
        barraDeBusqueda = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath))
        barraDeBusqueda.send_keys(usuario)
        time.sleep(5)
        
        
        # encuentra todos los elementos de la tabla usuarios
        
        try:
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row'
            tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_elements(By.XPATH, xpath))
            time.sleep(1)
        except Exception as err:
            print(f"Error cambiando password al usuario: {usuario}. Posiblemente usuario bloqueado.")
            informe = "*ERROR.* Tu usuario esta bloqueado. Entra en la opcion 4 del menu. Y luego volve a la opcion 2."
            # Seteo visualizacion de usuarios
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
            dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
            usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()   
            return True, informe
        x = 1

        for filaUsuarios in tablaUsuarios:
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row['+str(
                x)+']/mat-cell[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                try:
                    print(f"Usuario {usuario} encontrado. Descargando fichas")
                    xpath = xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row['+str(
                        x)+']/mat-cell[4]/app-set-credits[2]/button'
                    botonDescarga = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    time.sleep(2)
                    xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/app-set-player-credits-dialog/mat-dialog-content/section[2]/app-credits-form-field/mat-form-field/div/div[1]/div/input'
                    inputDescarga = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).send_keys(monto)
                    time.sleep(1)
                    xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/app-set-player-credits-dialog/footer/button[2]'
                    botonAceptar = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    print(f"Descarga exitosa de {monto} fichas al usuario {usuario}")
                    informe = "*Descarga exitosa.* " + \
                        str(monto) + " al usuario " + nombreUsuario + "\n"
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    
                    return True, informe
                    break
                except Exception as err:
                    print(f"Error descargando fichas al usuario: {usuario}. Usuario bloqueado. Ya fue notificado el jugador")
                    informe = "*ERROR.* Tu usuario esta bloqueado. Entra en la opcion 4 del menú. Y luego volve a la opción 3."
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    
                    return True, informe
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
            x = x+1
    except Exception as err:
        informe = f"Error descargando fichas al usuario: {usuario}. Funcion botDescarga(). Linea 219. Archivo bp05.py"
        print(f"Error descargando fichas al usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)
        return informe


def botNuevoJugador(admin, clave_admin, nombreNuevoUsuario, contrasenaNuevoUsuario):
    proceso = f"Creando nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}. Funcion botNuevoJugador(). Linea 226. Archivo bp05.py"
    print(f"Creando nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}")
    track_procesos.agregar_proceso(proceso)
    global driverPlataforma
    try:
        xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/header/app-create-users/div/app-create-user-button[2]/button'
        btnNuevoJugador = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).click()
        time.sleep(1)
        xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/ng-component/mat-dialog-content/app-players-creation-form/mat-stepper/div/div[2]/div[1]/app-players-creation-credential/app-form-credential/app-form-group/form/app-form-field-username/mat-form-field/div/div[1]/div/input'
        inputNombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).send_keys(nombreNuevoUsuario)
        time.sleep(1)
        xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/ng-component/mat-dialog-content/app-players-creation-form/mat-stepper/div/div[2]/div[1]/app-players-creation-credential/app-form-credential/app-form-group/form/app-form-field-password/mat-form-field/div/div[1]/div[1]/input'
        inputPassUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).send_keys(contrasenaNuevoUsuario)
        time.sleep(1)
        xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/ng-component/mat-dialog-content/app-players-creation-form/mat-stepper/div/div[2]/div[1]/app-players-creation-credential/app-stepper-footer/div/button'
        submit = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).click()
        time.sleep(2)
        xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/ng-component/mat-dialog-content/app-players-creation-form/mat-stepper/div/div[2]/div[2]/app-players-creation-person/app-stepper-footer/div/button[2]'
        submitFinal = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath)).click()
        time.sleep(1)
        xpath = '/html/body/div[4]/div[3]/div/snack-bar-container/div/div/simple-snack-bar'
        errormsj = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_elements(By.XPATH, xpath))
        print(errormsj[0].text)
        if "Error" in errormsj[0].text:
            informe = False
        else:
            informe = True
        time.sleep(1)
        ventana = driverPlataforma.execute_script(
            "return document.getElementsByClassName('mat-focus-indicator mat-button mat-button-base ng-star-inserted')[0];")
        driverPlataforma.execute_script("arguments[0].click();", ventana)
        # parche para actualizar pag por medio el boton bloqueados, asi se actualiza la tabla usuarios.
        btn = driverPlataforma.execute_script(
            "return document.getElementById('mat-slide-toggle-1-input');")
        driverPlataforma.execute_script("arguments[0].click();", btn)
        time.sleep(2)
        btn = driverPlataforma.execute_script(
            "return document.getElementById('mat-slide-toggle-1-input');")
        driverPlataforma.execute_script("arguments[0].click();", btn)
        return informe
    except Exception as err:
        ventana = driverPlataforma.execute_script(
            "return document.getElementsByClassName('mat-focus-indicator mat-button mat-button-base ng-star-inserted')[0];")
        driverPlataforma.execute_script("arguments[0].click();", ventana)
        informe = f"Error al crear un nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}. Funcion botNuevoJugador(). Linea 276. Archivo bp05.py"
        print(
            f"Error al crear un nuevo jugador con el nombre de usuario: {nombreNuevoUsuario}")
        reporte_errores.reportar_error(informe, err)
        return False


def botCambiarPw(usuario):
    proceso = f"Cambiando contraseña del usuario: {usuario}. Funcion botCambiarPw(). Linea 284. Archivo bp05.py"
    print(f"Buscando usuario: {usuario} para cambio de contraseña")
    track_procesos.agregar_proceso(proceso)
    try:
        # busco el usuario por barra de busqueda
        xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[1]/app-users-page-search/app-search-user-form-field/mat-form-field/div/div[1]/div[1]/input'
        barraDeBusqueda = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath))
        barraDeBusqueda.send_keys(usuario)
        time.sleep(5)
        try:
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row'
            tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_elements(By.XPATH, xpath))
            time.sleep(1)
        except Exception as err:
            print(f"Error cambiando password al usuario: {usuario}. Posiblemente usuario bloqueado.")
            informe = "*ERROR.* Tu usuario esta bloqueado. Entra en la opcion 4 del menu. Y luego volve a la opcion 2."
            # Seteo visualizacion de usuarios
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
            dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
            usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).click()   
            return True, informe
            
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row['+str(
                x)+']/mat-cell[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                try:
                    print("Usuario " + usuario +
                          " encontrado.. Cambiando password..")
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row['+str(
                        x)+']/mat-cell[5]/app-change-password/button'
                    botonCambiarPw = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    time.sleep(2)
                    xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/ng-component/mat-dialog-content/app-change-password-form/app-form-group/form/app-form-field-password[1]/mat-form-field/div/div[1]/div[1]/input'
                    inputNewPw1 = WebDriverWait((driverPlataforma), timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).send_keys("Hola123")
                    time.sleep(1)
                    xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/ng-component/mat-dialog-content/app-change-password-form/app-form-group/form/app-form-field-password[2]/mat-form-field/div/div[1]/div[1]/input'
                    inputNewPw2 = WebDriverWait((driverPlataforma), timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).send_keys("Hola123")
                    time.sleep(1)
                    xpath = '/html/body/div[4]/div[2]/div/mat-dialog-container/ng-component/mat-dialog-content/button[2]'
                    btn_submit = WebDriverWait((driverPlataforma), timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    informe = f"CAMBIO DE CONTRASEÑA EXITOSO PARA EL USUARIO {usuario}"
                    print(f"Contraseña del usuario {usuario} cambiada")
                    time.sleep(3)
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    
                    return True, informe
                    break
                except Exception as err:
                    print(f"Error cambiando password al usuario: {usuario}. Posiblemente usuario bloqueado.")
                    informe = "*ERROR.* Tu usuario esta bloqueado. Entra en la opcion 4 del menu. Y luego volve a la opcion 2."
                    # Seteo visualizacion de usuarios
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                    dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                    usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
                    
                    return True, informe
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
                x = x+1
    except Exception as err:
        informe = f"Error al cambiar contraseña del usuario {usuario}. Funcion botCambiarPw(). Linea 337. Archivo bp05.py"
        print(f"Error al cambiar contraseña del usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)
        return True, informe


def botDesbloquearUser(usuario):
    proceso = f"Buscando usuario: {usuario} para desbloqueo. Funcion botDesbloquearUser(). Linea 344. Archivo bp05.py"
    print(f"Buscando usuario: {usuario} para desbloqueo")
    track_procesos.agregar_proceso(proceso)
    try:
         # busco el usuario por barra de busqueda
        xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[1]/app-users-page-search/app-search-user-form-field/mat-form-field/div/div[1]/div[1]/input'
        barraDeBusqueda = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_element(By.XPATH, xpath))
        barraDeBusqueda.send_keys(usuario)
        time.sleep(5)
        
        xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row'
        tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
            lambda d: d.find_elements(By.XPATH, xpath))
        time.sleep(2)
        x = 1
        for filaUsuarios in tablaUsuarios:
            xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row['+str(
                x)+']/mat-cell[1]'
            nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(
                lambda d: d.find_element(By.XPATH, xpath)).text
            if nombreUsuario == usuario:
                xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer-content/app-users/section[2]/app-users-page-table/section/mat-table/mat-row['+str(
                    x)+']/mat-cell[5]/app-block-user/button'
                btnDesbloquear = WebDriverWait(driverPlataforma, timeout=15).until(
                    lambda d: d.find_element(By.XPATH, xpath)).click()
                time.sleep(1)
                informe = "desbloqueado"
                time.sleep(1)
                print(f"Usuario {usuario} desbloqueado")
                xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[1]/a'
                dashboard = WebDriverWait(driverPlataforma, timeout=15).until(
                    lambda d: d.find_element(By.XPATH, xpath)).click()
                xpath = '/html/body/app-root/app-default/mat-drawer-container/mat-drawer/div/app-sidebar/mat-nav-list/app-sidebar-items/app-sidebar-link-item[2]/a'
                usuarios =  WebDriverWait(driverPlataforma, timeout=15).until(
                    lambda d: d.find_element(By.XPATH, xpath)).click()
                time.sleep(4)
                # activo vision de usuarios bloqueados
                btn_bloqueados = driverPlataforma.execute_script(
                    "return document.getElementById('mat-slide-toggle-1-input');")
                driverPlataforma.execute_script("arguments[0].click();", btn_bloqueados)
                    
                return True, informe
            else:
                if x == (len(tablaUsuarios)):
                    informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
                    return False, informe
                    break
                x = x+1
    except Exception as err:
        informe = f"Error al desbloquear cuenta del usuario: {usuario}. Funcion botDesbloquearUser(). Linea 376. Archivo bp05.py"
        print(f"Error al desbloquear cuenta del usuario: {usuario}")
        reporte_errores.reportar_error(informe, err)
        return True, informe


def cd_bot_plataforma(accion, admin, clave_admin, usuario, monto):
    global driverPlataforma
    if accion == "CARGA":
        proceso = "Llamando bot de carga. Funcion cd_bot_plataforma(). Linea 385. Archivo bp05.py"
        print("Llamando bot de carga")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botCarga(usuario, monto)
    elif accion == "DESCARGA":
        proceso = "Llamando bot de descarga. Funcion cd_bot_plataforma(). Linea 390. Archivo bp05.py"
        print("Llamando bot de descarga")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botDescarga(usuario, monto)
    elif accion == "PASSW":
        proceso = "Llamando bot de cambio de contraseña. Funcion cd_bot_plataforma(). Linea 395. Archivo bp05.py"
        print("Llamando bot de cambio de contraseña")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botCambiarPw(usuario)
    elif accion == "DESBLOQ":
        proceso = "Llamando bot de desbloqueo. Funcion cd_bot_plataforma(). Linea 400. Archivo bp05.py"
        print("Llamando bot de desbloqueo")
        track_procesos.agregar_proceso(proceso)
        bolean, informe = botDesbloquearUser(usuario)
    elif accion == "FICHAS":
        proceso = "Llamando bot de consulta de fichas. Funcion cd_bot_plataforma(). Linea 405. Archivo bp05.py"
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
            volver_pag_1(num)
        except:
            time.sleep(2)
            pass
    except Exception as err:
        informe = f"Error inesperado. Funcion cd_bot_plataforma(). Linea 432. Archivo bp05.py"
        print("Error inesperado", err)
        reporte_errores.reportar_error(informe, err)
    return informe
