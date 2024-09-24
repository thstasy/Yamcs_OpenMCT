import struct

from ds import telemetry


DAQ_TLM_DF = {
    "ch[8]": ("int16", 0, 16),
    "tv_sec": ("int32", 16, 4),
    "tv_nsec": ("int32", 20, 4),
    "sequence": ("uint16", 24, 2),
    "daq_no": ("uint16", 26, 2),
}

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
}


class Telemetry(telemetry.Telemetry):
    def __init__(self, data):
        super().__init__(data, **DAQ_TLM_DF)
        self.timestamp = (self.tv_sec[0] + self.tv_nsec[0] / 10 ** 9,)

    def voltage(self):
        # return list(map(lambda v: 5.0 * ((v + 0.0) / 0x7FF), self.ch))
        return list(self.ch)

    def convert(self):
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
