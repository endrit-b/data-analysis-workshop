from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Declare the Base Model
Base = declarative_base()

class CurrencyExchangeRates(Base):
    __tablename__ = "curr_exchange_rates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency_rate_date = Column(Date)
    base_currency_symbol = Column(String)
    base_currency_rate = Column(Float)
    exchanged_currency_rate = Column(Float)
    exchanged_exchange_symbol = Column(Date)
    last_name = Column(String)



