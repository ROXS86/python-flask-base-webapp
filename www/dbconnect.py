import mysql.connector
from mysql.connector import Error


def connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="web_app_flask",
            user="root",
            password="pwd",
        )

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)

    return cursor, connection
