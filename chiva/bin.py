import binascii
import string
from typing import List, TypeVar, Union


TBools = List[int]  # Should be 1 or 0 only.


class Bits(object):
    """ Bits containers. Internally stores bits as an int list.

    The Bits class is more a collection of static methods acting on TBools
    objects and data rather than a regular OOP class.
    """

    def __init__(self) -> None:
        self.bools = []  # type: TBools

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
        data = ''.join([c for c in data if c in string.hexdigits])
        data_bytes = binascii.unhexlify(data)
        return Bits.from_bytes(data_bytes)

    @staticmethod
    def from_bitstring(data: str) -> 'Bits':
        """ Convert a str with 0 and 1 to Bits. """
        if data.lower().startswith('0b'):
            data = data[2:]
        bits = Bits()
        bits.bools = [int(bit) for bit in data if bit in ('0', '1')]
        return bits

    @staticmethod
    def xor_bools(bools_a: TBools, bools_b: TBools) -> TBools:
        """ XOR two TBools, same length is assumed. """
        return [a ^ b for a, b in zip(bools_a, bools_b)]

    @staticmethod
    def parity_bit(bools: TBools, parity: str ='odd') -> int:
        """ Return the parity bit for bools.
        
        The parity parameter can be 'odd' (default) or 'even', determining the
        evenness of the result.
        """
        pb = 1 if parity == 'odd' else 0
        for b in bools:
            pb ^= b
        return pb

    @staticmethod
    def lrc(bools: TBools, bits_per_char: int) -> Union[TBools, None]:
        """ Return the LRC for bools, or None on error.
        
        It assumes there are bits_per_char bits for each character inside bools.
        If bools length can't be divded by bits_per_char, return None.
        """
        num_bools = len(bools)
        if num_bools == 0 or bits_per_char == 0 or num_bools % bits_per_char != 0:
            return None

        lrc_char = bools[:bits_per_char]  # Init LRC with first char
        num_chars = num_bools // bits_per_char
        for _ in range(1, num_chars):
            bools = bools[bits_per_char:]
            char = bools[:bits_per_char]
            lrc_char = Bits.xor_bools(lrc_char, char)
        return lrc_char
