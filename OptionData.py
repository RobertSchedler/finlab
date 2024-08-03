import pandas as pd
import yfinance as yf


class OptionData:
    def __init__(self, ticker_symbol):
        self.ticker = yf.Ticker(ticker_symbol)
        self.options_data = {}
        self.download_option_data()

    def download_option_data(self):
        try:
            # Get expiry dates
            for expiry_date in self.ticker.options:
                # Fetch option chain for given expiry date
                option_chain = self.ticker.option_chain(expiry_date)

                # Loop over strike prices in calls and puts
                for df in [option_chain.calls, option_chain.puts]:
                    for idx, row in df.iterrows():
                        option_symbol = row['contractSymbol']

                        # Fetch historical data if not already done
                        if option_symbol not in self.options_data:
                            print(f"Downloading historical data for option {option_symbol}...")
                            try:
                                option_ticker = yf.Ticker(option_symbol)
                                self.options_data[option_symbol] = option_ticker.history(period="max")
                            except Exception as e:
                                print(f"Could not download historical data for option {option_symbol}: {e}")
        except Exception as e:
            print(f"Error in downloading option data: {e}")