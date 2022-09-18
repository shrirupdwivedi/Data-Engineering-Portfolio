import pandas as pd
import json
import pprint
import os
import logging
from transform import *
class etl:

    def __init__(self):

        for filename in os.listdir(os.getcwd()):
  
            if filename.endswith("business.json"):
                logging.info('Business dataset processing')
                count =1
                for df in pd.read_json(filename,chunksize=1000,lines=True):
                    b = business(df)
                    df = b.businesstransform()
                    chunkname = 'business_' + str(count) +'.csv'
                    df.to_csv(chunkname,index= False)      
                    count += 1
            
            elif filename.endswith("review.json"):
                logging.info('Review dataset processing')
                count =1
                for df in pd.read_json(filename,chunksize=1000,lines=True):
               
                    chunkname = 'review_' + str(count) +'.csv'
                    df.to_csv(chunkname,index= False)      
                    count += 1
            
            elif filename.endswith("checkin.json"):
                logging.info('Checkin dataset processing')
                count =1
                for df in pd.read_json(filename,chunksize=1000,lines=True):
                    c = checkin(df)
                    df = c.checkintransform()
                    chunkname = 'checkin_' + str(count) +'.csv'
                    df.to_csv(chunkname,index= False)      
                    count += 1
            
            elif filename.endswith("tip.json"):
                logging.info('Tip dataset processing')
                count =1
                for df in pd.read_json(filename,chunksize=1000,lines=True):
               
                    chunkname = 'tip_' + str(count) +'.csv'
                    df.to_csv(chunkname,index= False)      
                    count += 1 
            
            elif filename.endswith("user.json"):
                logging.info('User dataset processing')
                count =1
                for df in pd.read_json(filename,chunksize=1000,lines=True):
               
                    chunkname = 'user_' + str(count) +'.csv'
                    df.to_csv(chunkname,index= False)      
                    count += 1


        
