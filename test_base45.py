from hamcrest import assert_that, equal_to, calling, raises
from base58 import (b58encode, b58decode, b58encode_check, b58decode_check)

BASE45_ALPHABET = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"


def test_simple_encode():
    data = b58encode(b'hello world', alphabet=BASE45_ALPHABET)
    assert_that(data, equal_to(b'K3*J+EGLBVAYYB36'))


def test_leadingz_encode():
    data = b58encode(b'\0\0hello world', alphabet=BASE45_ALPHABET)
    assert_that(data, equal_to(b'00K3*J+EGLBVAYYB36'))


def test_encode_empty():
    data = b58encode(b'', alphabet=BASE45_ALPHABET)
    assert_that(data, equal_to(b''))


def test_simple_decode():
    data = b58decode('K3*J+EGLBVAYYB36', alphabet=BASE45_ALPHABET)
    assert_that(data, equal_to(b'hello world'))


def test_simple_decode_bytes():
    data = b58decode(b'K3*J+EGLBVAYYB36', alphabet=BASE45_ALPHABET)
    assert_that(data, equal_to(b'hello world'))


def test_autofix_decode_bytes():
    data = b58decode(
        b'K3*J+EGLBVAYYB36', alphabet=BASE45_ALPHABET, autofix=True)
    assert_that(data, equal_to(b'hello world'))


def test_leadingz_decode():
    data = b58decode('00K3*J+EGLBVAYYB36', alphabet=BASE45_ALPHABET)
    assert_that(data, equal_to(b'\0\0hello world'))


def test_leadingz_decode_bytes():
    data = b58decode(b'00K3*J+EGLBVAYYB36', alphabet=BASE45_ALPHABET)
    assert_that(data, equal_to(b'\0\0hello world'))


def test_empty_decode():
    data = b58decode('1', alphabet=BASE45_ALPHABET)
    assert_that(data, equal_to(b'\x01'))


def test_empty_decode_bytes():
    data = b58decode(b'1', alphabet=BASE45_ALPHABET)
    assert_that(data, equal_to(b'\x01'))


def test_check_str():
    data = 'hello world'
    out = b58encode_check(data, alphabet=BASE45_ALPHABET)
    assert_that(out, equal_to(b'AHN49RN6G8B%AWUALA8K2D'))
    back = b58decode_check(out, alphabet=BASE45_ALPHABET)
    assert_that(back, equal_to(b'hello world'))


def test_autofix_check_str():
    data = 'AHN49RN6G8B%AWUALA8K2D'
    back = b58decode_check(data, alphabet=BASE45_ALPHABET, autofix=True)
    assert_that(back, equal_to(b'hello world'))


def test_autofix_not_applicable_check_str():
    charset = BASE45_ALPHABET.replace(b'x', b'l')
    msg = b'hello world'
    enc = b58encode_check(msg, alphabet=BASE45_ALPHABET)
    modified = enc.replace(b'x', b'l').replace(b'o', b'0')
    back = b58decode_check(modified, alphabet=charset, autofix=True)
    assert_that(back, equal_to(msg))


def test_check_failure():
    data = '3vQB7B6MrGQZaxCuFg4oH'
    assert_that(calling(b58decode_check).with_args(data), raises(ValueError))


def test_invalid_input():
    data = 'xyz0'   # 0 is not part of the bitcoin base58 alphabet
    assert_that(
        calling(b58decode).with_args(data),
        raises(ValueError, "Invalid character '0'"))
