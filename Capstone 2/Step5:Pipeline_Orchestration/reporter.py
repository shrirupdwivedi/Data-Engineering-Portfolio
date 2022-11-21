import datetime
from configdirectory import ConfigDirectory

class Reporter():
    """
    Reporter class consists of the report() method.py
    we use Reporter class to be used to inherit the Spark context object and the
    configuration settings as the input.py
    
    The report() method will be used to read parquet files and run some queries for the report
    """

    def __init__(self, spark):
        self.spark = spark

    def report(self, spark, trade_date, eod_dir):
        """
        This method is used to read the parquet files and automate some queries in order to create
        the output as the report() method
        :param spark: Spark sesion object
        :param trade_date: The trade date for the needed dataset
        :param eod_dir: The directory of the dataset
        :return:
        """

        # assigns variable for the date time
        date = datetime.datetime.strptime(trade_date, "%Y-%m-%d" )
        prev_date = date - datetime.strptime(days=1)
        prev_date = prev_date.strftime("%Y-%m-%d")

        # get azure config
        params_azure = ConfigDirectory("azureconfig.ini", "azure_storage_config").config_directory()

        # mount the blob storage
        mount_dir = "/mnt/data"
        dbutils.fs.mount(
                        source = "wasbs://%s@%s.blob.core.windows.net" %(params_azure["container_name"], params_azure["storage_name"]),
                        mount_point = mount_dir,
                        extra_configs = {"fs.azure.account.key.%s.blob.core.windows.net" % (params_azure["storage_name"]): params_azure["key"] })

        # read the desired trade 
        df = spark.read.parquet("{}trade/trade_dt={}".format(eod_dir, trade_date))\
            .selectExpr("trade_dt", 
                        "symbol", 
                        "exchange", 
                        "CAST(event_tm as timestamp)  AS event_tm",
                        "event_seq_nb", "trade_pr")

        # create a temporary view
        df.creatOrReplaceTempView("temp_last_trade")

        # read the previous trade 
        df = spark.read.parquet("{}trade/trade_dt={}".format(eod_dir, prev_date))\
            .selectExpr("trade_dt", 
                        "symbol", 
                        "exchange", 
                        "CAST(event_tm as timestamp)  AS event_tm",
                        "event_seq_nb", "trade_pr")

        # read the quote
        df = spark.read.parquet("{}trade/trade_dt={}".format(eod_dir, trade_date)) \
            .selectExpr("trade_dt", "symbol", "exchange", "cast(event_tm as timestamp) as event_tm",
                        "event_seq_nb", "bid_pr", "bid_size", "ask_pr", "ask_size")
        
        # create a temporary view
        df.createOrReplaceTempView("temp_quotes")

        # moving average query
        moving_avg_df = spark.sql("""
        SELECT trade_dt, 
               symbol, 
               exchange, 
               event_tm, 
               event_seq_nb, 
               trade_pr,
               mean(trade_pr) OVER (PARTITION BY symbol, exchange ORDER BY event_tm 
                              RANGE BETWEEN INTERVAL 30 MINUTES PRECEDING AND CURRENT ROW
        FROM temp_quotes)
        """)

        # create temporary view
        moving_avg_df.createOrReplaceTempView("temp_moving_avg")

        # create union quote query
        quote_union = spark.sql("""
        SELECT trade_dt, 'Q' as rec_type, symbol, event_tm, event_seq_nb, exchange,
               bid_pr, bid_size, ask_pr, ask_size, null as trade_pr, null as mov_avg_pr
        FROM quotes
        UNION ALL
            SELECT trade_dt, 'T' as rec_type, symbol, event_tm, event_seq_nb, exchange,
                   null as bid_pr, null as bid_size, null as ask_pr, null as ask_size, trade_pr, mov_avg_pr
        FROM temp_moving_avg
        """)

        # create temporary view
        quote_union.createOrReplaceTempView("temp_quote_union")

        # create updated quote
        quote_union_update = spark.sql("""
        SELECT *,
               last_value(trade_pr, true) OVER (PARTITION BY symbol, exchange ORDER BT event_tm ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS last_trade_pr,
               last_value(mov_avg_pr, true) OVER (PARTITION BY symbol, exchange ORDER BT event_tm ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS last_mov_avg_pr
        FROM temp_quote_union
        """)
        quote_union_update.createOrReplaceTempView("temp_quote_union_update")

        # Quote Update
        quote_update = spark.sql("""
        SELECT trade_dt, 
               symbol, 
               event_tm, 
               event_seq_nb, 
               exchange,
               bid_pr, 
               bid_size, 
               ask_pr, 
               ask_size, 
               last_trade_pr, 
               last_mov_avg_pr
        FROM temp_quote_union_update
        WHERE rec_type = 'Q'
        """)
        quote_update.createOrReplaceTempView("temp_quote_union_update")

        # create quote final query
        quote_final = spark.sql("""
        SELECT trade_dt, 
               symbol, 
               event_tm, 
               event_seq_nb, 
               exchange, 
               bid_pr, 
               bid_size, 
               ask_pr, 
               ask_size, 
               last_trade_pr, 
               last_mov_avg_pr,
               bid_pr - close_pr as bid_pr_mv, 
               ask_pr - close_pr as ask_pr_mv
        FROM (
            SELECT /*+ BROADCAST(t) */ q.trade_dt, 
                                       q.symbol, 
                                       q.event_tm, 
                                       q.event_seq_nb, 
                                       q.exchange,
                                       q.bid_pr, 
                                       q.bid_size, 
                                       q.ask_pr, 
                                       q.ask_size, 
                                       q.last_trade_pr, 
                                       q.last_mov_avg_pr,
                                       t.last_pr as close_pr
                FROM quote_update AS q
            LEFT OUTER JOIN temp_last_trade AS t 
            ON  q.symbol = t.symbol 
            AND q.exchange = t.exchange
        ) AS a
        """)

        quote_final.write.mode("overwrite").parquet("{}quote-trade-analytical/trade_dt={}".format(eod_dir, trade_date))

        return

    def save_as_csv(self, df, filename):
        df.write("overwrite").csv(filename)
        return