import os

from src.data_mining import CurrencyExchangeRates, ManufacturerScraper
from src.utils.mysql_db import MySQLConnection
from src.utils import load_env_vars


def bootstrap_app(solution):
    """
    A function to initiate running of one of the solutions, based on the given parameter
    :param solution: to run
    :return: <void>
    """
    # Create database connection
    conn = MySQLConnection(os.getenv('MYSQL_USERNAME'), os.getenv('MYSQL_PASSWORD'),
                           f"{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}",
                           os.getenv('MYSQL_DB_NAME')).connect()

    # Run solution
    if solution == "download":
        # Download the data
        CurrencyExchangeRates(conn).download_exchange_rates_data()
    elif solution == "ex1":
        # Download the data
        convert_amounts = [
            {'exchange_rate_date': '2021-01-22', 'base_currency_symbol': 'USD', 'target_currency_symbol': 'EUR', 'amount': 22.01},
            {'exchange_rate_date': '2021-01-05', 'base_currency_symbol': 'USD', 'target_currency_symbol': 'SEK', 'amount': 100},
            {'exchange_rate_date': '2021-01-05', 'base_currency_symbol': 'USD', 'target_currency_symbol': 'BRL', 'amount': 20},
        ]
        CurrencyExchangeRates(conn).convert_amounts_to_target_currency(convert_amounts)

    elif solution == "scraper":
        # Init scraping of manufacturer catalog
        ManufacturerScraper().scrape()


# If it is the main module - run this block
if __name__ == '__main__':
    # Load environment variables
    load_env_vars()
    # Begin process
    bootstrap_app("scraper")
