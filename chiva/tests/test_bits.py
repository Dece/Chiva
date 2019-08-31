import pytest

from chiva.bits import Bits


DEAD_BITS = "1101111010101101"  # 0xDEAD


def test_bools():
    assert Bits().bools == []
    assert Bits(0).bools == [0]
    assert Bits(1).bools == [1]
    assert Bits(10).bools == [1, 0, 1, 0]


def test_set_value():
    bits = Bits()
    bits.set_value(0)
    assert bits.bools == []
    bits.set_value(0, explicit_zero=True)
    assert bits.bools == [0]
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


def test_format():
    bits = Bits()
    assert bits.format(4) == bits.format(5) == ""
    bits = Bits.from_hexstring("B4B120")
    assert bits.format(4) == "1011 0100 1011 0001 0010 0000"
    assert bits.format(5) == "10110 10010 11000 10010 0000"


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
    assert str(Bits.from_hexstring("DE AD")) == DEAD_BITS


def test_from_bitstring():
    assert str(Bits.from_bitstring("")) == ""
    assert str(Bits.from_bitstring("1")) == "1"
    assert str(Bits.from_bitstring("11010100010")) == "11010100010"
    assert str(Bits.from_bitstring("110 10100010")) == "11010100010"
    assert str(Bits.from_bitstring("110 1010 0010")) == "11010100010"
    assert str(Bits.from_bitstring("110,1010,0010")) == "11010100010"
    assert str(Bits.from_bitstring("0b11010100010")) == "11010100010"


def test_xor():
    b_null = Bits()
    b_0 = Bits.from_bitstring("0")
    b_1 = Bits.from_bitstring("1")
    
    assert b_null.xor(b_null) == []
    assert b_0.xor(b_0) == [0]
    assert b_1.xor(b_0) == [1]
    assert b_0.xor(b_1) == [1]
    assert b_1.xor(b_1) == [0]

    b_00101 = Bits.from_bitstring("00101")
    b_11110 = Bits.from_bitstring("11110")
    assert b_00101.xor(b_11110) == [1, 1, 0, 1, 1]


def test_parity_bit():
    assert Bits().parity_bit() == 1
    assert Bits(0b0000).parity_bit() == 1
    assert Bits(0b0001).parity_bit() == 0
    assert Bits(0b0010).parity_bit() == 0
    assert Bits(0b0011).parity_bit() == 1
    assert Bits(0b1111).parity_bit() == 1
    assert Bits(0b11110).parity_bit() == 1
    assert Bits(0b111100).parity_bit() == 1
    assert Bits(0b1111001).parity_bit() == 0

    assert Bits().parity_bit(parity='even') == 0
    assert Bits(0b1111).parity_bit(parity='even') == 0
    assert Bits(0b1111001).parity_bit(parity='even') == 1


def test_lrc():
    b = Bits()
    assert b.lrc(0) == None
    assert b.lrc(4) == None

    b.bools = [0]
    assert b.lrc(0) == None
    assert b.lrc(1) == [0]

    b.bools = [
        0, 0, 0, 0,
        1, 0, 0, 0,
        0, 1, 0, 0,
        1, 1, 0, 0,
    ]
    assert b.lrc(4) == [0, 0, 0, 0]
    assert b.lrc(6) == None
    assert b.lrc(8) == [0, 1, 0, 0, 0, 1, 0, 0]

    # With parity bits
    b.bools = [
        0, 0, 0, 0, 1,
        1, 0, 0, 0, 0,
        0, 1, 0, 0, 0,
        1, 1, 0, 0, 1,
    ]
    assert b.lrc(5) == [0, 0, 0, 0, 0]


def test_luhn():
    b = Bits(1111)
    # TODO


def test_pack_chars():
    assert Bits().pack_chars(1) == None
    assert Bits(0).pack_chars(1) == [0]
    assert Bits(1).pack_chars(1) == [1]
    assert Bits(2).pack_chars(1) == [1, 0]
    assert Bits(3).pack_chars(1) == [1, 1]

    assert Bits(0b11001010).pack_chars(1) == [1, 1, 0, 0, 1, 0, 1, 0]
    assert Bits(0b11001010).pack_chars(2) == [3, 0, 2, 2]
    assert Bits(0b11001010).pack_chars(4) == [12, 10]
    assert Bits(0b11001010).pack_chars(8) == [202]
    assert Bits(0b11001010).pack_chars(9) == None

    assert Bits(0b110010101).pack_chars(9) == [405]
    assert Bits(0b110010101).pack_chars(3) == [0b110, 0b010, 0b101]
    assert Bits(0b110010101).pack_chars(2) == None


def test_bools_to_int():
    assert Bits.bools_to_int([0]) == 0
    assert Bits.bools_to_int([1]) == 1
    assert Bits.bools_to_int([0, 1]) == 1
    assert Bits.bools_to_int([1, 0]) == 2
    assert Bits.bools_to_int([1, 0, 0, 1]) == 0b1001
    assert Bits.bools_to_int([1, 0, 1, 1]) == 0b1011
    assert Bits.bools_to_int([1, 0, 1, 1], byteorder='little') == 0b1101
    assert Bits.bools_to_int([1]*8) == 0xFF
