import pytest
from itertools import product
from random import getrandbits
from hamcrest import assert_that, equal_to, calling, raises
from base58 import (
    b58encode, b58decode, b58encode_check, b58decode_check, b58encode_int,
    b58decode_int, BITCOIN_ALPHABET, alphabet)


def test_simple_encode():
    data = b58encode(b'hello world')
    assert_that(data, equal_to(b'StV1DL6CwTryKyV'))


def test_leadingz_encode():
    data = b58encode(b'\0\0hello world')
    assert_that(data, equal_to(b'11StV1DL6CwTryKyV'))


def test_encode_empty():
    data = b58encode(b'')
    assert_that(data, equal_to(b''))


def test_simple_decode():
    data = b58decode('StV1DL6CwTryKyV')
    assert_that(data, equal_to(b'hello world'))


def test_simple_decode_bytes():
    data = b58decode(b'StV1DL6CwTryKyV')
    assert_that(data, equal_to(b'hello world'))


def test_leadingz_decode():
    data = b58decode('11StV1DL6CwTryKyV')
    assert_that(data, equal_to(b'\0\0hello world'))


def test_leadingz_decode_bytes():
    data = b58decode(b'11StV1DL6CwTryKyV')
    assert_that(data, equal_to(b'\0\0hello world'))


def test_empty_decode():
    data = b58decode('1')
    assert_that(data, equal_to(b'\0'))


def test_empty_decode_bytes():
    data = b58decode(b'1')
    assert_that(data, equal_to(b'\0'))


def test_check_identity():
    data = b'hello world'
    out = b58decode_check(b58encode_check(data))
    assert_that(out, equal_to(data))


def test_check_str():
    data = 'hello world'
    out = b58encode_check(data)
    assert_that(out, equal_to(b'3vQB7B6MrGQZaxCuFg4oh'))
    back = b58decode_check(out)
    assert_that(back, equal_to(b'hello world'))


def test_check_failure():
    data = '3vQB7B6MrGQZaxCuFg4oH'
    assert_that(calling(b58decode_check).with_args(data), raises(ValueError))


def test_round_trips():
    possible_bytes = [b'\x00', b'\x01', b'\x10', b'\xff']
    for length in range(0, 5):
        for bytes_to_test in product(possible_bytes, repeat=length):
            bytes_in = b''.join(bytes_to_test)
            bytes_out = b58decode(b58encode(bytes_in))
            assert_that(bytes_in, equal_to(bytes_out))


def test_simple_integers():
    for idx, char in enumerate(BITCOIN_ALPHABET):
        charbytes = bytes([char])
        assert_that(b58decode_int(charbytes), equal_to(idx))
        assert_that(b58encode_int(idx), equal_to(charbytes))


def test_large_integer():
    number = 0x111d38e5fc9071ffcd20b4a763cc9ae4f252bb4e48fd66a835e252ada93ff480d6dd43dc62a641155a5  # noqa
    assert_that(b58decode_int(BITCOIN_ALPHABET), equal_to(number))
    assert_that(b58encode_int(number), equal_to(BITCOIN_ALPHABET[1:]))


def test_alphabet_alias_exists_and_equals_bitcoin_alphabet():
    assert_that(alphabet, equal_to(BITCOIN_ALPHABET))


def test_invalid_input():
    data = 'xyz0'   # 0 is not part of the bitcoin base58 alphabet
    assert_that(calling(b58decode).with_args(data), raises(ValueError))


@pytest.mark.parametrize('length', [8, 32, 256, 1024])
def test_encode_random(benchmark, length) -> None:
    data = getrandbits(length * 8).to_bytes(length, byteorder='big')
    encoded = benchmark(lambda: b58encode(data))
    assert_that(b58decode(encoded), equal_to(data))


@pytest.mark.parametrize('length', [8, 32, 256, 1024])
def test_decode_random(benchmark, length) -> None:
    origdata = getrandbits(length * 8).to_bytes(length, byteorder='big')
    encoded = b58encode(origdata)
    data = benchmark(lambda: b58decode(encoded))
    assert_that(data, equal_to(origdata))
