import schedule
import telebot
import time
import datetime as dt
from database_operations import *
from constants import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


def send_birthday_reminders():
    """
    Envía recordatorios de cumpleaños a los usuarios registrados para el día actual.

    Esta función busca los cumpleaños de los usuarios registrados que coincidan con la fecha
    actual y envía un mensaje a cada usuario para recordarles sobre los cumpleaños.

    Args:
        No recibe argumentos, ya que utiliza la fecha actual.

    Returns:
        None

    """
    current_date = dt.datetime.now()
    registered_users = getRegisteredUsers()
    for user in registered_users:
        # Obtén todos los cumpleaños para el día actual
        chat_id = user["chatId"]
        user_id = user["userId"]
        birthdays = getBirthdaysForToday(current_date.day, current_date.month, user_id)

        if birthdays:
            for birthday in birthdays:
                name = birthday["name"]
                surname = birthday["surname"]
                bot.send_message(chat_id, f"Hoy es el cumpleaños de {name} {surname}")


def send_weekly_birthday_reminders():
    """
    Envía recordatorios de cumpleaños de la semana a los usuarios registrados los lunes.

    Esta función busca los cumpleaños de los usuarios registrados que caen dentro de la semana actual,
    que se define como desde el lunes al domingo, y envía un mensaje los lunes a cada usuario con los cumpleaños de la semana.

    Args:
        No recibe argumentos, ya que se ejecuta los lunes automáticamente.

    Returns:
        None

    """
    current_date = dt.datetime.now()
    current_day_of_week = current_date.weekday()  # 0 para lunes, 1 para martes, etc.

    # Calcula el inicio y fin de la semana (lunes a domingo)
    start_of_week = current_date - dt.timedelta(days=current_day_of_week)
    end_of_week = start_of_week + dt.timedelta(days=6)

    registered_users = getRegisteredUsers()

    for user in registered_users:
        chat_id = user["chatId"]
        user_id = user["userId"]
        birthdays = getBirthdaysInRange(
            start_of_week.day,
            start_of_week.month,
            end_of_week.day,
            end_of_week.month,
            user_id,
        )

        if birthdays:
            message = "Cumpleaños de la semana:\n"
            for birthday in birthdays:
                name = birthday["name"]
                surname = birthday["surname"]
                birthdayDay = birthday["birthdayDay"]
                birthdayMonth = birthday["birthdayMonth"]
                message += f"{name} {surname} {birthdayDay}/{birthdayMonth}\n"

            bot.send_message(chat_id, message)


def schedule_thread():
    """
    Ejecuta las tareas programadas de acuerdo a la lógica definida.

    Esta función programa dos tareas: una para enviar recordatorios de cumpleaños diariamente a las 10:00 AM y otra para enviar recordatorios de cumpleaños de la semana todos los lunes a las 9:59 AM.

    Args:
        No recibe argumentos.

    Returns:
        None
    """
    schedule.every().day.at("10:00").do(send_birthday_reminders)
    schedule.every().monday.at("09:59").do(send_weekly_birthday_reminders)

    while True:
        schedule.run_pending()
        time.sleep(1)
