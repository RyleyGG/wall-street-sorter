from WallStreetManager import WallStreetManager
import yfinance as yf
import re

def main():
    manager = WallStreetManager()

    # Using microsoft as placeholder ticker to grab viable keys for sorting
    msft = yf.Ticker("MSFT")
    viableKeys = []
    displayKeyMap = {}
    for key in msft.info.keys():
        try:
            int(msft.info[key])
            viableKeys.append(key)
        except ValueError:
            pass
        except TypeError:
            pass
    
    for key in viableKeys:
        displayKeyMap[key] = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', key)).replace('  ', ' ').title()

    print('Once you press "Enter", a set of quantities will be presented to you. Once you\'ve reviewed the list, enter the number with the quantity you wish to sort by.')
    input()
    for i in range(len(displayKeyMap)):
        print(f'{i + 1}: {list(displayKeyMap.values())[i]}')
    sortChoice = input('Enter your choice now: ')

    while sortChoice not in [str(i) for i in range(1, len(displayKeyMap) + 1)]:
        sortChoice = input(f'Enter a number between 1 and {len(displayKeyMap)}: ')
    sortAttr = list(displayKeyMap.keys())[int(sortChoice) - 1]

    print('\nI prefer...')
    print('1. Tickers with lowest values\n2. Tickers with highest values')
    lowHighChoice = input()
    while lowHighChoice not in ['1', '2']:
        lowHighChoice = input('Enter the number associated with your choice: ')
    manager.resultPref = 'lowest' if lowHighChoice == '1' else 'highest'
    print(f'Beginning ticker sort by {displayKeyMap[sortAttr]}')
    manager.sortByAttr(sortAttr)
    print(f'The ticker with the {manager.resultPref} value for {displayKeyMap[sortAttr]}' +
          f' was {list(manager.tickerObj.keys())[0] if manager.resultPref == "lowest" else list(manager.tickerObj.keys())[-1]}' +
          f' with a value of {list(manager.tickerObj.values())[0] if manager.resultPref == "lowest" else list(manager.tickerObj.values())[-1]}')
    print(f'\nGrabbing historical data for 100 tickers with {"lowest" if lowHighChoice == "1" else "highest"} values for {displayKeyMap[sortAttr]}...')
    manager.historicalAnalysis()

        
if __name__ == '__main__':
    main()