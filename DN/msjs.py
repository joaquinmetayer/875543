################################ INFORMATIVOS ############################################
def cmd_info():
	msj1 = ("*COMANDOS:*\n"
			"*Start:* START\n"
			"*Carga:* CAR + codigoPlataforma + nombre de usuario + monto\n" 
			"*Descarga:* DES + codigoPlataforma + nombre de usuario + monto\n" 
			"*Carga multiple:* MULTIPLE + CAR\n"
			"*Descarga multiple:* MULTIPLE + DES\n"
			"*Nuevo jugador:* NJ + codigoPlataforma + NuevoUsuario + NuevaContraseña\n" 
			"*Nuevo agente:* NA + codigoPlataforma + NuevoUsuario + NuevaContraseña + comision deportes(sin %) + comision casino(sin %)\n"
			"*Consultar fichas en panel:* FICHAS + codigoPlataforma\n"
			"Para ver ejemplos, enviame el comando *EJEMPLOS*.\n"
			"Para conocer los codigos de plataforma, enviame el comando *PLATAFORMAS*"
			)
	return msj1

def cmd_ejemplos():
	msj1 = ("*CARGA:* CAR 01 Usuario99 3000\n"
			"*DESCARGA:* DES 02 Usuario99 1500\n"
			"*CARGA MULTIPLE:* MULTIPLE CAR\n"
			"*DESCARGA MULTIPLE:* MULTIPLE DES\n"
			"*NUEVO JUGADOR:* NJ 03 Jugador00 contraseña123\n"
			"*NUEVO AGENTE:* NA 01 Agente00 contra123 50 50\n"
			"*CONSULTAR FICHAS:* FICHAS 02\n"

			)
	return msj1

def cmd_plataformas():
	msj1 = ("*01* - JugaYganaOnline\n"
			"*02* - SiempreGana\n"
			"*03* - 24live\n"
			"*04* - Casino365Online"
			)
	return msj1

def cmd_start():
	msj1 = ("*¡BIENVENIDO!*\n Para darte de alta, necesito los siguientes datos:\n"
					"Codigo de plataforma: *01*(JUGAYGANA) // *02*(SIEMPREGANA) // *03*(24LIVE) // *04* (CASINO365online)\n"
					"Nombre de usuario y Contraseña de cuenta administrador \n"
					"Tene en cuenta que los datos se guardaran *encriptados*, y ninguna persona tendra acceso a ellos.\n"
					"Enviame el comando *CONFIG* más los datos pedidos, todo en una linea. De la siguiente manera:\n"
					"*Ejemplo:* CONFIG numero_plataforma usuario12 clave123"
			)
	return msj1

def cmd_multiple(tipo):
	msj1 = f"Cuantas {tipo} seguidas queres realizar? (en numero, ej: 2) maximo 10"
	return msj1

def usuarios_multiple(cantidad_usuarios):
	msj1 = f"Enviame los {cantidad_usuarios} nombres de usuario seguido de sus respectivos montos. Todo en un mismo mensaje."
	return msj1

def montos_multiple(tipo):
	msj1 = f"Enviame los montos de {tipo}. (Todo en un mismo mensaje)"
	return msj1


def confirmacion(usuarios_montos, codigo_plataf):
	msj1 = f"*La accion sera con los usuarios y los montos:*\n {usuarios_montos}\n En la plataforma {codigo_plataf}\n *Es correcto? (SI o NO)*"
	return msj1



#################################################### ERRORES #######################################
def err_cmd_incorrecto(tipo):
	msj1 = f"*ERROR.* COMANDO DE {tipo} INCORRECTO. \n Para saber más, enviame el comando *INFO* y/o *EJEMPLOS*"
	return msj1

def err_cuenta_plataforma(plataforma):
	msj1 = f"*ERROR*\n No tenes cuenta configurada para la plataforma: *{plataforma}* Por favor, envia el comando START y segui las instrucciones."
	return msj1

def err_cod_plataforma():
	msj1 = "*ERROR*\n Corrobora el codigo de plataforma, y volve a enviar el comando. O envía el comando *PLATAFORMAS* para saber más."
	return msj1

def err_clave():
	msj1 = "*ERROR*. La contraseña debe contener entre 6 y 16 caracteres. Por favor, envia el comando nuevamente."
	return msj1

def err_inesperado():
	msj1 = "*ERROR INESPERADO* por favor, volve a enviar el comando. Si el problema persiste, comunicate con soporte." 
	return msj1

def err_cmd_no_reconocible():
	msj1 = "*ERROR.* COMANDO NO RECONOCIBLE\n Comproba el uso de mayusculas y minusculas\n Para saber más, enviame el comando *INFO*"
	return msj1