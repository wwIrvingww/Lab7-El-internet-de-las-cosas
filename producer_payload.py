import time
import random
from kafka import KafkaProducer
from sensor_simulator import generate_data
from encode_decode import encode_payload

TOPIC_NAME = "202012345"
BOOTSTRAP_SERVER = "iot.redesuvg.cloud:9092"

def create_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_serializer=lambda v: v,  # Already bytes
        retries=5
    )

def run_producer():
    producer = create_producer()
    print("Payload Producer started. Sending 3-byte messages...")

    try:
        while True:
            data = generate_data()

            payload = encode_payload(
                data["temperature"],
                data["humidity"],
                data["wind_direction"]
            )

            producer.send(TOPIC_NAME, value=payload)
            producer.flush()

            print("Sent (encoded 3 bytes):", payload.hex(), " | original:", data)

            time.sleep(random.randint(15, 30))

    except KeyboardInterrupt:
        print("Producer stopped.")

if __name__ == "__main__":
    run_producer()
