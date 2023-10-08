from datetime import datetime
from db_model import app
from dotenv import dotenv_values
import json
import os


class DatabaseMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DatabaseMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=DatabaseMeta):
    def __init__(self):
        # Check if psycopg2 is installed
        try:
            import psycopg2
        except ImportError:
            raise ImportError("Please install psycopg2: 'pip install psycopg2'")

        # Check if flask_migrate is installed
        try:
            from flask_migrate import upgrade
        except ImportError:
            raise ImportError("Please install flask_migrate: 'pip install flask_migrate'")

        with app.app_context():
            upgrade()

        # Load environment variables
        config = dotenv_values(".env")
        self.db = psycopg2.connect(
            host=config["DB_HOST"],
            database=config["DB_DATABASE"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"]
        )
        self.cursor = self.db.cursor()

        # Remove unconfirmed users
        self.remove_unconfirmed()

        # Populate database with initial data
        self.__populate()

    # Private methods
    # Insert new user
    def __insert_user(self, first_name, last_name, password_hash, birth_date=None):
        self.cursor.execute(
            "INSERT INTO app_user (first_name, last_name, password_hash, birth_date, created_at) VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, password_hash, birth_date, datetime.now())
        )
        self.db.commit()

    # Insert new email
    def __insert_email(self, email_address):
        self.cursor.execute(
            "INSERT INTO email_address (email_address, created_at) "
            "VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (email_address, datetime.now())
        )
        self.db.commit()

    # Insert new phone number
    def __insert_phone(self, phone_number):
        self.cursor.execute(
            "INSERT INTO phone_number (phone_number, created_at) "
            "VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (phone_number, datetime.now())
        )
        self.db.commit()

    # Insert new device
    def __insert_device(self, serial_number, device_name):
        self.cursor.execute(
            "INSERT INTO device (device_name, device_sn, created_at) "
            "VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            (device_name, serial_number, datetime.now())
        )
        self.db.commit()

    # Return user's for a given active email address
    def __check_email(self, email_address):
        self.cursor.execute(
            "SELECT user_id FROM user_email "
            "WHERE email_id = (SELECT id FROM email_address WHERE email_address = %s) AND removed_at > %s",
            (email_address, datetime.now())
        )
        return self.cursor.fetchall()

    # Return user's for a given active phone number
    def __check_phone(self, phone_number):
        self.cursor.execute(
            "SELECT user_id FROM user_phone "
            "WHERE created_at = (SELECT id FROM phone_number WHERE phone_number = %s) AND removed_at > %s",
            (phone_number, datetime.now())
        )
        return self.cursor.fetchall()

    # Return devices associated with a user device
    def __check_device(self, serial_number):
        self.cursor.execute(
            "SELECT user_id FROM user_device "
            "WHERE created_at = (SELECT id FROM device WHERE device_sn = %s) AND removed_at > %s",
            (serial_number, datetime.now())
        )
        return self.cursor.fetchall()

    # Public methods
    # Remove unconfirmed users
    def remove_unconfirmed(self):
        self.cursor.execute(
            "DELETE FROM app_user WHERE confirmed = FALSE"
        )
        self.db.commit()

    # Create new user and associate it with an email, phone number and device
    # TODO: Finish
    def register(
            self,
            first_name,
            last_name,
            password,
            email_address,
            device_name=None,
            device_sn=None,
            phone_number=None,
            birth_date=None
    ):
        self.__insert_email(email_address)
        self.__insert_phone(phone_number)
        self.__insert_device(device_sn, device_name)

        # Get new email's id
        self.cursor.execute(
            "SELECT id FROM email_address "
            "WHERE email_address = %s",
            (email_address,)
        )
        email_id = self.cursor.fetchone()[0] if email_address is not None else None

        # Get new phone's id
        self.cursor.execute(
            "SELECT id FROM phone_number "
            "WHERE phone_number = %s",
            (phone_number,)
        )
        phone_id = self.cursor.fetchone()[0] if phone_number is not None else None

        # Get new device's id
        self.cursor.execute(
            "SELECT id FROM device "
            "WHERE device_sn = %s",
            (device_sn,)
        )
        device_id = self.cursor.fetchone()[0] if device_sn is not None else None

    # Populate database with initial data
    def __add_categories(self, name: str, prices: list):
        self.cursor.execute(
            "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) "
            "VALUES (%s, %s, %s, %s) "
            "ON CONFLICT DO NOTHING",
            (name + "-1", 1, prices[0], datetime.now())
        )
        self.cursor.execute(
            "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) "
            "VALUES (%s, %s, %s, %s) "
            "ON CONFLICT DO NOTHING",
            (name + "-3", 3, prices[1], datetime.now())
        )
        self.cursor.execute(
            "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) "
            "VALUES (%s, %s, %s, %s) O"
            "N CONFLICT DO NOTHING",
            (name + "-6", 6, prices[2], datetime.now())
        )
        self.db.commit()

    def __add_user_categories(self, name: str):
        self.cursor.execute(
            "INSERT INTO category (category_name, created_at) "
            "VALUES (%s, %s) "
            "ON CONFLICT DO NOTHING",
            (name, datetime.now())
        )
        self.db.commit()

    def __populate(self):
        self.__add_categories("G", [234, 594, 972])
        self.__add_categories("ST", [164, 416, 680])
        self.__add_categories("E", [117, 297, 486])
        self.__add_categories("AE", [234, 594, 972])
        self.__add_categories("FM", [140, 356, 583])
        self.__add_categories("FC", [117, 297, 483])
        self.__add_categories("DI", [164, 416, 680])
        self.__add_categories("DM", [164, 416, 680])
        self.__add_user_categories("general")
        self.__add_user_categories("student")
        self.__add_user_categories("elev")
        self.__add_user_categories("agent economic")
        self.__add_user_categories("familie monoparentala")
        self.__add_user_categories("familie cu multi copii")
        self.__add_user_categories("personal didactic")
        self.__add_user_categories("personal medical")
