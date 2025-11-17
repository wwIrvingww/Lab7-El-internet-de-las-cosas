import json
import random
import numpy as np

# Possible wind directions
WIND_DIRECTIONS = ["N", "NW", "W", "SW", "S", "SE", "E", "NE"]

def generate_temperature():
    """
    Generates a temperature value using a normal distribution
    centered at 55 degrees with a standard deviation of 15.
    The value is clamped to the range [0, 110].
    """
    temp = np.random.normal(loc=55, scale=15)
    temp = max(0, min(110, temp))
    return round(temp, 2)

def generate_humidity():
    """
    Generates an integer humidity value in the range [0, 100].
    """
    return random.randint(0, 100)

def generate_wind_direction():
    """
    Selects one of the eight possible wind directions.
    """
    return random.choice(WIND_DIRECTIONS)

def generate_data():
    """
    Returns a dictionary representing one sensor reading.
    """
    return {
        "temperature": generate_temperature(),
        "humidity": generate_humidity(),
        "wind_direction": generate_wind_direction()
    }

def generate_json():
    """
    Converts the sensor reading into a JSON string.
    """
    return json.dumps(generate_data(), ensure_ascii=False)

if __name__ == "__main__":
    # Simple test: generate 5 sensor readings
    for _ in range(5):
        reading = generate_json()
        print("Generated reading:", reading)
