#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This will test our output against what the bip39-vectors.json["english"]"""

import os
import json
from bip39 import mnemonic_from_bytes

def localfile(fname):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), fname))

def read_test_vectors():
    with open(localfile("bip39-vectors.json"), "rt", encoding="utf-8-sig") as jsfp:
        raw = json.load(jsfp)
    return raw["english"]

def main():
    test_vectors = read_test_vectors()
    for hexstr, expected, _, _ in test_vectors:
        barr = bytes([int(hexstr[idx:(idx+2)], 16) for idx in range(0, len(hexstr), 2)])
        mnemonic = " ".join(mnemonic_from_bytes(barr))
        assert mnemonic == expected, (expected, mnemonic)
    print("WOOT. All good.")

if __name__ == "__main__":
    main()
