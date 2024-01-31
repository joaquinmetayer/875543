import random as rd

def init():
	numeros = "123456789"
	letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	unidos = f"{letras}{numeros}"
	obj = ''.join(rd.sample(unidos,10))
	return obj + "@.com"
