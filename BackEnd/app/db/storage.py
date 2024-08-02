import mysql.connector
from mysql.connector import Error
from os import getenv, path
from dotenv import load_dotenv


# Loading the environment variables
dotenv_path = path.join(path.dirname(__file__), '..', 'config', '.env')
load_dotenv(dotenv_path)


class Database:
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None
        self.db_config = {
            'host': getenv('FILES_HOST_DEV'),
            'user': getenv('FILES_USER_DEV'),
            'password': getenv('FILES_USER_PASS_DEV'),
            'database': getenv('FILES_DATABASE_DEV')
        }

    def connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Successfully connected.")
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def disconnect(self) -> None:
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Successfully disconnected.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.connection.rollback()
            print(f"Transaction failed: {exc_value}")
        else:
            self.connection.commit()
            print("Transaction committed.")
        self.disconnect()

    def create(self, table_name: str, **kwargs):
        columns = ', '.join(kwargs.keys())
        values = ', '.join(['%s'] * len(kwargs))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        try:
            self.cursor.execute(query, tuple(kwargs.values()))
            print("Record inserted successfully.")
        except Error as e:
            print(f"Error inserting record: {e}")
            raise 

    def read(self, table_name: str, **kwargs):
        condition = ' AND '.join([f"{key}=%s" for key in kwargs])
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        try:
            self.cursor.execute(query, tuple(kwargs.values()))
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Error reading records: {e}")
            raise

    def read_all(self, table_name: str)-> list:
        query = f"SELECT * FROM {table_name}"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Error reading records: {e}")
            raise

    def update(self, table_name: str, filter_params: dict, **update_params):
        update_declaration = ', '.join([f"{key}=%s" for key in update_params])
        filter_declaration = ' AND '.join(
            [f"{key}=%s" for key in filter_params])
        query = f"UPDATE {table_name} SET {update_declaration} WHERE {filter_declaration}"
        try:
            self.cursor.execute(query, tuple(
                update_params.values()) + tuple(filter_params.values()))
            print("Record updated successfully.")
        except Error as e:
            print(f"Error updating record: {e}")
            raise

    def delete(self, table_name:str, **kwargs):
        condition = ' AND '.join([f"{key}=%s" for key in kwargs])
        query = f"DELETE FROM {table_name} WHERE {condition}"
        try:
            self.cursor.execute(query, tuple(kwargs.values()))
            print("Record deleted successfully.")
        except Error as e:
            print(f"Error deleting record: {e}")
            raise
