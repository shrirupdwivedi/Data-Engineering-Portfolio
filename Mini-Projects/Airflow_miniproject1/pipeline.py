from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta, date
import yfinance as yf
import pandas as pd



def download1():

    start_date = date.today() - timedelta(days=1)
    end_date = start_date + timedelta(days=1)
    tsla_df = yf.download('TSLA', start=start_date, end=end_date, interval='1m')
    tsla_df.to_csv("/opt/airflow/data_tsla.csv")

def download2():

    start_date = date.today() - timedelta(days=1)
    end_date = start_date + timedelta(days=1)
    appl_df = yf.download('AAPL', start=start_date, end=end_date, interval='1m')
    appl_df.to_csv("/opt/airflow/data_appl.csv")






default_args = {
    'owner' : 'Shrirup',
    'start_date' : datetime.today(),
    'retries' : 1,
    'retry_delay' : timedelta(minutes=5)

}

with DAG(
    'marketvol',
    default_args=default_args,
    description='A simple DAG',
    schedule_interval='0 18 * * 5') as dag :


    t0 = BashOperator(task_id='t0',
    #bash_command = 'mkdir -p /Users/shrirupdwivedi/Desktop/springboard-airflow'+ str(datetime.today() ),
    bash_command='mkdir -p /tmp/data/' + str(datetime.today() ),
    dag=dag)


    t1 = PythonOperator(task_id = 't1', python_callable=download1,dag=dag)
    t2 = PythonOperator(task_id = 't2', python_callable=download2,dag=dag)

    t3 = BashOperator(task_id='t3',
    
    bash_command='mv /opt/airflow/data_appl.csv /tmp/data/'+ str(date.today()) ,
    dag=dag)

    t4 = BashOperator(task_id='t4',
    
    bash_command='mv /opt/airflow/data_tsla.csv /tmp/data/'+ str(date.today()) ,
    dag=dag)

    def spread():
        """ Function that calculates the stock's spreading value.
        Formula: spread = high value - low value
        """
        LOCAL_DIR = '/tmp/data/' + str(date.today() )
        apple_data = pd.read_csv(LOCAL_DIR+"/data_appl.csv").sort_values(by = "Datetime", ascending = False)
        tesla_data = pd.read_csv(LOCAL_DIR + "/data_tsla.csv").sort_values(by = "Datetime", ascending = False)
        spread = [apple_data['High'][0] - apple_data['Low'][0], tesla_data['High'][0] - tesla_data['Low'][0]]
        return spread





    t5 = PythonOperator(task_id='t5',python_callable=spread,dag=dag)



t0 >> [t1,t2] 
t1 >> t3
t2 >> t4
[t3,t4] >> t5

