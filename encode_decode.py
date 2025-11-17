def encode_payload(temperature, humidity, wind_direction):
    """
    Encodes the meteorological data into a 3-byte payload (24 bits).
    temperature: float (0.00 - 110.00)
    humidity: int (0 - 100)
    wind_direction: one of ["N","NW","W","SW","S","SE","E","NE"]
    """
    wind_map = ["N", "NW", "W", "SW", "S", "SE", "E", "NE"]

    # Scale temperature: multiply by 10
    temp_int = int(round(temperature * 10))  # 0 - 1100 (fits in 11 bits)

    hum_int = humidity                      # 0 - 100 (fits in 7 bits)
    wind_int = wind_map.index(wind_direction)  # 0 - 7 (fits in 3 bits)

    # Pack into 24 bits
    packed = (temp_int << 10) | (hum_int << 3) | wind_int

    # Convert to bytes (3 bytes big-endian)
    return packed.to_bytes(3, byteorder="big")


def decode_payload(payload_bytes):
    """
    Decodes a 3-byte payload back into temperature, humidity, wind_direction.
    """
    wind_map = ["N", "NW", "W", "SW", "S", "SE", "E", "NE"]

    # Convert bytes to int
    packed = int.from_bytes(payload_bytes, byteorder="big")

    # Extract fields
    wind_int = packed & 0b111
    hum_int = (packed >> 3) & 0b1111111
    temp_int = (packed >> 10) & 0b11111111111  # 11 bits

    temperature = temp_int / 10.0
    humidity = hum_int
    wind = wind_map[wind_int]

    return {
        "temperature": temperature,
        "humidity": humidity,
        "wind_direction": wind
    }
