import pandas as pd

class business:

    def __init__(self,df):
        self.df = df

    def businesstransform(self):

        self.df = self.df.dropna(subset=['attributes'])
        self.df = self.df[self.df["categories"].str.contains("Restaurants") == True]

        return(self.df)

class checkin:

    def __init__(self,df):
        self.df = df

    def checkintransform(self):

        for i, row in enumerate(self.df['date']):
            row = row.split(",")
            self.df['date'][i] = len(row)
            self.df.columns = ['business','no_of_checkins']

        return(self.df)
        



