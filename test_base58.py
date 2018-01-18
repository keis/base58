from contextlib import contextmanager
from itertools import product
from hamcrest import assert_that, equal_to, instance_of
from base58 import (
    b58encode, b58decode, b58encode_check, b58decode_check, b58encode_int,
    b58decode_int, alphabet)


if bytes == str:
    bytes_from_char = (
        lambda c: c
    )
else:
    bytes_from_char = (
        lambda c: bytes([c])
    )


class RaisesContext(object):
    pass


@contextmanager
def assert_raises(matcher=None, message=''):
    # Short hand for instance_of matcher
    if isinstance(matcher, (type,)):
        matcher = instance_of(matcher)

    context = RaisesContext()
    try:
        yield context
    except Exception as e:
        context.exception = e

    assert_that(context.exception, matcher, message)


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


def test_check_failure():
    data = '3vQB7B6MrGQZaxCuFg4oH'
    with assert_raises(ValueError):
        b58decode_check(data)


def test_round_trips():
    possible_bytes = [b'\x00', b'\x01', b'\x10', b'\xff']
    for length in range(0, 5):
        for bytes_to_test in product(possible_bytes, repeat=length):
            bytes_in = b''.join(bytes_to_test)
            bytes_out = b58decode(b58encode(bytes_in))
            assert_that(bytes_in, equal_to(bytes_out))


def test_simple_integers():
    for idx, char in enumerate(alphabet):
        char = bytes_from_char(char)
        assert_that(b58decode_int(char), equal_to(idx))
        assert_that(b58encode_int(idx), equal_to(char))


def test_large_integer():
    number = 0x111d38e5fc9071ffcd20b4a763cc9ae4f252bb4e48fd66a835e252ada93ff480d6dd43dc62a641155a5  # noqa
    assert_that(b58decode_int(alphabet), equal_to(number))
    assert_that(b58encode_int(number), equal_to(alphabet[1:]))
