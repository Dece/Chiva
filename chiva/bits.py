import binascii
import string
from typing import List, Union


TBools = List[int]  # Should be 1 or 0 only.


class Bits(object):
    """ Bits containers. Internally stores bits as an int list.

    The Bits class is more a collection of static methods acting on TBools
    objects and data rather than a regular OOP class.
    """

    def __init__(self, initial_value: Union[int, None] =None):
        """ Initialise the Bits object with an optional initial integer value.

        Note that 0 will fill the bit list with a 0, but None will not. See
        set_value for details.
        """
        self.bools = []  # type: TBools
        if initial_value is not None:
            self.set_value(initial_value, explicit_zero=True)

    def __str__(self) -> str:
        return "".join([str(b) for b in self.bools])

    def set_value(self, integer: int, num_bits: Union[int, None] =None,
                  explicit_zero: bool =False):
        """ Represent this integer value.

        Make this Bits instance represent this integer. To keep prepending 0s,
        specify num_bits to the amount of bits expected to represent this int.
        If num_bits is smaller than the required amount of bits to represent
        integer, this Bits won't represent properly integer but a truncated
        value. In doubt, leave num_bits to its default None value, which will
        not impose an amount of prepending 0s nor a size limit.

        Passing a null integer to this function will not add any bits to the
        internal bools list by default, only if explicit_zero is True. This
        argument is only used internally by the constructor so Bits(0) can
        return an object with a non-empty list, but all factories will not
        follow this behaviour: an empty source will result to an empty bit list.
        See the test suite for examples.
        """
        if explicit_zero and integer == 0:
            self.bools = [0]
            return
        else:
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

    def format(self, group_by: int, sep: str =' ') -> str:
        packed = str(self)
        formatted = ""
        for i, b in enumerate(packed):
            if i > 0 and i % group_by == 0:
                formatted += sep
            formatted += b
        return formatted

    ################################
    # Factories
    ################################

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
        """ Convert a str with hexdigits to Bits. """
        if data.lower().startswith('0x'):
            data = data[2:]
        data = ''.join([c for c in data if c in string.hexdigits])
        data_bytes = bytes.fromhex(data)
        return Bits.from_bytes(data_bytes)

    @staticmethod
    def from_bitstring(data: str) -> 'Bits':
        """ Convert a str with 0 and 1 to Bits. """
        if data.lower().startswith('0b'):
            data = data[2:]
        bits = Bits()
        bits.bools = [int(bit) for bit in data if bit in ('0', '1')]
        return bits

    ################################
    # Converting
    ################################

    def xor(self, other: 'Bits') -> TBools:
        """ XOR these bits with another Bits object (same length is assumed). """
        return Bits.xor_bools(self.bools, other.bools)

    def parity_bit(self, parity: str ='odd') -> int:
        """ Return the parity bit of these bits.
        
        The parity parameter can be 'odd' (default) or 'even', determining the
        evenness of the result.
        """
        pb = 1 if parity == 'odd' else 0
        for b in self.bools:
            pb ^= b
        return pb

    def lrc(self, bits_per_char: int) -> Union[TBools, None]:
        """ Return the LRC of these bits, or None on error.
        
        It assumes there are bits_per_char bits for each character inside bools.
        If bools length can't be divded by bits_per_char, return None.
        """
        bools = self.bools
        num_bools = len(bools)
        invalid_input = (
            num_bools == 0 or
            bits_per_char == 0 or
            num_bools % bits_per_char != 0
        )
        if invalid_input:
            return None

        lrc_char = bools[:bits_per_char]  # Init LRC with first char
        num_chars = num_bools // bits_per_char
        for _ in range(1, num_chars):
            bools = bools[bits_per_char:]
            char = bools[:bits_per_char]
            lrc_char = Bits.xor_bools(lrc_char, char)
        return lrc_char

    def luhn(self, bits_per_char: int) -> int:
        """ Return the Luhn key of these bits. """
        chars = self.pack_chars(bits_per_char)
        chars.reverse()
        key = 0
        for index, char in enumerate(chars):
            if index % 2 == 1:
                pass
        return 0  # TODO

    def pack_chars(self, bits_per_char: int) -> List[int]:
        """ Pack bits to form and return a list of ints.
        
        Pack bits by groups with a length of bits_per_char to return a list of
        corresponding ints. Examples:
        - Bits.from_hexstring("ABCD").pack_chars(8) == [0xAB, 0xCD]
        - Bits.from_hexstring("ABCD").pack_chars(4) == [0xA, 0xB, 0xC, 0xD]
        """
        bools = self.bools
        num_bools = len(self.bools)
        invalid_input = (
            num_bools == 0 or
            bits_per_char == 0 or
            num_bools % bits_per_char != 0
        )
        if invalid_input:
            return None

        num_chars = num_bools // bits_per_char
        chars = [None] * num_chars
        for index in range(num_chars):
            char = bools[:bits_per_char]
            bools = bools[bits_per_char:]
            chars[index] = Bits.bools_to_int(char)
        return chars

    ################################
    # Static utilities
    ################################

    @staticmethod
    def bools_to_int(bools: TBools, byteorder: str ='big') -> int:
        """ Return the int represented by these bools. """
        out = 0
        if byteorder == 'little':
            bools.reverse()
        for bit in bools:
            out = (out << 1) | bit
        return out

    @staticmethod
    def xor_bools(bools_a: TBools, bools_b: TBools) -> TBools:
        return [a ^ b for a, b in zip(bools_a, bools_b)]
