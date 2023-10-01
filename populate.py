import psycopg2
from datetime import datetime
from Database import Database


db = Database()


def add_categories(name: str, prices: list):
    db.custom_query(
        "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) VALUES (%s, %s, %s, %s)",
        (name + "-1", 1, prices[0], datetime.now())
    )
    db.custom_query(
        "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) VALUES (%s, %s, %s, %s)",
        (name + "-3", 3, prices[1], datetime.now())
    )
    db.custom_query(
        "INSERT INTO subscription_type (subscription_type_name, months, cost, created_at) VALUES (%s, %s, %s, %s)",
        (name + "-6", 6, prices[2], datetime.now())
    )


def add_user_categories(name: str):
    db.custom_query(
        "INSERT INTO category (category_name, created_at) VALUES (%s, %s)",
        (name, datetime.now())
    )


def main():
    add_categories("G", [234, 594, 972])
    add_categories("ST", [164, 416, 680])
    add_categories("E", [117, 297, 486])
    add_categories("AE", [234, 594, 972])
    add_categories("FM", [140, 356, 583])
    add_categories("FC", [117, 297, 483])
    add_categories("DI", [164, 416, 680])
    add_categories("DM", [164, 416, 680])
    add_user_categories("general")
    add_user_categories("student")
    add_user_categories("elev")
    add_user_categories("agent economic")
    add_user_categories("familie monoparentala")
    add_user_categories("familie cu multi copii")
    add_user_categories("personal didactic")
    add_user_categories("personal medical")


if __name__ == '__main__':
    main()
