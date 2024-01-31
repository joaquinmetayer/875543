#crear una funcion que sirva para enviar reportes al grupo de BOT REPORTES. estos reportes son de errores que no rompen el main(confirmar esta hipotesis). toma como 
# parametro el texto del error + el err del Exception. Une los dos y los envia. Filtrar para no enviar el "err" cuando sea de Stacktrace: y lo cambie por "Selenium no encuentra el elemento web."
# estos errores vendran todos del archivo BP05.py

import wpEdge

def reportar_error(informe, err):
    msj = f"Error inesperado en bp05.py: \n {informe} \n {err} \n | *Bot corriendo normalmente*"
    wpEdge.buscar_chat("BOT REPORTES")
    wpEdge.enviar_mensaje(msj)

# Funcion para reportar el error. QUe abra el archivo errores.txt y lo envie al grupo "BOT REPORTES" y otra funcion que borre el txt.

