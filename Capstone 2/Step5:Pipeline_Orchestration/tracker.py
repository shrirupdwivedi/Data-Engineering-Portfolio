import json
import logging
from datetime import datetime
from random import randint
import psycopg2
from configdirectory import ConfigDirectory
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DecimalType

class Tracker:
    """
    The Tracker class is used for the desired job_id, status, and updated_time
    
    """

    def __init__(self, jobname, dbconfig):
        self.jobname = jobname
        self.dbconfig = dbconfig

    def get_db_connection(self):
        '''
        The method will establish the connection with PostgreSQL and automatically get the config file as input
        '''
        connection = None
        try:
            # read connection to the PostgreSQL database server
            params_postgres = ConfigDirectory("database.ini", "postgresql").config_directory()

            # connect to the PostgreSQL server
            connection = psycopg2.connect(params_postgres)

            return connection
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("Error while connecting to database for job tracker", error)

    def data_ingestion(self):
        """"
        The method that ingests both CSV and JSON formats
        """

        # create Spark Session
        spark = SparkSession.builder.master('local').appName('app').getOrCreate()
        sc = spark.sparkContext

        # get azure config
        params_azure = ConfigDirectory("azureconfig.ini", "azure_storage_config").config_directory()

        # create common event schema
        commonEventSchema = StructType([
            StructField("trade_dt", StringType(), True),
            StructField("rec_type", StringType(), True),
            StructField("symbol", StringType(), True),
            StructField("exchange", StringType(), True),
            StructField("event_tm", StringType(), True),
            StructField("event_seq_nb", StringType(), True),
            StructField("arrival_tm", StringType(), True),
            StructField("trade_pr", StringType(), True),
            StructField("bid_pr", StringType(), True),
            StructField("bid_size", StringType(), True),
            StructField("ask_pr", StringType(), True),
            StructField("ask_size", StringType(), True),
            StructField("execution_id", StringType(), True),
            StructField("trade_size", StringType(), True),
            StructField("partition", StringType(), True)
        ])

        # create csv parser
        def parse_csv(line):
            """
            Inner function that parses the CSV file and returns the desired output format
            """
            fields = line.split(',')
            try:
                if fields[2] == 'Q':
                    trade_dt = fields[0]
                    rec_type = fields[2]
                    symbol = fields[3]
                    exchange = fields[6]
                    event_tm = fields[1]
                    event_seq_nb = fields[5]
                    arrival_tm = fields[4]
                    trade_pr = '-'
                    bid_pr = fields[7]
                    bid_size = fields[8]
                    ask_pr = fields[9]
                    ask_size = fields[10]
                    execution_id = 'NA'
                    trade_size = 'NA'
                    partition = "Q"
                elif fields[2] == 'T':
                    trade_dt = fields[0]
                    rec_type = fields[2]
                    symbol = fields[3]
                    exchange = fields[6]
                    event_tm = fields[1]
                    event_seq_nb = fields[5]
                    arrival_tm = fields[4]
                    trade_pr = fields[7]
                    bid_pr = '-'
                    bid_size = '-'
                    ask_pr = '-'
                    ask_size = '-'
                    execution_id = 'NA'
                    trade_size = 'NA'
                    partition = "T"
                # Return event as list
                event = [trade_dt, rec_type, symbol, exchange, event_tm, event_seq_nb, arrival_tm,
                         trade_pr, bid_pr, bid_size, ask_pr, ask_size, execution_id, trade_size, partition]
                return event
            # Rejected events
            except Exception as e:
                event = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, "B"]
                logging.error("Bad record", e)
                return event
        
        def parse_json(self):
            fields = json.loads(line)
            try:
                if fields['event_type'] == 'Q':
                    trade_dt = fields['trade_dt']
                    rec_type = fields['event_type']
                    symbol = fields['symbol']
                    exchange = fields['exchange']
                    event_tm = fields['event_tm']
                    event_seq_nb = fields['event_seq_nb']
                    arrival_tm = fields['file_tm']
                    trade_pr = '-'
                    bid_pr = fields['bid_pr']
                    bid_size = fields['bid_size']
                    ask_pr = fields['ask_pr']
                    ask_size = fields['ask_size']
                    execution_id = '-'
                    trade_size = '-'
                    partition = "Q"
                elif fields['event_type'] == 'T':
                    trade_dt = fields['trade_dt']
                    rec_type = fields['event_type']
                    symbol = fields['symbol']
                    exchange = fields['exchange']
                    event_tm = fields['event_tm']
                    event_seq_nb = fields['event_seq_nb']
                    arrival_tm = fields['file_tm']
                    trade_pr = fields['price']
                    bid_pr = '-'
                    bid_size = '-'
                    ask_pr = '-'
                    ask_size = '-'
                    execution_id = fields['execution_id']
                    trade_size = fields['size']
                    partition = "T"
                # Return event object as list
                event = [trade_dt, rec_type, symbol, exchange, event_tm, event_seq_nb, arrival_tm,
                         trade_pr, bid_pr, bid_size, ask_pr, ask_size, execution_id, trade_size, partition]
                return event
            except Exception as e:
                event = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, "B"]
                logging.error("Bad record", e)
                return event
        
        # csv path
        csv_dir_1 = "/data/csv/2020-08-05/NYSE/part-00000-5e4ced0a-66e2-442a-b020-347d0df4df8f-c000.txt"
        csv_dir_2 = "/data/csv/2020-08-06/NYSE/part-00000-214fff0a-f408-466c-bb15-095cd8b648dc-c000.txt"

        json_dir_1 = "/data/json/2020-08-05/NASDAQ/part-00000-c6c48831-3d45-4887-ba5f-82060885fc6c-c000.txt"
        json_dir_2 = "/data/json/2020-08-06/NASDAQ/part-00000-092ec1db-39ab-4079-9580-f7c7b516a283-c000.txt"

        # Raw text files
        raw_csv_1 = sc.textFile( "wasbs://%s@%s.blob.core.windows.net%s" %( params_azure["container_name"], params_azure["storage_name"], csv_dir_1))

        raw_csv_2 = sc.textFile( "wasbs://%s@%s.blob.core.windows.net%s" %( params_azure["container_name"], params_azure["storage_name"], csv_dir_2))

        raw_json_1 = sc.textFile( "wasbs://%s@%s.blob.core.windows.net%s" %( params_azure["container_name"], params_azure["storage_name"], json_dir_1))

        raw_json_2 =  sc.textFile( "wasbs://%s@%s.blob.core.windows.net%s" %( params_azure["container_name"], params_azure["storage_name"], json_dir_2))

        # Parsed files
        parsed_csv1 = raw_csv_1.map(lambda line: parse_csv(line))
        parsed_csv2 = raw_csv_2.map(lambda line: parse_csv(line))

        parsed_json1= raw_json_1.map(lambda line: parse_json(line))
        parsed_json2= raw_json_2.map(lambda line: parse_json(line))

        # Create Data Frames
        spark_df1 = spark.createDataFrame(parsed_csv1, commonEventSchema)
        spark_df2 = spark.createDataFrame(parsed_csv2, commonEventSchema)
        spark_df3 = spark.createDataFrame(parsed_json1, commonEventSchema)
        spark_df4 = spark.createDataFrame(parsed_json2, commonEventSchema)

        # Join all the dataframe
        union_df = spark_df1.union(spark_df2)\
                    .union(spark_df3)\
                    .union(spark_df4)

        # Write The Common Events Into Partitions As Parquet Files To HDFS
        union_df.write.partitionBy("partition").mode("overwrite").parquet("output_dir")

        # Stop Spark
        sc.stop()

    def assign_job_id(self):
        """
        This method creates a combination of jobname, 5 digits string and datetime object to automatically
        generate a job_id.
        :return: job_id
        """
        num_string = str(randint(0, 10000)).zfill(5)
        job_id = self.jobname + str(num_string) + datetime.today().strftime("%Y%m%d")
        return job_id

    def update_job_status(self, status, assigned_job_id, connection):
        """
        This method initializes the PostgreSql connection and insert the table information into
        :param status: gives the job_status which could be "SUCCESS", "FAILED", or other descriptive message as
        "processing CSV/JSON files"
        :param assigned_job_id: gets the returned value from assign_job_id() method and stores as a variable
        :param connection: is the value from get_db_connection() method and is stored as a variable
        """
        job_id = assigned_job_id
        print("Job ID Assigned: {}".format(job_id))
        update_time = datetime.now()

        try:
            # start the cursor
            dbCursor = connection.cursor()
            # create query
            job_command = "INSERT INTO job_tracker_table(job_id, job_status, update_time) " \
                            "VALUES('" + job_id + "', '" + status + "', '" + str(update_time) + "')"
            # execute the query
            dbCursor.execute(job_command)
            # close the cursor
            dbCursor.close()
            print("Inserted data into job tracker table.")
        except (Exception, psycopg2.DatabaseError) as error:
            return logging.error("Error executing db statement for job tracker.", error)