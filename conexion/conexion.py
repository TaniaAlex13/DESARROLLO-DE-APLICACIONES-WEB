import os

import psycopg
from psycopg.rows import dict_row


def obtener_conexion():

    database_url = os.getenv("DATABASE_URL")

    if database_url:

        conexion = psycopg.connect(
            database_url,
            row_factory=dict_row
        )

    else:

        conexion = psycopg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="123456",
            dbname="ferreteria",
            row_factory=dict_row
        )

    return conexion