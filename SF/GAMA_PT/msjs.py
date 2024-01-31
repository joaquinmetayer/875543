def msj_bienvenida(nombre_robot):
    msj = f"Hola! Bienvenido, soy *{nombre_robot}* y estoy todo el día a tu disposición para cargar fichas, retirar, derivar con nuestro equipo y más...!"
    return msj

def msj_no_user():    
    msj = "No encontré un *usuario* asociado a tu número de teléfono!" 
    msj0 = "*Creemos uno:* ¿cómo querés que sea tu usuario?"
    msj1 = "Puede tener letras  *minúsculas*  y *números*"
    msj2 = "Debe ser de 4 hasta 16 caracteres."
    msj3 = "Debe comenzar con una letra."
    msj4 = "Sin acentos ni simbolos."
    msj5 = "Ejemplo: jorge505"
    msj6 = "Por favor, respondé con un solo mensaje"
    return msj, msj0, msj1, msj2, msj3, msj4, msj5, msj6

def msj_err_crear_user():
    msj = "*Hubo un problema al crear tu usuario*"
    msj0 = "Parece que ese usuario ya existe. ¿Se te ocurre otro?"
    msj1 = "Por favor, respondé con un solo mensaje"
    return msj, msj0, msj1

def msj_user_creado(web_jugador):
    msj = f"*Listo.* Sos bienvenido a nuestra plataforma: {web_jugador}"
    msj0 = "Te creamos una contraseña *temporal*: Hola123"
    msj1 = "Después tenés que poner una vos. ¡No se la digas a nadie!"
    msj2 = "_*¡Ahora a jugar! !MUCHA SUERTE!*_"
    return msj, msj0, msj1, msj2

def msj_a_jugar(web_jugador):   
    msj = f"""¡Ahora, a jugar! {web_jugador}
            Te deseo  MUCHA SUERTE """
    return msj

def msj_menu_acciones(usuario,web_jugador):
    msj = f"Tu usuario es: *{usuario}*"
    msj0 = f"Plataforma: {web_jugador}"
    msj1 = "Escribí el número según lo que quieras hacer:"
    msj2 = "*1* - Cargar Fichas"
    msj3 = "*2* - Cambiar Contraseña"
    msj4 = "*3* - Retirar Fichas"
    msj5 = "*4* - Desbloquear Cuenta"
    msj6 = "*5* - Atención al cliente"
    return msj, msj0, msj1, msj2, msj3, msj4, msj5, msj6

def msj_no_entendi():
    msj = """No entendí qué quisiste decir """
    return msj

def msj_pasos_transf(alias,cbu,nombre_cuenta):
    msj = "Seguí estos pasos para cargar fichas: *(CARGA MINIMA $600)* "
    msj0 ="*# PASO 1*"
    msj1 = f"""Hacé una transferencia con la cantidad a cargar al alias o CBU que te envio
        {alias}
        {cbu}
        Nombre: {nombre_cuenta}"""
    msj2 ="*# PASO 2*"
    msj3 ="Una vez transferido el dinero, volvé al chat y continuá con el *#PASO 3*"
    msj4 ="Tené en cuenta que a veces las transferencias pueden demorar un tiempo en ser recibidas"
    msj5 ="*# PASO 3*"
    msj6 = "Escribí el nombre completo de la cuenta de la cual hiciste la transferencia. *(como aparece en tu app)*"
    msj7 = "Ejemplo: Sofia Abigail Botino"
        
    return msj, msj0, msj1, msj2, msj3, msj4, msj5, msj6, msj7

def msj_nombre_transf_recibido():
    msj = "*Excelente, ahora reviso.* Apenas llegue te cargo las fichas y te aviso. Si ves que no te respondi dentro de 5 minutos, volve a escribirme."
    return msj

def msj_err_nombre_transf():
    msj = "Por favor, enviame el nombre completo con el que transferiste. \n O la palabra *CANCELAR* para volver al menu."
    return msj

def msj_pago_no_confirmado():
    msj = "No encontré ninguna transferencia a tu nombre"
    msj0 = "Tené en cuenta que las transferencias pueden tomar hasta treinta minutos en acreditarse"
    msj1 = "Probemos de nuevo: escribi el nombre completo de la cuenta desde la que transferiste, *(como aparece en la app)*."
    msj2 = "Para descartar este proceso, escribí *CANCELAR*"
    return msj, msj0, msj1, msj2

def msj_confirmacion_pw():
    msj = """¿Estás seguro de que querés cambiar tu contraseña? Tu nueva contraseña será *Hola123* y podes cambiarla cuando vuelvas a iniciar sesión
    - Si querés continuar el proceso, escribí *CONFIRMAR* en el siguiente mensaje
    - Si querés cancelar el proceso, escribí *CANCELAR* en el siguiente mensaje"""
    return msj

def msj_cambio_pw_exitoso():
    msj = "*Listo.* Tu contraseña ahora es *Hola123*"
    return msj

def msj_cancelar():
    msj = "Te confirmo que cancele lo que estabamos haciendo"
    return msj

def msj_user_desbloqueado():
    msj = "*Listo.* Ya podes volver a entrar. Si llegase a seguir bloqueado, repeti este proceso una vez más."
    return msj

def msj_user_no_bloqueado():
    msj = "*Tu usuario no esta bloqueado.* Te habras olvidado la contraseña? Si es asi, entra en la opcion 2 y te ayudo."
    return msj

def msj_carga_exitosa(web_jugador):
    msj = "*Listo. Ya tenes tus fichas en tu panel.* Cuando quieras volve a escribime."
    msj0 = f"Ahora a jugar en: {web_jugador}"
    msj1 = "_*¡MUCHA SUERTE!*_"
    return msj, msj0, msj1

def msj_descarga_exitosa():
    msj = "*Listo.* Tu descarga ya fue transferida. ¡FELICIDADES POR TU PREMIO!"
    return msj

def msj_carga_cancelada():
    msj = "Me ordenaron cancelar esta operacion por transferencia inexistente. *Realmente queres cargar fichas?*"
    return msj

def msj_descarga_cancelada():
    msj = "Me ordenaron cancelar esta operacion. *Realmente queres descargar fichas?*. Podes volver a entrar a la opcion 3. O opcion 5 para comunicarte con atencion al cliente."
    return msj

def msj_atencion_cliente():
    msj = "*Listo. Tu solicitud ya fue asignada,* dentro de unos minutos se comunicara una persona fisica con vos."
    return msj

def msj_err_reglas_user(usuario):
    msj = f"*{usuario}* tiene una longitud de *{len(usuario)}*. Recorda debe contener más de 6 letras y menos de 18. Probemos con otro"
    return msj

def msj_err_no_num():
    msj = "Recorda que no puede empezar con un número. Enviame otro"
    return msj

def msj_confirmacion_datos():
    msj = """*Empecemos el proceso de retiro.* Enviame cuantas fichas queres retirar, seguido de tu CBU o ALIAS. Todo en un mismo mensaje.
    Ejemplo: 1000 alias.roca.rojo"""
    return msj

def msj_err_formato_datos_retiro():
    msj = """*Error.* Enviame la cantidad de fichas que queres retirar seguido de tu ALIAS o CBU. Todo en un mismo mensaje.
             O la palabra *CANCELAR*, para volver al menu."""
    return msj

def msj_err_cantidad_fichas(fichas_a_retirar, fichas_reales):
    msj = f"""No tenes *{fichas_a_retirar}* en tu cuenta. tenes *{fichas_reales}* . Enviame de nuevo cuantas fichas queres retirar seguido de tu CBU o ALIAS. Todo en un mismo mensaje.
            O la palabra *CANCELAR*, para volver al menu."""
    return msj

def msj_datos_retiro(fichas_a_retirar, cbu):
    msj = f"""*Listo*. {fichas_a_retirar} fichas van a ser retiradas de tu cuenta.
           *Ya genere la solicitud al administrador.* Te aviso cuando la transferencia haya sido realizada al cbu/alias: *{cbu}*"""
    return msj

def msj_err_datos_retiro():
    msj = "*Error.* Enviame por favor, tu cbu más el nombre de tu cuenta a recibir. (tal como aparece en tu app)"
    return msj

def msj_solicitud_retiro():
    msj = """*Listo. Tu solicitud de retiro ya fue asignada.* Dentro de unos minutos se comunicara una persona fisica con vos."""
    return msj

def msj_info_solicitud_retiro(id):
    msj = f"Por cualquier duda sobre tu solicitud, podes comunicarte con atención al cliente proporcionandole el siguiente codigo: *SOL-DESC-{id}*"
    return msj
