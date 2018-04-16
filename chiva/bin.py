from typing import List, TypeVar


TBits = List[int]  # Should be 1 or 0 only.


class Bits(object):
    """ Bits containers. Internally stores bits as a boolean list. """

    def __init__(self) -> None:
        self.bools = []  # type: TBits

    def __str__(self) -> str:
        return "".join([str(b) for b in self.bools])

    @staticmethod
    def from_bytes(data: bytes, byteorder: str ='big') -> 'Bits':
        bits = Bits()
        num_bits = len(data) * 8
        integer = int.from_bytes(data, byteorder)
        while integer or num_bits:
            bits.bools.insert(0, integer & 1)
            integer = integer >> 1
            num_bits -= 1
        return bits

    @staticmethod
    def from_hexstring(data: str) -> 'Bits':
        bits = Bits()
        return bits
