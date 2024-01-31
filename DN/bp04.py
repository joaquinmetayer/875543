from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
import re

import random_mail
import descomprimir
import db


def get(admin, clave_admin):
	try:
		#iniciacion plataforma
		s = Service('./driver/chromedriver.exe')
		options = Options()
		driverPlataforma = webdriver.Chrome(service=s, options=options)
		driverPlataforma.get("https://agentes.casino365online.net")
		driverPlataforma.maximize_window()
	except Exception as err:
		informe = "*ERROR*. Problemas con conexión de red. Vuelva a intentarlo, si el problema persiste. Comunicarse con soporte con el codigo - BP01-L19"
		return driverPlataforma, ""	

	# logeo
	try:
		user = WebDriverWait(driverPlataforma, timeout=10).until(lambda d: d.find_element(
		    By.XPATH, '//*[@id="kt_login"]/div/div[2]/div[2]/ng-component/div/form/div[1]/input')).send_keys(admin)
		time.sleep(1)
		passwd = WebDriverWait(driverPlataforma, timeout=10).until(lambda d: d.find_element(
		    By.XPATH, '//*[@id="kt_login"]/div/div[2]/div[2]/ng-component/div/form/div[2]/input')).send_keys(clave_admin)
		time.sleep(1)
		submit = WebDriverWait(driverPlataforma, timeout=10).until(lambda d: d.find_element(
		    By.XPATH, '//*[@id="kt_login"]/div/div[2]/div[2]/ng-component/div/form/div[3]/button')).click()
		time.sleep(5)
		elem_chequeo_ignorar = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_element(By.CLASS_NAME, 'MainAgentBalance'))
		chequeo = True
	except Exception as err:
		print("LINEA 31 funcion get() bp04", err)
		chequeo = False
		driverPlataforma.close()
		driverPlataforma.quit()
	return driverPlataforma, chequeo


def acomodar():
	try:
		pyautogui.hotkey("ctrl", "-")
		pyautogui.hotkey("ctrl", "-")
		pyautogui.hotkey("ctrl", "-")
		pyautogui.hotkey("ctrl", "-")
		pyautogui.hotkey("ctrl", "-")
		time.sleep(1)
		dp = WebDriverWait(driverPlataforma, timeout=10).until(lambda d: d.find_element(
		    By.XPATH, '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/div/p-paginator/div/p-dropdown/div')).click()
		time.sleep(2)
		dp50 = driverPlataforma.execute_script(
		    "return document.getElementsByClassName('ui-dropdown-item')[2];")
		driverPlataforma.execute_script("arguments[0].click();", dp50)
		time.sleep(1)
	except Exception as err:
		print("ERROR. acomodar() linea 54 bp04", err)
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte y enviar el siguiente codigo(bp04-L53)."
		driverPlataforma.quit()
		return informe


def conteo_fichas(admin, clave_admin):
	try:
		driverPlataforma, nn = get(admin, clave_admin)
		time.sleep(1)
		fichas1 = WebDriverWait(driverPlataforma, timeout=15).until(
		    lambda d: d.find_element(By.CLASS_NAME, 'MainAgentBalance')).text
		fichas = fichas1.split()
		fichas = fichas[0]
		return fichas
	except Exception as err:
		print("ERROR. conteo_fichas() linea 66 bp04", err)
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.quit()
		return informe


def cambio_de_pagina(num):
	y = num
	try:
		elem_paginacion = WebDriverWait(driverPlataforma, timeout=10).until(lambda d: d.find_element(
		    By.XPATH, '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/div/p-paginator/div/a[' + str(y) + ']')).click()
		print(f"Pasando a pagina: {num}")
		time.sleep(1)
		return True
	except:
		print("Usuario no existe. No hay más paginas, y no se encontro usuario con ese nombre. Linea 77 bp04")
		return False

def cambio_de_pagina2():
	try:
		elemen_paginacion = WebDriverWait(driverPlataforma, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "ui-paginator-next ui-paginator-element ui-state-default ui-corner-all"[1]))
		elemen_paginacion.click()
		return True
	except:
		return False


def botCarga(usuario, monto, nombre_cajero):
	try:
		fichas = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_element(By.CLASS_NAME, 'MainAgentBalance')).text
		punto = fichas.count(".")
		print(punto)
		# si no existe "." sigfnicia que tiene 999fichas o menos, entonces "fichas_en_panel" va a ser igual a "fichas_split1[0]"
		# si existe "." significa que tiene 1.000 o más fichas. En este caso hago split eliminando el "." y vuelvo a juntar las partes sumandolas (recordar que estoy manipulando un STRING)
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
			xpathstring = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
			    str(x) + ']/td[1]'
			nombreUsuario = WebDriverWait(driverPlataforma, timeout=10).until(
			    lambda d: d.find_element(By.XPATH, xpathstring)).text
			if nombreUsuario == usuario:
				try:
					print("Usuario " + usuario + " encontrado.. Cargando fichas..")
					xpathCarga = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
					    str(x) + ']/td[3]/div/div[1]/div'
					botonCarga = WebDriverWait(driverPlataforma, timeout=10).until(
					    lambda d: d.find_element(By.XPATH, xpathCarga))
					time.sleep(5)
					botonCarga.click()
					time.sleep(2)

					inputCarga = WebDriverWait(driverPlataforma, timeout=10).until(
					    lambda d: d.find_element(By.ID, "txt_monto")).send_keys(monto)
					print("bot cargando..: ", inputCarga)
					time.sleep(2)
					# boton depositar por javascript executor
					btn_depositar = driverPlataforma.execute_script(
					    "return document.getElementsByClassName('btn btn-primary')[2];")
					driverPlataforma.execute_script("arguments[0].click();", btn_depositar)
					time.sleep(4)
					botonConfirmacion = WebDriverWait(driverPlataforma, timeout=10).until(
					    lambda d: d.find_element(By.CLASS_NAME, "swal2-confirm"))
					botonConfirmacion.click()
					time.sleep(2)
					print("CARGA REALIZADA EXITOSAMENTE.")
					informe = "*Carga exitosa.* " + \
					    str(monto) + " al usuario " + nombreUsuario + "\n"
					
					# agrego la carga exitosa a la tabla registros de la base de datos
					id_cajero = db.select_id_cajero(nombre_cajero)
					# transofrmo id_cajero y id_plataforma de tupla a int
					id_cajero_int = (''.join(map(str, id_cajero[0])))
					db.insertar_registro(id_cajero_int, "camelBet", "carga", usuario, monto)
					# Seteo visualizacion de usuarios
					xpath = '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[1]/div/ul/li[1]/button'
					btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
                        lambda d: d.find_element(By.XPATH, xpath)).click()
					
					return True, informe
					break
				except Exception as err:
					print("ERROR INESPERADO. Linea 127", err)
					informe = f"*ERROR INESPERADO.* CARGA NO REALIZADA al usuario {usuario}.por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte.\n"
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
		print("ERROR. botCarga linea 140")
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.close()
		driverPlataforma.quit()
		return False, informe


def botDescarga(usuario, monto, nombre_cajero):
	try:
		# encuentra todos los elementos de la tabla usuarios
		xpathTablaUsuarios = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr'
		tablaUsuarios = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_elements(By.XPATH, xpathTablaUsuarios))
		x = 1
		for filaUsuarios in tablaUsuarios:
			xpathstring = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
			    str(x) + ']/td[1]'
			nombreUsuario = WebDriverWait(driverPlataforma, timeout=10).until(
			    lambda d: d.find_element(By.XPATH, xpathstring)).text
			if nombreUsuario == usuario:
				id_generico_usuario = "itemBlc__"+usuario
				print(f"ID generico usuario: {id_generico_usuario}")
				fichas = WebDriverWait(driverPlataforma, timeout=10).until(
				    lambda d: d.find_element(By.ID, id_generico_usuario)).text
				print(f"fichas que tiene el usuario {usuario}: {fichas}")
				# teniendo en cuenta que siempre va a haber decimales.. simplemente hago el split
				fichas_split1 = fichas.split(",")
				fichas_del_usuario = fichas_split1[0]
				# chequeo si existe un "." en la cantidad de fichas. Si existe, significa que tiene mas de 999 fichas. ej: 1.000 fichas
				punto = fichas.count(".")
				if punto == 1:
					fichas_split2 = fichas_split1[0].split(".")
					fichas_del_usuario = fichas_split2[0] + fichas_split2[1]
					print(fichas_del_usuario)
					if int(monto) > int(fichas_del_usuario):
						informe = f"*ERROR.* El usuario: {nombreUsuario} *no tiene* {monto} fichas en su cuenta. *Tiene* {fichas_del_usuario}"
						return True, informe
						break
				# una vez tengo separado el string de fichas obtenidos en el elemento "fichas". chequeo:
				if int(monto) > int(fichas_del_usuario):
					informe = f"*ERROR.* El usuario: {nombreUsuario} *no tiene* {monto} fichas en su cuenta. *Tiene* {fichas_del_usuario}"
					return True, informe
					break
				else:
					try:
						time.sleep(1)
						print("Usuario " + usuario + " encontrado.. Descargando fichas..")
						xpathDescarga = '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[2]/div[2]/div/div/p-table/div/div/div/div[2]/table/tbody/tr[' + \
						    str(x) + ']/td[3]/div/div[2]/div'
						botonDescarga = WebDriverWait(driverPlataforma, timeout=10).until(
						    lambda d: d.find_element(By.XPATH, xpathDescarga))
						botonDescarga.click()
						time.sleep(1)
						# input monto
						pyautogui.FAILSAFE = True
						#pgui_own.txt_monto()
						time.sleep(1)
						pyautogui.write(monto)
						time.sleep(1)
						btn_retirar = driverPlataforma.execute_script(
						    "return document.getElementsByClassName('btn btn-primary')[3];")
						driverPlataforma.execute_script("arguments[0].click();", btn_retirar)
						time.sleep(2)
						# confirmacion
						botonConfirmacion = WebDriverWait(driverPlataforma, timeout=10).until(
						    lambda d: d.find_element(By.CLASS_NAME, "swal2-confirm"))
						botonConfirmacion.click()
						time.sleep(2)
						print("DESCARGA REALIZADA EXITOSAMENTE.")
						informe = "*Descarga exitosa.* " + \
						    str(monto) + " al usuario " + nombreUsuario + "\n"


						# agrego la carga exitosa a la tabla registros de la base de datos
						id_cajero = db.select_id_cajero(nombre_cajero)
						# transofrmo id_cajero y id_plataforma de tupla a int
						id_cajero_int = (''.join(map(str, id_cajero[0])))
						db.insertar_registro(id_cajero_int, "camelBet", "descarga", usuario, monto)
						return True, informe
					except Exception as err:
						print("ERROR INESPERADO. DESCARGA NO REALIZADA.", err)
						informe = "*ERROR INESPERADO.* DESCARGA NO REALIZADA.\n"
						return True, informe
			else:
				if x == (len(tablaUsuarios)):
					informe = f"Bot reviso los {len(tablaUsuarios)} usuarios y no encontro el solicitado. es hora  de pasar de pagina."
					return False, informe
					break
			x = x+1
	except Exception as err:
		print("ERROR. botDescarga linea 212", err)
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.close()
		driverPlataforma.quit()
		return informe


def botNuevoAgente(admin, clave_admin, nombreNuevoUsuario, contrasenaNuevoUsuario):
	driverPlataforma, chequeo = get(admin, clave_admin)
	try:
		btn_nuevo_agente = WebDriverWait(driverPlataforma, timeout=10).until(lambda d: d.find_element(
		    By.XPATH, '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[1]/div[2]/div/div/button[1]')).click()
		time.sleep(3)
		botonsitoAgente = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_element(By.ID, "inlineRadio2")).click()
		agente_name = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_element(By.ID, "txt_createusr_name")).send_keys(nombreNuevoUsuario)
		agente_pass = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_element(By.ID, "txt_createusr_pass")).send_keys(contrasenaNuevoUsuario)
		user_mail = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_element(By.ID, "txt_create_email")).send_keys(random_mail.init())
		btn_submit = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_element(By.ID, "btn_submit")).click()
		errormsj = WebDriverWait(driverPlataforma, timeout=15).until(
		    lambda d: d.find_elements(By.XPATH, '//*[@id="swal2-content"]/span'))
		if errormsj[0].text == "The username is already in use.":
			informe = f"El nombre de usuario '{nombreNuevoUsuario}' ya esta en uso.\n Por favor, vuelva a iniciar el comando."
		elif errormsj[0].text == "El nombre de usuario ya esta en uso.":
			informe = f"El nombre de usuario '{nombreNuevoUsuario}' ya esta en uso.\n Por favor, vuelva a iniciar el comando."
		else:
			informe = errormsj[0].text, "\n", f"*Nombre de usuario:* {nombreNuevoUsuario}\n *Contraseña:* {contrasenaNuevoUsuario} \n Debido al sistema de la plataforma, los porcentajes de comision debe agregarlos usted de manera manual."
		return informe
		driverPlataforma.close()
		driverPlataforma.quit()
	except Exception as err:
		print("ERROR DESCONOCIDO. PROBABLEMENTE INTERNET LENTO NO ENCUENTRA ELEMENTO. LINEA 236 bp04", err)
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.close()
		driverPlataforma.quit()
		return informe


def botNuevoJugador(admin, clave_admin, nombreNuevoUsuario, contrasenaNuevoUsuario):
	driverPlataforma, chequeo = get(admin, clave_admin)
	try:
		btn_nuevo_jugador = WebDriverWait(driverPlataforma, timeout=10).until(lambda d: d.find_element(
		    By.XPATH, '//*[@id="kt_wrapper"]/div[2]/div[1]/app-users-manage/div/div[2]/div/div/div[1]/div[2]/div/div/button[2]')).click()
		time.sleep(2)
		jugador_name = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_element(By.ID, "txt_createusr_name")).send_keys(nombreNuevoUsuario)
		time.sleep(2)
		jugador_pass = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_element(By.ID, "txt_createusr_pass")).send_keys(contrasenaNuevoUsuario)
		btn_submit = WebDriverWait(driverPlataforma, timeout=10).until(
		    lambda d: d.find_element(By.ID, "btn_submit")).click()
		time.sleep(2)
		errormsj = WebDriverWait(driverPlataforma, timeout=15).until(
		    lambda d: d.find_elements(By.XPATH, '//*[@id="swal2-content"]/span'))
		if errormsj[0].text == "The username is already in use.":
			informe = f"El nombre de usuario '{nombreNuevoUsuario}' ya esta en uso. \n Por favor, vuelva a iniciar el comando."
		elif errormsj[0].text == "El nombre de usuario ya esta en uso.":
			informe = f"El nombre de usuario '{nombreNuevoUsuario}' ya esta en uso. \n Por favor, vuelva a iniciar el comando."
		else:
			informe = errormsj[0].text, "\n", f"Nombre de usuario: {nombreNuevoUsuario}, Contraseña: {contrasenaNuevoUsuario}"
		return informe
		driverPlataforma.close()
		driverPlataforma.quit()
	except Exception as err:
		print("ERROR DESCONOCIDO. PROBABLEMENTE INTERNET LENTO NO ENCUENTRA ELEMENTO. LINEA 246 bp04", err)
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.close()
		driverPlataforma.quit()
		return informe


def cd_bot_plataforma(accion, admin, clave_admin, usuario, monto, nombre_cajero):
	global driverPlataforma
	driverPlataforma, chequeo = get(admin, clave_admin)
	acomodar()
	if accion == "CAR":
		bolean, informe = botCarga(usuario, monto, nombre_cajero)
	elif accion == "DES":
		bolean, informe = botDescarga(usuario, monto, nombre_cajero)
	try:
		num = 3
		while bolean == False:
			print(num, "NUM...")
			time.sleep(1)
			k = cambio_de_pagina(num)
			num = num + 1
			if k == True:
				time.sleep(1)
				if accion == "CAR":
					print("llamando bot carga... linea 218")
					bolean, informe = botCarga(usuario, monto, nombre_cajero)
				elif accion == "DES":
					print("llamando bot descarga... linea 221")
					bolean, informe = botDescarga(usuario, monto, nombre_cajero)
			else:
				informe = f"*Usuario inexistente.* El usuario {usuario}, no existe en tu lista."
				break
	except Exception as err:
		informe = f"*Usuario inexistente.* El usuario {usuario}, no existe en tu lista."
	driverPlataforma.quit()
	return informe


def cargar(usuarios, montos, nombre_cajero):
	x = 0
	informes = []
	users_no_cargados = []
	montos_no_cargados = []

	for usuario in usuarios:
		chequeo, informe = botCarga(usuario, montos[x], nombre_cajero)
		if chequeo == True:
			informes.append(informe)
		else:
			users_no_cargados.append(usuario)
			montos_no_cargados.append(montos[x])
		x = x + 1
	return informes, users_no_cargados, montos_no_cargados

def descargar(usuarios, montos, nombre_cajero):
	x = 0
	informes = []
	users_no_cargados = []
	montos_no_cargados = []

	for usuario in usuarios:
		chequeo, informe = botDescarga(usuario, montos[x], nombre_cajero)
		if chequeo == True:
			informes.append(informe)
		else:
			users_no_cargados.append(usuario)
			montos_no_cargados.append(montos[x])
		x = x + 1
	return informes, users_no_cargados, montos_no_cargados


def multiple_carga(admin, clave_admin, usuarios, montos, cant_users, nombre_cajero):
	global driverPlataforma
	driverPlataforma, chequeo = get(admin, clave_admin)
	acomodar()
	informes_final = []
	num = 2
	informes, users_no_cargados, montos_no_cargados = cargar(usuarios, montos, nombre_cajero)
	informes_final.append("".join(informes))

	if len(users_no_cargados) != 0:
		k = cambio_de_pagina(num)
		while k == True:
			informes, users_no_cargados, montos_no_cargados = cargar(users_no_cargados,montos_no_cargados, nombre_cajero)
			informe_temp = [str(x) for sublist in informes for x in sublist]
			informes_final.extend(informe_temp)
			num = num +1
			k = cambio_de_pagina(num)
		if len(users_no_cargados) != 0:
			users_no_cargados_str = ", ".join(str(x) for x in users_no_cargados)
			informes_final.append(f"El/Los usuarios: *{users_no_cargados_str}*, no estan en la lista. Usuario/s inexistente.")
			driverPlataforma.close()
			driverPlataforma.quit()
		return "".join(informes_final)
	else:
		informes_final = [''.join(x) for x in informes_final]
		driverPlataforma.close()
		driverPlataforma.quit()
		return "".join(informes_final)



def multiple_descarga(admin, clave_admin, usuarios, montos, cant_users, nombre_cajero):
	global driverPlataforma
	driverPlataforma, chequeo = get(admin, clave_admin)
	acomodar()
	informes_final = []
	num = 2
	informes, users_no_cargados, montos_no_cargados = descargar(usuarios, montos, nombre_cajero)
	informes_final.append("".join(informes))

	if len(users_no_cargados) != 0:
		k = cambio_de_pagina(num)
		while k == True:
			informes, users_no_cargados, montos_no_cargados = descargar(users_no_cargados,montos_no_cargados, nombre_cajero)
			informe_temp = [str(x) for sublist in informes for x in sublist]
			informes_final.extend(informe_temp)
			num = num +1
			k = cambio_de_pagina(num)
		if len(users_no_cargados) != 0:
			users_no_cargados_str = ", ".join(str(x) for x in users_no_cargados)
			informes_final.append(f"El/Los usuarios: *{users_no_cargados_str}*, no estan en la lista. Usuario/s inexistente.")
			driverPlataforma.close()
			driverPlataforma.quit()
		return "".join(informes_final)
	else:
		informes_final = [''.join(x) for x in informes_final]
		driverPlataforma.close()
		driverPlataforma.quit()
		return "".join(informes_final)
	



