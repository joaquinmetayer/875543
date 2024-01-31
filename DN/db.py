import mysql.connector
import csv
import pandas as pd

import time

def db_get():
	try:
		conexion = mysql.connector.connect(host='localhost',
			port=3306,user='root',passwd='',database='diana.chat2')
	except Exception as err:
		print("Error al conectar base de datos.", err)
	else:
		print("Conexion exitosa.")
	return conexion

def select_id_cajero(nombre_cajero):
	conexion = db_get()
	try: 
		cur01 = conexion.cursor()
		query = "SELECT id_cajero FROM cajeros WHERE nombre_cajero = %s"
		nombre_cajero_list = (nombre_cajero, )
		print("NOMBRE CAJERO: ", nombre_cajero)
		id_cajero = cur01.execute(query, nombre_cajero_list)
		id_cajero = cur01.fetchall()
		return id_cajero
	except Exception as err:
		print("ERROR. ID NO SELECCIONADO.", err)
	conexion.close()

def select_id_plataforma(nombre_plataforma):
	conexion = db_get()
	try: 
		cur01 = conexion.cursor()
		query = "SELECT id_plataforma FROM plataformas WHERE nombre_plataforma = %s"
		nombre_plataforma_list = (nombre_plataforma, )
		id_plataforma = cur01.execute(query, nombre_plataforma_list)
		id_plataforma = cur01.fetchall()
		print(id_plataforma, "base de datos")
		return id_plataforma
	except Exception as err:
		print("ERROR. ID NO SELECCIONADO.", err)
	cur01.close()
	conexion.close()

def traer_usuario_y_clave(nombre_cajero, plataforma):
	conexion = db_get()

	if plataforma == "01":
		nombre_plataforma = 'jugalo'
	elif plataforma == "02":
		nombre_plataforma = 'siempregana'
	elif plataforma == "03":
		nombre_plataforma = '24live'
	elif plataforma == "04":
		nombre_plataforma = 'camelBet'

	id_cajero = select_id_cajero(nombre_cajero)
	id_plataforma = select_id_plataforma(nombre_plataforma)
	id_cajero_int = int(''.join(map(str, id_cajero[0])))
	id_plataforma_int = int(''.join(map(str, id_plataforma[0])))

	try:
		cur01 = conexion.cursor()
		queryUsuario = "SELECT usuario FROM usuarios WHERE id_cajero = %s AND id_plataforma = %s"
		values = (id_cajero_int, id_plataforma_int)
		cur01.execute(queryUsuario, values)
		usuario = cur01.fetchall()
		queryClave = "SELECT clave FROM usuarios WHERE id_cajero = %s AND id_plataforma = %s"
		values = (id_cajero_int, id_plataforma_int)
		cur01.execute(queryClave, values)
		clave = cur01.fetchall()
		return usuario,clave
	except Exception as err:
		print("ERROR. usuario y clave no selecionado.", err)

	cur01.close()
	conexion.close()

def traer_registros(nombre_cajero, tipo, plataforma, usuario):
	plataforma = plataforma + "IGNORAR ESTE STRING"
	conexion = db_get()
	id_cajero = select_id_cajero(nombre_cajero)
	id_cajero_int = (''.join(map(str, id_cajero[0])))

	try:
		cur01 = conexion.cursor()
		query = "SELECT nombre_plataf, operacion, usuario, monto, fecha_hora FROM registros WHERE id_cajero = %s AND usuario = %s"
		values = (id_cajero_int, usuario)
		cur01.execute(query, values)
		registros = cur01.fetchall()
		print(registros)
		if registros != []:
			add = ('Plataforma   //', 'Operacion   //', 'Usuario   //', 'Monto   //', 'Fecha y hora')
			registros.insert(0, add)

			total_cargado = 0
			total_descargado = 0
			ganancia_obtenida = 0
			info_final = ""
			for i in registros:
				if i[1] == "carga":
					total_cargado = total_cargado + i[3]
				elif i[1] == "descarga":
					total_descargado = total_descargado + i[3]	
				ganancia_obtenida = total_cargado - total_descargado

			with open('registros.csv', 'w', newline=None) as file:
				writer = csv.writer(file, delimiter=',')
				writer.writerows(registros)
				file.close()
			df = pd.read_csv("registros.csv")
			print(df)

			if tipo == "DETALLADO":
				info_final = str(df) + "\n" + "total cargado: " + str(total_cargado) + "\n" + "total descargado: " + str(total_descargado) + "\n" + "ganancia obtenida: " + str(ganancia_obtenida)
				return info_final
			elif tipo == "GENERAL":
				info_final = "total cargado: " + str(total_cargado) + "\n" + "total descargado: " + str(total_descargado) + "\n" + "ganancia obtenida: " + str(ganancia_obtenida)
				return info_final
		else:
			informe = None
	except Exception as err:
		print("ERROR LINEA 65. TRAER REGISTROS..", err)
		informe = "*ERROR*. Error al ingresar a base de datos. Vuelva a intentarlo. SI el problema persiste, comunicarse con soporte dandoles el siguiente codigo: DB-L126"
		return informe

def insertar_usuarios(id_cajero, usuario, clave, plataforma):
    conexion = db_get()
    # segundo, inserto los datos del nuevo usuario.
    try:
        print("ENTRANDO LINEA 135 DB...")
        cur01 = conexion.cursor()
        # tabla usuarios = ID / ID_CAJERO / USUARIO / CONTRASEÑA / PLATAFORMA
        query = "INSERT INTO usuarios VALUES(%s, %s, %s, %s, %s)"
        # en values, voy a recibir los datos desde parametros exportados desde wpbot
        values = (None, id_cajero[0], usuario, clave, plataforma)
        cur01.execute(query, values)
        conexion.commit()
        print("USUARIO insertado correctamente en BD..")
        return True
    except Exception as err:
        print("ERROR. datos no insertados.", err)
        return False
    else:
        print("DATOS INSERTADOS CORRECTAMENTE.")
    finally:
        cur01.close()
        conexion.close()


def insertar_registro(id_cajero, plataforma, operacion, usuario, monto):
	conexion = db_get()
	try:
		cur01 = conexion.cursor()
		query = "INSERT INTO registros VALUES(%s,%s,%s,%s,%s,%s,%s)"
		values = (None, id_cajero[0], plataforma, operacion, monto, usuario, None)
		print(values)
		cur01.execute(query, values)
		conexion.commit()
		print("REGISTRO insertado correctamente en BD..")
		return True
	except Exception as err:
		print("ERROR. registro no insertado.", err)
		return False

	cur01.close()
	conexion.close()

def chequeo_plataforma(nombre_cajero, plataforma):
	try:
		usuario,clave = traer_usuario_y_clave(nombre_cajero,plataforma)
		print("173 DB: ", usuario, clave)
		if len(usuario) == 0 and len(clave) == 0:
			print("Retornando True, usuario y clave vacíos")
			return False, 0
		else:
			print("Retornando False, usuario o clave no están vacíos")
			return True, usuario
	except:
		print("Retornando False,0")
		return False, 0



