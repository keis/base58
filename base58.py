'''Base58 encoding

Implementations of Base58 and Base58Check endcodings that are compatible
with the bitcoin network.
'''

from hashlib import sha256

# 58 character alphabet used
alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def b58encode(v):
    '''Encode a string using Base58'''

    origlen = len(v)
    v = v.lstrip('\0')
    newlen = len(v)

    p, acc = 1, 0
    for c in v[::-1]:
        acc += p * ord(c)
        p = p << 8

    result = ''
    while acc >= 58:
        acc, mod = divmod(acc, 58)
        result += alphabet[mod]

    return (result + alphabet[acc] + alphabet[0] * (origlen - newlen))[::-1]


def b58decode(v):
    '''Decode a Base58 encoded string'''

    origlen = len(v)
    v = v.lstrip(alphabet[0])
    newlen = len(v)

    p, acc = 1, 0
    for c in v[::-1]:
        acc += p * alphabet.index(c)
        p *= 58

    result = ''
    while acc >= 256:
        acc, mod = divmod(acc, 256)
        result += chr(mod)

    return (result + chr(acc) + '\0' * (origlen - newlen))[::-1]


def b58encode_check(v):
    '''Encode a string using Base58 with a 4 character checksum'''

    digest = sha256(sha256(v).digest()).digest()
    return b58encode(v + digest[:4])


def b58decode_check(v):
    '''Decode and verify the checksum of a Base58 encoded string'''

    result = b58decode(v)
    result, check = result[:-4], result[-4:]
    digest = sha256(sha256(result).digest()).digest()

    if check != digest[:4]:
        raise ValueError("Invalid checksum")

    return result
