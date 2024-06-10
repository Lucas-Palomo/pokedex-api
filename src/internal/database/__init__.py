import psycopg2
from psycopg2._psycopg import connection as Connection, cursor as Cursor
from pypika import Table, PostgreSQLQuery


def insert(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


class Database:
    host: str
    port: int

    user: str
    password: str
    database: str

    conn: Connection

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def execute(self, query: str):
        cursor: Cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def fetchall(self, query: str) -> list[tuple]:
        cursor: Cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def fetchone(self, query: str) -> tuple:
        cursor: Cursor = self.conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()

    def open(self):
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
