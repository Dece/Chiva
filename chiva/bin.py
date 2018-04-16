import binascii
from typing import List, TypeVar, Union


TBits = List[int]  # Should be 1 or 0 only.


class Bits(object):
    """ Bits containers. Internally stores bits as a boolean list. """

    def __init__(self) -> None:
        self.bools = []  # type: TBits

    def __str__(self) -> str:
        return "".join([str(b) for b in self.bools])

    def set_value(self, integer: int, num_bits: Union[int, None] =None):
        """ Represent this integer value.

        Make this Bits instance represent this integer. To keep prepending 0s,
        specify num_bits to the amount of bits expected to represent this int.
        If num_bits is smaller than the required amount of bits to represent
        integer, this Bits won't represent properly integer but a truncated
        value, In doubt, leave num_bits to its default None value, which will
        not impose an amount of prepending 0s nor a size limit.
        """
        self.bools = []
        while True:
            if num_bits == 0:
                break

            if integer > 0:
                self.bools.insert(0, integer & 1)
                integer = integer >> 1
                if num_bits is not None:
                    num_bits -= 1
            elif num_bits is not None and num_bits > 0:
                self.bools = [0] * num_bits + self.bools
                break
            else:
                break

    @staticmethod
    def from_bytes(data: bytes, byteorder: str ='big') -> 'Bits':
        """ Convert the integer represented the bytes data to Bits. """
        bits = Bits()
        num_bits = len(data) * 8
        integer = int.from_bytes(data, byteorder)
        bits.set_value(integer, num_bits)
        return bits

    @staticmethod
    def from_hexstring(data: str) -> 'Bits':
        """ Convert a str with hex digits to Bits. """
        if data.lower().startswith('0x'):
            data = data[2:]
        data_bytes = binascii.unhexlify(data)
        return Bits.from_bytes(data_bytes)

    @staticmethod
    def from_bitstring(data: str) -> 'Bits':
        """ Convert a str with 0 and 1 to Bits. """
        if data.startswith('0b'):
            data = data[2:]
        bits = Bits()
        bits.bools = [int(bit) for bit in data if bit in ('0', '1')]
        return bits
