import pickle
import zlib

# Dummy classes for fsw and daq telemetry objects
class FSWTelemetry:
    def __init__(self, timestamp):
        self.timestamp = [timestamp]

class DAQTelemetry:
    def __init__(self, timestamp):
        self.timestamp = [timestamp]

def generate_dummy_data(filename, num_entries=10):
    with open(filename, "wb") as log_file:
        for i in range(num_entries):
            # Creating dummy data for FSW and DAQ
            fsw_tlm = FSWTelemetry(timestamp=i)
            daq_tlm = DAQTelemetry(timestamp=i)

            # Pickling the FSW telemetry
            fsw_data = pickle.dumps(fsw_tlm)
            fsw_crc = zlib.crc32(fsw_data).to_bytes(4, 'little')
            fsw_entry = [b'ARRC-FSW', fsw_data, fsw_crc]

            # Pickling the DAQ telemetry
            daq_data = pickle.dumps(daq_tlm)
            daq_crc = zlib.crc32(daq_data).to_bytes(4, 'little')
            daq_entry = [b'ARRC-DAQ-AVI.0x00', daq_data, daq_crc]

            # Write FSW and DAQ data to the file
            pickle.dump(fsw_entry, log_file)
            pickle.dump(daq_entry, log_file)

if __name__ == "__main__":
    generate_dummy_data("telemetry.log", num_entries=20)
    print("Dummy telemetry data generated in telemetry.log")
