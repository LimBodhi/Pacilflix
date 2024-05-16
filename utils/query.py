from collections import namedtuple
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from django.db import connection

try:
    connection = psycopg2.connect(user="postgres.metqwdhmcccoqtmnxzzq",
                        password="5775eQ5ksZ9P0hF4",
                        host="aws-0-us-west-1.pooler.supabase.com",
                        port="5432",
                        database="postgres")

    # Create a cursor to perform database operations
    connection.autocommit = True
    cursor = connection.cursor()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [dict(row) for row in cursor.fetchall()]


def query(query_str: str):
    hasil = []
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SET SEARCH_PATH TO PACILFLIX")
        try:
            cursor.execute(query_str)

            if query_str.strip().upper().startswith("SELECT"):
                # Kalau ga error, return hasil SELECT
                hasil = map_cursor(cursor)
            else:
                # Kalau ga error, return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE
                hasil = cursor.rowcount
                connection.commit()
        except Exception as e:
            # Ga tau error apa
            hasil = e

    return hasil

def connectdb(func):
    def wrapper(request):
        res = ""
        with connection.cursor() as cursor:
            # cursor.execute("SET search_path to PACILFLIX;")
            res = func(cursor, request)
        return res
    return wrapper