import re
import struct


ARRAY_PATTERN = r"\[(\d+)\]"
RE_ARRAY = re.compile(ARRAY_PATTERN)


class Telemetry:
    TYPEMAP = {
        "char": "c",
        "int8": "b",
        "uint8": "B",
        "int16": "h",
        "uint16": "H",
        "int32": "i",
        "uint32": "I",
        "int64": "q",
        "uint64": "Q",
        "float": "f",
        "double": "d",
        "int8_t": "b",
        "uint8_t": "B",
        "int16_t": "h",
        "uint16_t": "H",
        "int32_t": "i",
        "uint32_t": "I",
        "int64_t": "q",
        "uint64_t": "Q",
        "CCSDS_TelemetryPacket_t": "B",
    }
    SIZEMAP = {"c": 1, "b": 1, "h": 2, "i": 4, "f": 4, "d": 8, "q": 8}

    def __init__(self, data, **attrs):
        self._data = data
        self._unpacked_attrs = {}
        self._attrs = {}
        for k in attrs:
            if "[" in k or "]" in k:
                self._attrs[RE_ARRAY.sub("", k)] = attrs[k]
            else:
                self._attrs[k] = attrs[k]

        # Magic for the CCSDS header
        if "TlmHeader" in self._attrs:
            # Assume primary header & secondary header use 12 bytes
            hdr = self._data[:12]
            self.sid = hdr[0] << 8 | hdr[1]
            self.seq = hdr[2] << 8 | hdr[3]
            self.length = hdr[4] << 8 | hdr[5]
            self.timestamp = (get_ccsds_timestamp(hdr[6:]),)

    def keys(self):
        for k in self._attrs:
            if k == "PACK":
                continue
            yield k

    def values(self):
        for k in self.keys():
            if k == "PACK":
                continue
            yield self.__getattr__(k)

    def items(self):
        for k in self.keys():
            if k == "PACK":
                continue
            yield k, self.__getattr__(k)

    def fvalues(self):
        v = []
        for i in self.values():
            if i == "PACK":
                continue
            if isinstance(i, str):
                v.append(i)
            else:
                v.extend(i)
        return v

    def __getattr__(self, name):
        if name in self._attrs:
            # Return if we have already unpacked the attribues
            if name in self._unpacked_attrs:
                return self._unpacked_attrs[name]

            if isinstance(self._attrs[name], dict):
                try:
                    self._unpacked_attrs[name] = Telemetry(
                        self._data, **self._attrs[name]
                    )
                except TypeError:
                    # Assume this field is an array
                    if name not in self._unpacked_attrs:
                        self._unpacked_attrs[name] = {}
                    for k in self._attrs[name]:
                        # Make them to be the Telemetry
                        self._unpacked_attrs[name][k] = Telemetry(
                            self._data, **self._attrs[name][k]
                        )
                    return self._unpacked_attrs[name]
            if (
                isinstance(self._attrs[name], tuple)
                and name not in self._unpacked_attrs
            ):
                try:
                    sformat = self.TYPEMAP[self._attrs[name][0]]
                except KeyError:
                    # Assume the type is enum
                    sformat = "i"

                base = self._attrs[name][1]
                offset = self._attrs[name][2]
                size = offset // self.SIZEMAP[sformat.lower()]
                self._unpacked_attrs[name] = struct.unpack(
                    sformat * size, self._data[base : base + offset]
                )

                # XXX: assume char size lager than 12 is string
                if sformat == "c" and size > 12:
                    self._unpacked_attrs[name] = (
                        b"".join(self._unpacked_attrs[name])
                        .decode("ascii")
                        .strip("\x00")
                    )

            return self._unpacked_attrs[name]
        raise KeyError(f"Key '{name}' not found in telemetry")

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __iter__(self):
        return iter([i for i in self._attrs if i != "PACK"])

    def __repr__(self):
        if "TlmHeader" in self._attrs:
            return (
                f"<Stream ID: 0x{self.sid:04x}, "
                f"Sequence: {self.seq & 0x3FFF}, "
                f"Length: {self.length}, "
                f"Timestamp: {self.timestamp} >"
            )
        return super().__repr__()


def get_ccsds_timestamp(data):
    second = data[3] << 24 | data[2] << 16 | data[1] << 8 | data[0]
    ms = (data[5] << 8 | data[4]) / 65536.0
    return second + ms
