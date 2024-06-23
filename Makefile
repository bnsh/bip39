PYTHON=$(sort $(wildcard *.py))
PYLINT3=$(addprefix .,$(PYTHON:py=pylint3))

all: pylint

bip39-en.txt:
	wget -O $(@) "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt"

bip39-vectors.json:
	wget -O $(@) "https://raw.githubusercontent.com/trezor/python-mnemonic/master/vectors.json"

pylint: $(PYLINT3)

.%.pylint3: %.py
	python3 -m pylint -r n $(^)
	@>$(@)
