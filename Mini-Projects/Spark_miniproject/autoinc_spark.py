from pyspark import SparkContext
import findspark
findspark.init()
from func import extract_vin_key_value, populate_make, extract_make_key_value
from operator import add

sc = SparkContext("local", "My Application")

raw_rdd = sc.textFile("data.csv")

vin_kv = raw_rdd.map(lambda x: extract_vin_key_value(x))

enhance_make = vin_kv.groupByKey().flatMap(lambda kv: populate_make(kv[1]))

make_kv = enhance_make.map(lambda list_val: extract_make_key_value(list_val))

# Assign final result
final_output = make_kv.reduceByKey(add).collect()
print(final_output)

# Export to text file
with open("final_output.txt", "w") as output:
    for val in final_output:
        print(val)
        output.write(str(val).strip("( )") + "\n")
        
# Stop Spark Application
sc.stop()
