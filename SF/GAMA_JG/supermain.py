# Archivo supermain.py
# Funcionamiento:
# 1) Aparece un error inesperado en main.py
# 2) Este error es capturado en el except bajo la variable "err"
# 3) Se agrega el error al trackeo de procesos "procesos.txt"
# 4) Se envia un reporte de lo ocurrido al grupo de whatsapp "SOFIA REPORTES"
# 5) El reporte  enviado al grupo contiene: Toda la información del trackeo de procesos hasta ANTES de que ocurra el error + el error de sistema capturado en "err".
# Con esta información se conoce, QUE error es, y en CUAL proceso EXACTO ocurrio. 

while True:
    try:
        import main
        main.whatsapp_bot_init()
    except Exception as err:
        import wpEdge
        import wp
        import track_procesos
        track_procesos.agregar_proceso(f"Error en consola: {err}")
        reporte = track_procesos.leer_archivo()
        #track_procesos.eliminar_archivo()
        msj = f"Error inesperado en main.py : \n {reporte} \n | *Bot corriendo normalmente*"
        print("Error inesperado en main.py. Reporte enviado. Levantando bot nuevamente..")
        wpEdge.buscar_chat("BOT REPORTES")
        wpEdge.enviar_mensaje(msj)
        wp.buscar_chat("Leem")
        
        

