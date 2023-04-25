import yfinance as yf
import pandas as pd
import numpy as np
import requests
from collections import OrderedDict
from datetime import datetime


class WallStreetManager:
    tickerObj: OrderedDict[str, float]
    resultPref: str
    historicalData: OrderedDict[str, float]

    # Constructor
    def __init__(self):
        pass

    # Primary functions
    def sortByAttr(self, attr: str):
        print('Grabbing list of tickers...')
        tickerUrl = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        response = requests.get(tickerUrl)
        tickerTbl = pd.read_html(response.text, attrs={"class": "wikitable"})[0]
        allTickers = tickerTbl["Symbol"].tolist()
        sortedTickers = []

        tickerIter = 1
        for ticker in allTickers:
            try:
                print(f'Grabbing details for ticker {tickerIter} out of {len(allTickers)} ({round((tickerIter / len(allTickers)) * 100, 2)}%)')
                tickerObj = yf.Ticker(ticker)
                tickerVal = tickerObj.info[attr]
                if type(tickerVal) in [int, float]:
                    sortedTickers.append((ticker, tickerVal))
            except KeyError as e:
                pass
            tickerIter += 1

        print('Beginning sort algorithm...')
        sortedTickers = self.mergeSort(sortedTickers)
        self.tickerObj = OrderedDict()
        for res in sortedTickers:
            self.tickerObj[res[0]] = res[1]

    def historicalAnalysis(self):
        tickerIter = 1
        tickers = []
        avgVolaArr = []
        totalVolaArr = []
        totalDataPoints = 0
        if self.resultPref == 'lowest':
            tickers = list(self.tickerObj.keys())[:100]
        else:
            tickers = list(self.tickerObj.keys())[-100:]
        for ticker in tickers:
            print(f'Grabbing details for ticker {tickerIter} out of 100')
            startDate = yf.Ticker(ticker).info['firstTradeDateEpochUtc']
            if startDate < 0:
                print('Ticker contains invalid start date, skipping...')
                tickerIter += 1
                continue
            startDate = datetime.fromtimestamp(startDate).strftime('%Y-%m-%d')
            endDate = datetime.now().strftime('%Y-%m-%d')

            historicalData = yf.download(
                tickers=ticker,
                start=startDate,
                end=endDate,
                interval='1d',
                progress=False
            )
            totalDataPoints += len(historicalData)
            historicalData['daily_volatility'] = historicalData['Close'].pct_change().abs()
            historicalData.reset_index(inplace=True)
            historicalData.rename(columns={'index': 'Date'}, inplace=True)

            # Getting histoical lowest & highest prices and calculating average volatility
            lowPrice, highPrice = float('inf'), float('-inf')
            for _, row in historicalData.iterrows():
                low = row['Low']
                high = row['High']
                if low < lowPrice:
                    lowPrice = low
                if high > highPrice:
                    highPrice = high
                if not np.isnan(row['daily_volatility']):
                    totalVolaArr.append((ticker, str(row['Date']).split(' ')[0], row['daily_volatility']))
                    
            dailyReturns = historicalData['Close'].pct_change().dropna()
            avgVolatility = dailyReturns.std()
            avgVolaArr.append((ticker, lowPrice, highPrice, avgVolatility))
            tickerIter += 1

        print('\nSorting tickers by average historical volatility...')
        self.quickSort(avgVolaArr, 3)
        for result in avgVolaArr:
            print(f"{result[0]}: Lowest price: {result[1]}, Highest price: {result[2]}, Volatility: {round(result[3], 2)}")
        print('\nSorting tickers by daily volatility...')
        self.quickSort(totalVolaArr, 2)
        print('LOWEST 50 NONZERO VOLATILITIES:')
        volaIter = 0
        printed = 0
        while printed < 50:
            if round(totalVolaArr[volaIter][2], 2) != 0.0:
                print(f"{totalVolaArr[volaIter][0]}: Date: {totalVolaArr[volaIter][1]}, Volatility: {round(totalVolaArr[volaIter][2], 2)}")
                printed += 1
            volaIter += 1
        print('\nHIGHEST 50 VOLATILITIES:')
        for result in totalVolaArr[-50:]:
            print(f"{result[0]}: Date: {result[1]}, Volatility: {round(result[2], 2)}")
        print(f'\nTotal data points considered: {totalDataPoints}')

    # Helper functions
    def quickSort(self, arr, sortIndex):
        def recurse(arr, left, right, sortIndex):
            if left >= right:
                return

            pivIndex = (left + right) // 2
            pivot = arr[pivIndex]

            i, j = left, right
            while i <= j:
                while arr[i][sortIndex] < pivot[sortIndex]:
                    i += 1
                while arr[j][sortIndex] > pivot[sortIndex]:
                    j -= 1
                if i <= j:
                    arr[i], arr[j] = arr[j], arr[i]
                    i += 1
                    j -= 1

            recurse(arr, left, j, sortIndex)
            recurse(arr, i, right, sortIndex)

        recurse(arr, 0, len(arr) - 1, sortIndex)


    def mergeSort(self, arr):
        if len(arr) < 2:
            return

        midIndex = len(arr) // 2
        leftHalf = arr[:midIndex]
        rightHalf = arr[midIndex:]

        self.mergeSort(leftHalf)
        self.mergeSort(rightHalf)

        i = j = k = 0

        while i < len(leftHalf) and j < len(rightHalf):
            if leftHalf[i][1] < rightHalf[j][1]:
                arr[k] = leftHalf[i]
                i += 1
            else:
                arr[k] = rightHalf[j]
                j += 1
            k += 1

        while i < len(leftHalf):
            arr[k] = leftHalf[i]
            i += 1
            k += 1

        while j < len(rightHalf):
            arr[k] = rightHalf[j]
            j += 1
            k += 1
        return arr
    
    def printTickers(self):
        print('Ticker List:')
        for key, value in self.tickerObj.items():
            print(f'{key}: {value}')