import requests
from pprint import pprint
from datetime import datetime
import calendar
from functools import reduce

from ..utils.mysql_db.models import CurrencyExchangeRatesModel, CurrConversionResult


class CurrencyExchangeRates:
    def __init__(self, conn):
        self.conn = conn
        self.EXCHANGE_RATES_API_BASE_URL = "https://api.exchangeratesapi.io/history"

    def convert_amounts_to_target_currency(self, amounts: list):
        """
        Converts an array of amounts to base currency
        :param amounts:
        :return:
        """
        # Build SQL expression for given amounts
        sql_statement = reduce(self.build_conversion_expression, amounts, "")
        # Execute expression
        converted_amounts = list(self.conn.execute_sql_statement_with_type(CurrConversionResult, sql_statement))
        return converted_amounts

    def build_conversion_expression(self, acc, obj):
        """
        Parse  object to an SQL conversion expr
        :param acc: accumulator
        :param obj: payload
        :return: SQL expression
        """
        return f"""
            SELECT id, exchange_rate_date, base_currency_symbol, target_currency_symbol, target_currency_rate,
            CAST(target_currency_rate * {obj['amount']} AS DECIMAL(11, 4)) as amount
            FROM curr_exchange_rates
            WHERE exchange_rate_date= DATE '{obj['exchange_rate_date']}' 
            AND base_currency_symbol='{obj['base_currency_symbol']}' 
            AND target_currency_symbol='{obj['target_currency_symbol']}' """ + (" " if acc == "" else " UNION ") + acc

    def download_exchange_rates_data(self, currency='EUR'):
        """
        This is a method that downloads exchange rates the provided API from different
        :return: <void>
        """
        # Load all available exchanges for the current year into a database
        today = datetime.now().date()
        # To keep the data size under control I'll limit the batch size to 1 month of data that I get from API
        for month in range(1, today.month + 1):
            first_day = today.replace(day=1, month=month)
            last_day = today.replace(day=calendar.monthrange(first_day.year, first_day.month)[1], month=month)

            # Get exchange rate for given month
            date_range = f"?start_at={first_day}&end_at={last_day}&base={currency}"
            print(date_range)
            data = requests.get(self.EXCHANGE_RATES_API_BASE_URL + date_range).json()
            if data['rates']:
                self.conn.insert_batch(self.__parse_json_response(data))

    def __parse_json_response(self, json_obj):
        """
        Parse json response and map it to currency object
        :param json_obj: json response that API returns
        :return: List<CurrencyExchangeRatesModel>
        """
        batch = []
        for item in json_obj['rates'].items():
            for curr in item[1].items():
                batch.append(CurrencyExchangeRatesModel(item[0], json_obj['base'], curr[0], curr[1]))
        return batch
