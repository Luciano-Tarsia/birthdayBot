import telebot
import operator
from database_operations import *
from datetime import datetime, timedelta
from constants import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

# Definir un diccionario de mapeo de días de la semana en inglés a español
dias_semana_ingles = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dias_semana_espanol = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
mapeo_dias_semana = dict(zip(dias_semana_ingles, dias_semana_espanol))

# Función para obtener el nombre del día de la semana en español
def obtener_dia_semana_en_espanol(fecha):
    dia_semana_ingles = fecha.strftime("%A")
    dia_semana_espanol = mapeo_dias_semana.get(dia_semana_ingles, dia_semana_ingles)
    return dia_semana_espanol

@bot.message_handler(commands=["ayuda"])
def help(message):
    response = "Aquí tienes la lista de comandos disponibles y su descripción:\n\n"
    response += "/suscribir - Suscribe a un usuario al bot y lo registra en la base de datos si no está registrado. Ejemplo: /suscribir\n\n"
    response += "/registrar - Registra un cumpleaños en la base de datos del bot. Ejemplo: /registrar Luciano Tarsia 14/7\n\n"
    response += "/listar - Lista los cumpleaños registrados por el usuario. Ejemplo: /listar\n\n"
    response += "/actualizar - Actualiza la información de cumpleaños de un usuario en la base de datos. Ejemplo: /actualizar Luciano Tarsia 14/7\n\n"
    response += "/eliminar - Elimina un registro de cumpleaños de un usuario en la base de datos. Ejemplo: /eliminar Luciano Tarsia\n\n"
    response += "/listar_mes - Muestra los cumpleaños en el mes especificado. Ejemplo: /listar_mes [Número del mes]\n\n"
    response += "/listar_semana - Muestra los cumpleaños en la semana actual. Ejemplo: /listar_semana\n\n"

    bot.reply_to(message, response)


@bot.message_handler(commands=["suscribir"])
def subscribe(message):
    """
    Suscribe a un usuario al bot y lo registra en la base de datos si no está registrado.

    Args:
        message (telebot.types.Message): El objeto del mensaje que desencadenó la función.

    Returns:
        None
    """
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id

    if isRegister(user_id):
        response = f"Hola {username}, ya estás suscrito."
    else:
        data = {
            "userId": user_id,
            "username": username,
            "firstName": message.from_user.first_name,
            "chatId": chat_id,
            "deleted": 0,
        }
        addData(data, "MessagesRegister")
        response = f"Gracias, {username}. Ahora estás suscrito."

    bot.reply_to(message, response)


@bot.message_handler(commands=["registrar"])
def registerBirthday(message):
    """
    Registra un cumpleaños en la base de datos del bot.

    Args:
        message (telebot.types.Message): El objeto del mensaje que desencadenó la función.

    Returns:
        None

    Usage:
        /registrar [Nombre] [Apellido] [Día/Mes]
    """
    if not isRegister(message.from_user.id):
        response = "Usted no está suscrito. Para poder usar el bot, necesita estar suscrito. Utilice el comando /suscribirse para hacerlo."
    else:
        input = message.text.split()
        if len(input) != 4:
            response = "No estás utilizando el comando correctamente. Ejemplo de uso: /registrar Luciano Tarsia 14/7"
        else:
            date = input[3].split("/")
            try:
                day = int(date[0])
                month = int(date[1])
                if month < 1 or month > 12:
                    response = (
                        "El mes proporcionado no es válido. Debe estar entre 1 y 12."
                    )
                elif (
                    day < 1
                    or (month == 2 and day > 29)
                    or (day > 31 and (month in [1, 3, 5, 7, 8, 10, 12]))
                    or (day > 30 and (month in [4, 6, 9, 11]))
                ):
                    response = "La fecha proporcionada no es válida. Asegúrate de ingresar un día válido para el mes especificado."
                else:
                    # Verificar si ya existe un registro con el mismo nombre, apellido y userId
                    user_id = message.from_user.id
                    existing_records = getBirthdaysForUserId(user_id)
                    for record in existing_records:
                        if record["name"] == input[1] and record["surname"] == input[2]:
                            response = "Ya has registrado a una persona con el mismo nombre y apellido. No es posible registrar la misma persona más de una vez."
                            break
                    else:
                        data = {
                            "name": input[1],
                            "surname": input[2],
                            "birthdayDay": day,
                            "birthdayMonth": month,
                            "userId": user_id,
                            "deleted": 0,
                        }

                        response = "Trabajo en progreso..."
                        bot.reply_to(message, response)
                        addData(data, "Birthdays")
                        response = f"Listo. Recibirás un recordatorio del cumpleaños de {input[1]} {input[2]} el {day}/{month}"
            except ValueError:
                response = "La fecha proporcionada no es válida. Asegúrate de ingresar una fecha en el formato Día/Mes válido."

    bot.reply_to(message, response)


@bot.message_handler(commands=["listar"])
def listBirthdays(message):
    """
    Lista los cumpleaños registrados por el usuario.

    Args:
        message (telebot.types.Message): El objeto del mensaje que desencadenó la función.

    Returns:
        None
    """
    user_id = message.from_user.id
    if not isRegister(user_id):
        response = "Usted no está suscrito. Para poder usar el bot, necesita estar suscrito. Utilice el comando /suscribirse para hacerlo."
    else:
        data = getBirthdaysForUserId(user_id)
        if len(data) < 1:
            response = "Aún no has registrado ningún cumpleaños. Puedes utilizar el comando /registrar para hacerlo."
        else:
            data = sorted(data, key=operator.itemgetter("birthdayMonth", "birthdayDay"))
            response = "Esta es tu lista de cumpleaños registrados:\n"

            for reg in data:
                birthdayDay = reg["birthdayDay"]
                birthdayMonth = reg["birthdayMonth"]
                birthdayPersonName = reg["name"]
                birthdayPersonSurname = reg["surname"]

                aux = f"{birthdayPersonName} {birthdayPersonSurname} {birthdayDay}/{birthdayMonth}.\n"
                response = response + aux

    bot.reply_to(message, response)


@bot.message_handler(commands=["actualizar"])
def updateBirthday(message):
    """
    Actualiza la información de cumpleaños de un usuario en la base de datos.

    Args:
        message (telegram.Message): El mensaje que activa el comando.

    Returns:
        None

    Usage:
        /actualizar [Nombre] [Apellido] [Día/Mes]
    """

    if not isRegister(message.from_user.id):
        response = "Usted no está suscrito. Para poder usar el bot, necesita estar suscrito. Utilice el comando /suscribirse para hacerlo."
    else:
        input = message.text.split()
        if len(input) != 4:
            response = "No estás utilizando el comando correctamente. Ejemplo de uso: /actualizar Luciano Tarsia 14/7"
        else:
            date = input[3].split("/")
            response = "Trabajo en progreso..."
            bot.reply_to(message, response)
            updateBirthdayForUser(
                int(message.from_user.id),
                input[1],
                input[2],
                int(date[0]),
                int(date[1]),
            )
            response = f"Listo, ya lo actualizamos. Recibirás un recordatorio del cumpleaños de {input[1]} {input[2]} el {int(date[0])}/{int(date[1])}"

    bot.reply_to(message, response)


@bot.message_handler(commands=["eliminar"])
def deleteBirthday(message):
    """
    Elimina un registro de cumpleaños de un usuario en la base de datos.

    Args:
        message (telegram.Message): El mensaje que activa el comando.

    Returns:
        None

    Usage:
        /eliminar [Nombre] [Apellido]
    """

    if not isRegister(message.from_user.id):
        response = "Usted no está suscrito. Para poder usar el bot, necesita estar suscrito. Utilice el comando /suscribirse para hacerlo."
    else:
        input = message.text.split()
        if len(input) != 3:
            response = "No estás utilizando el comando correctamente. Ejemplo de uso: /eliminar Luciano Tarsia"
        else:
            response = "Trabajo en progreso..."
            bot.reply_to(message, response)

            deleteBirthdayForUser(
                int(message.from_user.id),
                input[1],
                input[2],
            )
            response = f"Listo, el registro fue eliminado."

    bot.reply_to(message, response)


@bot.message_handler(commands=["listar_mes"])
def birthdays_in_month(message):
    """
    Lista los cumpleaños de los usuarios registrados que tienen cumpleaños en el mes especificado.

    Args:
        message (telebot.types.Message): El objeto del mensaje que desencadenó la función.

    Returns:
        None
    """
    user_id = message.from_user.id

    if not isRegister(user_id):
        response = (
            "Debes suscribirte para usar esta función. Utiliza el comando /suscribir."
        )
    else:
        input = message.text.split()
        if len(input) != 2:
            response = "No estás utilizando el comando correctamente. Ejemplo de uso: /listar_mes 7"
        else:
            month_to_get = input[1]

            if not month_to_get.isdigit() or not 1 <= int(month_to_get) <= 12:
                response = "El mes proporcionado no es válido. Debe ser un número entre 1 y 12."
            else:
                data = getBirthdaysForUserId(user_id)
                data = sorted(
                    data, key=operator.itemgetter("birthdayMonth", "birthdayDay")
                )
                upcoming_birthdays = []

                for birthday in data:
                    if birthday["birthdayMonth"] == int(month_to_get):
                        upcoming_birthdays.append(birthday)

                if len(upcoming_birthdays) > 0:
                    response = "Cumpleaños en el mes:\n"
                    for birthday in upcoming_birthdays:
                        today = datetime.now()
                        day_of_week = obtener_dia_semana_en_espanol(today)

                        response += f"{birthday['name']} {birthday['surname']} - {birthday['birthdayDay']}/{birthday['birthdayMonth']} - {day_of_week}\n"
                else:
                    response = "No hay cumpleaños en el mes."

    bot.reply_to(message, response)


@bot.message_handler(commands=["listar_semana"])
def birthdays_in_week(message):
    """
    Lista los cumpleaños de los usuarios registrados que tienen cumpleaños en la semana actual.

    Args:
        message (telebot.types.Message): El objeto del mensaje que desencadenó la función.

    Returns:
        None
    """
    user_id = message.from_user.id

    if not isRegister(user_id):
        response = (
            "Debes suscribirte para usar esta función. Utiliza el comando /suscribir."
        )
    else:
        today = datetime.now()
        current_weekday = today.weekday()  # 0: Monday, 6: Sunday
        upcoming_birthdays = []

        data = getBirthdaysForUserId(user_id)
        data = sorted(data, key=operator.itemgetter("birthdayMonth", "birthdayDay"))

        for birthday in data:
            if (
                datetime(today.year, today.month, today.day)
                <= datetime(
                    today.year, birthday["birthdayMonth"], birthday["birthdayDay"]
                )
                <= today + timedelta(days=6 - current_weekday)
            ):
                upcoming_birthdays.append(birthday)

        if len(upcoming_birthdays) > 0:
            response = "Cumpleaños en la semana:\n"
            for birthday in upcoming_birthdays:
                today = datetime.now()
                day_of_week = obtener_dia_semana_en_espanol(today)

                response += f"{birthday['name']} {birthday['surname']} - {birthday['birthdayDay']}/{birthday['birthdayMonth']} - {day_of_week}\n"
        else:
            response = "No hay cumpleaños en la semana."

    bot.reply_to(message, response)
