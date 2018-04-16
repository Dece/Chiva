import pytest

from chiva.bin import Bits


DEAD_BOOLS = [1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1]


def test_bools():
    assert Bits().bools == []


def test_str():
    bits = Bits()
    assert str(bits) == ""
    bits.bools = [1]
    assert str(bits) == "1"
    bits.bools = [1, 1, 0, 1]
    assert str(bits) == "1101"
    bits.bools = DEAD_BOOLS
    assert str(bits) == "1101111010101101"


def test_from_bytes():
    assert Bits.from_bytes(b"").bools == []
    assert Bits.from_bytes(b"\x00").bools == [0] * 8
    assert Bits.from_bytes(b"\xFF").bools == [1] * 8
    assert Bits.from_bytes(b"\xF0").bools == [1] * 4 + [0] * 4
    assert Bits.from_bytes(b"\x0F").bools == [0] * 4 + [1] * 4
    assert Bits.from_bytes(b"\xDE\xAD").bools == DEAD_BOOLS


def test_from_hexstring():
    assert Bits.from_hexstring("").bools == []
    assert Bits.from_hexstring("").bools == []
    assert Bits.from_hexstring("DEAD").bools == DEAD_BOOLS
