Post-Sale Automobile Report using Hadoop MapReduce framework in Docker

The following steps are needed in order to run the files in this folder:

1) Install Docker and Hadoop framework in Docker
2) Publish the following command to get the result:
   docker exec -it namenode bash
   
   cat data.csv | python3 autoinc_mapper1.py | sort | python3
   autoinc_reducer1.py | python3 autoinc_mapper2.py | sort | python3
   autoinc_reducer2.py
   
Due to problems relating to installation of Hadoop framework in Docker, Hadoop could not be used to get the results. Instead bash pipeline was used to get the results.

The CLI file provides the command line interactions to get the results.
   
   
