import mysql.connector 
import csv

def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",port = '3306', database = 'Springboard'
        )
        
    except Exception as error:
        print("Error while connecting to database for job tracker", error)
    return connection


def load_third_party(connection):
    cursor = connection.cursor()
    #cursor.execute('CREATE TABLE sales (ticket_id INT, trans_date DATE, event_id INT , event_name VARCHAR (50), event_date DATE, event_type VARCHAR(10), event_city VARCHAR(20), customer_id INT, price DECIMAL, num_tickets INT)') 

    sql = "INSERT INTO sales (ticket_id, trans_date, event_id, event_name, event_date, event_type,event_city, customer_id, price, num_tickets) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    with open('third_party_sales_1.csv','r') as csvfile:
        datareader = csv.reader(csvfile)
        r = []
        for row in datareader:
            r.append(row)

    cursor.executemany(sql, r)
    connection.commit()
    cursor.close()
    return

def query_popular_tickets(connection):
    sql = "SELECT event_name FROM sales ORDER BY num_tickets DESC"
    cursor = connection.cursor()
    cursor.execute(sql)
    record = cursor.fetchone()
    print("The most popular ticket came from the event {dd1}".format(dd1=record[0]) )

connection = get_db_connection()
load_third_party(connection)
query_popular_tickets(connection)

