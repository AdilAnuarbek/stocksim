""" 
Price - Latest open price value

"""



import yfinance as yf
import mysql.connector

# TODO: When Molda and Kanysh add sending and receiving tickers from website, change portfolio to receiving tickers
portfolio = ['MSFT', 'AAPL', 'GOOG', 'AMZN', 'META', 'NVDA', 'TSLA']  # Example portfolio

class Stocks:
    def __init__(self, ticker=[]) -> None:
        self.portfolio = ticker
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="stocksim"
        )
    
    def add_ticker(self, symbol: str) -> None:
        self.portfolio.append(symbol)
    
    def remove_ticker(self, symbol: str) -> None:
        self.portfolio.remove(symbol)
    
    def get_portfolio(self) -> list[str]:
        return self.portfolio
    
    def set_portfolio(self, new_portfolio: list[str]) -> None:
        self.portfolio = new_portfolio
    
    def send_to_db(self) -> None:
        vals = self.add_tickers_to_dict()
        final_vals = []
        for i in range(len(self.portfolio)):
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT 1 FROM stocks WHERE stock_datetime = %s", (vals[i][2],))
            result = mycursor.fetchone()
            does_exist = mycursor.rowcount == 0
            if not does_exist:
                final_vals.append(vals[i])
            # mycursor.fetchall()
            mycursor.close()
        mycursor = self.mydb.cursor()
        if final_vals:
            mycursor.executemany("INSERT INTO stocks (stock_name, stock_price, stock_datetime) VALUES (%s, %s, %s)", final_vals)
        
        self.mydb.commit()

        mycursor.close()


    def add_tickers_to_dict(self) -> list:
        data = yf.download(' '.join(self.portfolio), period='1d', interval='1m') # returns <class 'pandas.core.frame.DataFrame'>

        latest_price_time = list(map(lambda x: list(data['Open'][x].to_dict())[-1], self.portfolio)) # Timestamp objects

        final = list()

        for i in range(len(self.portfolio)):
            ticker_values = data['Open'][self.portfolio[i]].to_dict()
            ticker_datetime_str = latest_price_time[i].strftime('%Y-%m-%d %H:%M:%S')
            rounded_price = round(ticker_values[latest_price_time[i]], 2)

            final.append(tuple([self.portfolio[i], rounded_price, ticker_datetime_str]))
        return final

    def print_db(self) -> None:
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM stocks")
        result = mycursor.fetchall()

        for x in result:
            print(x)
    
    def close_connection(self) -> None:
        self.mydb.close()
        


if __name__ == '__main__':
    stocks = Stocks(portfolio)
    # res = stocks.add_tickers_to_dict()
    
    # pprint.pprint(res)
    stocks.send_to_db()
    stocks.print_db()
    # print(stocks.add_tickers_to_dict())
    stocks.close_connection()