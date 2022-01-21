BASE58(1)

# NAME

base58 - Base58 encode or decode

# SYNOPSIS

*base58* [options...] [FILE]

# OPTIONS

*-h, --help*
	Show help message and exit.

*-d, --decode*
	Decode data instead of encoding

*-c, --check*
	Calculate a checksum and append to encoded data or verify existing checksum when decoding

# DESCRIPTION

Base58 encode or decode FILE (or standard input) to standard output. Optionally
a checksum can be used that is given by the first 4 bytes of the digest after
two passes of sha256.
