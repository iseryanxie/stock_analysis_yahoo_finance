'''
stock.py: Python Module callable
Mosel will invoke this scriptas a module
'''

try:
    import inputdata
except Exception:
    print("In Unit Test mode")
    modeUnitTest = True
    modeRun = 'groupcorr'
else:
    modeUnitTest = False
    modeRun = inputdata.modeRun

from yahoofinancials import YahooFinancials
import pandas as pd

def get_stock_price(startDate,endDate,periodtype,listStock):
    dfListStocks = pd.DataFrame(columns=['Date'])
    for s in listStock:
        dictStockPrice = YahooFinancials(s).get_historical_price_data(startDate, endDate, periodtype)
        dfStockPrice = pd.DataFrame.from_dict(dictStockPrice[s]["prices"])[['formatted_date','adjclose']]
        dfStockPrice.columns = ['Date', s]
        dfListStocks = dfListStocks.merge(dfStockPrice, how='right', on='Date')
    dfListStocks = dfListStocks.set_index('Date')
    return dfListStocks

class ClsEquity:

    def __init__(self, ticker, startdate, enddate, periodtype):
        self.ticker = ticker
        self.startDate = startdate
        self.endDate = enddate
        self.periodtype = periodtype

    def __str__(self):
        return "Ticker: {}, StartDate: {} ~ EndDate: {}".format(self.ticker,self.startDate,self.endDate)

    def queryPrice(self):
        yf_stock_single = YahooFinancials(self.ticker)
        # query historical price from startDate to endDate, return json
        single_stock_prices = yf_stock_single.get_historical_price_data(self.startDate, self.endDate, self.periodtype)
        # open,close,high,low,volume
        df = pd.DataFrame.from_dict(single_stock_prices[self.ticker]["prices"])
        self.dateRange = df['formatted_date'].tolist()
        self.openPrices = df['open'].tolist()
        self.closePrices = df['close'].tolist()
        self.highPrices = df['high'].tolist()
        self.lowPrices = df['low'].tolist()
        self.volume = df['volume'].tolist()


if __name__ == '__main__':

    if modeRun == 'single':
        if modeUnitTest:
            modeRun = 'single'
            aStock = ClsEquity('BABA', '2015-10-12', '2017-12-15', 'weekly')
        else:
            modeRun = 'single'
            aStock = ClsEquity(inputdata.ticker, inputdata.startDate, inputdata.endDate, inputdata.periodType)
        aStock.queryPrice()
        dateRange = aStock.dateRange
        # print(dateRange)
        closePrices = aStock.closePrices
        openPrices = aStock.openPrices
        highPrices = aStock.highPrices
        lowPrices = aStock.lowPrices
        volume = aStock.volume
    elif modeRun == 'groupcorr':
        if modeUnitTest:
            lstStockNames = ['C','BAC','WFC','JPM']
            df = get_stock_price('2015-10-12', '2018-10-11', 'weekly', lstStockNames)
            dfPriceCorr = df.corr()
            dfPctChange = df.pct_change()
            dfPriceChgCorr = dfPctChange.corr()
            arPriceChgCorr = {}
            for row,fs in enumerate(lstStockNames):
                for col,ft in enumerate(lstStockNames):
                    arPriceChgCorr[(fs,ft)] = dfPriceChgCorr.iloc[row,col]
            # print(arPriceChgCorr)
        else:
            lstStockNames = ['C', 'BAC', 'WFC', 'JPM']
            df = get_stock_price('2015-10-12', '2018-10-11', 'weekly', lstStockNames)
            dfPriceCorr = df.corr()
            dfPctChange = df.pct_change()
            dfPriceChgCorr = dfPctChange.corr()
            arPriceChgCorr = {}
            for row, fs in enumerate(lstStockNames):
                for col, ft in enumerate(lstStockNames):
                    arPriceChgCorr[(fs, ft)] = dfPriceChgCorr.iloc[row, col]








