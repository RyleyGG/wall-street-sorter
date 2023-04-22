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
    manager = WallStreetManager()
    sortedTickers = manager.sortByAttr(sortAttr)

    print('RESULTS:')
    for ticker in sortedTickers:
        print(ticker)

        
if __name__ == '__main__':
    main()