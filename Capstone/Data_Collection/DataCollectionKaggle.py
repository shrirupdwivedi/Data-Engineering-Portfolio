#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install kaggle')


# In[2]:


get_ipython().system('kaggle --Version')


# In[5]:


get_ipython().system('kaggle --Version')


# In[6]:


get_ipython().system('kaggle --help')


# In[7]:


pip install opendatasets


# In[ ]:


import opendatasets as od
dataset_url = 'https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store?select=2019-Nov.csv'
od.download(dataset_url,force=True)


# In[ ]:


dataset_url1 = 'https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop?select=2019-Nov.csv'
od.download(dataset_url1,force=True)

