import json
import time
import random
from kafka import KafkaProducer
from sensor_simulator import generate_data

# Edit this with your actual topic (student ID)
TOPIC_NAME = "202012345"  

# Kafka broker
BOOTSTRAP_SERVER = "iot.redesuvg.cloud:9092"

def create_producer():
    """
    Creates and returns a Kafka producer configured to send JSON messages.
    """
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        retries=5
    )

def run_producer():
    """
    Continuously generates sensor readings and sends them
    to the Kafka topic every 15–30 seconds.
    """
    producer = create_producer()
    print("Kafka Producer started. Sending data to topic:", TOPIC_NAME)

    try:
        while True:
            data = generate_data()
            producer.send(TOPIC_NAME, value=data)
            producer.flush()

            print("Sent:", data)

            # Sleep between 15 and 30 seconds
            wait_time = random.randint(15, 30)
            time.sleep(wait_time)

    except KeyboardInterrupt:
        print("Producer stopped manually.")

if __name__ == "__main__":
    run_producer()
