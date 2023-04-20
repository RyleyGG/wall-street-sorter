### Purpose
The Wall Street Sorter will sort and filter stock market data based on user input parameters (i.e. sorting by dividend rate or popularity or filtering based on ticker sector). Between pandas and the yfinance API much of this could be achieved natively, but this is a semester project for COP3530, the requirements of which stipulate we must implement the primary algorithms/data structures ourselves. Therefore, it is likely that throughout development various features of pandas and especially yfinance will be ignored in favor of custom solutions.


### How to install
After installing Python, the package requirements can be run by opening a terminal/command prompt instance in the project directory and typing in the command

`pip install -r requirements.txt`

If you have multiple versions of Python installed, you can also use

`py -{version} -m pip install -r requirements.txt` 

to ensure that the packages are installed for the correct version of the interpretor. Note that the version used during development and testing is Python 3.10.