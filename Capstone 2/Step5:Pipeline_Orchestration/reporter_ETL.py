import sys
import logging
from reporter import Reporter
from configdirectory import ConfigDirectory
from pyspark.sql import SparkSession


# Create SparkSession object
spark = SparkSession.builder.master('local').appName('app').getOrCreate()
sc = spark.sparkContext

# Assign directory variable
eod_dir = "/mnt/data/cloud-storage-path/"

def run_reporter_etl(config):
    """
    Take config object from "if ... main" block and use it to get trade_date as shown below.
    Initiate reporter object to report data using spark session object, trade_data, and eod_dir (directory for EOD Load).
    :param config: Config file object .
    :return:
    """
    trade_date = config  # TODO: Need to create section for trade_date later on.
    reporter = Reporter(spark)
    try:
        reporter.report(spark, trade_date, eod_dir)
    except Exception as e:
        print(e)
    return

if __name__ == "__main__":

    # Get logging info
    logger = logging.getLogger(__name__) 

    # Create config file
    my_config = ConfigDirectory("dateconfig.ini", "production").config_directory()["processing_date"]

    # Obtain log file from config file
    log_file = ConfigDirectory("logconfig.ini", "log_file").config_directory()["log_name"]

    # Write data to logfile
    logging.basicConfig(
        # components of logging file i.e. format.
        filename=log_file,
        filemode='w',
        format='%(asctime)s %(message)s',
        datefmt='%m%d%Y %I:%M:%S',
        level=logging.DEBUG
    )

    # StreamHandler object to send logging output to streams such as sys.stdout, sys.stderr.
    sh = logging.StreamHandler()

    # Set level for logging
    sh.setLevel(logging.INFO)

    # Call addHandler
    logger.addHandler(sh)

    # Call run_reporter_etl(my_config)
    run_reporter_etl(my_config)

    # Enter logging information.
    logger.info("Daily Reporting ETL Job complete!")