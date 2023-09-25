import sqlalchemy


class Database:
    def __init__(self):
        self.db = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost:5432/postgres')


