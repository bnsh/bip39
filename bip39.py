#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This is our attempt to recreate the bip39 mnemonic method.
    What do we want? We want to have two modes:

        1. From a 128 bit seed and a password to make the mnemonic.
        2. From a mnemonic and a password to make the 128 bit seed.
    
    https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
    Test vectors
    The test vectors include input entropy, mnemonic and seed. The passphrase "TREZOR" is used for all vectors.

    https://github.com/trezor/python-mnemonic/blob/master/vectors.json
"""

import os
import random
import hashlib
import argparse
from functools import reduce

def localfile(fname):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), fname))

def generate_entropy(bitsz: int) -> bytes:
    """No, this is _not_ cryptographically secure! Don't use this in real life!
        This is just for our own educational purposes to understand bip39.
    """
    ent = bytes([random.randint(0, 256) for _ in range(0, bitsz // 8)])
    return ent

def byte2hexstr(values: bytes) -> str:
    return "".join(f"{value:02x}" for value in values)

def hexstr2byte(hexstr: str) -> bytes:
    assert len(hexstr) % 2 == 0
    return bytes([int(hexstr[start:(start+2)], 16) for start in range(0, len(hexstr), 2)])

def compute_sha256(values: bytes) -> str:
    s256 = hashlib.sha256()
    s256.update(values)
    return s256.hexdigest()

def mnemonic_from_bytes(values: bytes) -> str:
    # This is a really dumb way of doing it. Educational purposes again
    # I said!
    # ENT is divisible by 32 : call this 32k
    # We take ENT/32 bits of the sha256 hash: 32k/32 = k
    # 32k + k = 33k

    assert 8 * len(values) % 32 == 0

    checksum = compute_sha256(values)
    # This is much simpler than I thought. Really, all we have to do is shift this checksum (256-8*len(values)//32) bits to the left..
    # 8 because the values are in bytes.
    checksum_bip = int(checksum, 16) >> (256-8*len(values)//32)

    emitted_indices = []
    bucket_of_11_or_more_bits = []
    ladle_of_exactly_11bits = None
    for bits, bitsz in [(byte, 8) for byte in values] + [(checksum_bip, 8*len(values)//32)]:
        if len(bucket_of_11_or_more_bits) >= 11:
            ladle_of_exactly_11bits = bucket_of_11_or_more_bits[0:11]
            emitted_indices.append(reduce(lambda acc, x: acc*2+x, ladle_of_exactly_11bits, 0))
            ladle_of_exactly_11bits = None
            bucket_of_11_or_more_bits = bucket_of_11_or_more_bits[11:]

        # range(bitsz-1, -1, -1) because we need to append these in reversed order.
        bitarray = [1 if (bits & (2 ** idx)) == (2 ** idx) else 0 for idx in range(bitsz-1, -1, -1)]
        bucket_of_11_or_more_bits.extend(bitarray)

    if len(bucket_of_11_or_more_bits) >= 11:
        ladle_of_exactly_11bits = bucket_of_11_or_more_bits[0:11]
        emitted_indices.append(reduce(lambda acc, x: acc*2+x, ladle_of_exactly_11bits, 0))
        ladle_of_exactly_11bits = None
        bucket_of_11_or_more_bits = bucket_of_11_or_more_bits[11:]

    assert len(bucket_of_11_or_more_bits) == 0, len(bucket_of_11_or_more_bits)

    with open(localfile("bip39-en.txt"), "rt", encoding="utf-8-sig") as vfp:
        vocabulary = [word.strip() for word in vfp.readlines()]
    assert len(vocabulary) == 2048, len(vocabulary)
    return [vocabulary[idx] for idx in emitted_indices]

def bip39_encode(*, seed: str, password: str) -> list[str]:
    # https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
    pass

def bip39_decode(*, mnemonic: list[str], password: str) -> str:
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--password", "-p", type=str, required=True)
    parser.add_argument("--seed", "-s", type=str, required=False)
    parser.add_argument("--mnemonic", "-m", type=str, required=False)
    args = parser.parse_args()

    assert (args.seed is None and args.mnemonic is not None) or (args.seed is not None and args.mnemonic is None), "Only one of seed or mnemonic can be specified."
    if args.seed is not None and args.mnemonic is None:
        seed = int(args.seed, 16)
        mnemonic = bip39_encode(seed, args.password)
        print(" ".join(mnemonic))
    elif args.seed is None and args.mnemonic is not None:
        seed = bip39_decode(args.mnemonic, args.password)
        print("{seed:x}")

if __name__ == "__main__":
    main()
