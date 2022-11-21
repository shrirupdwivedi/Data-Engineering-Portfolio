import logging
from tracker import Tracker
from configdirectory import ConfigDirectory

def track_data_ingestion(config):
    """
    The method is used to keep track on the actions of the data ingestion.py
    update_job_status() method is used to store the needed data; for example: "job_id", "status", "updated_time" will be stored in Postgresql
    :param config: obtain the configuration data from config.py file
    :return: 
    """

    tracker = Tracker("data_ingestion", config)
    job_id = tracker.assign_job_id()
    connection = tracker.get_db_connection()
    connection
    try:
        # In addition, create methods to assign job_id and get db connection.
        tracker.data_ingestion()
        tracker.update_job_status("successful", job_id, connection)
    except Exception as e:
        print(e)
        tracker.update_job_status("failed", job_id, connection)
    return


if __name__ == '__main__':
    # Get logging info
    logger = logging.getLogger(__name__) 

    # Create config file
    my_config = ConfigDirectory("logconfig.ini", "log_name").config_directory()

    # Obtain log file from config file
    log_file = my_config["log_name"]

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

    # Call reporter_etl(my_config)
    track_data_ingestion(my_config)

    # Enter logging information.
    logger.info("Daily Data Ingestion Job complete!")