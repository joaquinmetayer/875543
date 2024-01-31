from ast import Str
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from unicodedata import normalize
from keepSession import driver
import time
import re
import sys
import pyautogui

import bp01
import bp02
import bp03
import bp04
import db
import msjs
import pass_generator
import descomprimir
import random_mail

def buscar_chats():
	print("BUSCANDO CHATS..")
	chats = WebDriverWait(driver, timeout=15).until(lambda d: d.find_elements(By.CLASS_NAME, "_8nE1Y"))
	for chat in chats:
		print("DETECTANDO MENSAJES SIN LEER..")
		chats_nuevos = chat.find_elements(By.CLASS_NAME, "_2H6nH")
		if len(chats_nuevos) == 0:
			print("NO HAY MENSAJES SIN LEER")
			continue
        #si continua es porque existe un mensaje sin leer    
		print("@@@@@@@MENSAJE SIN LEER")
        #localiza el elemento donde se encuentra el nombre del chat sin leer
		chat_nombre = chat.find_element(By.CLASS_NAME, "_21S-L")
		nombre = chat_nombre.text.strip()
		print("IDENTIFICANDO CONTACTO..")
		with open("./resource/contactos_autorizados.txt", mode='r', encoding='utf-8') as archivo:
			contactos = [linea.strip() for linea in archivo]
			if nombre not in contactos:
				print(nombre, " CONTACTO NO AUTORIZADO.")
				continue
		print(nombre, " AUTORIZADO PARA SER ATENDIDO POR BOT")
		usuario = nombre
		chat.click()
		time.sleep(1)
		return True
	return False

def identificar_comando(res_automatica):
	#llegada esta funcion, ya esta dentro de un chat sin leer, localiza todos los mensajes del chat.
	element_box_message = WebDriverWait(driver, timeout=15).until(lambda d: d.find_elements(By.CLASS_NAME, "_2AOIt"))
	posicion = len(element_box_message) -1
    #selecciona con la posicion, el ultimo mensaje de la conversacion(mensaje recibido)
    #y localiza el texto de ese ultimo mensaje. es decir, localiza el comando
	element_message = element_box_message[posicion].find_elements(By.CLASS_NAME, "_21Ahp")
	comando = element_message[0].text.strip()
	print("COMANDO RECIBIDO :", comando)
	# respuesta automatica
	print("Ejecutando respuesta automatica..")
	xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
	chatbox = WebDriverWait(driver, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath))
	chatbox.send_keys(res_automatica)
	chatbox.send_keys(Keys.ENTER)
	return normalizar(comando)

def normalizar(comando: str):
    # -> NFD y eliminar diacríticos
	comando = re.sub(
		r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
		normalize( "NFD", comando), 0, re.I
	)
    # -> NFC
	return normalize( 'NFC', comando)

def enviar_mensaje(mensaje):
	#enviar un mensaje si y solo si se esta dentro del chat..
	xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
	chatbox = WebDriverWait(driver, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath))
	chatbox.send_keys(mensaje)
	chatbox.send_keys(Keys.ENTER)

def leer_ultimo_mensaje():
	#lee el ultimo mensaje dentro del chat..
	#tomo el ultimo mensaje del chat
	element_box_message = WebDriverWait(driver, timeout=15).until(lambda d: d.find_elements(By.CLASS_NAME, "_2AOIt"))
	posicion = len(element_box_message) -1
	element_message = element_box_message[posicion].find_elements(By.CLASS_NAME, "_21Ahp")
	ultimo_mensaje = element_message[0].text.strip()
	return ultimo_mensaje

def setear_bot():
		xpath = '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]'
		barraDeBusqueda = WebDriverWait(driver, timeout=15).until(
			lambda d: d.find_element(By.XPATH, xpath))
		barraDeBusqueda.send_keys("Leem")
		time.sleep(1)
		barraDeBusqueda.send_keys(Keys.ENTER)
		time.sleep(1)
		cancel = WebDriverWait(driver, timeout=15).until(
			lambda d: d.find_element(By.CLASS_NAME, "-Jnba"))
		cancel.click()

def busca_nombre_cajero():
	nombre_elemento = WebDriverWait(driver, timeout=15).until(lambda d: d.find_element(By.CLASS_NAME, "_3W2ap"))
	nombre_cajero = nombre_elemento.text
	print(nombre_cajero)
	return nombre_cajero

def ejecutar_comando(comando, nombre_cajero):
	print("EJECUTANDO COMANDO..")
	if "INFO" in comando:
		informe = msjs.cmd_info()

	elif "EJEMPLOS" in comando:
		informe = msjs.cmd_ejemplos()

	elif "PLATAFORMAS" in comando:
		informe = msjs.cmd_plataformas()

	elif "FICHAS" in comando:
		comandoSplit = comando.split()
		if len(comandoSplit) != 2:
			informe = msjs.err_cmd_incorrecto("FICHAS")
		else:
			if comandoSplit[1] == "01":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero, comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp01.conteo_fichas(admin[0], clave_admin[0])
					informe = f"*Fichas en panel:* {informe}"
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			elif comandoSplit[1] == "02":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp02.conteo_fichas(admin[0], clave_admin[0])
					informe = f"*Fichas en panel:* {informe}"
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			elif comandoSplit[1] == "03":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp03.conteo_fichas(admin[0], clave_admin[0])
					informe = f"*Fichas en panel:* {informe}"
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			elif comandoSplit[1] == "04":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp04.conteo_fichas(admin[0], clave_admin[0])
					informe = f"*Fichas en panel:* {informe}"
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			else:
				informe = msjs.err_cmd_incorrecto("FICHAS")

	elif "MULTIPLE" in comando:
		print("COMANDO MULTIPLE..")

		def cod_plataforma():
			codigo_plataf = leer_ultimo_mensaje()
			count = 0
			while codigo_plataf == "Enviame codigo de plataforma":
				codigo_plataf = leer_ultimo_mensaje()
				count = count + 1
				if count > 1000:
					codigo_plataf = 999
					break
			return codigo_plataf

		def chequeo_numero_de_usuarios_carga():
			cantidad_usuarios = leer_ultimo_mensaje()
			#hago chequeo del ultimo mensaje del chat
			count = 0
			while cantidad_usuarios == msjs.cmd_multiple("CARGAS"):
				cantidad_usuarios = leer_ultimo_mensaje()
				count = count + 1
				if count > 1000:
					cantidad_usuarios = None
					break
			return cantidad_usuarios

		def chequeo_numero_de_usuarios_descarga():
			cantidad_usuarios = leer_ultimo_mensaje()
			#hago chequeo del ultimo mensaje del chat
			count = 0
			while cantidad_usuarios == msjs.cmd_multiple("DESCARGAS"):
				cantidad_usuarios = leer_ultimo_mensaje()
				count = count + 1
				if count > 2500:
					cantidad_usuarios = None
					break
			return cantidad_usuarios

		def chequeo_usuarios_y_montos(cantidad_usuarios):
			usuarios_montos = leer_ultimo_mensaje()
			#hago chequeo del ultimo mensaje del chat
			count = 0
			while usuarios_montos == msjs.usuarios_multiple(cantidad_usuarios):
				usuarios_montos = leer_ultimo_mensaje()
				count = count + 1
				if count > 1000:
					usuarios_montos = None
					break
			return usuarios_montos

		def confirmacion(usuarios_montos, codigo_plataf):
			respuesta = leer_ultimo_mensaje()
			count = 0
			while respuesta == "Es correcto? (SI o NO)":
				respuesta = leer_ultimo_mensaje()
				count = count + 1
				if count > 2000:
					respuesta = None
					break
			return respuesta

		def insertar_en_registros(nombre_cajero, usuarios, montos, plataforma):
			x = 0
			for i in informe:
				if "Carga exitosa" in i:
					id_cajero = db.select_id_cajero(nombre_cajero)
					id_plataforma = db.select_id_plataforma("camelBet")
					# transofrmo id_cajero y id_plataforma de tupla a int
					id_cajero_int = (''.join(map(str, id_cajero[0])))
					id_plataforma_int = (''.join(map(str, id_plataforma[0])))
					db.insertar_registro(id_cajero_int, id_plataforma_int, "carga", usuarios[x], montos[x])
					x = x + 1
				else:
					x = x + 1
					continue

		comandoSplit = comando.split()
		if len(comandoSplit) != 2:
			informe = msjs.err_cmd_incorrecto("ACCION MULTIPLE")
		else:
			enviar_mensaje("Enviame codigo de plataforma")
			codigo_plataf = cod_plataforma()

			print(codigo_plataf)
			if codigo_plataf != "01" and codigo_plataf != "02" and codigo_plataf != "03" and codigo_plataf != "04":
				print("CODIGO PLATAFORMA ES DISTINTO A 01 02 03 y 04")
				informe = msjs.err_cod_plataforma()
			else:	
				if comandoSplit[1] == "CAR":
					enviar_mensaje(msjs.cmd_multiple("CARGAS"))
					cantidad_usuarios = chequeo_numero_de_usuarios_carga()
					if cantidad_usuarios is None:
						informe = "Tiempo de espera de confirmación terminado. Por favor, si desea las cargas, vuelva a iniciar el comando."
						return informe
					try:
						if int(cantidad_usuarios) >= 11:
							informe = "*ERROR*. Por el momento, el numero maximo de usuarios multiples es 10. Por favor, vuelva a iniciar el comando."
							return informe
					except Exception as err:
						if len(cantidad_usuarios) > 2:
							informe = "*ERROR*. la cantidad de usuarios debe ser un numero de 2 a 10. Por favor, vuelva a iniciar el comando."
					else:
						enviar_mensaje(msjs.usuarios_multiple(cantidad_usuarios))
						usuarios_montos = chequeo_usuarios_y_montos(cantidad_usuarios)
						if usuarios_montos == None:
							informe = "Tiempo de espera de confirmación terminado. Por favor, si desea las cargas, vuelva a iniciar el comando."
							return informe

						chequeo = int(cantidad_usuarios) * 2
						data = usuarios_montos.split()

						if len(data) != chequeo:
							ejemplo = "Ejemplo, para 10 usuarios, 20 campos. Usuario1 monto1 usuario2 monto2 usuario3 monto3 ...... usuario10 monto10"
								
							informe = f"*ERROR*. Para accion multiple a {cantidad_usuarios} usuarios. Necesito {chequeo} campos. Cada usuario, con su monto. \n {ejemplo}.  Por favor, vuelva a iniciar el comando."
						else:	
							enviar_mensaje(msjs.confirmacion(usuarios_montos, codigo_plataf))
							respuesta = confirmacion(usuarios_montos, codigo_plataf)
							if respuesta == "SI":
								enviar_mensaje("*...Ejecutando mensaje...*")
								if codigo_plataf == "01":
									admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,"01")
									if admin and clave_admin != None:
										data_ordenada = descomprimir.main(usuarios_montos, cantidad_usuarios, codigo_plataf)
										usuarios, montos = descomprimir.descomprimir_data(data_ordenada, cantidad_usuarios, codigo_plataf)
										informe = bp01.multiple_carga(admin[0], clave_admin[0],usuarios, montos, cantidad_usuarios, nombre_cajero)
									else:
										informe = msjs.err_cuenta_plataforma("01")
										
								elif codigo_plataf == "02":
									admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,"02")
									if admin and clave_admin != None:
										data_ordenada = descomprimir.main(usuarios_montos, cantidad_usuarios, codigo_plataf)
										usuarios, montos = descomprimir.descomprimir_data(data_ordenada, cantidad_usuarios, codigo_plataf)
										informe = bp02.multiple_carga(admin[0], clave_admin[0],usuarios,montos, cantidad_usuarios, nombre_cajero)
									else:
										informe = msjs.err_cuenta_plataforma("02")	
										
								elif codigo_plataf == "03":
									admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,"03")
									if admin and clave_admin != None:
										data_ordenada = descomprimir.main(usuarios_montos, cantidad_usuarios, codigo_plataf)
										usuarios, montos = descomprimir.descomprimir_data(data_ordenada, cantidad_usuarios, codigo_plataf)
										informe = bp03.multiple_carga(admin[0], clave_admin[0],usuarios, montos, cantidad_usuarios, nombre_cajero)
									else:
										informe = msjs.err_cuenta_plataforma("03")
										
								elif codigo_plataf == "04":
									admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,"04")
									if admin and clave_admin != None:
										data_ordenada = descomprimir.main(usuarios_montos, cantidad_usuarios, codigo_plataf)
										usuarios, montos = descomprimir.descomprimir_data(data_ordenada, cantidad_usuarios, codigo_plataf)
										informe = bp04.multiple_carga(admin[0], clave_admin[0],usuarios, montos, cantidad_usuarios,nombre_cajero)
									else:
										informe = msjs.err_cuenta_plataforma("04")
										
							elif respuesta == "NO":
								informe = "Entiendo. Por favor inicie nuevamente el comando MULTIPLE CAR con los usuarios y montos correspondientes"
							elif respuesta == None:
								informe = "Tiempo de espera de confirmación terminado. Por favor, si desea las cargas, vuelva a iniciar el comando."
							else:
								informe = "Confirmacion incorrecta. Por favor, vuelva a iniciar comando y confirme con SI o NO."

				elif comandoSplit[1] == "DES":
					enviar_mensaje(msjs.cmd_multiple("DESCARGAS"))
					cantidad_usuarios = chequeo_numero_de_usuarios_descarga()
					if cantidad_usuarios is None:
						informe = "Tiempo de espera de confirmación terminado. Por favor, si desea las descargas, vuelva a iniciar el comando."
						return informe
						
					if int(cantidad_usuarios) >= 11:
						informe = "*ERROR*. Por el momento, el numero maximo de usuarios multiples es 10."
						return informe
					elif codigo_plataf == "04":
						informe = ("Estoy teniendo problemas con las DESCARGAS en la plataforma 04. Por favor, por el momento, debe realizarlas de forma manual.")
						return informe
					else:
						enviar_mensaje(msjs.usuarios_multiple(cantidad_usuarios))
						usuarios_montos = chequeo_usuarios_y_montos(cantidad_usuarios)
						if usuarios_montos is None:
							informe = "Tiempo de espera de confirmación terminado. Por favor, si desea las descargas, vuelva a iniciar el comando."
							return informe

						chequeo = int(cantidad_usuarios) * 2
						data = usuarios_montos.split()

						if len(data) != chequeo:
							ejemplo = "Ejemplo, para 10 usuarios, 20 campos. Usuario1 monto1 usuario2 monto2 usuario3 monto3 ...... usuario10 monto10"
								
							informe = f"*ERROR*. Para accion multiple a {cantidad_usuarios} usuarios. Necesito {chequeo} campos. Cada usuario, con su monto. \n {ejemplo}"
						else:	
							enviar_mensaje(msjs.confirmacion(usuarios_montos, codigo_plataf))
							respuesta = confirmacion(usuarios_montos, codigo_plataf)
							if respuesta == "SI":
								enviar_mensaje("*...Ejecutando comando...*")
								if codigo_plataf == "01":
									admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,"01")
									if admin and clave_admin != None:
										data_ordenada = descomprimir.main(usuarios_montos, cantidad_usuarios, codigo_plataf)
										usuarios, montos = descomprimir.descomprimir_data(data_ordenada, cantidad_usuarios, codigo_plataf)
										informe = bp01.multiple_descarga(admin[0], clave_admin[0],usuarios, montos, cantidad_usuarios, nombre_cajero)
									else:
										informe = msjs.err_cuenta_plataforma("01")

								elif codigo_plataf == "02":
									admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,"02")
									if admin and clave_admin != None:
										data_ordenada = descomprimir.main(usuarios_montos, cantidad_usuarios, codigo_plataf)
										usuarios, montos = descomprimir.descomprimir_data(data_ordenada, cantidad_usuarios, codigo_plataf)
										informe = bp02.multiple_descarga(admin[0], clave_admin[0],usuarios,montos, cantidad_usuarios, nombre_cajero)
									else:
										informe = msjs.err_cuenta_plataforma("02")

								elif codigo_plataf == "03":
									admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,"03")
									if admin and clave_admin != None:
										data_ordenada = descomprimir.main(usuarios_montos, cantidad_usuarios, codigo_plataf)
										usuarios, montos = descomprimir.descomprimir_data(data_ordenada, cantidad_usuarios, codigo_plataf)
										informe = bp03.multiple_descarga(admin[0], clave_admin[0],usuarios, montos, cantidad_usuarios, nombre_cajero)
									else:
										informe = msjs.err_cuenta_plataforma("03")
										
								elif codigo_plataf == "04":
									admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,"04")
									if admin and clave_admin != None:
										data_ordenada = descomprimir.main(usuarios_montos, cantidad_usuarios, codigo_plataf)
										usuarios, montos = descomprimir.descomprimir_data(data_ordenada, cantidad_usuarios, codigo_plataf)
										informe = bp04.multiple_descarga(admin[0], clave_admin[0],usuarios, montos, cantidad_usuarios, nombre_cajero)
									else:
										informe = msjs.err_cuenta_plataforma("04")


							elif respuesta == "NO":
								informe = "Entiendo. Por favor inicie nuevamente el comando MULTIPLE DES con los usuarios y montos correspondientes"
							elif respuesta == None:
								informe = "Tiempo de espera de confirmacion terminado. Por favor, si desea, vuelva a iniciar el comando MULTIPLE"
							else:
								informe = "Confirmacion incorrecta. Por favor, vuelva a iniciar comando y confirme con SI o NO."
				else:
					informe = msjs.err_cmd_incorrecto("MULTIPLE ACCION")			

	elif "CAR" in comando:
		print("CARGANDO FICHAS..")
		comandoSplit = comando.split()
		# parametros comandoSplit: [0]Comando [1]numero plataforma [2]usuario [3]monto
		if len(comandoSplit) != 4:
			informe = msjs.err_cmd_incorrecto("CARGA")
		else:
			if comandoSplit[1] == "01":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp01.cd_bot_plataforma(comandoSplit[0], admin[0], clave_admin[0], comandoSplit[2].capitalize(), comandoSplit[3], nombre_cajero)
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			elif comandoSplit[1] == "02":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp02.cd_bot_plataforma(comandoSplit[0], admin[0], clave_admin[0], comandoSplit[2].capitalize(), comandoSplit[3], nombre_cajero)
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			elif comandoSplit[1] == "03":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp03.cd_bot_plataforma(comandoSplit[0], admin[0], clave_admin[0], comandoSplit[2].capitalize(), comandoSplit[3], nombre_cajero)
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			elif comandoSplit[1] == "04":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp04.cd_bot_plataforma(comandoSplit[0], admin[0], clave_admin[0], comandoSplit[2].lower(), comandoSplit[3], nombre_cajero)
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			else:
				informe = msjs.err_cod_plataforma()
		
	elif "DES" in comando:
		print("DESCARGANDO FICHAS..")
		comandoSplit = comando.split()
		# parametros comandoSplit: [0]Comando [1]numero plataforma [2]usuario [3]monto
		if len(comandoSplit) != 4:
			informe = msjs.err_cmd_incorrecto("DESCARGA")
		else:	
			if comandoSplit[1] == "01":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp01.cd_bot_plataforma(comandoSplit[0], admin[0], clave_admin[0], comandoSplit[2].capitalize(), comandoSplit[3], nombre_cajero)
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			elif comandoSplit[1] == "02":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp02.cd_bot_plataforma(comandoSplit[0], admin[0], clave_admin[0], comandoSplit[2].capitalize(), comandoSplit[3], nombre_cajero)
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			elif comandoSplit[1] == "03":
				admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
				if admin and clave_admin != None:
					informe = bp03.cd_bot_plataforma(comandoSplit[0], admin[0], clave_admin[0], comandoSplit[2].capitalize(), comandoSplit[3], nombre_cajero)
				else:
					informe = msjs.err_cuenta_plataforma(comandoSplit[1])
			elif comandoSplit[1] == "04":
				informe = ("Estoy teniendo problemas con las *descargas* en la plataforma 04. Por favor, por el momento, debe realizarla de forma manual.")
			else:
				informe = msjs.err_cod_plataforma()
			
	elif "NJ" in comando:
		print("CREANDO NUEVO JUGADOR..")
		comandoSplit = comando.split()
		if len(comandoSplit) != 4:
			informe = msjs.err_cmd_incorrecto("NUEVO JUGADOR")
		else:
			# parametros comandoSplit: [0]Comando [1]numero plataforma [2]usuario a crear [3]contraseña a crear
			if len(comandoSplit[3]) < 6 or len(comandoSplit[3]) > 16:
				informe = msjs.err_clave()
			else:
				if comandoSplit[1] == "01":
					admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
					if admin and clave_admin != None:
						informe = bp01.botNuevoJugador(admin[0], clave_admin[0], comandoSplit[2], comandoSplit[3])
					else:
						informe = msjs.err_cuenta_plataforma(comandoSplit[1])
				elif comandoSplit[1] == "02":
					admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
					if admin and clave_admin != None:
						informe = bp02.botNuevoJugador(admin[0], clave_admin[0], comandoSplit[2], comandoSplit[3])
					else:
						informe = msjs.err_cuenta_plataforma(comandoSplit[1])
				elif comandoSplit[1] == "03":
					admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
					if admin and clave_admin != None:
						informe = bp03.botNuevoJugador(admin[0], clave_admin[0], comandoSplit[2], comandoSplit[3])
					else:
						msjs.err_cuenta_plataforma(comandoSplit[1])
				elif comandoSplit[1] == "04":
					admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
					if admin and clave_admin != None:
						informe = bp04.botNuevoJugador(admin[0], clave_admin[0], comandoSplit[2], comandoSplit[3])
					else:
						informe = msjs.err_cuenta_plataforma(comandoSplit[1])
				else:
					informe = msjs.err_cod_plataforma()

	elif "NA" in comando:
		print("CREANDO NUEVO AGENTE..")
		comandoSplit = comando.split()
		# parametros comandoSplit: [0]Comando [1]numero plataforma [2]usuario a crear [3]contraseña a crear [4]comision deporte [5]comision casino
		if len(comandoSplit) != 6:
			informe = msjs.err_cmd_incorrecto("NUEVO AGENTE")
		else:	
			if len(comandoSplit[3]) < 6 or len(comandoSplit[3]) > 16:
				informe = msjs.err_clave()
			else:
				if comandoSplit[1] == "01":
					admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
					if admin and clave_admin != None:
						informe = bp01.botNuevoAgente(admin[0], clave_admin[0], comandoSplit[2], comandoSplit[3], comandoSplit[4], comandoSplit[5])
					else:
						informe = msjs.err_cuenta_plataforma(comandoSplit[1])	
				elif comandoSplit[1] == "02":
					admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
					if admin and clave_admin != None:
						informe = bp02.botNuevoAgente(admin[0], clave_admin[0], comandoSplit[2], comandoSplit[3], comandoSplit[4], comandoSplit[5])
					else:
						informe = msjs.err_cuenta_plataforma(comandoSplit[1])
				elif comandoSplit[1] == "03":
					admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
					if admin and clave_admin != None:
						informe = bp03.botNuevoAgente(admin[0], clave_admin[0], comandoSplit[2], comandoSplit[3], comandoSplit[4], comandoSplit[5])		
					else:
						informe = msjs.err_cuenta_plataforma(comandoSplit[1])
				elif comandoSplit[1] == "04":
					admin, clave_admin = db.traer_usuario_y_clave(nombre_cajero,comandoSplit[1])
					if admin and clave_admin != None:
						informe = bp04.botNuevoAgente(admin[0], clave_admin[0], comandoSplit[2], comandoSplit[3])		
					else:
						informe = msjs.err_cuenta_plataforma(comandoSplit[1])
				else:
					informe = msjs.err_cod_plataforma()

	elif "START" in comando:
		print("BIENVENIDA Y SETEO")
		informe = msjs.cmd_start()

	elif "CONFIG" in comando:
		print("CONFIGURANDO ASISTENTE..")
		comandoSplit = comando.split()
		# COMANDO[0] + CODIGO PLATAFORMA[1] + USUARIO[2] + CLAVE[3]
		if len(comandoSplit) != 4:
			informe = "*ERROR.* COMANDO DE CONFIGURACION INCORRECTO.\n Para saber más, enviame el comando *START*"
		else:
			id_cajero = db.select_id_cajero(nombre_cajero)
			chequeo = True
			if comandoSplit[1] == "01":
				nn, chequeo = bp01.get(comandoSplit[2], comandoSplit[3])
			elif comandoSplit[1] == "02":
				nn, chequeo = bp02.get(comandoSplit[2], comandoSplit[3])
			elif comandoSplit[1] == "03":
				nn, chequeo = bp03.get(comandoSplit[2], comandoSplit[3])
			elif comandoSplit[1] == "04":
				nn, chequeo = bp04.get(comandoSplit[2], comandoSplit[3])
			else:
				informe = msjs.err_cod_plataforma()
				return informe

			if chequeo == False:
				informe = f"*ERROR*\n Usuario o clave incorrecta.\n *Usuario enviado:* {comandoSplit[2]} \n *Contraseña enviada:* {comandoSplit[3]}"
			else:	
				try:
					print("ENTRANDO LINEA 587")
					registro_previo, usuario = db.chequeo_plataforma(nombre_cajero, comandoSplit[1])
					if registro_previo == True:
						informe = f"Ya estas registrado para la plataforma: {comandoSplit[1]} con el usuario: {usuario[0]}"
						return informe
					else:
						print("ENTRANDO LINEA 592.....")
						print(id_cajero,comandoSplit[2],comandoSplit[3],comandoSplit[1])
						informeDB = db.insertar_usuarios(id_cajero[0],comandoSplit[2],comandoSplit[3],comandoSplit[1])
						print("ENTRANDO LINEA 595....")
						if informeDB == False: 
							print("*ERROR CON BASE DE DATOS.* (insertar_usuario) error.")
							informe = msjs.err_inesperado()
							return informe
						else:
							print("ENTRANDO LINEA 601....")
							#contra_pass_generator = pass_generator.pg_init()
							informe = f"*DATOS DE LOGEO CARGADOS CORRECTAMENTE.*\n *Usuario:* {comandoSplit[2]}\n *Contraseña:* #############\n DIANA Configurada para empezar a trabajar. Enviame el comando *INFO* y comencemos!"
							return informe
				except Exception as err:
					print("linea 685 mainFinal", err)
					informe = msjs.err_inesperado()
					return informe

	elif "REGISTRO" in comando:
		comandoSplit = comando.split()
		# COMANDO[0] TIPO[1] PLATAFORMA[2] USUARIO[3]
		if len(comandoSplit) != 4:
			informe = msjs.err_cmd_incorrecto("REGISTRO")
		else:
			if comandoSplit[1] != "DETALLADO" and comandoSplit[1] != "GENERAL":
				informe = msjs.err_cmd_incorrecto("REGISTRO")
			else:
				informe = db.traer_registros(nombre_cajero, comandoSplit[1], comandoSplit[2], comandoSplit[3])
				if informe is None:
					informe = f"No hay actividad registrada sobre el usuario *{comandoSplit[3]}* en la palataforma *{comandoSplit[2]}*"		
	
	elif "ARCHIVO" in comando:
		informe = "Archivo no disponible"
	
	else:
		informe = msjs.err_cmd_no_reconocible()
	return informe

def procesar_informe(comando, nombre_cajero):
	xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
	chatbox = WebDriverWait(driver, timeout=15).until(lambda d: d.find_element(By.XPATH, xpath))
	informe = ejecutar_comando(comando, nombre_cajero)
	chatbox.send_keys(informe)
	chatbox.send_keys(Keys.ENTER)

def enviar_archivo():

	clipp = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "_1OT67")).click()
	time.sleep(2)
	xpath = '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[4]/button/input'
	subir_documento = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, xpath))
	time.sleep(5)
	subir_documento.send_keys('C:\\Users\\Chonazak\\Desktop\\diana.chat-main\\diana.chat\\registros.csv')
	

	#btn_enviar = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CLASS_NAME, "_3wFFT")).click()

def whatsapp_bot_init():
	global driver
	driver.maximize_window()

	while True:
		try:
			if not buscar_chats():
				time.sleep(3)
				continue
			
			comando = identificar_comando("*...Ejecutando comando...*")
			
			if comando == None:
				continue
			
			nombre_cajero = busca_nombre_cajero()

			procesar_informe(comando, nombre_cajero)
			time.sleep(2)
			setear_bot()
		except Exception as err:
			print("ERROR EN MAIN. ERR: ", err)
			enviar_mensaje("ERROR INESPERADO. COMANDO NO EJECUTADO")
			setear_bot()
		
		
whatsapp_bot_init()
