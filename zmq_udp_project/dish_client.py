import zmq
import struct  # For unpacking telemetry data

context = zmq.Context()

# Set up a SUB socket for receiving data over TCP
dish = context.socket(zmq.SUB)
dish.connect("tcp://localhost:5555")  # Connect to the TCP port 5555
dish.setsockopt_string(zmq.SUBSCRIBE, "telemetry_channel")  # Subscribe to the telemetry channel

def receive_telemetry():
    message = dish.recv()
    # Strip out the channel name (first part) and unpack the telemetry data
    telemetry_data = message[len(b"telemetry_channel"):]  # Skip the channel name part
    timestamp, sensor_value1, sequence_count, sensor_value2, sequence_count2, sensor_value3 = struct.unpack('!IfIfIf', telemetry_data)

    # Display the telemetry values
    print(f"Received telemetry: timestamp={timestamp}, temp={sensor_value1}, pressure={sensor_value2}, humidity={sensor_value3}")

if __name__ == "__main__":
    while True:
        receive_telemetry()
