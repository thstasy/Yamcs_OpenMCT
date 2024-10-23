# import binascii
# import io
# import socket
# import struct
# import time
# import logging
# import os

# # Setup logging configuration
# logging.basicConfig(
#     filename='simulator.log',
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s',
# )

# def send_tm(simulator):
#     # Ensure the testdata.ccsds file exists before attempting to open it
#     if not os.path.exists('testdata.ccsds'):
#         logging.error("Telemetry data file 'testdata.ccsds' not found.")
#         return
    
#     # Set up the UDP socket
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     yamcs_address = ('localhost', 10000)  # Adjust to your Yamcs UDP port

#     with io.open('testdata.ccsds', 'rb') as f:
#         logging.info("Opened telemetry data file successfully.")
#         simulator.tm_counter = 1
#         header = bytearray(6)
#         while f.readinto(header) == 6:
#             logging.info(f"Reading telemetry header for packet {simulator.tm_counter}")
#             (length,) = struct.unpack('>H', header[4:6])
#             packet = bytearray(length + 7)
#             f.seek(-6, io.SEEK_CUR)
#             f.readinto(packet)

#             # Send packet over UDP
#             udp_socket.sendto(packet, yamcs_address)
#             logging.info(f"Sent telemetry packet {simulator.tm_counter} with length: {len(packet)} bytes")
#             simulator.tm_counter += 1
#             time.sleep(1)

# class Simulator:
#     def __init__(self):
#         self.tm_counter = 0

#     def start(self):
#         send_tm(self)

# if __name__ == '__main__':
#     simulator = Simulator()
#     simulator.start()

#     try:
#         prev_status = None
#         while True:
#             status = f'Sent: {simulator.tm_counter} packets.'
#             if status != prev_status:
#                 logging.info(status)
#                 prev_status = status
#             time.sleep(0.5)
#     except KeyboardInterrupt:
#         logging.info("Simulator stopped by user.")
#         print('\n')

import binascii
import io
import struct
import time
import logging
import os
import zmq

# Setup logging configuration
logging.basicConfig(
    filename='simulator.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def send_tm(simulator):
    # Ensure the testdata.ccsds file exists before attempting to open it
    if not os.path.exists('testdata.ccsds'):
        logging.error("Telemetry data file 'testdata.ccsds' not found.")
        return
    
    # Set up the ZMQ context and socket for UDP transport
    context = zmq.Context()
    zmq_socket = context.socket(zmq.RADIO)  # ZMQ RADIO socket for UDP
    zmq_socket.connect("udp://localhost:5555")  # Connect to UDP transport

    with io.open('testdata.ccsds', 'rb') as f:
        logging.info("Opened telemetry data file successfully.")
        simulator.tm_counter = 1
        header = bytearray(6)
        while f.readinto(header) == 6:
            logging.info(f"Reading telemetry header for packet {simulator.tm_counter}")
            (length,) = struct.unpack('>H', header[4:6])
            packet = bytearray(length + 7)
            f.seek(-6, io.SEEK_CUR)
            f.readinto(packet)

            # Send packet over ZMQ (UDP) using the RADIO socket
            zmq_socket.send(packet)
            logging.info(f"Sent telemetry packet {simulator.tm_counter} with length: {len(packet)} bytes via ZMQ+UDP")
            simulator.tm_counter += 1
            time.sleep(1)

class Simulator:
    def __init__(self):
        self.tm_counter = 0

    def start(self):
        send_tm(self)

if __name__ == '__main__':
    simulator = Simulator()
    simulator.start()

    try:
        prev_status = None
        while True:
            status = f'Sent: {simulator.tm_counter} packets.'
            if status != prev_status:
                logging.info(status)
                prev_status = status
            time.sleep(0.5)
    except KeyboardInterrupt:
        logging.info("Simulator stopped by user.")
        print('\n')
