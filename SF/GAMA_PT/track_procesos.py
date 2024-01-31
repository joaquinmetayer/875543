# track_procesos.py
# Funcionamiento:
# 1) Cada accion que realiza Sofia es registrada bajo una variable "proceso" al principio de la mayoria de funciones.
# 2) Luego debajo de esa variable "proceso" se llama a la funcion agregar_proceso(proceso) de este archivo.
# 3) La funcion agregar_proceso(proceso) registra dicho proceso en un .txt
# 4) Al ocurrir un error inesperado en main.py, toda la información detallada e importante de los procesos estan registradas en ese txt.
# 5) Con esta infromación, se puede saber exactamente QUE ocurrio y CUANDO. Y tomar desiciones en base a ello.
# 6) Luego enviarse el reporte al grupo en el archivo supermain.py este, llama a la funcion eliminar_archivo() de esta funcion. Con el objetivo de limpiar la información.

def agregar_proceso(proceso):
    try:
        with open("resource/procesos.txt", "a") as archivo:
            archivo.write(proceso + "\n")
    except IOError:
        print("Error al escribir proceso en procesos.txt")


def leer_archivo():
    ruta_archivo = "resource/procesos.txt"
    try:
        with open(ruta_archivo, "r") as archivo:
            contenido = archivo.read()
            return str(contenido)
    except FileNotFoundError:
        return "El archivo no fue encontrado."
    except IOError:
        return "Ocurrió un error al intentar leer el archivo."


def eliminar_archivo():
    try:
        with open("resource/procesos.txt", "w") as archivo:
            archivo.write("")
    except IOError:
        print("Error al eliminar el archivo.")



