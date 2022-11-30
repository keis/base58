'''Base58 encoding

Implementations of Base58 and Base58Check encodings that are compatible
with the bitcoin network.
'''

# This module is based upon base58 snippets found scattered over many bitcoin
# tools written in python. From what I gather the original source is from a
# forum post by Gavin Andresen, so direct your praise to him.
# This module adds shiny packaging and support for python3.

from functools import lru_cache
from hashlib import sha256
from typing import Mapping, Union
from math import log

try:
    from gmpy2 import mpz
except ImportError:
    mpz = None

__version__ = '2.1.1'

# 58 character alphabet used
BITCOIN_ALPHABET = \
    b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
RIPPLE_ALPHABET = b'rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz'
XRP_ALPHABET = RIPPLE_ALPHABET
POWERS = {
    45: {2 ** i: 45 ** (2 ** i) for i in range(4, 20)},
    58: {2 ** i: 58 ** (2 ** i) for i in range(4, 20)}
}

# Retro compatibility
alphabet = BITCOIN_ALPHABET


def scrub_input(v: Union[str, bytes]) -> bytes:
    if isinstance(v, str):
        v = v.encode('ascii')

    return v


def _encode_int(i: int, base: int = 58, alphabet: bytes = BITCOIN_ALPHABET) -> bytes:
    """
    Encode integer to bytes with base 58 alphabet by powers of 58
    """
    min_val = POWERS[base][2**8]
    if i <= min_val:
        string = bytearray()
        while i:
            i, idx = divmod(i, base)
            string.append(idx)
        return string[::-1]
    else:
        origlen0 = int(log(i, 58))//2
        try:
            split_num = POWERS[base][2**origlen0]
        except KeyError:
            POWERS[base][2**origlen0] = split_num = base ** origlen0
        i1, i0 = divmod(i, split_num)

        v1 = _encode_int(i1, base, alphabet)
        v0 = _encode_int(i0, base, alphabet)
        newlen0 = len(v0)
        if newlen0 < origlen0:
            v0[:0] = b'\0' * (origlen0 - newlen0)

        return v1 + v0


def _mpz_encode(i: int, alphabet: bytes) -> bytes:
    """
    Encode an integer to arbitrary base using gmpy2 mpz
    """
    base = len(alphabet)

    raw: bytes = mpz(i).digits(base).encode()
    tr_bytes = bytes.maketrans(''.join([mpz(x).digits(base) for x in range(base)]).encode(), alphabet)
    encoded: bytes = raw.translate(tr_bytes)

    return encoded


def b58encode_int(
    i: int, default_one: bool = True, alphabet: bytes = BITCOIN_ALPHABET
) -> bytes:
    """
    Encode an integer using Base58
    """
    if not i:
        if default_one:
            return alphabet[0:1]
        return b''
    if mpz:
        return _mpz_encode(i, alphabet)

    base = len(alphabet)
    raw_string = _encode_int(i, base, alphabet)
    string = raw_string.translate(bytes.maketrans(bytearray(range(len(alphabet))), alphabet))

    return string


def b58encode(
    v: Union[str, bytes], alphabet: bytes = BITCOIN_ALPHABET
) -> bytes:
    """
    Encode a string using Base58
    """
    v = scrub_input(v)

    origlen = len(v)
    v = v.lstrip(b'\0')
    newlen = len(v)

    acc = int.from_bytes(v, byteorder='big')  # first byte is most significant

    result = b58encode_int(acc, default_one=False, alphabet=alphabet)
    return alphabet[0:1] * (origlen - newlen) + result


@lru_cache()
def _get_base58_decode_map(alphabet: bytes,
                           autofix: bool) -> Mapping[int, int]:
    invmap = {char: index for index, char in enumerate(alphabet)}

    if autofix:
        groups = [b'0Oo', b'Il1']
        for group in groups:
            pivots = [c for c in group if c in invmap]
            if len(pivots) == 1:
                for alternative in group:
                    invmap[alternative] = invmap[pivots[0]]

    return invmap


def _decode(data: bytes, min_split: int = 256, base: int = 58) -> int:
    """
    Decode larger data blocks recursively
    """
    if len(data) <= min_split:
        ret_int = 0
        for val in data:
            ret_int = base * ret_int + val
        return ret_int
    else:
        split_len = 2**(len(data).bit_length()-2)
        try:
            base_pow = POWERS[base][split_len]
        except KeyError:
            POWERS[base] = base_pow = base ** split_len
        return (base_pow * _decode(data[:-split_len])) + _decode(data[-split_len:])


def b58decode_int(
    v: Union[str, bytes], alphabet: bytes = BITCOIN_ALPHABET, *,
    autofix: bool = False
) -> int:
    """
    Decode a Base58 encoded string as an integer
    """
    if b' ' not in alphabet:
        v = v.rstrip()
    v = scrub_input(v)

    base = len(alphabet)
    map = _get_base58_decode_map(alphabet, autofix=autofix)
    if mpz:
        tr_bytes = bytes.maketrans(bytearray(map.keys()), ''.join([mpz(x).digits(base) for x in map.values()]).encode())
    else:
        tr_bytes = bytes.maketrans(bytearray(map.keys()), bytearray(map.values()))
    del_chars = bytes(bytearray(x for x in range(256) if x not in map))

    cv = v.translate(tr_bytes, delete=del_chars)
    if len(v) != len(cv):
        err_char = chr(next(c for c in v if c not in map))
        raise ValueError("Invalid character {!r}".format(err_char))

    if cv == b'':
        return 0

    if mpz:
        try:
            return int(mpz(cv, base=base))
        except ValueError:
            raise ValueError(cv, base)

    return _decode(cv, base=base)


def b58decode(
    v: Union[str, bytes], alphabet: bytes = BITCOIN_ALPHABET, *,
    autofix: bool = False
) -> bytes:
    """
    Decode a Base58 encoded string
    """
    v = v.rstrip()
    v = scrub_input(v)

    origlen = len(v)
    v = v.lstrip(alphabet[0:1])
    newlen = len(v)

    acc = b58decode_int(v, alphabet=alphabet, autofix=autofix)

    return acc.to_bytes(origlen - newlen + (acc.bit_length() + 7) // 8, "big")


def b58encode_check(
    v: Union[str, bytes], alphabet: bytes = BITCOIN_ALPHABET
) -> bytes:
    """
    Encode a string using Base58 with a 4 character checksum
    """
    v = scrub_input(v)

    digest = sha256(sha256(v).digest()).digest()
    return b58encode(v + digest[:4], alphabet=alphabet)


def b58decode_check(
    v: Union[str, bytes], alphabet: bytes = BITCOIN_ALPHABET, *,
    autofix: bool = False
) -> bytes:
    '''Decode and verify the checksum of a Base58 encoded string'''

    result = b58decode(v, alphabet=alphabet, autofix=autofix)
    result, check = result[:-4], result[-4:]
    digest = sha256(sha256(result).digest()).digest()

    if check != digest[:4]:
        raise ValueError("Invalid checksum")

    return result
