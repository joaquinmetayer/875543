from selenium import webdriver
import time

import wp
import wpEdge
import db
import bp03
import msjs
import track_procesos
import num_admin
import config

admin, clave_admin = config.cuenta_logeo()
 
def setear():
    time.sleep(2)
    wpEdge.buscar_chat("Leem")

def setear2():
    time.sleep(1)
    wp.buscar_chat("Leem")

def solicitar_confirmacion(id_registro):
    tipo, usuario, nombre_transf = db.traer_registro(id_registro)
    wpEdge.buscar_chat("SOLICITUD DE CARGA")
    msj = f"OPERACION N° *{id_registro}*. *{tipo}* AL USUARIO *{usuario}*. TRANSFERIDO POR: *{nombre_transf}*"
    wpEdge.enviar_mensaje(msj)

def solicitar_confirmacion_desc(id_registro, numero):
    tipo,usuario,monto,cbu = db.traer_registro_desc(id_registro)
    wpEdge.buscar_chat("SOLICITUD DE DESCARGA")
    msj = f"OPERACION N° *{id_registro}.* *{tipo}* DE *{monto}* AL USUARIO *{usuario}*. \n CBU/ALIAS A TRANSFERIR: \n *{cbu}* \n TELEFONO: *{numero}* \n *(fichas ya retiradas de cuenta del usuario)* \n--------------------------------------------------"
    wpEdge.enviar_mensaje(msj)


def ejecutar_confirmacion(id, desicion, monto):
    proceso = f"Ejecutando confirmacion de carga n° {id}, desicion: {desicion}, por el monto {monto}. Linea 37. Funcion ejecutar_confirmacion(). Archivo bpConfirmar.py"
    print(f"Ejecutando confirmacion de carga n° {id}, desicion: {desicion}, por el monto {monto}.")
    track_procesos.agregar_proceso(proceso)

    tipo, usuario = db.tipo_usuario(id)
    if tipo == None:
        wpEdge.buscar_chat(num_admin.init())
        wpEdge.enviar_mensaje("*ERROR*. Puede que la operacion ya haya sido ejecutada anteriormente. O los datos que proporciona son incorrectos.")
        setear2()
    else:
        numero_admin = num_admin.init()
        numero = db.traer_numero(usuario)
        try:
            if desicion == "cancelar":
                if db.cancelar_registro(id):
                    wpEdge.buscar_chat(numero_admin)
                    wpEdge.enviar_mensaje(f"Operacion de carga *{id}* cancelada.")
                    db.cambiar_estado("estado2", numero)
                    wpEdge.buscar_chat(numero)
                    wpEdge.enviar_mensaje(msjs.msj_carga_cancelada())
                    wpEdge.enviar_mensaje_menu_acciones(usuario)
                    setear()
                    time.sleep(2)
                else:
                    wpEdge.buscar_chat(numero_admin)
                    wpEdge.enviar_mensaje(f"Error al cancelar operacion *{id}*. Volver a intentarlo. Si el problema persiste, comunicarse con soporte. Codigo(db-164).")
                    setear()
                    time.sleep(2)
            elif desicion == "recibido":
                if tipo == "CARGA":
                    informe = bp03.cd_bot_plataforma(tipo, admin, clave_admin, usuario, monto)
                    if "Error carga no realizada." in informe:
                        wpEdge.buscar_chat(numero_admin)
                        wpEdge.enviar_mensaje(f"Error cargando fichas al usuario {usuario}. Chequear que el usuario no este bloqueado. Si lo esta, desbloquear y volver a ejecutar comando de carga.")                        
                    elif "*ERROR.* Cantidad de fichas en panel insuficientes." in informe:
                        wpEdge.buscar_chat(numero_admin)
                        wpEdge.enviar_mensaje(informe)
                    else:
                        db.confirmar_registro(monto,id)
                        wpEdge.buscar_chat(numero)
                        wpEdge.enviar_mensaje_carga_exitosa()
                        db.cambiar_estado("estado2", numero)
                        wpEdge.enviar_mensaje_menu_acciones(usuario)
                        time.sleep(1)
                        wpEdge.buscar_chat(numero_admin)
                        wpEdge.enviar_mensaje(informe)
                    setear()
            time.sleep(2)
            return True
        except Exception as err:
            print("ERROR ejecutar_confirmacion() bpConfirmar. linea 77", err)

def ejecutar_confirmacion_desc(id, desicion):
    proceso = f"Ejecutando confirmacion de *descarga* n° *{id}*, desicion: *{desicion}*. Linea 80. Funcion ejecutar_confirmacion(). Archivo bpConfirmar.py"
    print(f"Ejecutando confirmacion  de descarga n° {id}, desicion: {desicion}.")
    track_procesos.agregar_proceso(proceso)

    tipo, usuario = db.tipo_usuario_desc(id)
    if tipo == None:
        wpEdge.buscar_chat(num_admin.init())
        wpEdge.enviar_mensaje("*ERROR*. Puede que la operacion ya haya sido ejecutada anteriormente. O los datos que proporciona son incorrectos.")
        setear2()
    else:
        numero_admin = num_admin.init()
        numero = db.traer_numero(usuario)
        try:
            if desicion == "cancelar":
                if db.cancelar_registro_desc(id):
                    wpEdge.buscar_chat(numero_admin)
                    wpEdge.enviar_mensaje(f"Operacion de descarga *{id}* cancelada. *Recorda que las fichas ya fueron retiradas del panel del jugador.*")
                    db.cambiar_estado("estado2", numero)
                    wpEdge.buscar_chat(numero)
                    wpEdge.enviar_mensaje(msjs.msj_descarga_cancelada())
                    wpEdge.enviar_mensaje_menu_acciones(usuario)
                    wpEdge.buscar_chat("Leem")
                    time.sleep(2)
                else:
                    wpEdge.buscar_chat(numero_admin)
                    wpEdge.enviar_mensaje(f"Error al cancelar operacion de descarga *{id}*. Volver a intentarlo. Si el problema persiste, comunicarse con soporte. Codigo(db-199). \n *Recorda que las fichas ya fueron retiradas del panel del jugador.*")
                    setear()
                    time.sleep(2)
            elif desicion == "transferido":
                if db.confirmar_registro_desc(id):
                    wpEdge.buscar_chat(numero)
                    wpEdge.enviar_mensaje(msjs.msj_descarga_exitosa())
                    wpEdge.enviar_mensaje_menu_acciones(usuario)
                    db.cambiar_estado("estado2", numero)
                    wpEdge.buscar_chat(numero_admin)
                    wpEdge.enviar_mensaje(f"El usuario *{usuario},* ya fue informado de la transferencia realizada. (No olvidar compartirle comprobante por privado de ser necesario).")
                    wpEdge.buscar_chat("Leem")
            time.sleep(2)
            return True
        except Exception as err:
            print("ERROR ejecutar_confirmacion_desc() bpConfirmar. linea 116", err)
