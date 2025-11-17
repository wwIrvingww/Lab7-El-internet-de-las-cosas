import json
import matplotlib.pyplot as plt
from kafka import KafkaConsumer

# Edit with your topic name
TOPIC_NAME = "202012345"

# Kafka broker
BOOTSTRAP_SERVER = "iot.redesuvg.cloud:9092"

def create_consumer():
    """
    Creates a Kafka consumer subscribed to a specific topic.
    """
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVER,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        group_id="group1"
    )

def plot_live(temperatures, humidities, wind_directions):
    """
    Plots the last N received values in a simple live chart.
    """
    plt.clf()

    plt.subplot(3, 1, 1)
    plt.plot(temperatures, marker="o")
    plt.title("Temperature")
    plt.ylabel("°C")

    plt.subplot(3, 1, 2)
    plt.plot(humidities, marker="o", color="orange")
    plt.title("Humidity")
    plt.ylabel("%")

    plt.subplot(3, 1, 3)
    plt.plot(wind_directions, marker="o", color="green")
    plt.title("Wind Direction")
    plt.ylabel("Index (0-7)")

    plt.tight_layout()
    plt.pause(0.1)

def run_consumer():
    """
    Reads meteorological data from Kafka and updates a live plot
    every time a new message arrives.
    """
    consumer = create_consumer()

    temperatures = []
    humidities = []
    wind_directions = []  # Convert categorical to numeric index

    direction_map = ["N", "NW", "W", "SW", "S", "SE", "E", "NE"]

    plt.ion()
    plt.show()

    print("Consumer started. Listening for messages...")

    for message in consumer:
        payload = message.value

        temp = payload.get("temperature")
        hum = payload.get("humidity")
        wind = payload.get("wind_direction")

        temperatures.append(temp)
        humidities.append(hum)
        wind_directions.append(direction_map.index(wind))

        print("Received:", payload)

        plot_live(temperatures, humidities, wind_directions)

if __name__ == "__main__":
    run_consumer()
