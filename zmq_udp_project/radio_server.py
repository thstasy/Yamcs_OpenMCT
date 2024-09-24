import zmq
import time
import struct  # For packing telemetry data into binary format

context = zmq.Context()

# Set up a PUB socket for publishing telemetry data over TCP
radio = context.socket(zmq.PUB)
radio.bind("tcp://*:5555")  # Bind to TCP port 5555

def send_telemetry():
    # Real-time data (example)
    timestamp = int(time.time())  # Current Unix timestamp
    sequence_count = 101  # Increment this in a real system
    sensor_value1 = 25.5  # Example sensor value 1 (e.g., temperature in Celsius)
    sensor_value2 = 1013.25  # Example sensor value 2 (e.g., pressure in hPa)
    sensor_value3 = 48.2  # Example sensor value 3 (e.g., humidity in %)

    # Pack the telemetry data into a binary format
    telemetry_packet = struct.pack('!IfIfIf', timestamp, sensor_value1, sequence_count, sensor_value2, sequence_count + 1, sensor_value3)

    # Send the binary telemetry packet over the TCP channel
    radio.send(b"telemetry_channel" + telemetry_packet)
    print(f"Sent telemetry: timestamp={timestamp}, temp={sensor_value1}, pressure={sensor_value2}, humidity={sensor_value3}")

if __name__ == "__main__":
    while True:
        send_telemetry()
        time.sleep(1)  # Send data every second
