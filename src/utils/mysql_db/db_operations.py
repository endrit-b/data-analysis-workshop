from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from .models import BaseModel, CurrencyExchangeRatesModel


class MySQLConnection:

    def __init__(self, username, password, host, db_name):
        self.session = None
        self.username = username
        self.password = password
        self.host = host
        self.db_name = db_name

    def connect(self):
        """
        Create a database connection with MySQL / create the database if it doesnt exist
        :return: obj
        """
        engine = create_engine(f"mysql://{self.username}:{self.password}@{self.host}/{self.db_name}")
        self.session = sessionmaker(bind=engine)()
        # Create the schema if it doesn't exist
        BaseModel.Declarative.metadata.create_all(engine, checkfirst=True)
        return self

    def insert_one(self, obj):
        """
        Inset one object into the table
        :param obj:
        :return:
        """
        self.session.add(obj)
        self.session.flush()
        self.session.commit()

    def insert_batch(self, list_of_objects: list):
        """
        Insert data into the table in batches
        :param list_of_objects:
        :return:
        """
        self.session.bulk_save_objects(list_of_objects)
        self.session.commit()

    def execute_sql_statement(self, sql_str):
        """
        :param sql_str:
        :return:
        """
        return self.session.execute(sql_str)

    def execute_sql_statement_with_type(self, data_type, sql_str):
        return self.session.query(data_type).from_statement(text(sql_str))

    def get_all_data(self, data_type):
        """
        Get data from database for a given data type (data model)
        :param data_type:
        :return:
        """
        return self.session.query(data_type).all()

    def close(self):
        """
        Close MySQL session
        :return:
        """
        self.session.close()

    # def drop(self, table_name):
    #     Base.metadata.drop_all(bind=self.session.engine, tables=[User.__table__])
