import enum
import struct
import pickle
# Py < 3.8, pickle only supports to highest protocol version 4.
# Use pickle5 to load TLM_DF.
# https://docs.python.org/3.8/library/pickle.html#data-stream-format
if pickle.HIGHEST_PROTOCOL < 5:
    import pickle5 as pickle

from ds import telemetry
from ds import files


# Open FSW Telemetry DictFlatten
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Py < 3.7
    import importlib_resources as pkg_resources
FSW_TLM_DF = pickle.load(pkg_resources.open_binary(files, "tlm_df.pkl"))


CFE_DS_HEADER_SIZE = 64 + 76  # CFE_FS_Header_t + DS_FileHeader_t


class SID(enum.IntEnum):
    EVS_LONG_MSG = 0x808
    PILOT = 0x829
    SENSOR = 0x81B
    SENSOR_EXT = 0x817
    NAV = 0x81C
    NAV_EXT = 0x81D
    NAV_NED_CORE = 0x81A
    NAV_NED_EXT = 0x81E
    CONTROL = 0x81F
    ECM = 0x838
    ECM_EXT = 0x839

    def __repr__(self):
        return "<%s.%s: 0x%04x/%04d>" % (
            self.__class__.__name__,
            self.name,
            self.value,
            self.value,
        )


class Telemetry(telemetry.Telemetry):
    def __init__(self, data):
        sid = data[0] << 8 | data[1]
        if sid in FSW_TLM_DF:
            super().__init__(data, **FSW_TLM_DF[sid])
        else:
            # Assume they are CCSDS telemetry, but not in our DF
            super().__init__(data, **{"TlmHeader[12]": ("uint8", 0, 12)})

    def imu(self, name):
        # Only IMU sensor can use this method!
        if self.sid != 0x81B:
            return TypeError
        if name not in ["accel", "gyro", "magn"]:
            return KeyError

        nd = []
        for i in range(10):
            nd.append(self.IMU_data.inav[name][i * 3 : i * 3 + 3])
        return nd


def process(filename, start_time=0, end_time=10 ** 10):
    with open(filename, "rb") as f:
        f.read(CFE_DS_HEADER_SIZE)
        while True:
            try:
                hdr = f.read(6)
                sid = hdr[0] << 8 | hdr[1]
                seq = hdr[2] << 8 | hdr[3]
                size = hdr[4] << 8 | hdr[5]
            except:
                break
            data = f.read(size + 1)
            timestamp = telemetry.get_ccsds_timestamp(data)
            if start_time <= timestamp <= end_time:
                yield timestamp, Telemetry(hdr + data)
