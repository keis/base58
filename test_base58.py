import pytest
from itertools import product
from random import getrandbits
from hamcrest import assert_that, equal_to, calling, raises
from base58 import (
    b58encode, b58decode, b58encode_check, b58decode_check, b58encode_int,
    b58decode_int,
    BITCOIN_ALPHABET,
    XRP_ALPHABET)


BASE45_ALPHABET = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"


@pytest.fixture(params=[BITCOIN_ALPHABET, XRP_ALPHABET, BASE45_ALPHABET])
def alphabet(request) -> str:
    return request.param


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


def test_autofix_decode_bytes():
    data = b58decode(b'StVlDL6CwTryKyV', autofix=True)
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


def test_check_str():
    data = 'hello world'
    out = b58encode_check(data)
    assert_that(out, equal_to(b'3vQB7B6MrGQZaxCuFg4oh'))
    back = b58decode_check(out)
    assert_that(back, equal_to(b'hello world'))


def test_autofix_check_str():
    data = '3vQB7B6MrGQZaxCuFg4Oh'
    back = b58decode_check(data, autofix=True)
    assert_that(back, equal_to(b'hello world'))


def test_autofix_not_applicable_check_str():
    charset = BITCOIN_ALPHABET.replace(b'x', b'l')
    msg = b'hello world'
    enc = b58encode_check(msg).replace(b'x', b'l').replace(b'o', b'0')
    back = b58decode_check(enc, alphabet=charset, autofix=True)
    assert_that(back, equal_to(msg))


def test_check_failure():
    data = '3vQB7B6MrGQZaxCuFg4oH'
    assert_that(calling(b58decode_check).with_args(data), raises(ValueError))


def test_check_identity(alphabet):
    data = b'hello world'
    out = b58decode_check(
        b58encode_check(data, alphabet=alphabet),
        alphabet=alphabet
    )
    assert_that(out, equal_to(data))


def test_round_trips(alphabet):
    possible_bytes = [b'\x00', b'\x01', b'\x10', b'\xff']
    for length in range(0, 5):
        for bytes_to_test in product(possible_bytes, repeat=length):
            bytes_in = b''.join(bytes_to_test)
            bytes_out = b58decode(
                b58encode(bytes_in, alphabet=alphabet),
                alphabet=alphabet)
            assert_that(bytes_in, equal_to(bytes_out))


def test_simple_integers(alphabet):
    for idx, char in enumerate(alphabet):
        charbytes = bytes([char])
        assert_that(b58decode_int(charbytes, alphabet=alphabet), equal_to(idx))
        assert_that(b58encode_int(idx, alphabet=alphabet), equal_to(charbytes))


def test_large_integer():
    number = 0x111d38e5fc9071ffcd20b4a763cc9ae4f252bb4e48fd66a835e252ada93ff480d6dd43dc62a641155a5  # noqa
    assert_that(b58decode_int(BITCOIN_ALPHABET), equal_to(number))
    assert_that(b58encode_int(number), equal_to(BITCOIN_ALPHABET[1:]))


def test_invalid_input():
    data = 'xyz\b'   # backspace is not part of the bitcoin base58 alphabet
    assert_that(
        calling(b58decode).with_args(data),
        raises(ValueError, "Invalid character '\\\\x08'"))


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
