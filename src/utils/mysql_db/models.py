from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import uuid


class BaseModel:
    # Initialize base class definitions
    Declarative = declarative_base()


class CurrencyExchangeRatesModel(BaseModel.Declarative):
    """
    Currency exchange rates model
    """

    __tablename__ = "curr_exchange_rates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange_rate_date = Column(Date)
    base_currency_symbol = Column(String(3))
    target_currency_symbol = Column(String(3))
    target_currency_rate = Column(Float)

    def __init__(self, exchange_rate_date,
                 base_currency_symbol,
                 target_currency_symbol,
                 target_currency_rate):
        self.exchange_rate_date = exchange_rate_date
        self.base_currency_symbol = base_currency_symbol
        self.target_currency_symbol = target_currency_symbol
        self.target_currency_rate = target_currency_rate

    def __repr__(self):
        return "<CurrencyExchangeRatesModel(exchange_rate_date='%s', base_currency_symbol='%s', target_exchange_symbol='%s'," \
               "target_currency_rate=%s)>" % (self.exchange_rate_date, self.base_currency_symbol,
                                              self.target_currency_symbol, self.target_currency_rate)


class CurrConversionResult(CurrencyExchangeRatesModel):
    """
    A class that can be used to map the SQL result of conversion
    """
    amount = Column(Float)
    def __init__(self, amount, **kwargs):
        super().__init__(**kwargs)
        self.amount = amount
