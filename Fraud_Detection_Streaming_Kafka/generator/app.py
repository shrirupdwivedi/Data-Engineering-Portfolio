from kafka import KafkaProducer
from time import sleep
import os
import json

from transactions import create_random_transaction

# grab the URL of our broker
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")

# extract the queueing.transactions topic 
TRANSACTIONS_TOPIC = os.environ.get("TRANSACTIONS_TOPIC")

# create sleep time variable
TRANSACTIONS_PER_SECOND = float(os.environ.get("TRANSACTIONS_PER_SECOND"))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND

if __name__ == "__main__":
    # instanciate the actual producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer=lambda value: json.dumps(value).encode(),
        )

    # naming the topic
    while True:
        transaction: dict = create_random_transaction()
        # Kafka messages are plain bytes => need to 'encode()' the string message
        producer.send(TRANSACTIONS_TOPIC, value=transaction)
        # Debug
        print(transaction)
        # sleep 
        sleep(SLEEP_TIME)