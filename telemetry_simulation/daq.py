import struct
from ds import telemetry

# Define the telemetry structure
DAQ_TLM_DF = {
    "ch[8]": ("int16", 0, 16),
    "tv_sec": ("int32", 16, 4),
    "tv_nsec": ("int32", 20, 4),
    "sequence": ("uint16", 24, 2),
    "daq_no": ("uint16", 26, 2),
}

# Coefficients for different DAQ numbers, including the newly added 768
DAQ_COEF = {
    3: [
        (0.08060576, -40),
        (0.2441, -48.634),
        (0.0972, -18.256),
        (0.0977, -18.647),
        (1.0, 0),  # Parachute line cutters
        (1.0, 0),
        (1.0, 0),
        (1.0, 0),
    ],
    7: [
        (0.0982, -19.079),
        (0.0981, -18.844),
        (0.0980, -18.925),
        (0.0981, -19.150),
        (0.0982, -18.863),
        (0.0981, -19.031),
        (0.0980, -18.970),
        (0.0981, -18.973),
    ],
    512: [
        (0.1, -20),
        (0.2, -25),
        (0.3, -30),
        (0.4, -35),
        (0.5, -40),
        (0.6, -45),
        (0.7, -50),
        (0.8, -55),
    ],
    768: [
        (0.05, -12),
        (0.1, -22),
        (0.15, -32),
        (0.2, -42),
        (0.25, -52),
        (0.3, -62),
        (0.35, -72),
        (0.4, -82),
    ],
    1023: [
        (0.2, -10),
        (0.3, -15),
        (0.4, -20),
        (0.5, -25),
        (0.6, -30),
        (0.7, -35),
        (0.8, -40),
        (0.9, -45),
    ]
}

class Telemetry(telemetry.Telemetry):
    def __init__(self, data):
        super().__init__(data, **DAQ_TLM_DF)
        self.timestamp = (self.tv_sec[0] + self.tv_nsec[0] / 10 ** 9,)

    def voltage(self):
        return list(self.ch)

    def convert(self):
        # Check if daq_no exists in DAQ_COEF, if not, use default coefficients
        if self.daq_no[0] not in DAQ_COEF:
            print(f"Warning: DAQ number {self.daq_no[0]} not found. Using default coefficients.")
            # Default safe coefficients (all zeroed voltages, as an example)
            return (0.0,) * 8  # Fallback to zero voltage across 8 channels

        return tuple(
            map(
                lambda x: x[1][0] * x[0] + x[1][1],
                zip(self.voltage(), DAQ_COEF[self.daq_no[0]]),
            )
        )

    def dump_header(self):
        header = ["timestamp"]
        header.extend([f"ch{i}" for i in range(8)])
        header.extend(["sequence", "daq_no"])
        return header

    def dump(self):
        return self.timestamp + self.convert() + self.sequence + self.daq_no

    def dump_raw(self):
        return self.timestamp + self.ch + self.sequence + self.daq_no


def process(filename, start_time=0, end_time=10 ** 10):
    with open(filename, "rb") as f:
        while True:
            try:
                data = f.read(28)
                telemetry = Telemetry(data)
            except:
                break
            timestamp = telemetry.timestamp[0]
            if start_time <= timestamp <= end_time:
                yield timestamp, telemetry

