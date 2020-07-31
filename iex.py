import os

from iexfinance.stocks import Stock
from iexfinance.stocks import get_market_gainers
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

# a = Stock("AAPL", token=os.getenv("IEX_TOKEN"))
# quote = a.get_quote()
# print(quote)

pprint(get_market_gainers())
