import mysql.connector
import time
import track_procesos


# REGISTROS SOLO ES IGUAL A registros_carga
# el otro es REGISTROS_DESC.

def db_get():
    try:
        conexion = mysql.connector.connect(host='localhost',
                                           port=3306, user='root', passwd='', database='sofia.chat')
    except Exception as err:
        print("Error al conectar base de datos.", err)
    #else:
        #print("Conexion exitosa.")
    return conexion

def chequear_usuario(numero):
    proceso = f"Chequeando numero de telefono: *{numero}*. funcion chequear_usuario(). Linea 20. Archivo db.py"
    print(f"Chequeando numero de telefono: {numero}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "SELECT * FROM usuarios WHERE numero = %s"
        data = cursor.execute(query, (numero, ))
        data = cursor.fetchall()

        if data == []:
            query = "INSERT INTO usuarios VALUES(%s,%s,%s,%s)"
            values = (None, numero, None, "En creacion de usuario")
            cursor.execute(query, values)
            conexion.commit()
            proceso = f"Numero de telefono: *{numero}* insertado correctamente en base de datos. funcion chequear_usuario(). Linea 34. Archivo db.py"
            print(f"Numero de telefono: {numero} insertado correctamente en base de datos.")
            track_procesos.agregar_proceso(proceso)

            estado = "En bienvenida"
            return estado, None
        else:
            proceso = f"Chequeando estado del número de telefono: *{numero}*. Funcion chequear_usuario(). Linea 44. Archivo db.py"
            print(f"Chequeando estado del número de telefono: {numero}")
            track_procesos.agregar_proceso(proceso)

            query = "SELECT estado FROM usuarios where numero = %s"
            estado = cursor.execute(query, (numero, ))
            estado = cursor.fetchall()
            estado = ''.join(map(str, estado[0]))
            if estado == "En creacion de usuario":
                print(
                    f"El numero {numero} aun no tiene un usuario registrado.")
                return estado, None
            else:
                query = "SELECT usuario FROM usuarios where numero = %s"
                usuario = cursor.execute(query, (numero, ))
                usuario = cursor.fetchall()
                usuario = ''.join(map(str, usuario[0]))

                return estado, usuario
        cursor.close()
        conexion.close()
    except Exception as err:
        print("Error funcion chequear_usuario(). Linea 57. db.py. Error:", err)
        cursor.close()
        conexion.close()

def vincular_usuario(numero, user):
    proceso = f"Vinculando usuario: *{user}* al número *{numero}*. Funcion vincular_usuario(). Linea 63. Archivo db.py"
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "UPDATE usuarios SET usuario = %s WHERE numero = %s"
        values = (user.capitalize(), numero)
        cursor.execute(query, values)
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as err:
        print("Error vincular usuario en db. ", err)
        cursor.close()
        conexion.close()

def cambiar_estado(tipo, numero):
    proceso = f"Cambiando estado: *{tipo}* al número: *{numero}*. Funcion cambiar_estado(). Linea 80. Archivo db.py"
    print(f"Cambiando estado: {tipo} al número: {numero}.")
    track_procesos.agregar_proceso(proceso)
    
    if tipo == "estado1":
        estado = "En creacion de usuario"
    elif tipo == "estado2":
        estado = "En menu de acciones"
    elif tipo == "estado3":
        estado = "En pasos de transferencia"
    elif tipo == "estado4":
        estado = "En confirmacion de pago"
    elif tipo == "estado5":
        estado = "En confirmacion de pw"
    elif tipo == "estado6":
        estado = "En datos de retiro"
    elif tipo == "estado7":
        estado = "En espera de datos"
    elif tipo == "estado8":
        estado = "En confirmacion de retiro"

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "UPDATE usuarios SET estado = %s WHERE numero = %s"
        values = (estado, numero)
        cursor.execute(query, values)
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as err:
        print("Estado no cambiado.. error.. funcion db cambiar_estado", err)
        cursor.close()
        conexion.close()

def insertar_registro(tipo, usuario, nombre_transf):
    proceso = f"Insertando registro.. Tipo: *{tipo}*, usuario: *{usuario}*, nombre de transferencia: *{nombre_transf}*. Funcion insertar_registro(). Linea 115. Archivo db.py"
    print(f"Insertando registro.. Tipo: {tipo}, usuario: {usuario}, nombre de transferencia: {nombre_transf}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO registros VALUES(%s,%s,%s,%s,%s,%s)"
        values = (None, tipo, usuario, nombre_transf, "En espera", None)
        cursor.execute(query, values)
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as err:
        print("Registro no insertado,  error db.insertar_registro()", err)
        cursor.close()
        conexion.close()

def insertar_registro_desc(tipo, usuario,monto,cbu, nombre_transf):
    proceso = f"Insertando registro.. Tipo: *{tipo}*, usuario: *{usuario}*, monto: *{monto}*, nombre de transferencia: *{nombre_transf}*. Funcion insertar_registro_desc(). Linea 133. Archivo db.py"
    print(f"Insertando registro.. Tipo: {tipo}, usuario: {usuario}, por el monto: {monto}")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO registros_desc VALUES(%s,%s,%s,%s,%s,%s,%s)"
        values = (None, tipo, usuario, monto, cbu, nombre_transf, "En espera")
        cursor.execute(query, values)
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as err:
        print("Registro no insertado,  error db.insertar_registro_desc()", err)
        cursor.close()
        conexion.close()

def id_registro(usuario,nombre_transf):
    proceso = f"Seleccionando ID del registro de *carga* del usuario: *{usuario}*, transferido a nombre de: *{nombre_transf}*. Funcion id_registro(). Linea 151. Archivo db.py"
    print(f"Seleccionando ID del registro de carga del usuario: {usuario}, transferido a nombre de: {nombre_transf}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "SELECT id_registro FROM registros WHERE usuario = %s AND nombre_transf = %s AND confirmacion = %s"
        values = (usuario, nombre_transf, "En espera")
        cursor.execute(query, values)
        id_registro = cursor.fetchall()
        id_registro = ''.join(map(str, id_registro[0]))
        cursor.close()
        conexion.close()
        return id_registro
    except Exception as err:
        print("ERROR def id_registro db. linea 153", err)
        cursor.close()
        conexion.close()

def id_registro_desc(usuario,monto):
    proceso = f"Seleccionando ID del registro de *descarga* del usuario: *{usuario}*, por el monto de: *{monto}*. Funcion id_registro_desc(). Linea 170. Archivo db.py"
    print(f"Seleccionando ID del registro de descarga del usuario: {usuario}, por el monto de: {monto}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "SELECT id_registro_desc FROM registros_desc WHERE usuario = %s AND monto = %s AND confirmacion = %s"
        values = (usuario, monto, "En espera")
        cursor.execute(query, values)
        id_registro = cursor.fetchall()
        id_registro = ''.join(map(str, id_registro[0]))
        cursor.close()
        conexion.close()
        return id_registro
    except Exception as err:
        print("ERROR def id_registro_desc db. linea 170", err)
        cursor.close()
        conexion.close()

def traer_registro(id_registro):
    proceso = f"Trayendo información del registro de *carga* con N° de ID: *{id_registro}*. Funcion traer_registro(). Linea 189. Archivo db.py"
    print(f"Trayendo información del registro de carga con N° de ID: {id_registro}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "SELECT tipo,usuario,nombre_transf FROM registros WHERE id_registro = %s AND confirmacion = %s"
        value = (id_registro, "En espera")
        cursor.execute(query, value)
        datos = cursor.fetchall()
        tipo = ''.join(map(str, datos[0][0]))
        usuario = ''.join(map(str, datos[0][1]))
        nombre_transf = ''.join(map(str, datos[0][2]))
        cursor.close()
        conexion.close()
        return tipo, usuario, nombre_transf
    except Exception as err:
        print("ERROR def traer_registro db. linea 149.", err)
        cursor.close()
        conexion.close()

def traer_registro_desc(id_registro):
    proceso = f"Trayendo información del registro de *descarga* con N° de ID: *{id_registro}*. Funcion traer_registro_desc(). Linea 211. Archivo db.py"
    print(f"Trayendo información del registro de descarga con N° de ID: {id_registro}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "SELECT tipo,usuario,monto,cbu FROM registros_desc WHERE id_registro_desc = %s AND confirmacion = %s"
        value = (id_registro, "En espera")
        cursor.execute(query, value)
        datos = cursor.fetchall()
        tipo = ''.join(map(str, datos[0][0]))
        usuario = ''.join(map(str, datos[0][1]))
        monto = ''.join(map(str, datos[0][2]))
        cbu = ''.join(map(str, datos[0][3]))
        cursor.close()
        conexion.close()
        return tipo, usuario, monto, cbu
    except Exception as err:
        print("ERROR def traer_registro_desc db. linea 211.", err)
        cursor.close()
        conexion.close()

def cancelar_registro(id_registro):
    proceso = f"Cancelando registro de *carga* con ID n°: *{id_registro}*. Funcion cancelar_registro(). Linea 234. Archivo db.py"
    print(f"Cancelando registro de carga con ID n°: {id_registro}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "UPDATE registros SET confirmacion = %s WHERE id_registro = %s"
        value = ("Cancelada",id_registro)
        cursor.execute(query,value)
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as err:
        print("ERROR def cancelar_registro db. linea 164.", err)
        cursor.close()
        conexion.close()

def cancelar_registro_desc(id_registro):
    proceso = f"Cancelando registro de *descarga* con ID n°: *{id_registro}*. Funcion cancelar_registro_desc(). Linea 252. Archivo db.py"
    print(f"Cancelando registro de descarga con ID n°: {id_registro}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "UPDATE registros_desc SET confirmacion = %s WHERE id_registro_desc = %s"
        value = ("Cancelada",id_registro)
        cursor.execute(query,value)
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as err:
        print("ERROR def cancelar_registro db. linea 164.", err)
        cursor.close()
        conexion.close()

def confirmar_registro_desc(id_registro):
    proceso = f"Confirmando registro de *descarga* con ID n°: *{id_registro}*. Funcion confirmar_registro_desc(). Linea 270. Archivo db.py"
    print(f"Confirmando registro de descarga con ID n°: {id_registro}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "UPDATE registros_desc SET confirmacion = %s WHERE id_registro_desc = %s"
        value = ("Transferido",id_registro)
        cursor.execute(query,value)
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as err:
        print("ERROR def confirmar_registro_desc db. linea 243.", err)
        cursor.close()
        conexion.close()

def confirmar_registro(monto, id_registro):
    proceso = f"Confirmando registro de *carga* con ID n°: *{id_registro}*. Funcion confirmar_registro(). Linea 288. Archivo db.py"
    print(f"Confirmando registro de carga con ID n°: {id_registro}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "UPDATE registros SET confirmacion = %s, monto = %s WHERE id_registro = %s"
        values = ("Recibido", monto, id_registro)
        cursor.execute(query,values)
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as err:
        print("ERROR Al modificar_registro() linea 178 db. ", err)
        cursor.close()
        conexion.close()
    
def tipo_usuario(id_registro):
    proceso = f"Seleccionando tipo y usuario del registro de *carga* con ID n°: *{id_registro}*. Funcion tipo_usuario(). Linea 306. Archivo db.py"
    print(f"Seleccionando tipo y usuario del registro de carga con ID n°: {id_registro}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "SELECT tipo,usuario FROM registros WHERE id_registro = %s AND confirmacion = %s"
        value = (id_registro, "En espera")
        cursor.execute(query, value)
        datos = cursor.fetchall()
        tipo = ''.join(map(str, datos[0][0]))
        usuario = ''.join(map(str, datos[0][1]))
        return tipo, usuario
    except Exception as err:
        print("ERROR al traer tipo_usuario() linea 197 db." , err)
        cursor.close()
        conexion.close()
        return None, None
        

def tipo_usuario_desc(id_registro):
    proceso = f"Seleccionando tipo y usuario del registro de *descarga* con ID n°: *{id_registro}*. Funcion tipo_usuario_desc(). Linea 325. Archivo db.py"
    print(f"Seleccionando tipo y usuario del registro de descarga con ID n°: {id_registro}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "SELECT tipo,usuario FROM registros_desc WHERE id_registro_desc = %s AND confirmacion = %s"
        value = (id_registro, "En espera")
        cursor.execute(query, value)
        datos = cursor.fetchall()
        print(len(datos))
        tipo = ''.join(map(str, datos[0][0]))
        usuario = ''.join(map(str, datos[0][1]))
        return tipo, usuario
    except Exception as err:
        print("ERROR al traer tipo_usuario_desc() linea 291 db." , err)
        cursor.close()
        conexion.close()
        return None, None

def traer_numero(usuario):
    proceso = f"Trayendo numero de telefono del usuario: *{usuario}*. Funcion traer_numero(). Linea 346. Archivo db.py"
    print(f"Trayendo numero de telefono del usuario: {usuario}.")
    track_procesos.agregar_proceso(proceso)

    conexion = db_get()
    try:
        cursor = conexion.cursor()
        query = "SELECT numero FROM usuarios WHERE usuario = %s"
        value = (usuario, )
        cursor.execute(query,value)
        numero = cursor.fetchall()
        numero = ''.join(map(str, numero[0][0]))
        return numero
    except Exception as err:
        print("ERROR traer_numero() db. linea 215.", err)