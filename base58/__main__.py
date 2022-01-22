"""Base58 encode or decode FILE (or standard input) to standard output."""

import argparse
import sys
from typing import Callable, Dict, Tuple

from base58 import b58decode, b58decode_check, b58encode, b58encode_check

_fmap = {
    (False, False): b58encode,
    (False, True): b58encode_check,
    (True, False): b58decode,
    (True, True): b58decode_check
}  # type: Dict[Tuple[bool, bool], Callable[[bytes], bytes]]


def main() -> None:

    stdout = sys.stdout.buffer

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'file',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('r'),
        help=(
            "File to encode or decode. If no file is provided standard "
            "input is used instead"),
        default='-')
    parser.add_argument(
        '-d', '--decode',
        action='store_true',
        help="decode data instead of encoding")
    parser.add_argument(
        '-c', '--check',
        action='store_true',
        help=(
            "calculate a checksum and append to encoded data or verify "
            "existing checksum when decoding"))

    args = parser.parse_args()
    fun = _fmap[(args.decode, args.check)]

    data = args.file.buffer.read()

    try:
        result = fun(data)
    except Exception as e:
        sys.exit(e)

    stdout.write(result)


if __name__ == '__main__':
    main()
