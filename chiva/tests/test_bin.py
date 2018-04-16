import pytest

from chiva.bin import Bits


DEAD_BITS = "1101111010101101"  # 0xDEAD


def test_bools():
    assert Bits().bools == []


def test_set_value():
    bits = Bits()
    bits.set_value(0)
    assert bits.bools == []
    bits.set_value(1)
    assert bits.bools == [1]
    bits.set_value(10)
    assert bits.bools == [1, 0, 1, 0]
    bits.set_value(255)
    assert bits.bools == [1] * 8

    # Test num_bits param
    bits.set_value(0, num_bits=0)
    assert bits.bools == []
    bits.set_value(1, num_bits=0)
    assert bits.bools == []

    bits.set_value(0, num_bits=1)
    assert bits.bools == [0]
    bits.set_value(1, num_bits=1)
    assert bits.bools == [1]

    bits.set_value(0xFF, num_bits=4)
    assert bits.bools == [1, 1, 1, 1]
    bits.set_value(0xFF, num_bits=8)
    assert bits.bools == [1, 1, 1, 1, 1, 1, 1, 1]
    bits.set_value(0xFF, num_bits=10)
    assert bits.bools == [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]


def test_str():
    bits = Bits()
    assert str(bits) == ""
    bits.bools = [1]
    assert str(bits) == "1"
    bits.bools = [1, 1, 0, 1]
    assert str(bits) == "1101"
    bits.bools = DEAD_BITS
    assert str(bits) == "1101111010101101"


def test_from_bytes():
    assert str(Bits.from_bytes(b"")) == ""
    assert str(Bits.from_bytes(b"\x00")) == "00000000"
    assert str(Bits.from_bytes(b"\xFF")) == "11111111"
    assert str(Bits.from_bytes(b"\xF0")) == "11110000"
    assert str(Bits.from_bytes(b"\x0F")) == "00001111"
    assert str(Bits.from_bytes(b"\xDE\xAD")) == DEAD_BITS


def test_from_hexstring():
    assert str(Bits.from_hexstring("")) == ""
    assert str(Bits.from_hexstring("0x00")) == "00000000"
    assert str(Bits.from_hexstring("DEAD")) == DEAD_BITS


def test_from_bitstring():
    assert str(Bits.from_bitstring("")) == ""
    assert str(Bits.from_bitstring("1")) == "1"
    assert str(Bits.from_bitstring("11010100010")) == "11010100010"
    assert str(Bits.from_bitstring("0b11010100010")) == "11010100010"
