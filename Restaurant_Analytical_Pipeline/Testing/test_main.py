import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col,split,size
import unittest
import os.path

spark = SparkSession.builder.master('local').appName('app').getOrCreate()

class Test(unittest.TestCase):


    def test_business_transform(self):
        
        """
            Reads business dataset, cleans data and stores processed files in output destination
        """

        self.input = "/Users/shrirupdwivedi/Library/CloudStorage/OneDrive-Personal/Springboard/Capstone_1/Code_Test/"
        self.output = "/Users/shrirupdwivedi/Library/CloudStorage/OneDrive-Personal/Springboard/Capstone_1/Code_Test/"
  
        df_b = spark.read.json(self.input+"yelp_academic_dataset_business.json")

        #take RestaurantsPriceRange2 value from attributes column :
        df_b = df_b.withColumn("price_range", col("attributes").getField("RestaurantsPriceRange2"))
        df_b = df_b.na.drop() #drop null values 
        df_b = df_b.filter(col("categories").contains("Restaurants")) #filter out non restaurant businesses
        df_b = df_b.drop("attributes") #drop attribute column
        df_b.write.format("parquet").mode("overwrite").save(self.output + "business.parquet")

        check1 = os.path.exists("business.parquet") #check if the file exist of not

        self.assertTrue(check1,"Test failed. The file does not exist.")


    def test_checkin_transform(self):

        """
            Reads checkin dataset, cleans data and stores processed files in output destination
        """

        self.input = "/Users/shrirupdwivedi/Library/CloudStorage/OneDrive-Personal/Springboard/Capstone_1/Code_Test/"
        self.output = "/Users/shrirupdwivedi/Library/CloudStorage/OneDrive-Personal/Springboard/Capstone_1/Code_Test/"
        df_c = spark.read.json(self.input+"yelp_academic_dataset_checkin.json")
        df_c = df_c.withColumn("no_of_checkins",size(split(col("date"),",")))
        df_c = df_c.drop("date")
        df_c.write.format("parquet").mode("overwrite").save(self.output + "checkin.parquet")

        check2 = os.path.exists("checkin.parquet")

        self.assertTrue(check2,"Test failed. The file does not exist.")



if __name__ == '__main__':
    unittest.main()