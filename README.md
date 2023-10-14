# Bot de Telegram de Cumpleaños 

Esta aplicación te permite gestionar y recibir recordatorios de cumpleaños. A continuación, te proporcionamos una guía detallada sobre cómo utilizar esta aplicación y cómo está organizado su código.

## Descripción General
El Bot de Telegram de Cumpleaños es una herramienta que te permite realizar las siguientes funciones:

- Suscribirte al bot y registrarte en la base de datos.
- Registrar cumpleaños de amigos y familiares en la base de datos.
- Listar los cumpleaños registrados por ti.
- Actualizar la información de los cumpleaños registrados.
- Eliminar registros de cumpleaños.
- Listar cumpleaños en un mes específico.
- Listar cumpleaños en la semana actual.

## Estructura de la Aplicación
La aplicación está dividida en tres archivos principales: `commands.py`, `scheduling.py`, y `main.py`.

### 1. `commands.py`
Este archivo contiene todas las funciones que manejan los comandos del bot y la lógica de la aplicación. Aquí se definen los comandos disponibles, como suscribir, registrar, listar, actualizar, eliminar, listar_mes y listar_semana. Las funciones en este archivo gestionan la interacción del usuario con el bot.

### 2. `scheduling.py`
En este archivo, se implementa la funcionalidad de enviar recordatorios de cumpleaños. El archivo incluye dos funciones: `send_birthday_reminders` y `send_weekly_birthday_reminders`. La primera función envía recordatorios diarios de cumpleaños, mientras que la segunda envía recordatorios semanales los lunes. Estas funciones son programadas para ser ejecutadas en momentos específicos del día o de la semana.

### 3. `main.py`
Este archivo es el punto de entrada de la aplicación. Inicia dos hilos para ejecutar el bot de Telegram y las tareas programadas definidas en los archivos `commands.py` y `scheduling.py`.

## Uso de la Aplicación
Para utilizar el bot, sigue estos pasos:

1. Suscríbete al bot con el comando `/suscribir`. Esto te registrará en la base de datos y permitirá que el bot te envíe recordatorios de cumpleaños.

2. Registra cumpleaños utilizando el comando `/registrar [Nombre] [Apellido] [Día/Mes]`. Asegúrate de seguir el formato indicado. Ejemplo: `/registrar Luciano Tarsia 14/7`.

3. Lista tus cumpleaños registrados con el comando `/listar`.

4. Actualiza información de cumpleaños con el comando `/actualizar [Nombre] [Apellido] [Día/Mes]`. También sigue el formato indicado.

5. Elimina registros de cumpleaños con el comando `/eliminar [Nombre] [Apellido]`.

6. Lista cumpleaños en un mes específico con el comando `/listar_mes [Número del mes]`.

7. Lista cumpleaños de la semana actual con el comando `/listar_semana`.

## Tareas Programadas
El bot está programado para enviar recordatorios de cumpleaños a diario a las 10:00 AM y recordatorios semanales los lunes a las 9:59 AM. Estas tareas están definidas en el archivo `scheduling.py` y se ejecutan en segundo plano.

¡Disfruta utilizando el Bot de Telegram de Cumpleaños para nunca olvidar un cumpleaños importante! Si tienes alguna pregunta o necesitas asistencia adicional, no dudes en contactarnos.

¡Gracias por usar nuestra aplicación!
