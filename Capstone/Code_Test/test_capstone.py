import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import unittest

spark = SparkSession.builder.master('local').appName('app').getOrCreate()

class Test(unittest.TestCase):


    def test_read_json(self):

        path = 'test.json'
        res = spark.read.json(path)
        self.assertEqual(type(res), pyspark.sql.dataframe.DataFrame)

    
    def test_eliminate_null_values(self):
        df = spark.read.csv("test.csv")
        self.assertEqual(df.na.drop().count(), 0)

    
    def test_filter(self):

        df = spark.read.csv("test.csv")
        self.assertEqual(df.filter(col('_c0').contains("D")).count(), 1)

    

if __name__ == '__main__':
    unittest.main()
