#!/usr/bin/env python3
# MCP_UDP_FWD.PY
# Sends telemetry data via UDP to Yamcs

import socket
import sys
import json
import random
from datetime import datetime
import time  # <-- Add this line

# UDP settings
UDP_IP = "localhost"
UDP_PORT_FSW = 5001
UDP_PORT_DAQ_AVI = 5002
UDP_PORT_DAQ_ACC = 5003
UDP_PORT_GPSR = 5004
UDP_PORT_RTK = 5005
UDP_PORT_IMU_PAYLOAD = 5006

# Define UDP sockets
sock_fsw = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_daq_avi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_daq_acc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_gpsr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_rtk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_imu_payload = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Telemetry generation functions

def generate_fsw_telemetry():
    return {
        "timestamp": int(datetime.timestamp(datetime.now()) * 1000),
        "value": random.uniform(0.0, 10.0),  # Simulated value
        "id": "fsw"
    }

def generate_daq_avi_telemetry():
    return {
        "timestamp": int(datetime.timestamp(datetime.now()) * 1000),
        "value": random.uniform(0.0, 100.0),  # Simulated value
        "id": "daq_avi"
    }

def generate_daq_acc_telemetry():
    return {
        "timestamp": int(datetime.timestamp(datetime.now()) * 1000),
        "value": random.uniform(0.0, 100.0),  # Simulated value
        "id": "daq_acc"
    }

def generate_gpsr_telemetry():
    return {
        "timestamp": int(datetime.timestamp(datetime.now()) * 1000),
        "value": random.uniform(-180.0, 180.0),  # Simulated GPS longitude value
        "id": "gpsr"
    }

def generate_rtk_telemetry():
    return {
        "timestamp": int(datetime.timestamp(datetime.now()) * 1000),
        "value": random.uniform(-50.0, 50.0),  # Simulated RTK data
        "id": "rtk"
    }

def generate_imu_payload_telemetry():
    return {
        "timestamp": int(datetime.timestamp(datetime.now()) * 1000),
        "value": random.uniform(0.0, 9.8),  # Simulated IMU acceleration value
        "id": "imu_payload"
    }

# Send telemetry data over UDP
def send_telemetry(sock, port, telemetry_data):
    telemetry_json = json.dumps(telemetry_data)
    sock.sendto(telemetry_json.encode(), (UDP_IP, port))
    print(f"Sent telemetry to port {port}: {telemetry_json}")

def main():
    while True:
        # Generate and send FSW telemetry
        fsw_data = generate_fsw_telemetry()
        send_telemetry(sock_fsw, UDP_PORT_FSW, fsw_data)

        # Generate and send DAQ AVI telemetry
        daq_avi_data = generate_daq_avi_telemetry()
        send_telemetry(sock_daq_avi, UDP_PORT_DAQ_AVI, daq_avi_data)

        # Generate and send DAQ ACC telemetry
        daq_acc_data = generate_daq_acc_telemetry()
        send_telemetry(sock_daq_acc, UDP_PORT_DAQ_ACC, daq_acc_data)

        # Generate and send GPSR telemetry
        gpsr_data = generate_gpsr_telemetry()
        send_telemetry(sock_gpsr, UDP_PORT_GPSR, gpsr_data)

        # Generate and send RTK telemetry
        rtk_data = generate_rtk_telemetry()
        send_telemetry(sock_rtk, UDP_PORT_RTK, rtk_data)

        # Generate and send IMU Payload telemetry
        imu_payload_data = generate_imu_payload_telemetry()
        send_telemetry(sock_imu_payload, UDP_PORT_IMU_PAYLOAD, imu_payload_data)

        # Sleep for a short period to simulate telemetry intervals
        time.sleep(1)  # 1 second interval

if __name__ == '__main__':
    main()
