#! /usr/bin/env python3
# vim: expandtab shiftwidth=4 tabstop=4

"""This will test our output against what the bip39-vectors.json["english"]"""

import os
import json
from bip39 import entropy2mnemonic, mnemonic2derived_seed, derived_seed2prvkey

def localfile(fname):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), fname))

def read_test_vectors():
    with open(localfile("bip39-vectors.json"), "rt", encoding="utf-8-sig") as jsfp:
        raw = json.load(jsfp)
    return raw["english"]

def main():
    test_vectors = read_test_vectors()
    for hexstr, expected_mnemonic, expected_derived_key, expected_prvkey in test_vectors:
        barr = bytes([int(hexstr[idx:(idx+2)], 16) for idx in range(0, len(hexstr), 2)])
        # entropy2mnemonic returns a _list_ of words, which we have to concatenate together with spaces in between.
        mnemonic = " ".join(entropy2mnemonic(barr))
# bip39_decode(mnemonic=mnemonic, passphrase="TREZOR")
        derived_key = mnemonic2derived_seed(mnemonic=mnemonic, passphrase="TREZOR")
        prvkey = derived_seed2prvkey(derived_seed=derived_key)
        assert mnemonic == expected_mnemonic, (expected_mnemonic, mnemonic)
        assert derived_key == expected_derived_key, (expected_derived_key, derived_key)
        assert prvkey == expected_prvkey, (expected_prvkey, prvkey)
    print("WOOT. All good.")

if __name__ == "__main__":
    main()
