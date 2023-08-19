from typing import NamedTuple

class ByteArrayReaderException(Exception):
    pass


class VersionException(Exception):
    def __init__(self, expected: int, actual: int) -> None:
        super().__init__(f"Version mismatch: expected {expected}, got {actual}")


class ByteArrayReader:
    def __init__(self, data: bytes) -> None:
        self.index = 0
        self.data = data
        if type(data) != bytes:
            raise Exception(f"Bad type: {type(data)}")

    def count_remaining(self) -> int:
        return len(self.data) - self.index

    def assert_remaining(self, min_count: int) -> None:
        actual = self.count_remaining()
        if actual < min_count:
            raise ByteArrayReaderException(f"Expected {min_count} byte(s), but only has {actual} remaining")

    def assert_finished(self) -> None:
        actual = self.count_remaining()
        if actual != 0:
            raise ByteArrayReaderException(f"Expected no more bytes, but only has {actual} remaining")

    def get_byte(self) -> int:
        self.assert_remaining(1)
        index = self.index
        self.index += 1
        return int(self.data[index])

    def get_bytes(self, length: int) -> bytes:
        self.assert_remaining(length)
        start = self.index
        self.index += length
        return self.data[start:self.index]

    def get_int32(self) -> int:
        data = self.get_bytes(4)
        value = 0
        value += data[0] << 24
        value += data[1] << 16
        value += data[2] << 8
        value += data[3]
        return value


class V1Frame(NamedTuple):
    version: int # 1 byte
    transfer_hash: bytes # 20 bytes
    transfer_offset: int # 4 bytes
    data: bytes # 1+ bytes


class V1Transfer(NamedTuple):
    version: int # 1 byte
    transfer_hash: bytes # 20 bytes (in each packet)
    name: str # 4 bytes + data
    contents: bytes # 4 bytes + data


def parse_v1_frame(payload: bytes) -> V1Frame:
    ba = ByteArrayReader(payload)
    version = ba.get_byte()
    if version != 1:
        raise VersionException(1, version)

    transfer_hash = ba.get_bytes(20)
    transfer_offset = ba.get_int32()
    data_len = ba.count_remaining()
    if data_len == 0:
        raise ByteArrayReaderException("No bytes for field data remaining")
    data = ba.get_bytes(data_len)
    ba.assert_finished()

    return V1Frame(version, transfer_hash, transfer_offset, data)


def parse_v1_transfer(payload: bytes, transfer_hash: bytes) -> V1Transfer:
    ba = ByteArrayReader(payload)
    version = ba.get_byte()
    if version != 1:
        raise VersionException(1, version)

    name_length = ba.get_int32()
    name = ba.get_bytes(name_length)
    contents_length = ba.get_int32()
    contents = ba.get_bytes(contents_length)
    ba.assert_finished()

    name_str = name.decode("utf-8")
    return V1Transfer(version, transfer_hash, name_str, contents)
