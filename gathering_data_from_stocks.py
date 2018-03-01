
# coding: utf-8

# In[59]:

import numpy as np
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import pandas as pd
import fix_yahoo_finance as yf
yf.pdr_override() 


# In[67]:

stocks = ["WMT"]

start_date="2001-01-01"
end_date= "2017-01-01"

data=pdr.get_data_yahoo(stocks, start=start_date, end=end_date) ["Adj Close"]
daily_return =(data/data.shift(1))-1

daily_return.hist(bins=100)
plt.show()


# In[ ]:



