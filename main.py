import yfinance as yf
import datetime as dt
import pprint

portfolio = ['MSFT', 'AAPL', 'GOOG', 'AMZN', 'META', 'NVDA', 'TSLA']


def add_tickers_to_dict(tickers_list):
    data = yf.download(' '.join(portfolio), period='1d', interval='5m') # returns <class 'pandas.core.frame.DataFrame'>

    latest_price_time = list(map(lambda x: list(data['Open'][x].to_dict())[0], portfolio)) # Timestamp objects

    final = dict()

    for i in range(len(portfolio)):
        ticker_values = data['Open'][portfolio[i]].to_dict()
        final[portfolio[i]] = round(ticker_values[latest_price_time[i]], 2)
    
    return final

if __name__ == '__main__':
    res = add_tickers_to_dict(portfolio)
    
    pprint.pprint(res)