
# coding: utf-8

# In[7]:

from math import exp

def discrete_future_value(x,r,n):
    return x*(1+r)**n

def discrete_present_value (x,r,n):
    return x*(1+r)**-n

def continouous_future_value(x,r,t):
    return x*exp(r*t)

def continouous_present_value(x,r,t):
    return x*exp(-r*t)
if __name__ == "__main__":
    x=100 # value of investment in dollars
    r=0.05 # interest rate
    n=5 # years
    
    print("Future value of $100 in 5 years (discrete model): ", discrete_future_value(x,r,n))
    print("Future value of $100 in 5 years (continouous model): ", continouous_future_value(x,r,n))
    print("Present value of $100 in 5 years (discrete model): ", discrete_present_value(x,r,n))
    print("Present value of $100 in 5 years (continouous model): ", continouous_present_value(x,r,n))


# In[ ]:




# In[ ]:



