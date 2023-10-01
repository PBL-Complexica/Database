import psycopg2
from datetime import datetime


class Database:
    def __init__(self, host="localhost"):
        self.db = psycopg2.connect(
            host=host,
            database="postgres",
            user="postgres",
            password="postgres"
        )
        self.cursor = self.db.cursor()

    def custom_query(self, query, values: tuple):
        self.cursor.execute(query, values)
        self.db.commit()
        if query.startswith("SELECT"):
            return self.cursor.fetchall()

    def insert_user(self, first_name, last_name, password_hash, birth_date=None):
        self.cursor.execute(
            "INSERT INTO app_user (first_name, last_name, password_hash, birth_date, created_at) VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, password_hash, birth_date, datetime.now())
        )
        self.db.commit()

    def insert_email(self, email_address):
        self.cursor.execute(
            "INSERT INTO email_address (email_address, created_at) VALUES (%s, %s)",
            (email_address, datetime.now())
        )
        self.db.commit()

    def insert_phone(self, phone_number):
        self.cursor.execute(
            "INSERT INTO phone_number (phone_number, created_at) VALUES (%s, %s)",
            (phone_number, datetime.now())
        )
        self.db.commit()

    def insert_device(self, serial_number, device_name):
        self.cursor.execute(
            "INSERT INTO device (device_name, device_sn, created_at) VALUES (%s, %s, %s)",
            (device_name, serial_number, datetime.now())
        )
        self.db.commit()
