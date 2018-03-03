
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime
import scipy.optimize as optimization
import fix_yahoo_finance as yf
yf.pdr_override()


# In[2]:

stocks = ['AAPL','WMT','TSLA','GE','AMZN','DB']

start_date="2010-01-01"
end_date="2017-01-01"


# In[3]:

#downloading the data from Yahoo Finance
def download_data(stocks):
    data=pdr.get_data_yahoo(stocks, start=start_date, end=end_date)["Adj Close"]
    data.columns = stocks
    return data


# In[4]:

def show_data(data):
    data.plot(figsize=(10,5))
    plt.show()


# In[5]:

# Use natural logarithm for normalization process
def calculate_returns(data):
    returns = np.log(data/data.shift(1))
    return returns;


# In[6]:

def plot_daily_returns(returns):
    returns.plot(figsize=(10,5))
    plt.show()


# In[7]:

# Print our mean and covariance of stock
def show_statistics(returns):
    print(returns.mean()*252)
    print(returns.cov()*252)


# In[8]:

def initialize_weights():
    weights=np.random.random(len(stocks))
    weights/=np.sum(weights)
    return weights;


# In[9]:

# Expected portfolio return
def calculate_portfolio_return(returns,weights):
    portfolio_return = np.sum(returns.mean()*weights)*252
    print("Expected portfolio return:", portfolio_return)


# In[10]:

# Expected portfolio variance
def calculate_portfolio_variance(returns, weights):
    portfolio_variance = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*252,weights)))
    print("Expected variance:", portfolio_variance)


# In[11]:

def generate_portfolios(weights,returns):
    preturns = []
    pvariances = []

#Monte-Carlo simulation: we generate several random weights -> so random portfolios !!!
    for i in range(10000):
        weights = np.random.random(len(stocks))
        weights/=np.sum(weights)
        preturns.append(np.sum(returns.mean()*weights)*252)
        pvariances.append(np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights))))

    preturns = np.array(preturns)
    pvariances = np.array(pvariances)
    return preturns,pvariances


# In[12]:

def plot_portfolios(returns, variances):
    plt.figure(figsize=(10,6))
    plt.scatter(variances,returns,c=returns/variances,marker='o')
    plt.grid(True)
    plt.xlabel("Expected Volatility")
    plt.ylabel("Expected Return")
    plt.colorbar(label="Sharpe Ratio")
    plt.show()


# In[13]:

#Using optimization techniques scipy can optimize functions
def statistics(weights,returns):
    portfolio_return=np.sum(returns.mean()*weights)*252
    portfolio_volatility=np.sqrt(np.dot(weights.T,np.dot(returns.cov()*252,weights)))
    return np.array([portfolio_return,portfolio_volatility,portfolio_return/portfolio_volatility])


# In[14]:

def min_func_sharpe(weights,returns):
    return -statistics(weights,returns)[2] 


# In[15]:

def optimize_portfolio(weights,returns):
    constraints = ({'type':'eq','fun': lambda x: np.sum(x)-1}) #the sum of weights is 1
    bounds = tuple((0,1) for x in range(len(stocks))) #the weights can be 1 at most: 1 when 100% of money is invested into a single stock
    optimum=optimization.minimize(fun=min_func_sharpe,x0=weights,args=returns,method='SLSQP',bounds=bounds,constraints=constraints) 
    return optimum


# In[16]:

def print_optimal_portfolio(optimum,returns):
    print("Optimal weights:", optimum['x'].round(3))
    print("Expected return, volatility and Sharpe ratio:", statistics(optimum['x'].round(3),returns))
    


# In[17]:

def show_optimal_portfolio(optimum, returns, preturns, pvariances):
    plt.figure(figsize=(10,6))
    plt.scatter(pvariances,preturns,c=preturns/pvariances,marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.plot(statistics(optimum['x'],returns)[1],statistics(optimum['x'],returns)[0],'g*',markersize=20.0)
    plt.show()


# In[18]:

if __name__=="__main__":
    data = download_data(stocks)
    show_data(data)
    returns = calculate_returns(data)
    plot_daily_returns(returns)
    show_statistics(returns)
    weights=initialize_weights()
    calculate_portfolio_return(returns,weights)
    calculate_portfolio_variance(returns,weights)
    preturns,pvariances=generate_portfolios(weights, returns)
    plot_portfolios(preturns,pvariances)
    optimum=optimize_portfolio(weights,returns)
    print_optimal_portfolio(optimum, returns)
    show_optimal_portfolio(optimum, returns, preturns, pvariances)


# In[ ]:



