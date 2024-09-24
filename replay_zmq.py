#!/usr/bin/python

import os
import sys
import zmq
import zlib
import time
import socket
import pickle
from datetime import datetime

from ds import fsw, daq

AVI_DAQ_PORT = 1230
FSW_PORT = 1235

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <log filename> <target IP> <loop>")
        exit(1)

    filename = sys.argv[1]
    DAQ_tlm = []
    FSW_tlm = []
    ALL_tlm = []
    last_timestamp = 0
    loop = 1

    if len(sys.argv) > 3:
        loop = int(sys.argv[3])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with open(filename, "rb") as log_file:
        # CRC verify
        tlm_ok = 0
        tlm_bad = 0

        while True:
            try:
                # [ ZMQ Tag, data, CRC ]
                tlm = pickle.load(log_file)

                # Verify CRC
                if (zlib.crc32(tlm[1]) & 0xffffffff).to_bytes(4, 'little') == tlm[2]:
                    tlm_ok += 1

                    # Ignore IPCam data
                    if b'ARRC-FSW' in tlm[0]:
                        t = fsw.Telemetry(tlm[1])
                        FSW_tlm.append((t.timestamp[0], tlm[1]))
                        ALL_tlm.append((t.timestamp[0], tlm[1], 'FSW'))
                    elif b'ARRC-DAQ-AVI.0x00' == tlm[0]:
                        t = daq.Telemetry(tlm[1])
                        DAQ_tlm.append((t.timestamp[0], tlm[1]))
                        ALL_tlm.append((t.timestamp[0], tlm[1], 'DAQ'))
                else:
                    tlm_bad += 1

            except Exception as e:
                print(e)
                break

        print(f'Verified packet count: {tlm_ok} \n Damaged packet count: {tlm_bad}')

        FSW_tlm.sort(key = lambda entry : entry[0])
        DAQ_tlm.sort(key = lambda entry : entry[0])
        ALL_tlm.sort(key = lambda entry : entry[0])

        print(f'FSW TLM count: {len(FSW_tlm)}')
        print(f'DAQ TLM count: {len(DAQ_tlm)}')
        print(f'ALL TLM count: {len(ALL_tlm)}')

        for i in range(0, loop):
            last_timestamp = ALL_tlm[0][0]
            for tlm in ALL_tlm:
                t_diff = tlm[0] - last_timestamp
                last_timestamp = tlm[0]
                time.sleep(t_diff)
                if(tlm[2] == 'FSW'):
                    sock.sendto(tlm[1], (sys.argv[2], FSW_PORT))
                if(tlm[2] == 'DAQ'):
                    sock.sendto(tlm[1], (sys.argv[2], AVI_DAQ_PORT))

if __name__ == '__main__':
    main()
