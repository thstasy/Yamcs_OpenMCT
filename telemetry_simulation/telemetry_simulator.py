import sys
import zmq
import socket
import asyncio
import struct
import random
import time
from daq import Telemetry as DAQTelemetry  # DAQ telemetry from daq.py
from fsw import Telemetry as FSWTelemetry  # FSW telemetry from fsw.py
from daq import DAQ_COEF  # Import DAQ_COEF from daq.py

# Ports for UDP and ZMQ
UDP_PORT = 10015  # Make sure this matches the port in your Yamcs config
ZMQ_PORT = 5555  # For future ZMQ setup

# Function to simulate DAQ telemetry data using daq.py and telemetry.py
def generate_daq_telemetry():
    # Simulate random telemetry values for the 8 channels and other fields
    ch = [random.randint(0, 32767) for _ in range(8)]  # 8 channels (2 bytes each)
    tv_sec = int(time.time())  # Current timestamp (seconds)
    tv_nsec = int((time.time() % 1) * 1e9)  # Nanoseconds part of the timestamp
    sequence = random.randint(0, 65535)  # Random sequence number (2 bytes)
    
    # Limit daq_no to valid values in DAQ_COEF
    daq_no = random.choice(list(DAQ_COEF.keys()))  # DAQ number (choose from available keys)
    
    print(f"Generating telemetry for DAQ number {daq_no}")

    # Pack the data into a binary structure (16 bytes for channels, 4+4 bytes for time, 2+2 bytes for sequence and DAQ no)
    raw_data = struct.pack(">8hIiHH", *ch, tv_sec, tv_nsec, sequence, daq_no)
    
    # Create a DAQTelemetry object using the packed data
    telemetry = DAQTelemetry(raw_data)
    
    # Dump the raw telemetry data
    packet = telemetry.dump()
    
    # Ensure that packet[1:9] are integers
    packed_data = struct.pack(">d", telemetry.timestamp[0]) + struct.pack(">8h", *map(int, packet[1:9]))  # Ensure int conversion
    return packed_data

# Function to simulate FSW telemetry data using fsw.py and telemetry.py
def generate_fsw_telemetry():
    # Generate raw binary data and use FSW telemetry logic to pack it
    raw_data = struct.pack(">I", random.randint(1000, 2000))  # Simulate a random 4-byte int packet
    telemetry = FSWTelemetry(raw_data)  # Use FSW telemetry class from fsw.py
    packet = telemetry.dump()  # Use the dump method to get telemetry data
    return struct.pack(">d", telemetry.timestamp[0]) + struct.pack(">6B", *packet[:6])  # Pack FSW fields

# Function to send telemetry over UDP
def send_udp(target_ip, data):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(data, (target_ip, UDP_PORT))

# Function to send telemetry over ZMQ
def send_zmq(target_ip, data):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUB)
    zmq_socket.connect(f"tcp://{target_ip}:{ZMQ_PORT}")
    zmq_socket.send(data)

# Asynchronous function to simulate telemetry data and send it
async def simulate_telemetry(target_ip, protocol, interval, telemetry_type):
    while True:
        if telemetry_type == 'daq':
            # Generate telemetry data for all DAQs
            data = generate_daq_telemetry()  # Simulate DAQ telemetry data
            if protocol == 'udp':
                print(f"Sending UDP DAQ telemetry: {data}")
                send_udp(target_ip, data)
            elif protocol == 'zmq':
                print(f"Sending ZMQ DAQ telemetry: {data}")
                send_zmq(target_ip, data)
            await asyncio.sleep(interval)
        elif telemetry_type == 'fsw':
            # Generate and send FSW telemetry data (no changes needed)
            data = generate_fsw_telemetry()
            if protocol == 'udp':
                print(f"Sending UDP FSW telemetry: {data}")
                send_udp(target_ip, data)
            elif protocol == 'zmq':
                print(f"Sending ZMQ FSW telemetry: {data}")
                send_zmq(target_ip, data)
            await asyncio.sleep(interval)
        else:
            raise ValueError(f"Invalid telemetry type: {telemetry_type}")

# Main function
def main():
    if len(sys.argv) < 5:
        print(f"Usage: {sys.argv[0]} <target IP> <protocol (udp|zmq)> <interval> <telemetry_type (daq|fsw)>")
        exit(1)

    target_ip = sys.argv[1]
    protocol = sys.argv[2].lower()
    interval = float(sys.argv[3])
    telemetry_type = sys.argv[4].lower()

    # Validate the protocol
    if protocol not in ['udp', 'zmq']:
        print("Invalid protocol specified. Use 'udp' or 'zmq'.")
        exit(1)

    # Validate telemetry type
    if telemetry_type not in ['daq', 'fsw']:
        print("Invalid telemetry type. Use 'daq' or 'fsw'.")
        exit(1)

    # Start the telemetry simulation
    try:
        asyncio.run(simulate_telemetry(target_ip, protocol, interval, telemetry_type))
    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == '__main__':
    main()

