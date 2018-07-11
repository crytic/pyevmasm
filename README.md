# pyevmasm

pyevmasm is an assembler and disassembler library for the Ethereum Virtual Machine (EVM). pyevmasm supports python 2.7 and newer. 

This library is currently new and under development.

New issues, feature requests, and contributions are welcome. Join us in #ethereum channel on the [Empire Hacking Slack](https://empireslacking.herokuapp.com) to discuss Ethereum security tool development.

# evmasm
evmasm is a commandline utility that uses pyevmasm to assemble or disassemble EVM. Below is an example of disassembling the preamble of compiled contract.

```
$ echo -n "608060405260043610603f57600035" | evmasm -d
00000000: PUSH1 0x80
00000002: PUSH1 0x40
00000004: MSTORE
00000005: PUSH1 0x4
00000007: CALLDATASIZE
00000008: LT
00000009: PUSH1 0x3f
0000000b: JUMPI
0000000c: PUSH1 0x0
0000000e: CALLDATALOAD
```

# Installation

Install the latest stable version using pip:
```
pip install pyevmasm
```

To install the library from source:
```
git clone https://github.com/trailofbits/pyevmasm
cd pyevmasm
python setup.py install
```

