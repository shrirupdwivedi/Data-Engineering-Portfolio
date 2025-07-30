![image](https://user-images.githubusercontent.com/68109182/215864008-ca1547a8-ac77-43b9-a49f-ababe04c11ed.png)

# Restaurants Review Analysis Data Pipeline using Yelp Dataset

This project involved creation of end-to-end data pipleine using Yelp dataset sized 8 GB. The purpose of the data pipeline is to analyse the dataset to answer questions such as: 

- Fiding cities with highest number of top-rated restaurants
- Fiding cities with highest number of lowest-rated restaurants
- Finding top 10 restaurants in New Orleans(city with highest rated restaurants) in terms of review counts and stars

The project follows the following steps:

**-[Data Collection](https://github.com/shrirupdwivedi/Springboard/tree/main/Capstone/Data_Collection)**

Kaggle API is used to acquire the 8 GB JSON formatted dataset

**-[Data Exploration](https://github.com/shrirupdwivedi/Springboard/tree/main/Capstone/Data_Exploration)**

 We did Exploratory Data Analysis (EDA) in order to gain a better understanding of your data.
 Once we have this knowledge in hand, we'll be able to better plan for transforming and loading your data later in the project
 
 **-[Data Pipeline Prototype](https://github.com/shrirupdwivedi/Springboard/tree/main/Capstone/Data_Pipeline_Prototype)**
 
 A data pipeline prototype is created before full-scale deployment later in cloud. For this, the ELT process is done in local python set-up.
 
**-[Scaled Data Pipeline](https://github.com/shrirupdwivedi/Springboard/blob/main/Capstone/Scaled_Data_Pipeline/main.ipynb)**

Azure HDInsight Spark cluster is used in this stage to create scaled data pipeline ELT

**-[Production Data Pipeline](https://github.com/shrirupdwivedi/Springboard/tree/main/Capstone/Production_Code)**

Finally, the fully functional pipeline with analytical queries in SparkSQL is done
