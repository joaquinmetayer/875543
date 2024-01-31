def init():
    with open('resource/contactos_autorizados.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[1]
        else:
            return lines[0]

