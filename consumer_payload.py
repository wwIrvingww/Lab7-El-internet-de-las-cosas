import matplotlib.pyplot as plt
from kafka import KafkaConsumer
from encode_decode import decode_payload

TOPIC_NAME = "202012345"
BOOTSTRAP_SERVER = "iot.redesuvg.cloud:9092"

def create_consumer():
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVER,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        value_deserializer=lambda m: m  # m is bytes
    )

def plot_live(temps, hums, winds):
    plt.clf()

    plt.subplot(3, 1, 1)
    plt.plot(temps, marker="o")
    plt.title("Temperature (°C)")

    plt.subplot(3, 1, 2)
    plt.plot(hums, marker="o")
    plt.title("Humidity (%)")

    plt.subplot(3, 1, 3)
    plt.plot(winds, marker="o")
    plt.title("Wind Direction (index)")

    plt.tight_layout()
    plt.pause(0.1)

def run_consumer():
    consumer = create_consumer()

    temps = []
    hums = []
    winds = []

    plt.ion()
    plt.show()

    print("Payload Consumer started. Listening...")

    for msg in consumer:
        decoded = decode_payload(msg.value)

        temps.append(decoded["temperature"])
        hums.append(decoded["humidity"])
        winds.append(["N","NW","W","SW","S","SE","E","NE"].index(decoded["wind_direction"]))

        print("Received (decoded):", decoded)

        plot_live(temps, hums, winds)

if __name__ == "__main__":
    run_consumer()
