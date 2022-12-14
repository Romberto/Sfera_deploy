from collections import namedtuple

import psycopg2
from config import DATABASE

Driver = namedtuple('Driver', [
    'id',
    'driver_name',
    'driver_last_name',
    'phone',
    'login',
    'password',
    'salt',
    'password_hash'


])


def connect():
    try:
        connection = psycopg2.connect(user=DATABASE['USER'],
                                      # пароль, который указали при установке PostgresSQL
                                      password=DATABASE['PASSWORD'],
                                      host=DATABASE['HOST'],
                                      port="5432",
                                      dbname=DATABASE['NAME'])
        return connection

    except Exception as _ex:
        print("*" * 20, " ошибка ", "*" * 20)
        print(_ex)
        return False


async def get_user_db(login):
    # возвращает пользователя по username
    conn = connect()
    if conn:

        try:
            cursor = conn.cursor()
            # Выполнение SQL-запроса

            cursor.execute("SELECT * FROM drivers_drivermodel WHERE login='" + login + "';")
            # Получить результат
            record = cursor.fetchone()
            driver = Driver(
                id=record[0],
                driver_name=record[1],
                driver_last_name=record[2],
                phone=record[3],
                login=record[4],
                password=record[5],
                salt=record[6],
                password_hash=record[7]
            )
            cursor.close()
            return driver

        except Exception as _err:
            print(' config_db.py => get_user_db()', _err)
            return None
        finally:
            conn.close()

    else:
        print("проблемы с подключением к базе")

async def get_user_chat_id(chat_id):
    pass


# Регистрация пользователя в базе
async def add_user(user_id, driver):
    # добавляет  chat_id в таблицу auth_user_authuserbot
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE drivers_drivermodel "
                           "SET bot_user_id=" + user_id + ""
                                                          "WHERE id=" + str(driver) + ";")
            conn.commit()
            cursor.close()
        except Exception as _ex:
            print('config_db.py => add_user ', _ex)

        finally:
            conn.close()
    else:
        print("проблемы с подключением к базе")


# Проверяет регистрацию бота в базе данных
async def check_auth(_id: str):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM drivers_drivermodel WHERE bot_user_id='" + _id + "'")
            record = cursor.fetchone()
            conn.close()
            driver = Driver(
                id=record[0],
                driver_name=record[1],
                driver_last_name=record[2],
                phone=record[3],
                login=record[4],
                password=record[5],
                salt=record[6],
                password_hash=record[7]
            )
            cursor.close()
            return driver
        except Exception as _err:
            print(_err)
            return False
        finally:
            conn.close()
    else:
        print("проблемы с подключением к базе")
