import yfinance as yf
import pandas as pd

class WallStreetManager:
    sectors: list[str]
    tickers: list[str]
    recommendedBuys: list[str] # TODO: eventually this should be a custom solution like a graph or hash map or something, not a list (to meet data struct requirement)

    # Constructor
    def __init__(self):
        pass

    # Primary functions
    def sortByAttr(self, attr: str):
        print(f'Beginning ticker sort by {attr}')
        print('Grabbing list of tickers...')
        tickerUrl = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        tickerTbl = pd.read_html(tickerUrl, attrs={"class": "wikitable"})[0]
        allTickers = tickerTbl["Symbol"].tolist()
        sortedTickers = []

        print('Grabbing ticker details...')
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
        return sortedTickers

    # Helper functions
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