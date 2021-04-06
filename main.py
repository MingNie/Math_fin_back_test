import numpy as np
import pandas as pd
import datetime as dt
from pylab import mpl, plt

plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

import sys
sys.path.append("D:\Github\Math_fin_back_test")
from backtest import back_test_bot

raw = pd.read_csv('D:\Github\Math_fin_back_test\MSFT.csv', index_col=0, parse_dates=True)
raw.info()

data = (pd.DataFrame(raw['Adj Close']))
test_bot1 = back_test_bot('equity', data)

# #choice equals 1, run the default sma strategy
# test_bot1.strategy_init_(10,30,0)
# test_bot1.data.info()
# print(test_bot1.data)

test_bot2 = back_test_bot('equity', data)
test_bot2.strategy_init_(10,30,1)
test_bot2.data.info()
test_bot2.ema_plot1().show()
