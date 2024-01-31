def descomprimir_data(usuarios_montos, cantidad_usuarios, codigo_plataf):
	print("entrando a descomprimir_data")
	print("Cantidad de usuarios a procesar: ", cantidad_usuarios)
	print("datos ingresados por wp:", usuarios_montos)
	usuarios_montos_split = usuarios_montos.split()
	usuarios = []
	montos = []
	count = 0
	for x in usuarios_montos_split:
		if (count % 2) == 0:
			if codigo_plataf != "04": #hago esta distincion, pq en bp04 el nombre de usuario no esta   capitalizado.
				usuarios.append(x.capitalize())
			else:
				usuarios.append(x.lower())
		else:
			montos.append(x)
		count = count + 1

	print("descomprimir_data: ",usuarios,montos)
	return usuarios,montos

def ordenar_data(usuarios, montos):
	print("entrando en ordenar_data")
	longitud_datos = 0
	for i in usuarios:
		longitud_datos = longitud_datos + 1
	print("longitud de datos:", longitud_datos)
	cargas = []
	count = 0
	while count < longitud_datos:
		cargas.append((usuarios[count], montos[count]))
		count = count +1

	print("ordenar_data: ", sorted(cargas))
	return sorted(cargas)

def main(usuarios_montos, cantidad_usuarios, codigo_plataf):
	print("entrando a descomprimir.main")
	usuarios, montos = descomprimir_data(usuarios_montos, cantidad_usuarios, codigo_plataf)
	datos_ord = ordenar_data(usuarios, montos)
	str_datos_ord = ""
	for i in datos_ord:
		for j in i:
			str_datos_ord = str_datos_ord + " " + j
	print("main data final: ", str_datos_ord)
	return str_datos_ord



	



