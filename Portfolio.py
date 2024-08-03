import numpy as np

from StockData import StockData

class Portfolio:
    def __init__(self):
        self.stocks_data = {}
        self.quantities = {}
        self.options_data = {}  # dictionary to hold the options
        self.option_quantities = {}  # dictionary to hold quantities of the options

    def add_stock(self, stock_data, quantity):
        self.stocks_data[stock_data.ticker.ticker] = stock_data
        self.quantities[stock_data.ticker.ticker] = quantity

    def add_option(self, option_data, quantity):
        self.options_data[option_data.ticker.ticker] = option_data
        self.option_quantities[option_data.ticker.ticker] = quantity

    def calculate_portfolio_return(self, start_date, end_date):
        total_return = 0
        for stock_symbol in self.stocks_data:
            stock_return = self.stocks_data[stock_symbol].fetch_return(start_date, end_date)
            total_return += stock_return * self.quantities[stock_symbol]

        for option_symbol in self.options_data:
            option_return = self.options_data[option_symbol].fetch_return(start_date, end_date)
            total_return += option_return * self.option_quantities[option_symbol]
        return total_return