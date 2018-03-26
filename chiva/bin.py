from typing import Union


class Bin(object):
    def __init__(self, data=None):
        self.data = data or b""

    @property
    def data(self) -> bytes:
        return self._data
    @data.setter
    def data(self, data: bytes):
        self._data = data
        self._integer = self.bytes_to_integer(self.data)

    @property
    def integer(self) -> int:
        return self._integer

    @staticmethod
    def bytes_to_integer(data: bytes, byteorder: Union["little", "big"] ="little") -> int:
        return int.from_bytes(data, byteorder=byteorder)

    def binary_str(self, bits_per_byte: int =8, sep: str ="") -> str:
        mask = 2 ** bits_per_byte - 1
        data = self.integer
        results = []
        while data or not results:
            masked = data & mask
            byte_str = str(bin(masked)[2:]).zfill(bits_per_byte)
            results.append(byte_str)
            data = data >> bits_per_byte
        result = sep.join(results)
        return result
