
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import math


# In[2]:

def winsorize_series(s):
    lower = s.quantile(0.05)
    upper = s.quantile(0.95)
    s[s < lower] = lower
    s[s > upper] = upper
    return s


# In[39]:

def GetCountByVal(data, column, bought):
    if bought == 1:
        new_data = data[[column]][(data[column] == 1) & (data.spend_usd_next_14_days > 0.001)]
    else:
        new_data = data[[column]][(data[column] == 1) & (data.spend_usd_next_14_days <= 0.001)]
    return (new_data.count())


# In[40]:

my_data = pd.read_csv("C:\Users\wangz_i6ij2py\Downloads\Python_project_eda.csv")


# In[41]:

my_data.describe()


# In[42]:

#clean up data
my_data['spend_usd_next_14_days'] = winsorize_series(my_data['spend_usd_next_14_days'])
clean_data = my_data.fillna(0)
clean_data.describe()


# In[43]:

pot_buyer = clean_data[['existing_buyer', 'saw_cart_before', 'user_added_credit_card', 'user_added_dcb', 'user_added_fop', 'user_added_gift_card', 'user_added_paypal' ,'spend_usd_next_14_days']][(clean_data.existing_buyer == 0) & (clean_data.saw_cart_before == 1.0)]
pot_buyer.describe()


# In[44]:

total = pot_buyer.shape[0]
cc_rate = GetCountByVal(pot_buyer, 'user_added_credit_card', 0) / float(total) / pot_buyer['user_added_credit_card'].mean()
dc_rate = GetCountByVal(pot_buyer, 'user_added_dcb', 0) / float(total) / pot_buyer['user_added_dcb'].mean()
gc_rate = GetCountByVal(pot_buyer, 'user_added_gift_card', 0) / float(total) / pot_buyer['user_added_gift_card'].mean()
pp_rate = GetCountByVal(pot_buyer, 'user_added_paypal', 0) / float(total) / pot_buyer['user_added_paypal'].mean()
rate = [cc_rate, dc_rate, gc_rate, pp_rate]
plt_index = ['credit_card', 'direct_carrier_billing', 'gift_card', 'paypal']
plt.bar((1, 2, 3, 4), rate, align='center')
plt.xticks((1, 2, 3, 4), plt_index)
plt.show()


# In[65]:

ret_buyer = clean_data[['existing_buyer', 'user_added_credit_card', 'user_added_dcb', 'user_added_fop', 'user_added_gift_card', 'user_added_paypal' ,'spend_usd_next_14_days']][(clean_data.existing_buyer == 0) & (clean_data.spend_usd_next_14_days >= 0.001)]
ret_buyer.describe()


# In[62]:

def GetRate(val):
    return(val.count()/float(ret_buyer.shape[0]))
def PlotList(data):
    plt_index = ['credit_card', 'direct_carrier_billing', 'gift_card', 'paypal', 'fop']
    plt.bar((1, 2, 3, 4, 5), data, align='center')
    plt.xticks((1, 2, 3, 4, 5), plt_index)
    plt.show()
cc_ret = ret_buyer[['spend_usd_next_14_days']][ret_buyer.user_added_credit_card == 1]
dc_ret = ret_buyer[['spend_usd_next_14_days']][ret_buyer.user_added_dcb == 1]
gc_ret = ret_buyer[['spend_usd_next_14_days']][ret_buyer.user_added_gift_card == 1]
pp_ret = ret_buyer[['spend_usd_next_14_days']][ret_buyer.user_added_paypal == 1]
fop_ret = ret_buyer[['spend_usd_next_14_days']][ret_buyer.user_added_fop == 1]
ret_sum = [cc_ret.sum(), dc_ret.sum(), gc_ret.sum(), pp_ret.sum(), fop_ret.sum()]
PlotList(ret_sum)


# In[64]:

ret_rate = [GetRate(cc_ret), GetRate(dc_ret), GetRate(gc_ret), GetRate(pp_ret), GetRate(fop_ret)]
PlotList(ret_rate)


# In[ ]:



