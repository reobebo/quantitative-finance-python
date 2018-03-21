
# coding: utf-8

# In[3]:

import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import fix_yahoo_finance as yf
yf.pdr_override()

risk_free_rate = 0.05



def capm(start_date, end_date, ticker1, ticker2):
    
    #get the data from yahoo finance
    stock1=pdr.get_data_yahoo(ticker1,start_date,end_date)
    stock2=pdr.get_data_yahoo(ticker2,start_date,end_date)
    
    # we prefer monthy returns instead of daily returns
    return_stock1 = stock1.resample('M').last()
    return_stock2 = stock2.resample('M').last()
    
    #creating a dataFrame from the data = Adjusted Closing Price is used as usual 
    data = pd.DataFrame({'s_adjclose' : return_stock1['Adj Close'], 'm_adjclose' : return_stock2['Adj Close']}, index=return_stock1.index)
    #natural logarith of the returns
    data[['s_returns','m_returns']] = np.log(data[['s_adjclose', 'm_adjclose']]/data[['s_adjclose','m_adjclose']].shift(1))
    #get rid of the NaN/missing values
    data = data.dropna()
    #covariance matrix: the diagonal items are the cariances- off diagnals are the covariances
    covmat = np.cov(data['s_returns'], data['m_returns'])
    #calculating beta according to the formula
    beta = covmat = np.cov(data['s_returns'], data['m_returns'])
    print('beta from formula: ', beta)
    #using linear regression to fit a line to the data [stock_returns, market_returns] - slope is beta
    beta,alpha = np.polyfit(data['m_returns'],data['s_returns'], deg=1)
    print('Beta from regression: ',beta)#plot
    fig,axis = plt.subplots(1,figsize=(20,10))
    axis.scatter(data['m_returns'], data['s_returns'], label='Data points')
    axis.plot(data['m_returns'], beta*data['m_returns']+alpha, color='red',label='CAP< Line')
    plt.title('Capital Asset Pricing Model, finding the alphas and betas')
    plt.xlabel('Market return $R_m$', fontsize=18)
    plt.legend()
    plt.grid(True)
    plt.show()
    
    #calculate the expected return according to the CAPM formula
    expected_return = risk_free_rate + beta*(data['m_returns'].mean()*12-risk_free_rate)
    print("Expected return: ", expected_return)
    
    



if __name__ =="__main__":
    #using historical data 2010-2017: the market is the S&P500
    capm('2010-01-01','2017-01-01','IBM','^GSPC')








# In[ ]:



