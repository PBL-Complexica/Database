from datetime import datetime
from db_model import app
import json


class DatabaseMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(DatabaseMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=DatabaseMeta):
    def __init__(self):
        try:
            import psycopg2
        except ImportError:
            raise ImportError("Please install psycopg2: 'pip install psycopg2'")

        try:
            from flask_migrate import upgrade
        except ImportError:
            raise ImportError("Please install flask_migrate: 'pip install flask_migrate'")

        with app.app_context():
            upgrade()

        try:
            with open("config.json", "r") as f:
                cfg = json.loads(f.read())

                if any([cfg["database"]["host"], cfg["database"]["database"], cfg["database"]["user"], cfg["database"]["password"]]) == "":
                    raise ValueError("Please fill in the database configuration file")

                self.db = psycopg2.connect(
                    host=cfg["database"]["host"],
                    database=cfg["database"]["database"],
                    user=cfg["database"]["user"],
                    password=cfg["database"]["password"]
                )
                self.cursor = self.db.cursor()
        except FileNotFoundError:
            open("config.json", "w").write(json.dumps({
                "database": {
                    "host": "",
                    "database": "",
                    "user": "",
                    "password": ""
                }
            }, indent=4))
            raise FileNotFoundError("Please fill in the database configuration file")

        self.__populate()

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
            "INSERT INTO email_address (email_address, created_at) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (email_address, datetime.now())
        )
        self.db.commit()

    def insert_phone(self, phone_number):
        self.cursor.execute(
            "INSERT INTO phone_number (phone_number, created_at) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (phone_number, datetime.now())
        )
        self.db.commit()

    def insert_device(self, serial_number, device_name):
        self.cursor.execute(
            "INSERT INTO device (device_name, device_sn, created_at) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            (device_name, serial_number, datetime.now())
        )
        self.db.commit()

    def check_email(self, email_address, user_id):
        self.cursor.execute(
            "SELECT * FROM user_email WHERE email_id = (SELECT id FROM email_address WHERE email_address = %s) AND user_id = %s",
            (email_address, user_id)
        )
        return self.cursor.fetchall()

    def check_phone(self, phone_number, user_id):
        self.cursor.execute(
            "SELECT * FROM user_phone WHERE phone_id = (SELECT id FROM phone_number WHERE phone_number = %s) AND user_id = %s",
            (phone_number, user_id)
        )
        return self.cursor.fetchall()

    # Public methods
    def register(self, first_name, last_name, password, email_address, device_name=None, phone_number=None, birth_date=None):
        self.insert_user(first_name, last_name, password, birth_date)
        self.cursor.execute(
            "SELECT id FROM app_user WHERE first_name = %s AND last_name = %s AND password_hash = %s AND birth_date = %s",
            (first_name, last_name, password, birth_date)
        )
        user_id = self.cursor.fetchone()[0]
        self.insert_email(email_address)
        self.insert_phone(phone_number)
        # self.insert_device(device_name, device_name)
        print(self.check_email(email_address, user_id))
        print(self.check_phone(phone_number, user_id))

    # Populate database with initial data
    def __add_categories(self, name: str, prices: list):
        self.custom_query(
            "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) "
            "VALUES (%s, %s, %s, %s) "
            "ON CONFLICT DO NOTHING",
            (name + "-1", 1, prices[0], datetime.now())
        )
        self.custom_query(
            "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) "
            "VALUES (%s, %s, %s, %s) "
            "ON CONFLICT DO NOTHING",
            (name + "-3", 3, prices[1], datetime.now())
        )
        self.custom_query(
            "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) "
            "VALUES (%s, %s, %s, %s) O"
            "N CONFLICT DO NOTHING",
            (name + "-6", 6, prices[2], datetime.now())
        )

    def __add_user_categories(self, name: str):
        self.custom_query(
            "INSERT INTO category (category_name, created_at) "
            "VALUES (%s, %s) "
            "ON CONFLICT DO NOTHING",
            (name, datetime.now())
        )

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

