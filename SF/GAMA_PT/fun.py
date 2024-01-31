import re
from unidecode import unidecode
import time


import msjs
import wp
import wpEdge
import bp04
import db
import bpConfirmar
import track_procesos
import config
import num_admin

numero_superadmin = config.numero_superadministrador()
numero_admin = num_admin.init()
admin, clave_admin = config.cuenta_logeo()
alias,cbu,nombre_cuenta = config.datos_transferencia()

def crear_usuario(numero):
    proceso = f"Creando usuario para el número de telefono: *{numero}*. Funcion crear_usuario(). Linea 23. Archivo fun.py"
    print(f"Creando usuario para el número de telefono: {numero}")
    track_procesos.agregar_proceso(proceso)

    u = wp.leer_ultimo_mensaje().lower()
    u = u.split()
    u = unidecode(u[0])
    usuario = re.sub(r'[^\w\s]','',u)
    if not (6 <= len(usuario) <= 18):
        wp.enviar_mensaje(msjs.msj_err_reglas_user(usuario))
    elif usuario[0].isdigit():
        wp.enviar_mensaje(msjs.msj_err_no_num())
    elif bp04.botNuevoJugador("arlequin21", "93113seba", usuario, "Hola123"):
        db.vincular_usuario(numero, usuario)
        db.cambiar_estado("estado2", numero)
        wp.enviar_mensaje_user_creado()
        wp.enviar_mensaje_menu_acciones(usuario)
    else:
        wp.enviar_mensaje_err_crear_user()
        wpEdge.buscar_chat("BOT REPORTES")
        wpEdge.enviar_mensaje(f"El número *{numero}* esta intentando crear un usuario, pero estoy teniendo problemas en crearlo. Chequea por favor que la plataforma este logueada. SI esta logeada, ignora este mensaje, simplemente esta enviando un usuario que ya existe.")


def menu_acciones(numero, usuario):
    opc = wp.leer_ultimo_mensaje()
    if opc != "1" and opc != "2" and opc != "3" and opc != "4" and opc != "5":
        proceso = f"Sin accion en menu. El usuario {usuario} vinculado al número de telefono: {numero} no ingreso ni al 1)2)3)4) ni 5). Funcion menu_acciones(). Linea 48. Archivo fun.py"
        print(f"Sin accion en menu. El usuario {usuario} vinculado al número de telefono: {numero} no ingreso ni al 1)2)3)4) ni 5).")
        track_procesos.agregar_proceso(proceso)

        wp.enviar_mensaje(msjs.msj_no_entendi())
        wp.enviar_mensaje_menu_acciones(usuario)
    else:
        if opc == "1":
            #BotCargaFichas
            proceso = f"Enviando pasos de carga al número: {numero} vinculado al usuario: {usuario}. Funcion menu_acciones(). Linea 53. Archivo fun.py"
            print(f"Enviando pasos de carga al número: {numero} vinculado al usuario: {usuario}")
            track_procesos.agregar_proceso(proceso)

            wp.enviar_mensaje_pasos_transf(cbu,alias,nombre_cuenta)
            db.cambiar_estado("estado3",numero)
        elif opc == "2":
            #BotCambiarContraseña
            proceso = f"Enviando confirmación de cambio de pass al número: {numero} vinculado al usuario: {usuario}. Funcion menu_acciones(). Linea 59. Archivo fun.py"
            print(f"Enviando confirmación de cambio de pass al número: {numero} vinculado al usuario: {usuario}")
            track_procesos.agregar_proceso(proceso)

            wp.enviar_mensaje(msjs.msj_confirmacion_pw())
            db.cambiar_estado("estado5", numero)
        elif opc == "3":
            #BotRetirarFichas
            proceso = f"Enviando pasos de descarga al número: {numero} vinculado al usuario: {usuario}. Funcion menu_acciones(). Linea 65. Archivo fun.py"
            print(f"Enviando pasos de descarga al número: {numero} vinculado al usuario: {usuario}")
            track_procesos.agregar_proceso(proceso)

            wp.enviar_mensaje(msjs.msj_confirmacion_datos())
            db.cambiar_estado("estado6", numero)
        elif opc == "4":
            #BotDesbloquearUser
            proceso = f"Procesando solicitud de desbloqueo del número: {numero} vinculado al usuario: {usuario}. Funcion menu_acciones(). Linea 71. Archivo fun.py"
            print(f"Procesando solicitud de desbloqueo del número: {numero} vinculado al usuario: {usuario}")
            track_procesos.agregar_proceso(proceso)

            wp.enviar_mensaje("Para *solicitud de desbloqueo* por favor, comunicate con soporte mediante la opcion 5")
            wp.enviar_mensaje_menu_acciones(usuario)
        else:
            # atencion cliente
            proceso = f"Derivando al area de atención al cliente al número: {numero} vinculado al usuario: {usuario}. Funcion menu_acciones(). Linea 88. Archivo fun.py"
            print(f"Derivando al area de atención al cliente al número: {numero} vinculado al usuario: {usuario}")
            track_procesos.agregar_proceso(proceso)

            wp.enviar_mensaje(msjs.msj_atencion_cliente())
            wp.enviar_mensaje_menu_acciones(usuario)
            wpEdge.buscar_chat("SOLICITUD ATENCION")
            wpEdge.enviar_mensaje(f"El usuario *{usuario}* con el numero de telefono: *{numero}* necesita que se contacten con el.")

def datos_retiro(numero,usuario):
    datos = wp.leer_ultimo_mensaje()
    datosSplit = datos.split()
    if datosSplit[0].lower() == "cancelar":
        proceso = f"Cancelando proceso de descarga al número: {numero} vinculado al usuario: {usuario}. Funcion datos_retiro(). Linea 99. Archivo fun.py"
        print(f"Cancelando proceso de descarga al número: {numero} vinculado al usuario: {usuario}")
        track_procesos.agregar_proceso(proceso)

        wp.enviar_mensaje(msjs.msj_cancelar())
        wp.enviar_mensaje_menu_acciones(usuario)
        db.cambiar_estado("estado2", numero)
    elif not datosSplit[0].isdigit():
        wp.enviar_mensaje(msjs.msj_err_formato_datos_retiro())
    elif len(datosSplit) != 2:
        wp.enviar_mensaje(msjs.msj_err_formato_datos_retiro())
    else:
        fichas_reales = bp04.cd_bot_plataforma("FICHAS", admin, clave_admin, usuario, None)
        if int(fichas_reales) < int(datosSplit[0]) or int(datosSplit[0]) == 0:
            wp.enviar_mensaje(msjs.msj_err_cantidad_fichas(datosSplit[0], fichas_reales))
        else:
            wp.enviar_mensaje(msjs.msj_datos_retiro(datosSplit[0], datosSplit[1]))
            db.insertar_registro_desc("DESCARGA", usuario, datosSplit[0], datosSplit[1], None)
            time.sleep(1)
            id_registro_desc = db.id_registro_desc(usuario, datosSplit[0])
            bpConfirmar.solicitar_confirmacion_desc(id_registro_desc, numero)
            db.cambiar_estado("estado8", numero)



def confirmacion_retiro(numero, usuario):
    proceso = f"Confirmando solicitud de retiro al usuario: *{usuario}*, con el número de telefono: *{numero}*. Funcion confirmacion_retiro(). Linea 118. Archivo fun.py"
    print(f"Confirmando solicitud de retiro al usuario: {usuario}, con el número de telefono: {numero}.")
    track_procesos.agregar_proceso(proceso)

    wp.enviar_mensaje("*Tu solicitud de retiro ya fue asignada.* Pronto se comunicaran con vos. ¿Puedo ayudarte en algo más?")
    wp.enviar_mensaje_menu_acciones(usuario)
    db.cambiar_estado("estado2", numero)

def pasos_transf(numero, usuario):
    proceso = f"En pasos de transferencia con el usuario: *{usuario}*, con el numero de telefono: *{numero}*. Funcion pasos_transf(). Linea 125. Archivo fun.py"
    print(f"En pasos de transferencia con el usuario: {usuario}, con el numero de telefono: {numero}.")
    track_procesos.agregar_proceso(proceso)

    nombre_transf = wp.leer_ultimo_mensaje()
    if nombre_transf.lower() == "cancelar" or nombre_transf == "This message was deleted":
        proceso = f"Cancelando proceso de carga al número: {numero} vinculado al usuario: {usuario}. Funcion pasos_transf(). Linea 141. Archivo fun.py"
        print(f"Cancelando proceso de carga al número: {numero} vinculado al usuario: {usuario}")
        track_procesos.agregar_proceso(proceso)

        wp.enviar_mensaje(msjs.msj_cancelar())
        db.cambiar_estado("estado2", numero)
        wp.enviar_mensaje_menu_acciones(usuario)
    elif len(nombre_transf.split()) < 2:
        wp.enviar_mensaje(msjs.msj_err_nombre_transf())
    else:
        wp.enviar_mensaje(msjs.msj_nombre_transf_recibido())
        db.insertar_registro("CARGA", usuario, nombre_transf)
        id_registro = db.id_registro(usuario, nombre_transf)
        time.sleep(1)
        bpConfirmar.solicitar_confirmacion(id_registro)
        db.cambiar_estado("estado4", numero)

def confirmacion_pago(numero,usuario):
    proceso = f"En confirmacion de pago con el usuario: *{usuario}*, con el número de telefono: *{numero}*. Funcion confirmacion_pago(). Linea 144. Archivo fun.py"
    print(f"En confirmacion de pago con el usuario: {usuario}, con el número de telefono: {numero}.")
    track_procesos.agregar_proceso(proceso)

    wp.enviar_mensaje_pago_no_confirmado()
    db.cambiar_estado("estado3", numero)
    

def confirmacion_pw(numero, usuario):
    proceso = f"En confirmacion de cambio de contraseña al número: {numero}, vinculado al usuario: {usuario}. Funcion confirmacion_pw(). Linea 151. Archivo fun.py"
    print(f"En confirmacion de cambio de contraseña al número: {numero}, vinculado al usuario: {usuario}.")
    track_procesos.agregar_proceso(proceso)

    confirmacion = wp.leer_ultimo_mensaje().lower()
    if confirmacion == "confirmar":
        wp.enviar_mensaje("Dame un momento, estoy procesando tu *solicitud de cambio de contrasena*")
        informe = bp04.cd_bot_plataforma("PASSW", admin, clave_admin, usuario, None)
        if not "ERROR" in informe:
            time.sleep(1)
            wp.enviar_mensaje(msjs.msj_cambio_pw_exitoso())
            wp.enviar_mensaje_menu_acciones(usuario)
            db.cambiar_estado("estado2", numero)
        else:
            wp.enviar_mensaje(informe)
            db.cambiar_estado("estado2", numero)
            wp.enviar_mensaje_menu_acciones(usuario)
    elif confirmacion == "cancelar":
        proceso = f"Cancelando cambio de contraseña al número: {numero} vinculado al usuario: {usuario}. Funcion confirmacion_pw(). Linea 177. Archivo fun.py"
        print(f"Cancelando cambio de contraseña al número: {numero} vinculado al usuario: {usuario}")
        track_procesos.agregar_proceso(proceso)

        wp.enviar_mensaje(msjs.msj_cancelar())
        wp.enviar_mensaje_menu_acciones(usuario)
        db.cambiar_estado("estado2", numero)
    else:
        wp.enviar_mensaje(msjs.msj_confirmacion_pw())

def detectar_comando():
    proceso = f"Detectando y ejecutando comando de contacto autorizado. Funcion detectar_comando(). Linea 170. Archivo fun.py"
    print(f"Detectando y ejecutando comando de contacto autorizado")
    track_procesos.agregar_proceso(proceso)

    global cbu, alias, nombre_cuenta
    comando = wp.leer_ultimo_mensaje()
    comandoSplit = comando.split()
    # COMANDO PARA ENTRAR EN MANTENIMIENTO
    if len(comandoSplit) == 1 and comandoSplit[0].lower() == "mantenimiento":
        return False
    # COMANDO DE SUPERADMIN PARA FIJAR NUMERO DE ADMINISTRADOR
    elif len(comandoSplit) > 2 and comandoSplit[0].lower() == "admin":
        num = wp.capturar_numero()
        if num == numero_superadmin:
            numero_admin = " ".join(comandoSplit[1:])
            with open("resource/contactos_autorizados.txt", "w") as archivo:
                archivo.write(numero_superadmin + "\n")
                archivo.write(numero_admin + "\n")
            wp.enviar_mensaje("Número de administrador asignado.")
            wp.buscar_chat("Leem")
            print(f"Numero de administrador asignado: {numero_admin}")
        else:
            wp.enviar_mensaje("*ERROR.* Comando ejecutable solo por superadmin.")
            wp.buscar_chat("Leem")
    #COMANDO CAMBIO DE DATOS DE CUENTA BANCARIA PARA TRANSFERENCIAS
    elif comandoSplit[0].lower() == "banco" and len(comandoSplit) <= 6:
        cbu = comandoSplit[1]
        alias = comandoSplit[2]
        nombre_cuenta = ' '.join(comandoSplit[3:])
        wp.enviar_mensaje("Datos de transferencia asignados.")
        wp.buscar_chat("Leem")
    #COMANDO CANCELAR UNA OPERACION, DE CARGA O DESCARGA
    elif len(comandoSplit) == 3 and comandoSplit[2].lower() == "cancelar":
        if comandoSplit[0].lower() == "carga":
            wp.enviar_mensaje("Ejecutando comando")
            wp.buscar_chat("Leem")
            bpConfirmar.ejecutar_confirmacion(comandoSplit[1], "cancelar", None)
        elif comandoSplit[0].lower() == "descarga":
            wp.enviar_mensaje("Ejecutando comando")
            wp.buscar_chat("Leem")
            bpConfirmar.ejecutar_confirmacion_desc(comandoSplit[1], "cancelar")
    # COMANDO DE CARGA RECIBIDA - LLAME A BOT CARGAR FICHAS Y AVISE
    elif len(comandoSplit) == 4 and comandoSplit[2].lower() == "recibido" and int(comandoSplit[3]) > 1:
        wp.enviar_mensaje("Ejecutando comando")
        wp.buscar_chat("Leem")
        bpConfirmar.ejecutar_confirmacion(comandoSplit[1], "recibido", comandoSplit[3])
    # COMANDO DE TRANSFERENCIA HECHA POR ADMINISTRADOR. MODIFIQUE DB COMO TRANSFERIDA Y AVISE AL JUGADOR
    elif len(comandoSplit) == 3 and comandoSplit[2].lower() == "transferido" and comandoSplit[0].lower() == "descarga":
        wp.enviar_mensaje("Ejecutando comando")
        wp.buscar_chat("Leem")
        bpConfirmar.ejecutar_confirmacion_desc(comandoSplit[1], "transferido") 
    # COMANDO PARA CONSULTAR FICHAS EN PANEL DE ADMINISTRADOR
    elif len(comandoSplit) == 2 and comandoSplit[0].lower() == "fichas" and comandoSplit[1] == "panel":
        wp.enviar_mensaje("Ejecutando comando")
        wp.buscar_chat("Leem")
        fichas = bp04.fichas_administrador()
        wpEdge.buscar_chat(num_admin.init())
        wpEdge.enviar_mensaje(f"*Fichas en panel:* {fichas}")
    else:
        wp.enviar_mensaje("*ERROR.* Comando irreconocible o datos mal proporcionados.")
        wp.buscar_chat("Leem")
    return True


