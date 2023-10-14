import threading
from commands import bot
from scheduling import schedule_thread

# Inicio los hilos
bot_thread = threading.Thread(target=bot.infinity_polling)
bot_thread.start()

schedule_thread = threading.Thread(target=schedule_thread)
schedule_thread.start()
