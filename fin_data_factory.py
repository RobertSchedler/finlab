import yfinance as yf


def get_stock_data(ticker_symbol, start_date, end_date):
    """
    Fetches historical stock data for a given ticker symbol from Yahoo Finance.

    Parameters:
    - ticker_symbol: The ticker symbol of the stock (e.g., 'AAPL' for Apple Inc.).
    - start_date: The start date for the data in 'YYYY-MM-DD' format.
    - end_date: The end date for the data in 'YYYY-MM-DD' format.

    Returns:
    - A pandas DataFrame containing the historical stock data.
    """
    # Fetch the data
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

    return stock_data


def get_options_chain(ticker_symbol, expiration_date=None):
    """
    Fetches the options chain for a given ticker symbol from Yahoo Finance.

    Parameters:
    - ticker_symbol: The ticker symbol of the stock (e.g., 'AAPL' for Apple Inc.).
    - expiration_date: The expiration date for the options in 'YYYY-MM-DD' format.
                      If None, fetches available expiration dates.

    Returns:
    - A tuple containing two pandas DataFrames: (calls, puts) for the specified expiration date.
      If expiration_date is None, returns the list of available expiration dates.
    """
    # Initialize the ticker object
    ticker = yf.Ticker(ticker_symbol)

    # If no expiration date is provided, return available expiration dates
    if expiration_date is None:
        return ticker.options

    # Fetch the options chain for the given expiration date
    options_chain = ticker.option_chain(expiration_date)

    # The options chain includes both calls and puts
    calls = options_chain.calls
    puts = options_chain.puts

    return calls, puts