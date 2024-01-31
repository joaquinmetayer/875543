import random as rd

def pg_init():
	letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	numeros = "0123456789"
	simbolos = "!#$%&?¡¿<>*^~"
	unidos = f"{letras}{numeros}{simbolos}"
	clave = ''.join(rd.sample(unidos,12))
	return clave
