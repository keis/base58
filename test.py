from contextlib import contextmanager
from hamcrest import assert_that, equal_to, instance_of
from base58 import b58encode, b58decode, b58encode_check, b58decode_check


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
    assert_that(data, equal_to('StV1DL6CwTryKyV'))


def test_leadingz_encode():
    data = b58encode(b'\0\0hello world')
    assert_that(data, equal_to('11StV1DL6CwTryKyV'))


def test_simple_decode():
    data = b58decode('StV1DL6CwTryKyV')
    assert_that(data, equal_to(b'hello world'))


def test_leadingz_decode():
    data = b58decode('11StV1DL6CwTryKyV')
    assert_that(data, equal_to(b'\0\0hello world'))


def test_check_identity():
    data = b'hello world'
    out = b58decode_check(b58encode_check(data))
    assert_that(out, equal_to(data))


def test_check_failure():
    data = '3vQB7B6MrGQZaxCuFg4oH'
    with assert_raises(ValueError):
        b58decode_check(data)
