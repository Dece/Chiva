import random

import pytest

from chiva.bin import Bin


random.seed()


class TestBin(object):
    def test_binary_str(self):
        assert Bin(b"\x00").binary_str() == "00000000"
        assert Bin(b"\x04").binary_str() == "00000100"
        assert Bin(b"\xFF").binary_str() == "11111111"
        assert Bin(b"\x0F\xFF").binary_str() == '0000111111111111'

        assert Bin(b"\xFF").binary_str(bits_per_byte=4) == '11111111'

        assert Bin(b"\xFF").binary_str(sep=" ") == '11111111'
        assert Bin(b"\xFF\x0F").binary_str(sep=" ") == '11111111 00001111'
        
        assert Bin(b"\xFF\x0F").binary_str(bits_per_byte=4, sep=" ") == '1111 1111 0000 1111'
        assert Bin(b"\xFF\x0F").binary_str(bits_per_byte=5, sep=" ") == '00001 11111 11000 01111'
