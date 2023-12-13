""" 
Price - Latest open price value

"""



import yfinance as yf
import datetime as dt
import pprint



portfolio = ['MSFT', 'AAPL', 'GOOG', 'AMZN', 'META', 'NVDA', 'TSLA']

class Stocks:
    def __init__(self, ticker=[]) -> None:
        self.portfolio = ticker
    
    def add_ticker(self, symbol: str) -> None:
        self.portfolio.append(symbol)
    
    def remove_ticker(self, symbol: str) -> None:
        self.portfolio.remove(symbol)
    
    def get_portfolio(self) -> list[str]:
        return self.portfolio
    
    def set_portfolio(self, new_portfolio: list[str]) -> None:
        self.portfolio = new_portfolio

    def add_tickers_to_dict(self) -> dict:  # e.g. {'AAPL': [100.0, '2020-01-01 09:30:00']}
        data = yf.download(' '.join(self.portfolio), period='1d', interval='5m') # returns <class 'pandas.core.frame.DataFrame'>

        latest_price_time = list(map(lambda x: list(data['Open'][x].to_dict())[-1], self.portfolio)) # Timestamp objects

        final = dict()

        for i in range(len(self.portfolio)):
            ticker_values = data['Open'][self.portfolio[i]].to_dict()
            ticker_datetime_str = latest_price_time[i].strftime('%Y-%m-%d %H:%M:%S')
            rounded_price = round(ticker_values[latest_price_time[i]], 2)

            final[self.portfolio[i]] = [rounded_price, ticker_datetime_str]
        
        return final

if __name__ == '__main__':
    stocks = Stocks(portfolio)
    res = stocks.add_tickers_to_dict()
    
    pprint.pprint(res)

