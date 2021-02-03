import os
import pytest

from src.utils.mysql_db import MySQLConnection
from src.utils.mysql_db.models import CurrencyExchangeRatesModel
from src.utils import load_env_vars
from src.data_mining.process_exchange_rates import CurrencyExchangeRates

from .utils.fakes import FakeDB


@pytest.fixture(scope="module")
def database_conn():
    # Load test variables
    load_env_vars('test')

    print(os.getenv('MYSQL_USERNAME'))
    # Init database connection
    conn = MySQLConnection(os.getenv('MYSQL_USERNAME'), os.getenv('MYSQL_PASSWORD'),
                           f"{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}",
                           "test_exchange_rates").connect()

    # Insert a record for testing
    CurrencyExchangeRates(conn).download_exchange_rates_data('USD')

    # Pass execution
    yield conn

    # Delete the test table
    conn.execute_sql_statement('DROP TABLE curr_exchange_rates')
    conn.close()


def test_util_execute_sql_statement(database_conn):
    assert 1 == len(list(database_conn.execute_sql_statement_with_type(CurrencyExchangeRatesModel,
                                                                       "select * from curr_exchange_rates limit 1")))


def test_conversion_of_base_curr_to_target(database_conn):
    converted = CurrencyExchangeRates(database_conn).convert_amounts_to_target_currency(FakeDB.conversion_payload)
    assert 16.1201 == float(converted[0].amount)
