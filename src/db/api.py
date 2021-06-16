import sqlite3

from config import Config


class DBApi:
    def __init__(self, db_filename: str):
        self.db_filename = db_filename
        self._init_connection()

    def insert(self, table: str, column_values: dict):
        columns = ', '.join(column_values.keys())
        values = [tuple(column_values.values())]
        placeholders = ", ".join("?" * len(column_values.keys()))
        self.cursor.executemany(
            f"INSERT INTO {table} "
            f"({columns}) "
            f"VALUES ({placeholders})",
            values
        )
        self.connection.commit()

    def fetchall(self, table: str, columns: list[str]) -> list[tuple]:
        columns_joined = ", ".join(columns)
        self.cursor.execute(f"SELECT {columns_joined} FROM {table}")
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result

    def delete(self, table: str, row_id: int):
        row_id = int(row_id)
        self.cursor.execute(f"delete from {table} where id={row_id}")
        self.connection.commit()

    def _init_connection(self):
        self.connection = sqlite3.connect(
            f"{Config.DB_DIR}/{self.db_filename}.db")
        self.cursor = self.connection.cursor()

        # if not self._check_db_exists():
        #     self.create_db()

    def _check_db_exists(self) -> bool:
        self.cursor.execute(f"SELECT name FROM {self.db_filename} "
                            "WHERE type='table'")
        table_exists = self.cursor.fetchall()
        if table_exists:
            return True
        return False

    def create_db(self):
        with open(f"{Config.SQL_SCRIPTS_DIR}/create_db.sql") as sql_script:
            sql = sql_script.read()
        self.cursor.executescript(sql)
        self.connection.commit()
