from contextlib import contextmanager
from itertools import product
from hamcrest import assert_that, equal_to, instance_of
from base58 import b58encode, b58decode, b58encode_check, b58decode_check

from typing import Any, Generator, Union

class RaisesContext(object):
    __slots__ = ('exception',)

    def __init__(self):
        #type: (RaisesContext) -> None
        self.exception = None  #type: Union[None, Exception]


@contextmanager
def assert_raises(matcher=None, message=''):
    #type: (Any, str) -> Generator[Any, None, None]
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
    #type: () -> None
    data = b58encode(b'hello world')
    assert_that(data, equal_to('StV1DL6CwTryKyV'))


def test_leadingz_encode():
    #type: () -> None
    data = b58encode(b'\0\0hello world')
    assert_that(data, equal_to('11StV1DL6CwTryKyV'))


def test_encode_empty():
    #type: () -> None
    data = b58encode(b'')
    assert_that(data, equal_to(''))


def test_simple_decode():
    #type: () -> None
    data = b58decode('StV1DL6CwTryKyV')
    assert_that(data, equal_to(b'hello world'))


def test_simple_decode_bytes():
    #type: () -> None
    data = b58decode(b'StV1DL6CwTryKyV')
    assert_that(data, equal_to(b'hello world'))


def test_leadingz_decode():
    #type: () -> None
    data = b58decode('11StV1DL6CwTryKyV')
    assert_that(data, equal_to(b'\0\0hello world'))


def test_decode_empty():
    #type: () -> None
    data = b58decode('1')
    assert_that(data, equal_to(b'\0'))


def test_check_identity():
    #type: () -> None
    data = b'hello world'
    out = b58decode_check(b58encode_check(data))
    assert_that(out, equal_to(data))


def test_check_failure():
    #type: () -> None
    data = '3vQB7B6MrGQZaxCuFg4oH'
    with assert_raises(ValueError):
        b58decode_check(data)


def test_round_trips():
    #type: () -> None
    possible_bytes = [b'\x00', b'\x01', b'\x10', b'\xff']
    for length in range(0, 5):
        for bytes_to_test in product(possible_bytes, repeat=length):
            bytes_in = b''.join(bytes_to_test)
            bytes_out = b58decode(b58encode(bytes_in))
            assert_that(bytes_in, equal_to(bytes_out))


def test_input_should_be_bytes():
    #type: () -> None
     data = u'3vQB7B6MrGQZaxCuFg4oH'
     with assert_raises(TypeError):
         b58encode(data)  #type: ignore
