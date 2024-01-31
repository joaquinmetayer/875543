from selenium import webdriver
from selenium.webdriver import ActionChains
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

import db
import descomprimir


def get(admin, clave_admin):
	try:
		#iniciacion plataforma
		s = Service('./driver/chromedriver.exe')
		options = Options()
		driverPlataforma = webdriver.Chrome(service=s, options=options)
		#driverPlataforma.get("https://admin.jugaygana.online/login.php")
		driverPlataforma.get("https://admin.jugalodos.com")
		driverPlataforma.maximize_window()
	except Exception as err:
		informe = "*ERROR*. Problemas con conexión de red. Vuelva a intentarlo, si el problema persiste. Comunicarse con soporte con el codigo - BP01-L19"
		return driverPlataforma, ""

	#logeo
	try:
		user = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "user")).send_keys(admin)
		time.sleep(1)
		passwd = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "passwd")).send_keys(clave_admin)
		time.sleep(1)
		submit = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "dologin")).click()
		time.sleep(1)
		elem_chequeo_ignorar = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, '//*[@id="userDropdown"]/span'))
		chequeo = True
	except Exception as err:
		print("LINEA 23 funcion get()", err)
		chequeo = False
		driverPlataforma.close()
		driverPlataforma.quit()
	return driverPlataforma, chequeo

def acomodar():
	time.sleep(1)
	try:
		areaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, '//*[@id="sidemenu_global_ul"]/li[2]/a')).click()
		time.sleep(2)
		pyautogui.hotkey("ctrl", "-")
		pyautogui.hotkey("ctrl", "-")
		pyautogui.hotkey("ctrl", "-")
		pyautogui.hotkey("ctrl", "-")
		pyautogui.hotkey("ctrl", "-")
		# Selecciona el dropdown 50 con pyautogui
		dp50 = driverPlataforma.execute_script("return document.getElementsByClassName('filtrable')[2];")
		driverPlataforma.execute_script("arguments[0].click();", dp50)
		time.sleep(2)
	except Exception as err:
		print("ERROR. acomodar() linea 45", err)
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.quit()
		return informe	

def conteo_fichas(admin, clave_admin):
	try:
		driverPlataforma, nn = get(admin, clave_admin)
		time.sleep(1)
		fichas1 = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, '/html/body/header/nav/ul/li[1]/a/span')).text
		fichas = fichas1.split()
		fichas = fichas[0]
		return fichas
	except Exception as err:
		print("ERROR. conteo_fichas() linea 59, err")
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.quit()
		return informe	


def cambio_de_pagina(num):
	y = num
	try:
		elem_paginacion = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, '//*[@id="users_paginate"]/ul/li['+ str(y) + ']/a')).click()
		return True
	except Exception as err:
		print("Usuario no existe. No hay más paginas, y no se encontro usuario con ese nombre. Linea 54", err)
		return False

def botCarga(usuario, monto, nombre_cajero):
	try:
		# Chequeo cantidad defichas en panel, con cantidad de fichas solicitadas para cargar
		fichas = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, '/html/body/header/nav/ul/li[1]/a/span')).text
		# teniendo en cuenta que en juga en vivo siempre va a haber decimales.. no creo un "if" preguntando si existe "," simplemente hago el split
		fichas_split1 = fichas.split(",")
		fichas_en_panel = fichas_split1[0]
		# chequeo si existe un "." en la cantidad de fichas. Si existe, significa que tiene en panel mas de 999 fichas. ej: 1.000 fichas
		punto = fichas.count(".")
		# si no existe "." sigfnicia que tiene 999fichas o menos, entonces "fichas_en_panel" va a ser igual a "fichas_split1[0]"
		# si existe "." significa que tiene 1.000 o más fichas. En este caso hago split eliminando el "." y vuelvo a juntar las partes sumandolas (recordar que estoy manipulando un STRING)
		if punto == 1:
			fichas_split2 = fichas_split1[0].split(".")
			fichas_en_panel = fichas_split2[0] + fichas_split2[1]
			# luego de hacer toda la manipulacion de datos, eliminar "," y "." ahora puedo pasar el string a INT sin problemas..
			if int(monto) > int(fichas_en_panel):
				informe = f"*ERROR.* Cantidad de fichas en panel insuficientes.\n *Fichas en panel*: {fichas} \n *Monto a cargar:* {monto}\n Solicite más fichas a su superior, y vuelva a ejectuar el comando."
				return True, informe
		elif punto == 2:
			fichas_split2 = fichas_split1[0].split(".")
			fichas_en_panel = fichas_split2[0] + fichas_split2[1] + fichas_split2[2]
            # luego de hacer toda la manipulacion de datos, eliminar "." ahora puedo pasar el string a INT sin problemas..
			if int(monto) > int(fichas_en_panel):
				informe = f"*ERROR.* Cantidad de fichas en panel insuficientes.\n *Fichas en panel*: {fichas} \n *Monto a cargar:* {monto} al usuario {usuario}\n Solicite más fichas a su superior, y vuelva a ejectuar el comando.\n"
				return True, informe
		elif punto == 3:
			fichas_split2 = fichas_split1[0].split(".")
			fichas_en_panel = fichas_split2[0] + fichas_split2[1] + fichas_split2[2] + fichas_split2[3]
			# luego de hacer toda la manipulacion de datos, eliminar "." ahora puedo pasar el string a INT sin problemas..
			if int(monto) > int(fichas_en_panel):
				informe = f"*ERROR.* Cantidad de fichas en panel insuficientes.\n *Fichas en panel*: {fichas} \n *Monto a cargar:* {monto} al usuario {usuario}\n Solicite más fichas a su superior, y vuelva a ejectuar el comando.\n"
				return True, informe
		else:
			print(f"Entrando a comparar monto: {monto} con fichas: {fichas}")
			if int(monto) > int(fichas_en_panel):
				informe = f"*ERROR.* Cantidad de fichas en panel insuficientes.\n *Fichas en panel*: {fichas} \n *Monto a cargar:* {monto} al usuario {usuario}\n Solicite más fichas a su superior, y vuelva a ejectuar el comando.\n"
				return True, informe
			# busco el usuario por barra de busqueda
			xpath = '/html/body/main/div[1]/section/div/div[2]/div[1]/div/div/div[1]/div[1]/div/input'
			barraDeBusqueda = WebDriverWait(driverPlataforma, timeout=15).until(
				lambda d: d.find_element(By.XPATH, xpath))
			barraDeBusqueda.send_keys(usuario)
			time.sleep(1)
			xpath = '/html/body/main/div[1]/section/div/div[2]/div[1]/div/div/div[1]/div[2]/div/button'
			barraDebusquedaClick = WebDriverWait(driverPlataforma, timeout=15).until(
				lambda d: d.find_element(By.XPATH, xpath)).click()
			time.sleep(5)
			# encuentra todos los elementos de la tabla usuarios        
			try:
				xpath = '//*[@id="users"]/tbody/tr'
				tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
					lambda d: d.find_elements(By.XPATH, xpath))
				time.sleep(2)
			except Exception as err:
				print(f"Error cargando fichas al usuario: {usuario}. Chequear que el usuario no este bloqueado")
				informe = f"Error carga no realizada. Chequear que el usuario *{usuario}* no este bloqueado. Y volver a ejectuar comando de carga."
				#  seteo visualizacion de usuarios
				xpath = '/html/body/header/div[1]/ul/li[2]/ul/li[2]/a'
				btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
					lambda d: d.find_element(By.XPATH, xpath)).click()
				return True, informe


			x = 1
			for filaUsuarios in tablaUsuarios:
					xpathstring = '//*[@id="users"]/tbody/tr[' + str(x) + ']/td[1]'
					nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpathstring)).text
					if nombreUsuario == usuario:
						try:
							print("Usuario " + usuario + " encontrado.. Cargando fichas..")
							xpathCarga = '//*[@id="users"]/tbody/tr['+ str(x) + ']/td[3]/a[1]'
							botonCarga = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpathCarga)).click()
							time.sleep(2)
							inputCarga = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "ModalCreditAmount")).send_keys(monto)
							time.sleep(1)
							botonAceptar = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "ModalCreditSubmit")).click()
							print("CARGA REALIZADA EXITOSAMENTE.")
							informe = "*Carga exitosa.* " + str(monto) + " al usuario " + nombreUsuario + "\n"

							# agrego la carga exitosa a la tabla registros de la base de datos
							id_cajero = db.select_id_cajero(nombre_cajero)
							# transofrmo id_cajero y id_plataforma de tupla a int
							id_cajero_int = (''.join(map(str, id_cajero[0])))
							db.insertar_registro(id_cajero_int, "jugalo", "carga", usuario, monto)
							#  seteo visualizacion de usuarios
							xpath = '/html/body/header/div[1]/ul/li[2]/ul/li[2]/a'
							btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
								lambda d: d.find_element(By.XPATH, xpath)).click()
							return True, informe
							break
						except Exception as err:
							print("ERROR INESPERADO.", err, "Linea 51")
							informe = "*ERROR INESPERADO.* CARGA NO REALIZADA."
							#  seteo visualizacion de usuarios
							xpath = '/html/body/header/div[1]/ul/li[2]/ul/li[2]/a'
							btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
								lambda d: d.find_element(By.XPATH, xpath)).click()
							return True, informe
					else:
						if x == (len(tablaUsuarios)):
							informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
							return False, informe
							break
						
					x=x+1
	except Exception as err:
		print("ERROR. botCarga linea 130", err)
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.quit()
		return informe		

def botDescarga(usuario, monto, nombre_cajero):
	try:
		# busco el usuario por barra de busqueda
		xpath = '/html/body/main/div[1]/section/div/div[2]/div[1]/div/div/div[1]/div[1]/div/input'
		barraDeBusqueda = WebDriverWait(driverPlataforma, timeout=15).until(
			lambda d: d.find_element(By.XPATH, xpath))
		barraDeBusqueda.send_keys(usuario)
		time.sleep(1)

		xpath = '/html/body/main/div[1]/section/div/div[2]/div[1]/div/div/div[1]/div[2]/div/button'
		barraDebusquedaClick = WebDriverWait(driverPlataforma, timeout=15).until(
			lambda d: d.find_element(By.XPATH, xpath)).click()
		time.sleep(5)

		# encuentra todos los elementos de la tabla usuarios
		try:
			xpath = '//*[@id="users"]/tbody/tr'
			tablaUsuarios = WebDriverWait(driverPlataforma, timeout=15).until(
				lambda d: d.find_elements(By.XPATH, xpath))
			time.sleep(2)
		except Exception as err:
			print(f"Error descargando fichas al usuario: {usuario}. Chequear que el usuario no este bloqueado")
			informe = f"Error descarga no realizada. Chequear que el usuario *{usuario}* no este bloqueado."
			#  seteo visualizacion de usuarios
			xpath = '/html/body/header/div[1]/ul/li[2]/ul/li[2]/a'
			btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
				lambda d: d.find_element(By.XPATH, xpath)).click()
			return True, informe

		x = 1
		for filaUsuarios in tablaUsuarios:
			xpathstring = '//*[@id="users"]/tbody/tr[' + str(x) + ']/td[1]'
			nombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpathstring)).text
			if nombreUsuario == usuario:
				fichas = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, '//*[@id="users"]/tbody/tr['+ str(x) + ']/td[2]')).text
				# teniendo en cuenta que en juga en vivo siempre va a haber decimales.. no creo un "if" preguntando si existe "," simplemente hago el split
				fichas_split1 = fichas.split(",")
				fichas_del_usuario = fichas_split1[0]
				# chequeo si existe un "." en la cantidad de fichas. Si existe, significa que tiene mas de 999 fichas. ej: 1.000 fichas
				punto = fichas.count(".")
				if punto == 1:
					fichas_split2 = fichas_split1[0].split(".")
					fichas_del_usuario = fichas_split2[0] + fichas_split2[1]
				elif punto == 2:
					fichas_split2 = fichas_split1[0].split(".")
					fichas_del_usuario = fichas_split2[0] + fichas_split2[1] + fichas_split2[2]
					# luego de hacer toda la manipulacion de datos, eliminar "." ahora puedo pasar el string a INT sin problemas..
				elif punto == 3:
					fichas_split2 = fichas_split1[0].split(".")
					fichas_del_usuario = fichas_split2[0] + fichas_split2[1] + fichas_split2[2] + fichas_split2[3]
					# luego de hacer toda la manipulacion de datos, eliminar "." ahora puedo pasar el string a INT sin problemas..

				# una vez tengo separado el string de fichas obtenidos en el elemento "fichas"
				# una vez lo haya dividido de sus decimales con "fichas_split1"
				# y una vez haya divido de su "." y vuelto a unir sus string sin el "." mediante "fichas_del_usuario"(dentro del if)
				# habiendo pasado todo esos parametros, estoy en condiciones de chequear si el monto es > que fichas del usuario (transformandolo a int previamente)
				if int(monto) > int(fichas_del_usuario):
					informe = f"*ERROR.* El usuario: {nombreUsuario} *no tiene* {monto} fichas en su cuenta. *Tiene* {fichas_del_usuario}"
					#  seteo visualizacion de usuarios
					xpath = '/html/body/header/div[1]/ul/li[2]/ul/li[2]/a'
					btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
						lambda d: d.find_element(By.XPATH, xpath)).click()
					return True, informe
					break
				else:	
					try:
						print("Usuario " + usuario + " encontrado.. Descargando fichas..")
						xpathDescarga = '//*[@id="users"]/tbody/tr['+ str(x) + ']/td[3]/a[2]'
						botonDescarga = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.XPATH, xpathDescarga)).click()
						time.sleep(2)
			            #carga100 descolorea la zona azul (para evitar error por not find element)- es necesario?????
						inputDescarga = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "ModalCreditAmount")).send_keys(monto)
						time.sleep(1)
						botonAceptar = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "ModalCreditSubmit")).click()
						print("DESCARGA REALIZADA EXITOSAMENTE.")
						informe = "*Descarga exitosa.* " + str(monto) + " al usuario " + nombreUsuario + "\n"

						# agrego la descarga exitosa a la tabla registros de la base de datos
						id_cajero = db.select_id_cajero(nombre_cajero)
						# transofrmo id_cajero y id_plataforma de tupla a int
						id_cajero_int = (''.join(map(str, id_cajero[0])))
						db.insertar_registro(id_cajero_int, "jugalo", "descarga", usuario, monto)
						#  seteo visualizacion de usuarios
						xpath = '/html/body/header/div[1]/ul/li[2]/ul/li[2]/a'
						btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
							lambda d: d.find_element(By.XPATH, xpath)).click()
						return True, informe
						break
					except Exception as err:
						print("ERROR INESPERADO. DESCARGA NO REALIZADA.", err)
						informe = "*ERROR INESPERADO.* DESCARGA NO REALIZADA."
						#  seteo visualizacion de usuarios
						xpath = '/html/body/header/div[1]/ul/li[2]/ul/li[2]/a'
						btnTodos = WebDriverWait(driverPlataforma, timeout=15).until(
							lambda d: d.find_element(By.XPATH, xpath)).click()
						return True, informe
			else:
				if x == (len(tablaUsuarios)):
					informe = "Bot reviso 100 usuarios y no encontro el solicitado. es hora  de pasar de pagina."
					return False, informe
					break
			x=x+1
	except Exception as err:
		print("ERROR. botDescarga linea 180", err)
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.quit()
		return informe	
				
def botNuevoJugador(admin, clave_admin, nombreNuevoUsuario, contrasenaNuevoUsuario):
	driverPlataforma, chequeo = get(admin, clave_admin)
	try:
		btnNuevoJugador = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "NewPlayerButton")).click()
		time.sleep(1)
		inputNombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "NewUserPlayerUsername")).send_keys(nombreNuevoUsuario)
		time.sleep(1)
		inputPassUsuario = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "NewUserPlayerPassword")).send_keys(contrasenaNuevoUsuario)
		time.sleep(1)
		submit = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "ModalNewUserPlayerSubmit")).click()
		time.sleep(2)
		errormsj = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_elements(By.ID, "NewUserPlayerError"))
		if not errormsj[0].text:
			informe = "*JUGADOR CREADO CORRECTAMENTE.*\n Nombre de usuario: " + nombreNuevoUsuario + "\n Contraseña: " + contrasenaNuevoUsuario
		else:
			informe = "*ERROR.* " + errormsj[0].text + "\n Por favor, vuelva a iniciar el comando."
		time.sleep(1)
		driverPlataforma.quit()
		return informe
	except Exception as err:
		print("ERROR DESCONOCIDO. PROBABLEMENTE INTERNET LENTO NO ENCUENTRA ELEMENTO. LINEA 204", err)
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.quit()
		return informe

def botNuevoAgente(admin, clave_admin, nombreNuevoUsuario, contrasenaNuevoUsuario, comision1deporte, comision2casino):
	driverPlataforma, chequeo = get(admin, clave_admin)
	try:
		btnNuevoAgente = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "NewAffiliateButton")).click()
		time.sleep(1)
		inputNombreUsuario = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "NewUserAffiliateUsername")).send_keys(nombreNuevoUsuario)
		time.sleep(1)
		inputPassUsuario = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "NewUserAffiliatePassword")).send_keys(contrasenaNuevoUsuario)
		time.sleep(1)
		submit = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "ModalNewUserAffiliateSubmit")).click()
		time.sleep(1)
		comisionDeporte = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "SelectAllCommissions2")).send_keys(comision1deporte)#comision1deporte
		comisionCasino = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "SelectAllCommissions3")).send_keys(comision2casino)#comision2deporte
		submit = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_element(By.ID, "ModalNewUserAffiliateSubmit")).click()
		time.sleep(2)
		errormsj = WebDriverWait(driverPlataforma, timeout=15).until(lambda d: d.find_elements(By.ID, "NewUserAffiliateError"))
		if not errormsj[0].text:
			informe = f"*AGENTE CREADO CORRECTAMENTE*\n Nombre de usuario: {nombreNuevoUsuario}\n Contraseña: {contrasenaNuevoUsuario}\n Comision deportes: {comision1deporte}%\n Comision casino: {comision2casino}%"		
		else:
			informe = "*ERROR.* " + errormsj[0].text + "\n Por favor, vuelva a iniciar el comando."
		time.sleep(1)
		driverPlataforma.quit()
		return informe
	except Exception as err:
		print("ERROR DESCONOCIDO. PROBABLEMENTE INTERNET LENTO NO ENCUENTRA ELEMENTO. LINEA 233", err)
		informe = "*ERROR DESCONOCIDO*. por favor, envie comando nuevamente. Si el error persiste, comunicarse con soporte."
		driverPlataforma.quit()
		return informe

def cd_bot_plataforma(accion,admin,clave_admin,usuario,monto, nombre_cajero):
	global driverPlataforma
	driverPlataforma, chequeo = get(admin,clave_admin)
	acomodar()
	if accion == "CAR":
		bolean, informe = botCarga(usuario,monto, nombre_cajero)
	elif accion == "DES":
		bolean, informe = botDescarga(usuario,monto, nombre_cajero)
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
					bolean, informe = botCarga(usuario,monto, nombre_cajero)
				elif accion == "DES":
					print("llamando bot descarga... linea 221")
					bolean, informe = botDescarga(usuario,monto, nombre_cajero)
			else:
				informe = f"*Usuario inexistente.*\n El usuario {usuario}, no existe en tu lista."
				break
	except Exception as err:
		informe = f"*Usuario inexistente.*\n El usuario {usuario}, no existe en tu lista."
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
	
