from firebase import firebase
from constants import DATABASE_URL

# DataBase CRUD operations

firebase_app = firebase.FirebaseApplication(DATABASE_URL, None)


# Manejo de errores personalizado
class FirebaseError(Exception):
    pass


def addData(data, collection):
    """
    Agrega datos a una colección en la base de datos Firebase.

    Args:
        data (dict): Los datos que se agregarán a la colección.
        collection (str): El nombre de la colección en la que se agregarán los datos.

    Returns:
        dict: El resultado de la operación de inserción.

    """
    result = firebase_app.post(f"/birthdayBot/{collection}/", data)
    return result


def getData(collection):
    """
    Obtiene datos de una colección en la base de datos Firebase.

    Args:
        collection (str): El nombre de la colección de la que se obtendrán los datos.

    Returns:
        dict: Los datos obtenidos de la colección.

    Raises:
        FirebaseError: Se lanza si ocurre un error al obtener datos.

    """
    try:
        result = firebase_app.get(f"/birthdayBot/{collection}/", "")
        return result
    except Exception as e:
        raise FirebaseError(f"Error al obtener datos de {collection}: {e}")


def isRegister(userId):
    """
    Verifica si un usuario está registrado en la base de datos.

    Args:
        userId (str): El ID de usuario a verificar.

    Returns:
        bool: True si el usuario está registrado; False en caso contrario.

    """
    data = getData("MessagesRegister")
    return any(reg["userId"] == userId and reg["deleted"] == 0 for reg in data.values())


def getRegisteredUsers():
    """
    Obtiene la lista de usuarios registrados.

    Returns:
        list: Una lista de diccionarios con información de usuarios registrados.

    """
    data = getData("MessagesRegister")
    return [
        {
            "userId": user_data["userId"],
            "username": user_data["username"],
            "firstName": user_data["firstName"],
            "chatId": user_data["chatId"],
        }
        for user_data in data.values()
        if user_data["deleted"] == 0
    ]


def getBirthdaysForUserId(userId):
    """
    Obtiene los cumpleaños de un usuario específico.

    Args:
        userId (str): El ID de usuario para el que se obtienen los cumpleaños.

    Returns:
        list: Una lista de cumpleaños del usuario.

    """
    data = getData("Birthdays")
    return [
        reg for reg in data.values() if reg["userId"] == userId and reg["deleted"] == 0
    ]


def getBirthdaysForToday(day, month, userId):
    """
    Obtiene los cumpleaños de un usuario que coinciden con la fecha actual.

    Args:
        day (int): El día actual.
        month (int): El mes actual.
        userId (str): El ID de usuario para el que se obtienen los cumpleaños.

    Returns:
        list: Una lista de cumpleaños del usuario que coinciden con la fecha actual.

    """
    birthdays = getBirthdaysForUserId(userId)
    return [
        birthday
        for birthday in birthdays
        if birthday["birthdayDay"] == day
        and birthday["birthdayMonth"] == month
        and birthday["deleted"] == 0
    ]


def getBirthdaysInRange(start_day, start_month, end_day, end_month, user_id):
    """
    Obtiene los cumpleaños de un usuario que caen en un rango de fechas especificado.

    Args:
        start_day (int): El día de inicio del rango.
        start_month (int): El mes de inicio del rango.
        end_day (int): El día de finalización del rango.
        end_month (int): El mes de finalización del rango.
        user_id (str): El ID de usuario para el que se obtienen los cumpleaños.

    Returns:
        list: Una lista de cumpleaños del usuario que caen en el rango de fechas.

    """
    birthdays = getBirthdaysForUserId(user_id)
    return [
        birthday
        for birthday in birthdays
        if start_month <= birthday["birthdayMonth"] <= end_month
        and end_day >= birthday["birthdayDay"] >= start_day
        and birthday["deleted"] == 0
    ]


def updateBirthdayForUser(userId, name, surname, newBirthdayDay, newBirthdayMonth):
    """
    Actualiza la fecha de cumpleaños de un usuario en la base de datos.

    Args:
        userId (str): El ID de usuario.
        name (str): El nombre del usuario.
        surname (str): El apellido del usuario.
        newBirthdayDay (int): El nuevo día de cumpleaños.
        newBirthdayMonth (int): El nuevo mes de cumpleaños.

    Raises:
        FirebaseError: Se lanza si ocurre un error al actualizar el cumpleaños.

    """
    data = getData("Birthdays")
    for key, record in data.items():
        if (
            record["userId"] == userId
            and record["name"] == name
            and record["surname"] == surname
            and record["deleted"] == 0
        ):
            record["birthdayDay"] = newBirthdayDay
            record["birthdayMonth"] = newBirthdayMonth
            try:
                firebase_app.put("/birthdayBot/Birthdays", key, record)
            except Exception as e:
                raise FirebaseError(f"Error al actualizar el cumpleaño: {e}")


def deleteBirthdayForUser(userId, name, surname):
    """
    Elimina un registro de cumpleaños de un usuario en la base de datos.

    Args:
        userId (str): El ID de usuario.
        name (str): El nombre del usuario.
        surname (str): El apellido del usuario.

    Raises:
        FirebaseError: Se lanza si ocurre un error al eliminar el registro.

    """
    data = getData("Birthdays")
    for key, record in data.items():
        if (
            record["userId"] == userId
            and record["name"] == name
            and record["surname"] == surname
        ):
            record["deleted"] = 1
            try:
                firebase_app.put("/birthdayBot/Birthdays", key, record)
            except Exception as e:
                raise FirebaseError(f"Error al eliminar el registro: {e}")
